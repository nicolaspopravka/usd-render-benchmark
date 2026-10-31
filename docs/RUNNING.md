# Running the benchmark

A run branch supplies the harness, Rez packages and scenes; its container
image supplies OpenUSD and the delegates. Outputs stay in the mounted checkout.
Use a new checkout for each attempt. The demo overwrites its recorded outputs;
the annual recipe archives them before rendering.
Rootful Docker may create root-owned files.

## Software demo

This renders Teapot with Storm, stock `usdrecord`
and Mesa under Xvfb. It needs Git and Docker with Linux x86-64 support,
but no NVIDIA GPU. It demonstrates the run model, not renderer performance.

### Clone

```bash
git clone --depth 1 --branch demo/run1 --single-branch \
  https://github.com/nicolaspopravka/usd-render-benchmark.git demo-run
cd demo-run
git submodule update --init assets
```

Only the assets submodule is needed. Its pinned Teapot files are regular Git
files; Git LFS, ALab and Moana downloads are unnecessary for this demo.

### Run

```bash
DEMO_IMAGE=ghcr.io/nicolaspopravka/usd-render-benchmark:2026
docker pull "$DEMO_IMAGE"
docker run --rm --platform linux/amd64 \
  --mount type=bind,source="$PWD",target=/benchmark \
  --workdir /benchmark --entrypoint bash "$DEMO_IMAGE" -c '
    set -e
    dnf install -y --disablerepo=cuda mesa-dri-drivers
    LIBGL_ALWAYS_SOFTWARE=1 \
      xvfb-run -a bash render_script.sh
    python3 generate_render_summary.py --system-specs "Software-rendered Docker demo"
  '
```

The runnable image sets `REZ_PACKAGES_PATH=./packages`, so it finds the mounted
checkout’s packages from `/benchmark`.

Open `renderers/Storm/Teapot.jpg` and read `render_summary.md`. If the summary
reports Failure, inspect `logs/Storm_Teapot.log`; an old image may remain after a
failed attempt. The harness itself can exit 0 after a renderer failure.

The image tag can change. Mesa is installed at execution time. The summary's
system description is a demo label, not measured hardware specifications.

### GitHub Actions alternative

With permission to dispatch workflows in the stack repository, set `DEMO_IMAGE`
to the value in the Run command above and run:

```bash
gh workflow run run-demo.yml \
  --repo nicolaspopravka/usd-render-benchmark-stack \
  -f run_branch=demo/run1 -f runnable_image="$DEMO_IMAGE"
```

The [workflow](https://github.com/nicolaspopravka/usd-render-benchmark-stack/blob/main/.github/workflows/run-demo.yml)
uploads logs, images and the summary as `run-output`. Inspect the artifact;
workflow success alone does not establish a successful render. The workflow's
summary currently records the image reference rather than collected hardware
specifications. Dispatch requires an authenticated account with repository access.

## Annual NVIDIA benchmark

Use a Linux x86-64 host with Docker, a compatible NVIDIA driver and the
[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
Docker Desktop on macOS does not supply this NVIDIA setup. Allow disk space for
the container and expanded assets, and enough memory for the selected scenes.

These branches use `tools/usdrecord_egl.py` through Rez instead of stock
`usdrecord`'s Qt display context. Even CPU-computing delegates need NVIDIA
graphics access for this wrapper. Device selection remains at its default;
Cycles uses the CPU. Recorded GPU hardware does not establish GPU computation.

### Prepare

This example uses CY2025. For CY2023 or CY2024, change `RUN_BRANCH` and select
the image from that branch's README. For the exact recorded image, use the full
Container value from the run README.

```bash
RUN_BRANCH=aswf/cy2025
RUNNABLE_IMAGE=ghcr.io/nicolaspopravka/usd-render-benchmark:2025.3@sha256:dc85819610d10b5d335a0c01e5bf80184ae42c9d07133f8c7be8ecce92e09032
git lfs install
git clone --branch "$RUN_BRANCH" --single-branch \
  https://github.com/nicolaspopravka/usd-render-benchmark.git annual-run
cd annual-run
git submodule update --init --recursive
git -C assets lfs pull
git -C scenes/ALab lfs pull
```

ALab also requires **v2.2.0 Techvar Assets** and **Baked Procedurals** from
[Digital Production Example Library (DPEL)](https://dpel.aswf.io/alab/). Merge them using the
[ALab setup instructions](https://github.com/DigitalProductionExampleLibrary/ALab/blob/20a3e1d5ea034072fc97d5fee04e51016c11218a/README.md).
Confirm `scenes/ALab/ALab/entry.usda` exists and its referenced payloads are
present. All three harnesses skip Moana, so no Moana download is needed.
Keep `problematic_combinations` unchanged; current skips may differ from
historical attempts in the published snapshot.

Fetch the shared hardware helper from main, without changing the run checkout:

```bash
docker pull "$RUNNABLE_IMAGE"
mkdir -p local-runs
git fetch origin main
git show FETCH_HEAD:tools/system_specs.py > local-runs/system_specs.py
```

### Render and summarize

Archive the checkout's published outputs so a failed attempt cannot reuse them:

```bash
PUBLISHED_OUTPUTS=$(mktemp -d "$PWD/local-runs/published.XXXXXX")
mv logs renderers render_summary.md "$PUBLISHED_OUTPUTS/"
docker run --rm --gpus all \
  --env NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics \
  --ulimit nofile=65536:65536 \
  --mount type=bind,source="$PWD",target=/benchmark \
  --env REZ_PACKAGES_PATH=/benchmark/packages \
  --workdir /benchmark --entrypoint bash "$RUNNABLE_IMAGE" -c '
    set -e
    bash render_script.sh
    python3 generate_render_summary.py --system-specs "$(python3 local-runs/system_specs.py)"
  '
```

Keep `/benchmark` as the working directory: the Rez package redirects
`usdrecord` using a relative path. The explicit Rez search path selects the
mounted branch’s packages, including when using older runnable images.
Read each new log and inspect every image. Summary Success/Failure records
process outcome, not visual correctness. Skipped renders should have no new
outputs. The helper collects a compact hardware description inside the container.

`--ulimit nofile=65536:65536` raises the container's soft and hard open-file
limits before MoonRay starts. It avoids the ALab texture failures reproduced
with OIIO's open-file clamp on a low-limit RunPod host
([issue #27](https://github.com/nicolaspopravka/usd-render-benchmark/issues/27#issuecomment-5832825316)).
An affinity-aware OIIO reserve is recorded there as an unfiled upstream
candidate.

### Optional evidence and preflight

For a contributed result, record the checkout and image before archiving the
published outputs:

```bash
git rev-parse HEAD > local-runs/checkout.txt
git diff --binary > local-runs/checkout.patch
git submodule status --recursive > local-runs/submodules.txt
printf '%s\n' "$RUNNABLE_IMAGE" > local-runs/image.txt
```

The following commands check OpenUSD’s Python import and record the visible
NVIDIA devices and open-file limit. They do not verify Hydra plugin loading
or successful rendering. Optionally insert them immediately after `set -e`
in the container command:

```bash
rez env aswf -- python3 -c "from pxr import Usd; print(Usd.GetVersion())"
nvidia-smi > local-runs/nvidia-smi.txt
ulimit -Sn > local-runs/nofile.txt
```

## Optional annual render sheet

After the annual images are ready, use the same `RUNNABLE_IMAGE` and checkout.
The helper comes from main fetched during preparation; if another Git fetch has
replaced `FETCH_HEAD`, run `git fetch origin main` again first:

```bash
git show FETCH_HEAD:tools/generate_render_sheet.py > local-runs/generate_render_sheet.py
docker run --rm \
  --mount type=bind,source="$PWD",target=/benchmark \
  --env REZ_PACKAGES_PATH=/benchmark/packages \
  --workdir /benchmark --entrypoint bash "$RUNNABLE_IMAGE" -c '
    set -e
    python3 -m pip install "Pillow>=10.1"
    rez env aswf -- python3 local-runs/generate_render_sheet.py
  '
```

The sheet reads images from `renderers/` and version labels from resolved Rez
packages. It does not read the README, summary or logs. Every missing image is
labeled “Skipped,” including images absent because rendering failed; consult
the logs and summary for the actual outcome.

## Limitations

- **Validation is limited.** The software demo completed on Docker Desktop and
  in GitHub Actions [run #119](https://github.com/nicolaspopravka/usd-render-benchmark-stack/actions/runs/41222067959).
  The Actions image was visually inspected and matches the previous published
  demo image byte-for-byte. The full annual NVIDIA commands were inspected
  against the published branches but were not rerun during this documentation
  review.
- **Image tags can change.** A short tag selects the image carrying that tag
  when it is pulled. The Container value with a digest in a run README selects
  that run's recorded image.
- **A clone does not include every scene file.** ALab needs extra downloads.
  The recorded Git versions do not prove those extra files are identical.
- **A completed command is not proof of a correct image.** Check the summary,
  logs and images. A render can write an image and still fail or have missing
  textures; the harness can return 0 after a renderer fails.
- **Timings and memory depend on the machine.** Hardware and drivers differ
  between runs. MoonRay's memory figure may miss some worker processes, so it
  may understate total memory use.
- **Coverage is incomplete.** The demo tests only Storm/Teapot. Annual runs skip
  some renders and disable some renderer features. They do not establish the
  same annual coverage on CY2026 and CY2027.
