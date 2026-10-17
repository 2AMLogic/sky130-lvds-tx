# sky130-lvds-tx — agent instructions

Open-source canary block: a ~1 Gb/s-per-lane LVDS-class transmitter with
custom pad cells on SkyWater sky130, designed and verified by AI agents.
**Mixed-signal** — a synthesized serializer plus a custom current-steering
driver — so both flows apply.

- **PDK**: SkyWater sky130 (open PDK, google/skywater-pdk). Analog: xschem +
  ngspice. Digital: cocotb + Icarus, Yosys, OpenROAD. Layout, DRC, and LVS
  through klayout-tools (`klt`) in both cases.
- **The pad is the point, and the risk.** The driver must reach a pad with
  ESD protection and a capacitance budget that a ~1 Gb/s low-swing signal
  survives. Establish first what the sky130 I/O library actually provides for
  a direct analog path to a pad, from the PDK's own documentation, before
  deciding to draw a custom cell. Pad pitch, ESD rules and the core-to-pad
  seam are where the tools are least exercised; expect friction there and
  file it.
- **The common mode is the second risk.** An LVDS output sits near 1.2 V,
  which constrains which device flavours the driver can use and how its
  common-mode feedback holds across PVT. The device-flavour choice is a
  decision record.
- **Scope discipline.** This repo has no `consumes:` edge. Do not design a
  PLL here. Specify the bit-clock interface — frequency, phases, duty cycle,
  jitter budget — and compare it against `sky130-pll` by name at a commit.
  If its band does not reach the requirement, write that gap into the spec
  and file the requirement on the sibling (see `2am/REUSE.md`). The
  serializer is PDK-independent RTL; if `gf180-tmds-tx` already has one that
  fits, take it by pinned reference rather than writing a second.
- **Friction protocol (the canary's job)**: every time klayout-tools is
  awkward, missing a capability, or wrong for what you need, file an issue at
  `2AMLogic/klayout-tools` describing the tool gap generically — that tracker
  is scoped to the tool, so keep design-specific detail out of it and describe
  the gap, not the design.
- **Verification is the product**: no claim without a testbench. PVT corners
  on every recorded analog result; recorded results are append-only evidence.
  Eye diagrams are simulated, and labelled so.
- Spec changes go through `spec/` with a decision record; agents do not relax
  the ratified spec to make results pass.
- **1 Gb/s LVDS is the target.** 400 Mb/s is the fallback; 1.5 Gb/s and the
  low-swing D-PHY-class mode are stretches. Do not let the stretch mode drive
  architecture before LVDS closes.

## On interface standards, and what may be said

The LVDS electrical levels follow TIA/EIA-644, and the low-swing stretch
mode is described only as "D-PHY-class". The MIPI specifications are
licensed to members, so nothing from them is copied into this repo, and the
block is not described as a MIPI or D-PHY implementation. Do not claim
compliance or conformance with either standard; state the electrical targets
as numbers and say which standard's window they follow.

<!-- BEGIN LOOM ORCHESTRATION -->
This repository uses [Loom](https://github.com/rjwalters/loom) for AI-powered development orchestration — see the Loom repository for the full guide (roles, labels, worktrees, configuration). When installed, Loom also writes a locally-substituted copy of that guide to `.loom/CLAUDE.md`.

Work is coordinated through `loom:` labels on issues and pull requests, and the same roles run either under `loom-daemon` or by hand in an attended session — daemon mode is optional. Create the labels once with `.loom/scripts/sync-labels.sh` (an install ships `.github/labels.yml` but does not create the labels on the forge). A pull request ready for review carries `loom:review-requested`; Judge reviews it and applies `loom:pr` (approved) or `loom:changes-requested`; Doctor fixes a `loom:changes-requested` pull request and returns it to `loom:review-requested`. Only a `loom:pr` pull request gets merged, and always via this repo's merge script (`.loom/scripts/merge-pr.sh`) — never a raw forge merge command such as `gh pr merge`. Full state machine: `.loom/docs/label-state-machine.md`.
<!-- END LOOM ORCHESTRATION -->

<!-- BEGIN REPO-SKILLS -->
This repository has [Repo Skills](https://github.com/rjwalters/repo) v0.24.3 installed —
general repository hygiene and environment commands invoked as `/repo:<command>`. Run
`/repo:help` for the command list, or see `.claude/skills/repo/SKILL.md` for the full
guide. Hygiene commands apply safe, reversible fixes by default and report each
change; run with `--ask` to review first, and `--prune` to allow irreversible
removals. Managed by `install.sh` — edit outside the markers only.
<!-- END REPO-SKILLS -->
