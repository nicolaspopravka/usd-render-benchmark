# ASWF CY2024 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2024
environment and OpenUSD 24.08. It is not a complete CY2024 rerun of the original benchmark.

![ASWF CY2024 / Storm compared with ASWF USD 24.08 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 24.08
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:aswf-cy2024-d6b710a0b02eea4cd3f06d19387c0d1d71f937c4@sha256:e3a37cb3edb9ce6b7ba8ed01102410f963036588cc411eb46416202669632987`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/GL/`](renderers/GL/). Complete logs are under [`logs/`](logs/).
