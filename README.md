# ASWF CY2023 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2023
environment and OpenUSD 23.08. It is not a complete CY2023 rerun of the original benchmark.

![ASWF CY2023 / Storm compared with ASWF USD 23.08 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 23.08
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:aswf-cy2023-047e110e6b6b0d0f2714bd12026df08a01fcdf92@sha256:bc724ebdb150d44932a4f73df5e8f042ee5a20ac374038812e974c209b9bf855`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/GL/`](renderers/GL/). Complete logs are under [`logs/`](logs/).
