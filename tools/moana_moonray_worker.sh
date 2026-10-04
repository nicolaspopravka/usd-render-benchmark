#!/usr/bin/env bash
# Shared render payload. The launcher owns deadlines and whole-runtime cleanup.
set -euo pipefail
[[ $# -eq 3 && ( "$3" == default || "$3" == xpu ) ]] || {
    echo 'Usage: bash moana_moonray_worker.sh SCENE OUTPUT default|xpu' >&2
    exit 2
}
repo=$(cd "$(dirname "$0")/.." && pwd -P)
scene=$(cd "$1" && pwd -P)
mkdir -p "$2"
out=$(cd "$2" && pwd -P)
mode=$3
[[ -f "$scene/usd/island.usda" ]] || exit 2
[[ "${MOANA_RUNTIME:-}" == docker || "${MOANA_RUNTIME:-}" == runpod ]] || exit 2
cd "$repo"
export REZ_PACKAGES_PATH="$repo/packages"
export TMPDIR="$out/tmp"
mkdir -p "$TMPDIR"
sampler=''
finish() {
    code=$?
    trap - EXIT
    if [[ -n "$sampler" ]]; then
        kill "$sampler" 2>/dev/null || true
        wait "$sampler" 2>/dev/null || true
    fi
    printf '%s\n' "$code" > "$out/worker-exit.txt"
    date -u +%FT%TZ > "$out/worker-end-utc.txt"
    exit "$code"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf '%s\n' "$MOANA_RUNTIME" > "$out/runtime.txt"
printf '%s\n' "$mode" > "$out/moonray-mode.txt"
sha256sum "$0" > "$out/worker.sha256"
sha256sum "$scene/usd/island.usda" > "$out/scene-root.sha256"
{ uname -a; command -v lscpu >/dev/null && lscpu; cat /proc/meminfo; } > "$out/host.txt"
for program in rez nvidia-smi sha256sum; do command -v "$program" >/dev/null; done
test -x /usr/bin/time
ulimit -n 65536
printf 'nofile soft=%s hard=%s\n' "$(ulimit -Sn)" "$(ulimit -Hn)" > "$out/nofile.txt"
nvidia-smi > "$out/nvidia-smi.txt" 2>&1
rez env aswf -- python3 -c 'from pxr import Usd; print(Usd.GetVersion())'
resources() {
    date -u +%FT%TZ
    nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>&1 || true
    nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv,noheader 2>&1 || true
    for f in /sys/fs/cgroup/memory.max /sys/fs/cgroup/memory.current \
             /sys/fs/cgroup/memory.peak /sys/fs/cgroup/memory.events \
             /sys/fs/cgroup/memory/memory.limit_in_bytes \
             /sys/fs/cgroup/memory/memory.max_usage_in_bytes \
             /sys/fs/cgroup/memory/memory.failcnt /sys/fs/cgroup/memory/memory.oom_control; do
        if test -r "$f"; then printf '%s\n' "$f"; cat "$f"; fi
    done
}
resources >> "$out/resources.txt"
(
    timer=''
    trap '[[ -z "$timer" ]] || kill "$timer" 2>/dev/null; exit 0' TERM INT
    while :; do
        sleep 30 &
        timer=$!
        wait "$timer"
        resources >> "$out/resources.txt"
    done
) >/dev/null 2>&1 &
sampler=$!
render=(rez env aswf -- usdrecord)
if [[ "$mode" == xpu ]]; then
    render=(rez env aswf -- env HDMOONRAY_EXEC_MODE=xpu REZ_MOONRAY_ROOT=/usr/local ./tools/usdrecord_egl.py)
fi
printf 'Requested MoonRay mode: %s\n' "$mode"
printf '%q ' "${render[@]}" --camera /island/cam/shotCam --renderer Moonray \
    --purposes render "$scene/usd/island.usda" "$out/island.jpg" > "$out/render-command.txt"
printf '\n' >> "$out/render-command.txt"
date -u +%FT%TZ > "$out/render-start-utc.txt"
set +e
/usr/bin/time -o "$out/time.txt" -f 'Time: %E\nMemory: %M KiB\nProcess exit: %x' \
    "${render[@]}" --camera /island/cam/shotCam --renderer Moonray \
    --purposes render "$scene/usd/island.usda" "$out/island.jpg"
status=$?
set -e
printf '%s\n' "$status" > "$out/render-exit.txt"
resources >> "$out/resources.txt"
exit "$status"
