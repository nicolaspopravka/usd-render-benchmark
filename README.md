# ASWF CY2023 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2023
environment and OpenUSD 23.08. It is not a complete CY2023 rerun of the original benchmark.

![ASWF CY2023 / Storm compared with Pixar USD 23.08 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 23.08
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:pixar-cy2023-runtime-d97e11fc668c35d8418d446da2ce8cadcd48f0df@sha256:dc7795de1475b29df6653780fac2a7b9dac97e1e9edb86e8321cf7cd32c4b551`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/GL/`](renderers/GL/). Complete logs are under [`logs/`](logs/).
