# ASWF CY2024 / GL Render Benchmark

This branch records a partial GL run using the ASWF CY2024
environment and OpenUSD 24.08. It is not a complete CY2024 rerun of the original benchmark.

![ASWF CY2024 / GL compared with Pixar USD 24.08 / GL](render_sheet.jpg)

## Run configuration

- Renderer: Hydra GL
- USD: OpenUSD 24.08, Pixar [build script](https://github.com/PixarAnimationStudios/OpenUSD/blob/v24.08/build_scripts/build_usd.py).
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:pixar-cy2024-runtime-d97e11fc668c35d8418d446da2ce8cadcd48f0df@sha256:7c00a1fa0bf35cf57a5486340febdc505a099c97f9653cc54a32929433088470`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/24.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/GL/`](renderers/GL/). Complete
logs are under [`logs/`](logs/).
