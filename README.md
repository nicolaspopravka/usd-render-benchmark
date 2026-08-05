# ASWF CY2024 / Cycles Render Benchmark

This branch records a partial Cycles 4.2.0 run using the ASWF CY2024
environment and OpenUSD 24.05. It is not a complete CY2024 rerun of the
original benchmark.

![Yard 2024 / Cycles compared with ASWF CY2024 / Cycles](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Cycles
- USD: OpenUSD 24.05
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-cycles:cycles-4.2.0-openusd-24.05-cy2024-split`
  (pinned by digest `sha256:de9f9d89bda4ddfb2ae7c63ea6231b58a1de13eae44756d4d84e688586f07c00`)
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.172.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/24.05/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously ran OOM.

ALab is also intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Cycles/`](renderers/Cycles/). Complete
logs are under [`logs/`](logs/).
