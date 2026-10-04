# Attempt the Moana Island Scene with MoonRay

This recipe runs only the Moana Island Scene with MoonRay in this branch's
pinned runnable image. It bypasses the ordinary harness's skip for that
combination and writes to a new `local-runs/` directory. It does not replace the
published images or change `render_script.sh`.

Coordinate in the project's scene-coverage discussion before starting a long
attempt. The initial contribution target is **CY2025**. Attempts on CY2023 or
CY2024 are separate results; use the recipe and image from the selected branch.

## What is known

The September 29 `2025.3` image includes MoonRay XPU and Cycles OptiX support.
The [annual run](../README.md) uses this image with default device selection;
GPU support is a build feature, not a promise of GPU use for every scene.

Two separate MoonRay attempts still have no image:

| Attempt | Container RAM limit | Observed peak | Outcome |
| --- | --- | --- | --- |
| Earlier CPU configuration | 262.6 GiB | 106.0 GiB | Scene preparation completed in 8:27; subsequently timed out without an image |
| September 29, XPU requested, A100 80 GB | 116.4 GiB | 83.1 GiB | Deadline reached during scene preparation after a 20-minute window |

Historical evidence: [CPU log](https://github.com/nicolaspopravka/usd-render-benchmark/blob/e93c102dd788a718138b5464c354bf4574407383/logs/Moonray_island.log),
[CPU resource record](https://github.com/nicolaspopravka/usd-render-benchmark/blob/e93c102dd788a718138b5464c354bf4574407383/logs/Moonray_island.resources.txt),
[XPU log](https://github.com/nicolaspopravka/usd-render-benchmark/blob/43b4263c4f6364a01dcefd1b7e71a31d919c2c75/logs/Moonray_island.log),
and [XPU resource record](https://github.com/nicolaspopravka/usd-render-benchmark/blob/43b4263c4f6364a01dcefd1b7e71a31d919c2c75/logs/Moonray_island.resources.txt).

Neither recorded an OOM kill. The second attempt did not reach the point where
GPU engagement could be established. These are failed, timed-out attempts;
final memory demand and completion time remain unknown.

Both configurations were attempted again on October 3, 2026, with separate
results shared through this recipe:

- [CPU/default attempt](https://github.com/nicolaspopravka/usd-render-benchmark/discussions/55#discussioncomment-18740786):
  preparation completed in 6:33; the 40-minute deadline expired without an image.
  Peak container memory was 105.7 GiB.
- [XPU-requested A100 attempt](https://github.com/nicolaspopravka/usd-render-benchmark/discussions/55#discussioncomment-18740787):
  the 20-minute deadline expired during preparation without an image.
  Peak sampled container memory was 90.7 GiB.

Each reply includes its configuration, differences from the earlier attempt,
full logs and resource records. Neither recorded a sampled OOM kill. These
remain incomplete attempts; they do not establish completion time, final memory
demand or GPU engagement.

There is no evidence yet that XPU reduces the Moana Island Scene's host-memory
requirement. Please record both GPU and container memory. MoonRay's Arras worker
can also exit while the client remains alive
([#51](https://github.com/nicolaspopravka/usd-render-benchmark/issues/51)); retain
the whole-container deadline even on a large machine.

## Prepare the scene

Use a Linux x86-64 NVIDIA host configured as described in the
[branch README](../README.md#run-this-branch-locally). The host also needs GNU
`timeout`, `sha256sum`, Git and Bash. For this isolated attempt, McUsd,
OpenChessSet and ALab are not needed; clone the run branch without initialising
its submodules if you do not intend to run them.

Download the USD v2.1 archive from the official
[Moana Island Scene page](https://www.disneyanimation.com/resources/moana-island-scene/):
[`island-usd-v2.1.tgz`](https://datasets.disneyanimation.com/moanaislandscene/island-usd-v2.1.tgz).
The historical benchmark used that USD archive; do not substitute a different
scene translation. Check it before extraction:

```bash
printf '%s  %s\n' \
  '72c0d0a5173e5183f8a1fa35218b980c453d103d74d7c5d8ba070468ea419b62' \
  'island-usd-v2.1.tgz' | sha256sum --check
```

Extract the archive into a dedicated asset directory, retaining its directory
structure. Pass the directory containing `usd/island.usda` to the helper; its
sibling texture directories must remain present. For example:

```text
/data/MoanaIsland/
  usd/island.usda
  textures/...
  ...
```

Allow space for both the archive and extracted assets, the image and logs.
Record any changes to the asset. The archive checksum identifies the source;
it does not prove an already modified extraction is identical.

## Run one bounded attempt

From the run checkout, pull its pinned image:

```bash
RUNNABLE_IMAGE=$(cat runnable_image.txt)
docker pull "$RUNNABLE_IMAGE"
```

Choose a time limit in seconds that fits your available machine time. This
example permits at most 12 hours; it is not an estimate of completion time:

```bash
bash tools/run_moana_moonray.sh /data/MoanaIsland 43200 xpu
```

The helper mounts the checkout and scene read-only, selects `Moonray`, the
`/island/cam/shotCam` camera and `render` purpose, and keeps the wrapper's default
frame, width and sampling settings. Its default output width is 960 pixels.
It sets the soft/hard open-file limit to 65536. The explicit `xpu` argument
sets `HDMOONRAY_EXEC_MODE=xpu` and `REZ_MOONRAY_ROOT=/usr/local` after Rez
resolves its packages, so MoonRay can locate its installed GPU programs.
Use `default` instead of `xpu` to leave device selection unchanged. The helper
records that choice. This targeted override does not change the annual
benchmark harness. An XPU request does not prove that the GPU was reached;
inspect the sampled GPU/process memory alongside the render log.

A host-side deadline stops the **entire container**, including Arras workers.
Interrupting the helper also stops it. The helper returns 124 on its deadline;
a normal return preserves the container's exit status. Inspect logs and image
separately in either case. To follow progress from another terminal, use the
container name saved in `local-runs/moana-moonray-*/container-name.txt`:

```bash
docker logs --follow CONTAINER_NAME
```

The output directory contains the image if written, timestamped container logs,
container state, sampled cgroup counters, timing/exit records when available,
host and GPU details, sampled GPU/process memory, requested mode, image identity
and checkout changes. Temporary files are
retained beneath `tmp/`; the stopped container is retained for investigation.
After reviewing the output, remove it with the `docker rm` command printed by
the helper. Rootful Docker can create root-owned output files.

The Docker helper delegates rendering and resource sampling to
`tools/moana_moonray_worker.sh`; the helper enforces the whole-container deadline
and retains Docker state and logs.
The shared worker was exercised in the two bounded attempts linked above using
direct RunPod execution. Worker and Docker lifecycle fixtures also pass, but
the refactored Docker helper has not been exercised on a real NVIDIA host.
Preserve setup failures as well as render failures.

## Share the result

Reply in the scene-coverage discussion with:

- The year, checkout commit, pinned image digest and any changes.
- CPU, vCPU count, host/container RAM limits, GPU and driver.
- Asset archive checksum, extracted-asset changes and chosen deadline.
- Whether an image was written, whether the process returned, and observed
  errors. Include the image even if its appearance is wrong.
- `container.log`, `container-state.json`, `resources.txt`, `time.txt` and
  `render-exit.txt` when present, plus the helper's metadata files.

Inspect files before sharing for machine names, local paths or other information
you prefer to remove; identify any redactions. Do not upload the scene archives
or temporary scene copies. Retain the complete local bundle for follow-up.

The scene is provided by Walt Disney Animation Studios under the
[Moana Island Scene license](https://media.disneyanimation.com/uploads/production/data_set_asset/4/asset/License.txt).
Follow its attribution and research/benchmarking conditions when sharing output;
this benchmark is independent of Disney. State how you want your contribution
credited and whether the project may republish your logs and image under the
applicable terms. A contributed attempt is reviewed separately before becoming
a published benchmark snapshot; no code contribution or asset redistribution
is required.
