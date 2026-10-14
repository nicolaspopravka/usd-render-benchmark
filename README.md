# USD Render Benchmark — `demo/run3`

This branch renders Teapot with Storm, Cycles and MoonRay using a mounted
benchmark checkout and a reusable container image. The image supplies the
software environment; this branch supplies the scene and renderer selection.

## Run configuration

- Renderers: Storm, Cycles and MoonRay
- Scene: `assets/full_assets/Teapot/Teapot.usd`
- Camera: `main_cam`
- Container: the runnable image selected for the run

## Run through GitHub Actions

Set `RUNNABLE_IMAGE` to the pinned runnable reference printed by the stack build:

```bash
gh workflow run run-demo.yml \
  --repo nicolaspopravka/usd-render-benchmark-stack \
  -f run_branch=demo/run3 \
  -f runnable_image="$RUNNABLE_IMAGE"
```

The workflow mounts this branch into the image, runs the harness with Mesa and
Xvfb, and uploads the `run-output` artifact.

## Outputs

The artifact contains per-renderer logs under `logs/`, produced images under
`renderers/`, and `render_summary.md`. The harness continues after a renderer
fails; inspect the logs and images as well as the workflow result.

This branch is a reusable demo. Versions, timings and render outcomes depend
on the selected image and belong to each run's outputs.
