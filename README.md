# USD Render Benchmark

This fork extends the original
[Yard renderer benchmark](https://github.com/TheYardVFX/usd-render-benchmark)
into a public results ledger for OpenUSD delivery paths, Hydra render
delegates, and VFX Platform stacks.

It records images, process outcomes, timings, memory, logs, and the build stack
used. Partial runs and regressions remain useful results when their logs and
outputs are preserved.

This is an independent community project. It is not ASWF or OpenUSD
certification, and it is not a renderer performance ranking.

> [!NOTE]
> **Snapshot — 2026-08-04**
>
> - **Published:** 15/15 OpenUSD delivery-path results; partial Cycles CY2024,
>   Cycles CY2025, and MoonRay CY2025 CPU results.
> - **Investigating:** Cycles 5.2 with OpenUSD 26.03 renders tiles but produces
>   transparent-black output. The next unmodified-source cross-version control is
>   defined; no job is currently running.
> - **Waiting upstream:** ASWF image/package findings and OpenUSD Ptex review.
> - **Paused:** MoonRay XPU is not built. It will not proceed until build review
>   and authorized NVIDIA validation are done.
> - **Not scheduled:** modern commercial-delegate coverage.

**Published** means a pinned snapshot of the run's outputs exists; it does not
mean the result was clean. **Investigating** has a concrete next control.
**Waiting upstream** is blocked on an external tracker, review, or release.
**Paused** needs a scope, cost, or build review decision. **Not scheduled** has
no current plan.

## OpenUSD delivery paths

Each linked label reports successful process exits out of three scenes,
followed by the observed OpenChessSet appearance. `Textured`, `black`, and
`fallback` describe that image, not the other two scenes.

| Cycle / renderer | Pixar `build_usd.py` | ASWF `build_usd.sh` | ASWF prebuilt `ci-vfxall` |
| --- | --- | --- | --- |
| CY2023 · GL | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/c9c991a999f8b9c2e9bb5337cc2272fa27d824aa) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/c5d06b7bbc17f752c090ddb39a71e402e1c46131) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/bb72885fc55ff8c746eb222f6869056a3add4a97) |
| CY2024 · GL | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/23402807430abc928e880bd13c24c0c09e52ebc3) | [2/3 black](https://github.com/nicolaspopravka/usd-render-benchmark/tree/46729937133729068f279e464784959667f09ab9) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/8daa2eeee2d9e2d969dc26472e5dfef4cf0fbe98) |
| CY2025 · Storm | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/20254fd1c5d17150de936d5716cbae2f144cc767) | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/b162dd7ec760db2d73ca6f34e382b727c070e6be) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/cc22a590d380bfdeb1d74859824df0304ddb29bf) |
| CY2026 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/b0ae01b750e713d61b9bfa1218b53fa4b9bdfef6) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/48e351a2bee476b4bdcd7e23028ca47579325e54) | [0/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/7c5cb01a9837815e29cda594d623a014d0d12ea2) |
| Candidate CY2027 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/35492323fb2648c69c0c560ce12512376d1bd59a) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/8a94d2e9e417af8dfaa1881d031aa308be3bed57) | [0/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/6b43bffc0ae3fd6cc2fc4008100d756ce05aecea) |

## Delegate coverage

| Delegate | Published results | Current state |
| --- | --- | --- |
| Cycles | **Published partial:** [CY2024 — 2/4 images](https://github.com/nicolaspopravka/usd-render-benchmark/tree/fbb3ea60e0f8ed691c1002354097741302f9ba93) · [CY2025 — 2/4 images](https://github.com/nicolaspopravka/usd-render-benchmark/tree/fc634112bd3212071f983080c781d3dc122c2b34) | **Investigating:** Cycles 5.2 / OpenUSD 26.03 renders tiles but produces transparent-black output. Follow [issue #16](https://github.com/nicolaspopravka/usd-render-benchmark/issues/16) and the [work branch](https://github.com/nicolaspopravka/aswf-docker/tree/codex/delegates/cycles-5.2-ghcr). |
| MoonRay | **Published partial:** [CY2025 CPU — three benchmark images, zero clean exits; Moana not run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/1cc28d9710815a9e5f1f85b708e093fafafdb240) | **Paused:** XPU is not built. The reviewed [MoonRay build](https://github.com/nicolaspopravka/aswf-docker/tree/10bffd7af10e6b2760ec43888d62f5cddd1f34c8) is CPU-only; an XPU rebuild and NVIDIA validation require separate review and authorization. |

Modern Karma, RenderMan, and Arnold coverage is **not scheduled**. The
[original Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark)
remains the historical mixed-result reference.

## Findings and upstream follow-up

| State | Finding | Public record |
| --- | --- | --- |
| **Published finding** | ASWF `build_usd.sh` CY2024 produced a solid-black OpenChessSet frame. | [Fork issue #1](https://github.com/nicolaspopravka/usd-render-benchmark/issues/1) · [pinned result](https://github.com/nicolaspopravka/usd-render-benchmark/tree/46729937133729068f279e464784959667f09ab9) |
| **Published finding** | CY2024 and CY2025 ALab runs preserve `Usd_ClipSet` failures after producing images. | [Fork issue #4](https://github.com/nicolaspopravka/usd-render-benchmark/issues/4) · [benchmark table](#openusd-delivery-paths) |
| **Waiting upstream** | The ASWF OSL discovery plugin fails to load without `LD_PRELOAD`. | [Fork issue #3](https://github.com/nicolaspopravka/usd-render-benchmark/issues/3) · [aswf-docker #450](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/450) is open |
| **Waiting upstream** | Prebuilt CY2027 MaterialX resources resolve incorrectly and OpenChessSet uses fallback materials. | [Fork issue #10](https://github.com/nicolaspopravka/usd-render-benchmark/issues/10) · [aswf-docker #454](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/454) is open. Related workaround-removal [PR #453](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/453) merged; it is not the fix for #454. |
| **Waiting upstream** | The ASWF-built CY2027 run reaches MaterialX GLSL compilation but fails on `AIRY_FRESNEL_ITERATIONS`. | [Fork issue #2](https://github.com/nicolaspopravka/usd-render-benchmark/issues/2) · [aswf-docker #455](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/455) is open |
| **Waiting upstream** | Storm fails in the Ptex mipmap-loader path on two Moana Island subtrees. | OpenUSD [#4168](https://github.com/PixarAnimationStudios/OpenUSD/issues/4168) and [#4169](https://github.com/PixarAnimationStudios/OpenUSD/issues/4169) are open; crash-prevention [PR #4176](https://github.com/PixarAnimationStudios/OpenUSD/pull/4176) is under review |

Additional run-level findings are tracked in the
[benchmark issues](https://github.com/nicolaspopravka/usd-render-benchmark/issues).

## Community coordination

Use the
[Ideas discussion](https://github.com/nicolaspopravka/usd-render-benchmark/discussions/18)
to suggest delegate/version combinations, available hardware and drivers,
licensed-renderer interest, scenes, upstream relevance, and priorities.
Failures are valid results, and ASWF reference, Pixar control, and delegate
diagnostic runs remain separate.

Two maintainer-run issues track the next defined work:

- [Audit reproduction guidance for the 18 published result refs](https://github.com/nicolaspopravka/usd-render-benchmark/issues/17)
- [Pin down the Cycles 5.2 / OpenUSD 26.03 transparent-black result](https://github.com/nicolaspopravka/usd-render-benchmark/issues/16)

This phase accepts feedback and coordination only. External code and benchmark
artifact submissions will wait until the MIT license and contribution terms
are restored on `main`.

## Reading the results

The default branch is intentionally a README-only landing page. Each result
link points to a pinned snapshot of the run's outputs whose README describes
the branch and whose `render_summary.md`, `logs/`, and `renderers/`
directories preserve the observed result.

A result README is a starting point, not a guarantee of exact replay. Container
digests, asset revisions, commands, graphics setup, hardware, drivers, and
known gaps in the build and asset origin are being checked in the
[reproduction audit](https://github.com/nicolaspopravka/usd-render-benchmark/issues/17).
