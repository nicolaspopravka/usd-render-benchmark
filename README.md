# ASWF CY2025 / Moonray Render Benchmark

This branch records a partial MoonRay 2026.29.1 run using the ASWF CY2025
environment and OpenUSD 25.05.01. It is not a complete CY2025 rerun of the
original benchmark.

![Yard 2024 / Moonray compared with ASWF CY2025 / Moonray](render_sheet.jpg)

## Run configuration

- Renderer: Hydra MoonRay
- USD: OpenUSD 25.05.01
- Container: `ghcr.io/nicolaspopravka/openmoonray-hydra@sha256:75945fa61e05ee39c46d9f82c6e2add7759ac242568f5a51127d76170e1661fc`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.172.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/25.05.01/package.py`) redirects
the `usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously ran OOM.

Rendered images are under [`renderers/Moonray/`](renderers/Moonray/). Complete
logs are under [`logs/`](logs/).
