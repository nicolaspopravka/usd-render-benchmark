# ASWF CY2025 / Embree Render Benchmark

This branch records a partial Embree 3.2.2 run using the ASWF CY2025
environment and OpenUSD 25.05.01. It is not a complete CY2025 rerun of the original benchmark.

![Yard 2024 / Embree compared with ASWF CY2025 / Embree](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Embree
- USD: OpenUSD 25.05.01
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-embree:cy2025`
  (pinned by digest `sha256:d158905b419e41d80e9b33da6d9305f730ae9ae7c519f81a7470fb23a9f60383`)
- GPU: NVIDIA L4, 24 GB
- Driver: NVIDIA 570.195.03
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/25.05.01/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Rendered images are under [`renderers/Embree/`](renderers/Embree/). Complete
logs are under [`logs/`](logs/).
