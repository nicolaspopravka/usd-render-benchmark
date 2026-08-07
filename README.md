# ASWF CY2027 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2027
environment and OpenUSD 26.05. It is not a complete CY2027 rerun of the original benchmark.

![ASWF CY2027 / Storm compared with Pixar USD 26.05 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 26.05
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:pixar-cy2027-runtime-d97e11fc668c35d8418d446da2ce8cadcd48f0df@sha256:b93a122bb7c173e1336aa210868162c7076f090f188be157116d3d9ee5e747d2`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 9.8

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete logs are under [`logs/`](logs/).
