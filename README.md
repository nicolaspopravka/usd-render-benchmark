# ASWF CY2026 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2026
environment and OpenUSD 26.03. It is not a complete CY2026 rerun of the original benchmark.

![ASWF CY2026 / Storm compared with ASWF USD 26.03 / Storm](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Storm
- USD: OpenUSD 26.03, ASWF [build script](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/2c8484137a2f056a0abfd504dd5ad166240ab47e/scripts/vfx/build_usd.sh).
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:aswf-cy2026-047e110e6b6b0d0f2714bd12026df08a01fcdf92@sha256:c3ce1f2a32f032a62750b60a70b241d732a435459dee6b07f880dd02da3a14c9`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/26.03/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete
logs are under [`logs/`](logs/).
