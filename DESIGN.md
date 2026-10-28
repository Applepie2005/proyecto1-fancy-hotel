---
name: Fancy Hotel 4400
description: Consola operativa con identidad de diagrama de tránsito nocturno
colors:
  midnight: "#07111f"
  surface: "#eef2f8"
  surface-raised: "#ffffff"
  ink: "#0b1220"
  ink-muted: "#3d4f6f"
  line-atlanta: "#dc2626"
  line-charlotte: "#2563eb"
  line-savannah: "#d97706"
  line-orlando: "#059669"
  line-miami: "#7c3aed"
  critical: "#dc2626"
  degraded: "#d97706"
  ok: "#059669"
typography:
  ui:
    fontFamily: "'Source Sans 3', system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: "'IBM Plex Mono', ui-monospace, monospace"
    fontSize: "0.92em"
    fontWeight: 400
rounded:
  sm: "6px"
  md: "8px"
spacing:
  rail: "248px"
  workspace: "clamp(1rem, 3vw, 2.5rem)"
---

# Fancy Hotel 4400 — Design System

## Visual thesis

Operate-mode hotel console: midnight rail navigation, light workspace, five property “lines” encoded as color. Signature move is the SVG network map on home and portal—not decorative transit cosplay on tables.

## Layout

- `fh-app`: flex row; collapses to stacked rail on ≤900px.
- `fh-rail`: sticky 248px; session chip; grouped links with line-colored nodes (`::before` dots).
- `fh-workspace`: max-width 960px content column.

## Components

- **fh-panel**: primary content surface (forms, tables, map).
- **fh-stations**: portal task list (replaces uniform card grids).
- **fh-table-wrap**: horizontal scroll for wide Angular tables.
- **calendar-day**: availability states (ok / degraded / critical palette).

## Motion

Single page rise (`fh-rise` 380ms). Honor `prefers-reduced-motion`.

## Do not

- Emoji icons; use SVG or text.
- Kicker labels above headings.
- Glass/blur decoration; this world is enamel + flat panels.
