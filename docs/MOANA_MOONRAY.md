# Attempt the Moana Island Scene with MoonRay

This recipe runs only the Moana Island Scene with MoonRay in this branch's
pinned runnable image. It bypasses the ordinary harness's skip for that
combination and writes to a new `local-runs/` directory. It does not replace the
published images or change `render_script.sh`.

Coordinate in the project's scene-coverage discussion before starting a long
attempt. The initial contribution target is **CY2025**. Attempts on CY2023 or
CY2024 are separate results; use the recipe and image from the selected branch.

## What is known

Earlier MoonRay attempts lost their Arras worker under memory pressure. The
client can remain alive after the worker exits
([#51](https://github.com/nicolaspopravka/usd-render-benchmark/issues/51)).

A later CY2025 attempt, using the same image as the annual CY2025 result, ran on
64 vCPUs with a 262.6 GiB container memory limit. It completed scene preparation
in about 8 minutes 27 seconds, then continued rendering until the roughly
40-minute window ended. There was no image. The sampled cgroup peak was
105.9 GiB, with zero recorded OOM kills. This is an incomplete attempt: neither
the final memory demand nor the time to completion is established. Those
figures are observations, not a guaranteed minimum machine specification.
The [retained resource record](moonray-island-observed-resources.txt) identifies
that CY2025 attempt; the full log remains available for investigation.

The ordinary process-memory field can miss the separately running Arras worker.
The helper therefore samples container memory counters as well as collecting
`/usr/bin/time` output. Missing timing records after a timeout are expected and
must not be reported as a successful render.

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
bash tools/run_moana_moonray.sh /data/MoanaIsland 43200
```

The helper mounts the checkout and scene read-only, selects `Moonray`, the
`/island/cam/shotCam` camera and `render` purpose, and keeps the wrapper's default
frame, width and sampling settings. Its default output width is 960 pixels.
It sets the soft/hard open-file limit to 65536 and preserves the image's
renderer environment. Do not switch to XPU or another image without identifying
that as a different configuration.

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
host and GPU details, image identity and checkout changes. Temporary files are
retained beneath `tmp/`; the stopped container is retained for investigation.
After reviewing the output, remove it with the `docker rm` command printed by
the helper. Rootful Docker can create root-owned output files.

This helper has been checked with lifecycle fixtures and local container
preflights. Its full GPU/Arras execution has not yet been validated on an NVIDIA
host. A first community attempt should preserve setup failures as well as
render failures.

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
