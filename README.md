# ASWF CY2023 / Cycles Render Benchmark

This branch records a partial Cycles 3.6.0 run using the ASWF CY2023
environment and OpenUSD 23.08. It is not a complete CY2023 rerun of the
original benchmark.

![Yard 2024 / Cycles compared with ASWF CY2023 / Cycles](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Cycles
- USD: OpenUSD 23.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-cycles@sha256:4e2e13e261595cc94d4e8c2e6290241f129c4a7e4f1dfd4646224289a9c50b20`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.195.03
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/23.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously failed or exceeded the practical memory limit.

ALab is also intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Cycles/`](renderers/Cycles/). Complete
logs are under [`logs/`](logs/).
