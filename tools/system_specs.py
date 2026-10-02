#!/usr/bin/env python3
"""Print one Arnold-style system description from inside a Linux container.

MB follows the historical Arnold spelling for binary megabytes. CPU affinity
and visible cgroup limits describe restrictions, not dedicated host resources.
The optional GPU clock is the reported maximum SM clock.
"""
import csv
import os
import subprocess
import sys
from pathlib import Path


def read(path):
    try:
        return Path(path).read_text().strip()
    except OSError:
        return ""


def command(*args):
    try:
        return subprocess.check_output(
            args, text=True, env={**os.environ, "LC_ALL": "C"},
            stderr=subprocess.DEVNULL, timeout=10,
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def cgroup_dirs(controller):
    """Find this process's cgroup and its visible ancestors, for v1 or v2."""
    groups = [line.split(":", 2) for line in read("/proc/self/cgroup").splitlines()]
    for line in read("/proc/self/mountinfo").splitlines():
        before, separator, after = line.partition(" - ")
        if not separator:
            continue
        fields, filesystem = before.split(), after.split()
        if filesystem[0] not in ("cgroup", "cgroup2"):
            continue
        if filesystem[0] == "cgroup" and controller not in filesystem[2].split(","):
            continue
        mount = Path(fields[4])
        for _, controllers, member in groups:
            if filesystem[0] == "cgroup2":
                if controllers:
                    continue
            elif controller not in controllers.split(","):
                continue
            try:
                relative = Path(member).relative_to(fields[3])
                # Some namespaces expose a host membership path outside the mount.
                current = mount if ".." in relative.parts else mount / relative
            except ValueError:
                current = mount
            while True:
                yield current
                if current == mount:
                    break
                current = current.parent


def cpu_description():
    model = next((line.split(":", 1)[1].strip()
                  for line in read("/proc/cpuinfo").splitlines()
                  if line.startswith("model name") and ":" in line), "CPU")
    allowed = len(os.sched_getaffinity(0))
    quotas, recorded = [], False
    for directory in cgroup_dirs("cpu"):
        maximum = read(directory / "cpu.max")
        if maximum:
            quota, period = maximum.split()
        else:
            quota = read(directory / "cpu.cfs_quota_us")
            period = read(directory / "cpu.cfs_period_us")
        if quota and period:
            recorded = True
            if quota != "max" and int(quota) > 0 and int(period) > 0:
                quotas.append(int(quota) / int(period))
    details = f"{allowed} logical {'CPU' if allowed == 1 else 'CPUs'} allowed"
    if quotas:
        quota = min(quotas)
        details += f", quota {quota:g} {'CPU' if quota == 1 else 'CPUs'}"
    elif not recorded:
        details += ", CPU quota unavailable"
    return f"{model} ({details})"


def memory_description():
    total = next((int(line.split()[1]) * 1024
                  for line in read("/proc/meminfo").splitlines()
                  if line.startswith("MemTotal:")), None)
    limits, recorded = [], False
    for directory in cgroup_dirs("memory"):
        limit = read(directory / "memory.max") or read(directory / "memory.limit_in_bytes")
        if limit:
            recorded = True
            if limit != "max" and int(limit) >= 0:
                limits.append(int(limit))
    if total is None:
        if limits:
            return f"with {min(limits) // 1048576}MB RAM limit"
        return "RAM information unavailable"
    effective = min([total] + limits)
    if effective < total:
        return f"with {effective // 1048576}MB RAM limit"
    description = f"with {total // 1048576}MB visible RAM"
    if not recorded:
        description += " (cgroup limit unavailable)"
    return description


def nvidia_query(fields, index=None):
    args = ["nvidia-smi", f"--query-gpu={fields}", "--format=csv,noheader,nounits"]
    if index is not None:
        args.append(f"--id={index}")
    return list(csv.reader(command(*args).splitlines(), skipinitialspace=True))


def gpu_description():
    gpus = nvidia_query("index,name,driver_version,memory.total,memory.free")
    if not gpus:
        return ["NVIDIA GPU information unavailable"]
    parts = [f"NVIDIA driver version {gpus[0][2]}"]
    for index, name, driver, total, available in gpus:
        description = f"GPU {index}: {name}"
        # Unsupported optional queries must not hide a GPU's basic information.
        for field, template in [("clocks.max.sm", " @ {}MHz"),
                                ("compute_cap", " (compute {})")]:
            result = nvidia_query(field, index)
            if result and result[0][0] not in ("N/A", "[N/A]", "[Not Supported]", ""):
                description += template.format(result[0][0])
        try:
            description += f" with {int(float(total))}MB"
            description += f" ({int(float(available))}MB available)"
        except ValueError:
            pass
        parts.append(description)
    return parts


def system_specs():
    distro = next((line.split("=", 1)[1].strip("\"'")
                   for line in read("/etc/os-release").splitlines()
                   if line.startswith("PRETTY_NAME=")), "Linux distribution unavailable")
    return " ".join([cpu_description(), memory_description(), *gpu_description(),
                     f"{distro}, Linux kernel {os.uname().release}"])


if __name__ == "__main__":
    if not sys.platform.startswith("linux"):
        sys.exit("system_specs.py must run inside the Linux render container")
    print(system_specs())
