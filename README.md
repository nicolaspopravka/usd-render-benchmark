# ASWF CY2023 / Embree Render Benchmark

This branch records a partial Embree 3.2.2 run using the ASWF CY2023
environment and OpenUSD 23.08. It is not a complete CY2023 rerun of the original benchmark.

![Yard 2024 / Embree compared with ASWF CY2023 / Embree](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Embree
- USD: OpenUSD 23.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-embree:cy2023`
  (pinned by digest `sha256:0bc44402ade952b0fe731ebbddddc58195bd6222ff94fffe6048d4c918645999`)
- GPU: NVIDIA L4, 24 GB
- Driver: NVIDIA 570.195.03
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/23.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Rendered images are under [`renderers/Embree/`](renderers/Embree/). Complete
logs are under [`logs/`](logs/).
