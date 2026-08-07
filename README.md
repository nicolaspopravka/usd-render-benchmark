# ASWF CY2026 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2026
environment and OpenUSD 26.03. It is not a complete CY2026 rerun of the original benchmark.

![ASWF CY2026 / Storm compared with Pixar USD 26.03 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 26.03
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:pixar-cy2026-runtime-d97e11fc668c35d8418d446da2ce8cadcd48f0df@sha256:e8be58f5aefd606cc7237e665d5c2c6f906968d21ca3e738f1378b545b438330`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete logs are under [`logs/`](logs/).
