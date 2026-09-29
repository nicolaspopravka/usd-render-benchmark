# ASWF CY2025 / Hydra Render Benchmark

This branch records a benchmark of the ASWF CY2025 environment with
Storm, MoonRay and Cycles built against the same OpenUSD installation and
packaged in one runnable image. Nine renders were attempted; eight produced images across McUsd,
OpenChessSet and ALab. This snapshot has no Moana Island Scene image.

![ASWF CY2025: Storm, MoonRay and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Hydra Storm, MoonRay 2026.29.1, Cycles 4.5.0
- OpenUSD: 25.05.01
- Runnable image: `ghcr.io/nicolaspopravka/usd-render-benchmark:2025.3`
- Digest: `sha256:dc85819610d10b5d335a0c01e5bf80184ae42c9d07133f8c7be8ecce92e09032`
- Run: `20260929T121029Z-31190`
- GPU: NVIDIA GeForce RTX 4090, 24 GB
- Driver: NVIDIA 580.126.20
- Container OS: Rocky Linux 8.10
- Asset revisions: `assets` at `907d5f17bbe933fc14441a3f3ab69a5bd8abe32a`;
  ALab at `20a3e1d5ea034072fc97d5fee04e51016c11218a`, with additional asset payloads

This project-built image uses the ASWF environment; it is not an ASWF-published
benchmark image. The build uses upstream default delegate features, including MoonRay XPU and
Cycles CUDA/OptiX and OSL support. The documented Cycles exceptions are
`WITH_CYCLES_NANOVDB=OFF`, `WITH_CYCLES_OPENIMAGEDENOISE=OFF` and
`WITH_LIBS_PRECOMPILED=OFF`, because of the available ASWF dependencies.
See the [build script](https://github.com/nicolaspopravka/usd-render-benchmark-stack/blob/fb1950393f17c8036c7fea4e98eaa11f496d4405/build_cycles.sh).

This benchmark leaves device selection at the delegates' defaults. Cycles
therefore uses the CPU; the branch does not force MoonRay XPU. A GPU-capable
build is not a claim that every render used the GPU. Separate Teapot probes
exercised forced MoonRay XPU and Cycles OptiX; the
[community recipe](docs/MOANA_MOONRAY.md) explains the evidence and limitations.
The new image replaces the earlier image served by the mutable `2025.3` tag;
the digest above identifies this run.

[`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) creates a headless EGL context
instead of the Qt context used by stock `usdrecord`. The
[OpenUSD Rez package](packages/openusd/25.05.01/package.py) redirects `usdrecord`
to this wrapper. These results therefore include that invocation adaptation.

## Results

| Scene | Storm | MoonRay | Cycles |
| --- | --- | --- | --- |
| McUsd | Success · image | Failure (exit 1) · image | Success · image |
| OpenChessSet | Success · image | Failure (exit 1) · image | Success · image |
| ALab | Failure (exit 1) · image | Failure (exit 1) · image | Failure (139) · no image |
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

Cycles/ALab was attempted and failed with status 139, without an image.
All Moana combinations were skipped. The current harness also skips
Cycles/ALab on subsequent reruns. The skip reasons are recorded in `problematic_combinations` in
[`render_script.sh`](render_script.sh): Cycles/ALab segmentation fault,
GL/Storm/Moana crash, Cycles/Moana killed, and MoonRay/Moana worker termination
with a client that can remain alive ([#51](https://github.com/nicolaspopravka/usd-render-benchmark/issues/51)).

This run used a soft open-file limit of 65536, also applied by the local recipe.

Timings and the recorded `/usr/bin/time` memory measurements are in
[`render_summary.md`](render_summary.md). Its `Success`/`Failure` labels report
process outcomes. They do not establish visual correctness. These measurements are not a
controlled performance comparison between years, and the process memory field
must not be assumed to include the complete Arras worker memory use.

All nine render logs are under [`logs/`](logs/); images are under
[`renderers/`](renderers/). The Cycles/ALab failure log is retained. The supervisor log is preserved
[separately](docs/evidence/render_watchdog.log) so it is not parsed as a render.
The summary was regenerated from the nine render logs using the unchanged
generator; no process outcome was reclassified.

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
git clone --branch aswf/cy2025 --single-branch \
  https://github.com/nicolaspopravka/usd-render-benchmark.git run-cy2025
cd run-cy2025
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
RUNNABLE_IMAGE='ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:dc85819610d10b5d335a0c01e5bf80184ae42c9d07133f8c7be8ecce92e09032'
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

The recorded run used this image on an NVIDIA host. The documentation and
helper have local syntax/lifecycle checks; a complete fresh-asset replay of
these exact instructions has not been performed.

For a separate, bounded Moana/MoonRay attempt, use the
[contribution recipe](docs/MOANA_MOONRAY.md). It deliberately runs that one
combination despite the normal skip and stores its outputs separately.
