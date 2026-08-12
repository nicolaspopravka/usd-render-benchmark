# ASWF CY2027 / Cycles Render Benchmark

This branch records a partial Cycles 5.2.0 run using the ASWF CY2027
environment and OpenUSD 26.05. It is not a complete CY2027 rerun of the
original benchmark.

![Yard 2024 / Cycles compared with ASWF CY2027 / Cycles](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Cycles
- USD: OpenUSD 26.05
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-cycles@sha256:01e83c16329522f430af67b3d5aa5d108f1c6c8d3f41868937b6d06957aa7c89`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 9.8

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/26.05/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Cycles/`](renderers/Cycles/). Complete
logs are under [`logs/`](logs/).
