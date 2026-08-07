# ASWF CY2025 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2025
environment and OpenUSD 25.05.01. It is not a complete CY2025 rerun of the original benchmark.

![ASWF CY2025 / Storm compared with ASWF USD 25.05.01 / Storm](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Storm
- USD: OpenUSD 25.05.01, ASWF [build script](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/2c8484137a2f056a0abfd504dd5ad166240ab47e/scripts/vfx/build_usd.sh).
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:aswf-cy2025-996dc7d09e24cac066facab2fb59b6a7b451594e@sha256:dddbaa772a7237a3c6ab0da7f01d38114905380667e6d30d9713184e6d047e89`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/25.05/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete
logs are under [`logs/`](logs/).
