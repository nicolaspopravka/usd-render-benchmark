# ASWF CY2024 / Hydra Render Benchmark

This branch records a benchmark of the ASWF CY2024 environment with
GL, MoonRay and Cycles built against the same OpenUSD installation and
packaged in one runnable image. Eight renders produced images across McUsd,
OpenChessSet and ALab. This snapshot has no Moana Island Scene image.

![ASWF CY2024: GL, MoonRay and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Hydra GL, MoonRay 2026.29.1, Cycles 4.3.0
- OpenUSD: 24.08
- Runnable image: `ghcr.io/nicolaspopravka/usd-render-benchmark:2024.3`
- Digest: `sha256:9327af68f87900bad78f838d8c1f7fad3df78bf7b8153f5b8eb5f0bb5765bcb3`
- Run: `20260925T130718Z-26308`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 580.159.04
- Container OS: Rocky Linux 8.10
- Asset revisions: `assets` at `907d5f17bbe933fc14441a3f3ab69a5bd8abe32a`;
  ALab at `20a3e1d5ea034072fc97d5fee04e51016c11218a`, with additional asset payloads

This result retains the earlier CY2024 image. Rebuilding with the newer
delegate defaults is currently blocked by the OSL compiler failing to load `libLTO.so.17`
([#54](https://github.com/nicolaspopravka/usd-render-benchmark/issues/54)).
The [CY2025 environment](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025)
is the current GPU-capable image offered for community attempts.

This project-built image uses the ASWF environment; it is not an ASWF-published
benchmark image. The GPU identifies the host used for the run, not a claim that
every delegate rendered on the GPU. Cycles used its CPU device.

[`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) creates a headless EGL context
instead of the Qt context used by stock `usdrecord`. The
[OpenUSD Rez package](packages/openusd/24.08/package.py) redirects `usdrecord`
to this wrapper. These results therefore include that invocation adaptation.

## Results

| Scene | GL | MoonRay | Cycles |
| --- | --- | --- | --- |
| McUsd | Success · image | Failure (exit 1) · image | Success · image |
| OpenChessSet | Success · image | Failure (exit 1) · image | Success · image |
| ALab | Failure (exit 1) · image | Failure (exit 1) · image | Skipped; earlier segmentation fault |
| Moana Island Scene | Skipped | Skipped | Skipped |

Success means the render process exited 0; a nonzero exit is a failure.
Image presence and appearance are additional observations, not a different
outcome classification.
GL/Storm shows textured McUsd and ALab but fallback OpenChessSet materials.
MoonRay's McUsd lacks the expected textures and its OpenChessSet pieces appear
magenta; ALab retains textures. Cycles shows an overexposed McUsd and white
OpenChessSet pieces without the expected material variation. The sheet preserves these differences without exposure correction.

Four of the eight renders with images failed with status 1:
all three MoonRay renders and GL/Storm on ALab. The logs include MoonRay empty
`TfToken` diagnostics and the ALab clip-set error at time code 1004. The same
MoonRay diagnostics occur with exit 0 in the CY2023 run; these observations do
not isolate a single cause across the different environments.

Cycles/ALab and all Moana combinations were skipped in this run after earlier
failures. The skip reasons are recorded in `problematic_combinations` in
[`render_script.sh`](render_script.sh): Cycles/ALab segmentation fault,
GL/Storm/Moana crash, Cycles/Moana killed, and MoonRay/Moana worker termination
with a client that can remain alive ([#51](https://github.com/nicolaspopravka/usd-render-benchmark/issues/51)).

The CY2023 and CY2024 MoonRay runs used a soft open-file limit of 65536.
Raising that limit was necessary for the CY2024 ALab texture-read follow-up;
the local recipe below applies it too. The CY2025 run predates that explicit
setting, so the recipe documents this setup difference rather than claiming an
exact replay of every process limit.

Timings and the recorded `/usr/bin/time` memory measurements are in
[`render_summary.md`](render_summary.md). Its `Success`/`Failure` labels report
process outcomes. They do not establish visual correctness. These measurements are not a
controlled performance comparison between years, and the process memory field
must not be assumed to include the complete Arras worker memory use.

The eight retained logs are under [`logs/`](logs/); images are under
[`renderers/`](renderers/). The no-image attempts are described above but their
logs are not part of this image-only publication snapshot.

The intended range is CY2023–CY2027. Equivalent GL/Storm, MoonRay and Cycles
coverage in one runnable environment is not yet available for CY2026/27; see
[environment coverage](https://github.com/nicolaspopravka/usd-render-benchmark#aswf-environments-by-year).

## Run this branch locally

Use a Linux x86-64 host with Docker, a compatible NVIDIA driver and the
[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
The EGL wrapper requires NVIDIA graphics access even when a delegate computes
on the CPU. Docker Desktop on macOS does not provide this NVIDIA setup.
Allow space for the container and the expanded assets. Host memory and driver
differences can change the outcome and timings.

Start in a **fresh checkout**: the harness overwrites `logs/` and `renderers/`.


```bash
git lfs install
git clone --branch aswf/cy2024 --single-branch \
  https://github.com/nicolaspopravka/usd-render-benchmark.git run-cy2024
cd run-cy2024
git submodule update --init --recursive
git -C assets lfs pull
git -C scenes/ALab lfs pull
```

The ALab Git checkout alone is insufficient. Obtain the **v2.2.0 Techvar Assets**
and **Baked Procedurals** from [ALab](https://dpel.aswf.io/alab/) and merge their
contents as explained in the [pinned ALab instructions](https://github.com/DigitalProductionExampleLibrary/ALab/blob/20a3e1d5ea034072fc97d5fee04e51016c11218a/README.md).
The merged scene must be `scenes/ALab/ALab/entry.usda`. The recorded techvars
archive SHA-256 is `d142891ed4ad2365f8dd6b583e9dac88982131d7709dd8e6f6bc0f1516007ec6`.
A complete checksum manifest of the expanded ALab payload was not retained, so
record the packages you use; the Git revision alone does not establish identical
asset contents. The current harness skips Moana, so that download is unnecessary
for this eight-render rerun.

```bash
RUNNABLE_IMAGE='ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:9327af68f87900bad78f838d8c1f7fad3df78bf7b8153f5b8eb5f0bb5765bcb3'
docker pull "$RUNNABLE_IMAGE"
mkdir -p local-runs
RUN_REVISION=$(git rev-parse HEAD)
printf '%s\n' "$RUN_REVISION" > local-runs/checkout.txt
git diff --binary > local-runs/checkout.patch
git submodule status --recursive > local-runs/submodules.txt

docker run --rm --gpus all \
  --env NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics \
  --env RUNNABLE_IMAGE="$RUNNABLE_IMAGE" --env RUN_REVISION="$RUN_REVISION" \
  --ulimit nofile=65536:65536 \
  --mount type=bind,source="$PWD",target=/benchmark \
  --workdir /benchmark --entrypoint bash "$RUNNABLE_IMAGE" -c '
    set -e
    nvidia-smi > local-runs/nvidia-smi.txt
    specs="image=$RUNNABLE_IMAGE; checkout=$RUN_REVISION; nofile=$(ulimit -Sn); $(uname -sr); $(nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader)"
    printf "%s\n" "$specs" > local-runs/system-specs.txt
    bash render_script.sh
    python3 generate_render_summary.py --system-specs "$specs"
  '
```

The image supplies the renderer environment; the mounted branch supplies the
harness, Rez packages and outputs. The wrapper and relative package paths require
the working directory shown above. Skips remain active. A zero Docker exit does
not prove every render succeeded: inspect each log and image. The summary is
regenerated after the harness returns; `render_sheet.jpg` remains the published
sheet and is not regenerated by this command. Rootful Docker may create
root-owned outputs; account for that when choosing your checkout directory.

The image startup, Rez resolution and shell commands were checked without a
GPU render. A complete fresh-asset rerun on an NVIDIA host has not been performed
for these instructions.

For community attempts with GPU support, start with the
[CY2025 recipe](https://github.com/nicolaspopravka/usd-render-benchmark/blob/aswf/cy2025/docs/MOANA_MOONRAY.md).
The [recipe here](docs/MOANA_MOONRAY.md) retains this older image for comparisons. It deliberately runs that one
combination despite the normal skip and stores its outputs separately.
