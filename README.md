# ASWF CY2023 / GL Render Benchmark

This branch records a partial GL run using the ASWF CY2023
environment and OpenUSD 23.08. It is not a complete CY2023 rerun of the original benchmark.

![ASWF CY2023 / GL compared with ASWF USD 23.08 / GL](render_sheet.jpg)

## Run configuration

- Renderer: Hydra GL
- USD: OpenUSD 23.08, ASWF [build script](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/2c8484137a2f056a0abfd504dd5ad166240ab47e/scripts/vfx/build_usd.sh).
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:aswf-cy2023-047e110e6b6b0d0f2714bd12026df08a01fcdf92@sha256:bc724ebdb150d44932a4f73df5e8f042ee5a20ac374038812e974c209b9bf855`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/23.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/GL/`](renderers/GL/). Complete
logs are under [`logs/`](logs/).
