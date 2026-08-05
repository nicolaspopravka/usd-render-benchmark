# ASWF CY2025 / Cycles Render Benchmark

This branch records a partial Cycles 5.0.0 run using the ASWF CY2025
environment and OpenUSD 25.08. It is not a complete CY2025 rerun of the
original benchmark.

![Yard 2024 / Cycles compared with ASWF CY2025 / Cycles](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Cycles
- USD: OpenUSD 25.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-cycles:cycles-5.0.0-openusd-25.08-cy2025-split`
  (pinned by digest `sha256:880723e5754e1a3794531410ea6e4d3a17dfee3b989d4deda19dda142c5e3a22`)
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.172.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/25.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously ran OOM.

ALab is also intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Cycles/`](renderers/Cycles/). Complete
logs are under [`logs/`](logs/).
