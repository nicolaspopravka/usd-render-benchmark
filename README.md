# ASWF CY2024 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2024
environment and OpenUSD 24.08. It is not a complete CY2024 rerun of the original benchmark.

![ASWF CY2024 / Storm compared with Pixar USD 24.08 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 24.08
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:pixar-cy2024-runtime-d97e11fc668c35d8418d446da2ce8cadcd48f0df@sha256:7c00a1fa0bf35cf57a5486340febdc505a099c97f9653cc54a32929433088470`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/GL/`](renderers/GL/). Complete logs are under [`logs/`](logs/).
