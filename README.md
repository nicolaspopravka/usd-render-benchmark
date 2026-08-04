# USD Render Benchmark

This fork extends the original
[Yard renderer benchmark](https://github.com/TheYardVFX/usd-render-benchmark)
into a public evidence ledger for OpenUSD delivery paths, Hydra render
delegates, and VFX Platform stacks.

It records images, process outcomes, timings, memory, logs, and stack
provenance. Partial runs and regressions remain useful results when their
evidence is preserved.

This is an independent community project. It is not ASWF or OpenUSD
certification, and it is not a renderer performance ranking.

> [!NOTE]
> **Snapshot — 2026-08-04**
>
> - **Published:** 15/15 OpenUSD delivery-path results; partial Cycles CY2024,
>   Cycles CY2025, and MoonRay CY2025 CPU evidence.
> - **Investigating:** Cycles 5.2 with OpenUSD 26.03 renders tiles but produces
>   transparent-black output. The next source-pristine cross-version control is
>   defined; no job is currently running.
> - **Waiting upstream:** ASWF image/package findings and OpenUSD Ptex review.
> - **Paused / gated:** MoonRay XPU is not built. It needs build-boundary review
>   and authorized NVIDIA validation.
> - **Not scheduled:** modern commercial-delegate coverage.

**Published** means an immutable evidence snapshot exists; it does not mean the
result was clean. **Investigating** has a concrete next control. **Waiting
upstream** is blocked on an external tracker, review, or release. **Paused /
gated** needs a scope, cost, or build-boundary decision. **Not scheduled** has
no current plan.

## OpenUSD delivery paths

Each linked label reports successful process exits out of three scenes,
followed by the observed OpenChessSet appearance. `Textured`, `black`, and
`fallback` describe that image, not the other two scenes.

| Cycle / renderer | Pixar `build_usd.py` | ASWF `build_usd.sh` | ASWF prebuilt `ci-vfxall` |
| --- | --- | --- | --- |
| CY2023 · GL | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/8dcd605784d72b57e2f858f7eb571182947128db) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/28a36e90d3e3faff31560c3807a94013a45da6db) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/80563c355d8b75a5645140831663c6c296f4a105) |
| CY2024 · GL | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/9c2ec3efd60e15b11c3771071b5805dea73eae7d) | [2/3 black](https://github.com/nicolaspopravka/usd-render-benchmark/tree/2f9cf9443483248074667b9840b4ba52f3637fd4) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/e6a30ac174d7ea953ea967b0dc4155c1f2d6a242) |
| CY2025 · Storm | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/6a59e98969bd6fbb452822b62837eb47ae7bc2cd) | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/922cf2e2b2e81c64f4df9055eff40155fadd79dc) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/bd42959e6a6e74ed42df4b037f6ebfd4aedf98ae) |
| CY2026 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/a1a45a81811a3a058c769911feb0195c7cd568f6) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/45412abdb688001c247a94d95b960afbac4fe50c) | [0/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/9731c90525bc9df4253f209685982857f51ddca9) |
| Candidate CY2027 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/59f9307aa3d2387d3c83122c1a6738ca4ca0ac3d) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/3bd61a9edcbf7dbb89b05755e85c75226006eddb) | [0/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/21149e0baaed60aa9dc98d633bec80ef5272dbc3) |

## Delegate coverage

| Delegate | Published evidence | Current state |
| --- | --- | --- |
| Cycles | **Published partial:** [CY2024 — 2/4 images](https://github.com/nicolaspopravka/usd-render-benchmark/tree/f50746e099d9639711688e9a4b3cda0e542abba7) · [CY2025 — 2/4 images](https://github.com/nicolaspopravka/usd-render-benchmark/tree/e3e2811c0b888552dec69b7b48b43e5de1288a7a) | **Investigating:** Cycles 5.2 / OpenUSD 26.03 renders tiles but produces transparent-black output. Follow [issue #16](https://github.com/nicolaspopravka/usd-render-benchmark/issues/16) and the [work branch](https://github.com/nicolaspopravka/aswf-docker/tree/codex/delegates/cycles-5.2-ghcr). |
| MoonRay | **Published partial:** [CY2025 CPU — three benchmark images, zero clean exits; Moana not run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/b5ce2645bb5ea457f08bee952559345c54953107) | **Paused / gated:** XPU is not built. The reviewed [MoonRay build](https://github.com/nicolaspopravka/aswf-docker/tree/10bffd7af10e6b2760ec43888d62f5cddd1f34c8) is CPU-only; an XPU rebuild and NVIDIA validation require separate review and authorization. |

Modern Karma, RenderMan, and Arnold coverage is **not scheduled**. The
[original Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark)
remains the historical mixed-result reference.

## Findings and upstream follow-up

| State | Finding | Public record |
| --- | --- | --- |
| **Published finding** | ASWF `build_usd.sh` CY2024 produced a solid-black OpenChessSet frame. | [Fork issue #1](https://github.com/nicolaspopravka/usd-render-benchmark/issues/1) · [immutable result](https://github.com/nicolaspopravka/usd-render-benchmark/tree/2f9cf9443483248074667b9840b4ba52f3637fd4) |
| **Published finding** | CY2024 and CY2025 ALab runs preserve `Usd_ClipSet` failures after producing images. | [Fork issue #4](https://github.com/nicolaspopravka/usd-render-benchmark/issues/4) · [matrix evidence](#openusd-delivery-paths) |
| **Waiting upstream** | The ASWF OSL discovery plugin fails to load without `LD_PRELOAD`. | [Fork issue #3](https://github.com/nicolaspopravka/usd-render-benchmark/issues/3) · [aswf-docker #450](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/450) is open |
| **Waiting upstream** | Prebuilt CY2027 MaterialX resources resolve incorrectly and OpenChessSet uses fallback materials. | [Fork issue #10](https://github.com/nicolaspopravka/usd-render-benchmark/issues/10) · [aswf-docker #454](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/454) is open. Related workaround-removal [PR #453](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/453) merged; it is not the fix for #454. |
| **Waiting upstream** | The ASWF-built CY2027 lane reaches MaterialX GLSL compilation but fails on `AIRY_FRESNEL_ITERATIONS`. | [Fork issue #2](https://github.com/nicolaspopravka/usd-render-benchmark/issues/2) · [aswf-docker #455](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/455) is open |
| **Waiting upstream** | Storm fails in the Ptex mipmap-loader path on two Moana Island subtrees. | OpenUSD [#4168](https://github.com/PixarAnimationStudios/OpenUSD/issues/4168) and [#4169](https://github.com/PixarAnimationStudios/OpenUSD/issues/4169) are open; crash-prevention [PR #4176](https://github.com/PixarAnimationStudios/OpenUSD/pull/4176) is under review |

Additional run-level findings are tracked in the
[benchmark issues](https://github.com/nicolaspopravka/usd-render-benchmark/issues).

## Community coordination

Use the
[Ideas discussion](https://github.com/nicolaspopravka/usd-render-benchmark/discussions/18)
to suggest delegate/version combinations, available hardware and drivers,
licensed-renderer interest, scenes, upstream relevance, and priorities.
Failures are valid evidence, and ASWF reference, Pixar control, and delegate
diagnostic lanes remain separate.

Two maintainer-owned issues track the next bounded work:

- [Audit reproduction guidance for the 18 published result refs](https://github.com/nicolaspopravka/usd-render-benchmark/issues/17)
- [Bound the Cycles 5.2 / OpenUSD 26.03 transparent-black result](https://github.com/nicolaspopravka/usd-render-benchmark/issues/16)

This phase accepts feedback and coordination only. External code and benchmark
artifact submissions will wait until the MIT license and contribution terms
are restored on `main`.

## Reading the evidence

The default branch is intentionally a README-only landing page. Each result
link points to an immutable evidence snapshot whose README describes the lane
and whose `render_summary.md`, `logs/`, and `renderers/` directories preserve
the observed result.

A result README is a starting point, not a guarantee of exact replay. Container
digests, asset revisions, commands, graphics setup, hardware, drivers, and
known provenance gaps are being checked in the
[reproduction audit](https://github.com/nicolaspopravka/usd-render-benchmark/issues/17).
