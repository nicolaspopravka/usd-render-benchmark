# ASWF CY2025 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2025
environment and OpenUSD 25.05.01. It is not a complete CY2025 rerun of the original benchmark.

![ASWF CY2025 / Storm compared with Pixar USD 25.05.01 / Storm](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Storm
- USD: OpenUSD 25.05.01, Pixar [build script](https://github.com/PixarAnimationStudios/OpenUSD/blob/v25.05.01/build_scripts/build_usd.py).
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:pixar-cy2025-runtime-d751e4438fad48a1d4898b83a930f22a729550b8@sha256:830e184d5323937e05cc30c739dbd321705dfa152f2bb73a5519bfee391fadd5`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/25.05/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete
logs are under [`logs/`](logs/).
