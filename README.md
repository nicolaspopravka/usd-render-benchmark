# ASWF CY2026 / Cycles Render Benchmark

This branch records a partial Cycles 5.2.0 run using the ASWF CY2026
environment and OpenUSD 26.03. It is not a complete CY2026 rerun of the
original benchmark.

![Yard 2024 / Cycles compared with ASWF CY2026 / Cycles](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Cycles
- USD: OpenUSD 26.03
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-cycles@sha256:5c1359c29c619c72afdcb39aab50b73c630f2dafa6e9a1fdc44d8b7bd9b30311`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.172.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/26.03/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

OpenChessSet is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously failed or exceeded the practical memory limit.

Rendered images are under [`renderers/Cycles/`](renderers/Cycles/). Complete
logs are under [`logs/`](logs/).
