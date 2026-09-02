# ASWF CY2024 / Embree Render Benchmark

This branch records a partial Embree 3.2.2 run using the ASWF CY2024
environment and OpenUSD 24.08. It is not a complete CY2024 rerun of the original benchmark.

![Yard 2024 / Embree compared with ASWF CY2024 / Embree](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Embree
- USD: OpenUSD 24.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-embree:cy2024`
  (pinned by digest `sha256:ed4a51a50d5a18e56a2e2e5f8d7b936b3ce3558273775e6b3cb43c4319893049`)
- GPU: NVIDIA L4, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/24.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Rendered images are under [`renderers/Embree/`](renderers/Embree/). Complete
logs are under [`logs/`](logs/).
