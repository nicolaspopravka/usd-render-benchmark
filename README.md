# ASWF CY2027 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2027
environment and OpenUSD 26.05. It is not a complete CY2027 rerun of the original benchmark.

![ASWF CY2027 / Storm compared with ASWF USD 26.05 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 26.05
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:aswf-cy2027-047e110e6b6b0d0f2714bd12026df08a01fcdf92@sha256:606f4e84d32e324026a0e220cd0513533bcb4ff7f4ff5e50c958a3a9b5a6dba8`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 9.8

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete logs are under [`logs/`](logs/).
