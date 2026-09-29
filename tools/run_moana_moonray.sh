#!/usr/bin/env bash
# Run one Moana/MoonRay attempt with a host-enforced deadline and retained evidence.
set -euo pipefail
if [[ $# -ne 2 || ! "$2" =~ ^[1-9][0-9]*$ ]]; then
    echo "Usage: bash tools/run_moana_moonray.sh /absolute/MoanaIsland MAX_SECONDS" >&2
    exit 2
fi
for command in docker timeout git sha256sum; do
    command -v "$command" >/dev/null || { echo "Missing host command: $command" >&2; exit 2; }
done
repo=$(cd "$(dirname "$0")/.." && pwd -P)
scene=$(cd "$1" && pwd -P)
[[ -f "$scene/usd/island.usda" ]] || { echo "Missing $scene/usd/island.usda" >&2; exit 2; }
# Docker --mount uses commas as separators.
[[ "$repo$scene" != *,* ]] || { echo 'Use paths without commas.' >&2; exit 2; }
image=$(cat "$repo/runnable_image.txt")
[[ "$image" =~ ^ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:[0-9a-f]{64}$ ]] || exit 2
seconds=$2
out=$(mktemp -d "$repo/local-runs/moana-moonray-XXXXXXXX" 2>/dev/null) || {
    mkdir -p "$repo/local-runs"
    out=$(mktemp -d "$repo/local-runs/moana-moonray-XXXXXXXX")
}
container="moana-moonray-$(date -u +%Y%m%dT%H%M%SZ)-$$"
created=0
finish() {
    code=$?
    trap - EXIT INT TERM
    if (( created )); then
        docker stop --time 30 "$container" >/dev/null 2>&1 || true
        docker logs --timestamps "$container" > "$out/container.log" 2>&1 || true
        docker inspect --format '{{json .State}}' "$container" > "$out/container-state.json" || true
        # Keep the stopped container for investigation; removal is explicit.
    fi
    printf '%s\n' "$code" > "$out/runner-exit.txt"
    printf 'Evidence: %s\nStopped container: %s\nRemove after review: docker rm %s\n' "$out" "$container" "$container"
    exit "$code"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf '%s\n' "$image" > "$out/image.txt"
printf '%s\n' "$seconds" > "$out/deadline-seconds.txt"
printf '%s\n' "$container" > "$out/container-name.txt"
date -u +%FT%TZ > "$out/start-utc.txt"
git -C "$repo" rev-parse HEAD > "$out/checkout.txt"
git -C "$repo" status --short > "$out/checkout-status.txt"
git -C "$repo" diff --binary HEAD > "$out/checkout.patch"
git -C "$repo" submodule status --recursive > "$out/submodules.txt"
sha256sum "$scene/usd/island.usda" > "$out/scene-root.sha256"
# A content manifest is optional because reading all textures can be expensive.
# Contributors supply the downloaded archive checksum in their report.
{ uname -a; command -v lscpu >/dev/null && lscpu; cat /proc/meminfo; } > "$out/host.txt"
docker version > "$out/docker-version.txt"
docker image inspect "$image" --format '{{.Id}} {{.Architecture}} {{json .RepoDigests}}' > "$out/image-inspect.txt"
docker create --name "$container" --init --gpus all \
    --env NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics \
    --env TMPDIR=/results/tmp --ulimit nofile=65536:65536 \
    --mount "type=bind,source=$repo,target=/benchmark,readonly" \
    --mount "type=bind,source=$scene,target=/moana,readonly" \
    --mount "type=bind,source=$out,target=/results" \
    --workdir /benchmark --entrypoint bash "$image" -c '
set -uo pipefail
mkdir -p /results/tmp
nvidia-smi > /results/nvidia-smi.txt 2>&1
printf "nofile soft=%s hard=%s\n" "$(ulimit -Sn)" "$(ulimit -Hn)"
rez env aswf -- python3 -c "from pxr import Usd; print(Usd.GetVersion())"
resources() {
    date -u +%FT%TZ
    for f in /sys/fs/cgroup/memory.max /sys/fs/cgroup/memory.current \
             /sys/fs/cgroup/memory.peak /sys/fs/cgroup/memory.events \
             /sys/fs/cgroup/memory/memory.limit_in_bytes \
             /sys/fs/cgroup/memory/memory.max_usage_in_bytes \
             /sys/fs/cgroup/memory/memory.failcnt /sys/fs/cgroup/memory/memory.oom_control; do
        if test -r "$f"; then printf "%s\n" "$f"; cat "$f"; fi
    done
}
(while :; do resources >> /results/resources.txt; sleep 30; done) &
sampler=$!
/usr/bin/time -o /results/time.txt -f "Time: %E\nMemory: %M KiB\nProcess exit: %x" \
    rez env aswf -- usdrecord --camera /island/cam/shotCam --renderer Moonray \
    --purposes render /moana/usd/island.usda /results/island.jpg
status=$?
printf "%s\n" "$status" > /results/render-exit.txt
resources >> /results/resources.txt
kill "$sampler" 2>/dev/null || true
wait "$sampler" 2>/dev/null || true
exit "$status"
' > "$out/container-id.txt"
created=1
docker start "$container" >/dev/null
set +e
timeout --signal=TERM "${seconds}s" docker wait "$container" > "$out/container-exit.txt"
wait_status=$?
set -e
if [[ "$wait_status" -eq 124 ]]; then
    printf 'Deadline reached; stopping the entire container.\n' > "$out/outcome.txt"
    exit 124
elif [[ "$wait_status" -ne 0 ]]; then
    printf 'Docker wait failed: %s\n' "$wait_status" > "$out/outcome.txt"
    exit "$wait_status"
fi
status=$(cat "$out/container-exit.txt")
[[ "$status" =~ ^[0-9]+$ && "$status" -le 255 ]] || exit 125
printf 'Container exited: %s. Inspect image and logs separately.\n' "$status" > "$out/outcome.txt"
exit "$status"
