---
name: Enterprise Verification Infrastructure
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#434655'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#575e70'
  on-secondary: '#ffffff'
  secondary-container: '#d9dff5'
  on-secondary-container: '#5c6274'
  tertiary: '#4e5562'
  on-tertiary: '#ffffff'
  tertiary-container: '#666d7b'
  on-tertiary-container: '#eaf0ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#dce2f7'
  secondary-fixed-dim: '#c0c6db'
  on-secondary-fixed: '#141b2b'
  on-secondary-fixed-variant: '#404758'
  tertiary-fixed: '#dce2f3'
  tertiary-fixed-dim: '#c0c7d6'
  on-tertiary-fixed: '#151c27'
  on-tertiary-fixed-variant: '#404754'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display:
    fontFamily: Inter
    fontSize: 2.25rem
    fontWeight: '600'
    lineHeight: 2.75rem
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 1.75rem
    fontWeight: '600'
    lineHeight: 2.25rem
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1rem
    letterSpacing: 0em
  label-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: 1.25rem
    letterSpacing: -0.005em
  label-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
    letterSpacing: 0.01em
  code-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1rem
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

The design system projects mission-critical reliability, architectural clarity, and institutional trust for high-throughput cybersecurity and data integrity platforms. The target audience comprises security architects, infrastructure engineers, compliance officers, and enterprise decision-makers who evaluate tools on precision, clarity, and performance rather than novelty.

The visual style is rooted in modern enterprise minimalism: crisp canvas planes, restrained cobalt guidance, exact typographic scales, and surgical micro-borders. It explicitly rejects cyberpunk tropes, decorative gradients, dark neon accents, and arbitrary ornamentation. Every visual token reinforces operational uptime, deterministic state representation, and high signal-to-noise density. The emotional tone is authoritative, composed, and engineering-grade—reminiscent of foundational systems like Cloudflare, Stripe, and Datadog.

## Colors

The palette operates under strict hierarchical discipline to maintain enterprise legibility and high contrast ratios.

- **Canvas & Surfaces:**
  - Base canvas: `#FFFFFF` (pure white for maximum contrast and clean separation)
  - Surface cards & panels: `#FFFFFF` primary container; `#F9FAFB` for muted utility layers, code containers, table headers, and nested sub-panels
  - Micro-borders & dividing rules: `#E5E7EB` (neutral structural divider)

- **Typography & Content:**
  - Primary text: Deep graphite `#111827` (achieves WCAG AAA compliance on white surfaces)
  - Secondary text: Neutral slate `#6B7280` (used for metadata, table subtext, and inactive UI labels)
  - Tertiary / Muted: `#9CA3AF` (disabled states, helper icons, placeholder inputs)

- **Interactive & Accent:**
  - Primary Accent: Precision cobalt `#2563EB` (focal action points, primary triggers, verified telemetry badges)
  - Accent Hover: Deep cobalt `#1D4ED8`
  - Subtle Accent Wash: `#EFF6FF` (active navigation states, light badge backgrounds, table selection highlights)

- **Functional Status Indicators:**
  - Verified / Success: `#059669` (surface wash: `#ECFDF5`, border: `#A7F3D0`)
  - Warning / Drift: `#D97706` (surface wash: `#FFFBEB`, border: `#FDE68A`)
  - Threat / Critical: `#DC2626` (surface wash: `#FEF2F2`, border: `#FECACA`)

## Typography

The typography uses Inter across display, editorial, and functional interface tiers to maintain visual consistency and legibility across dense data displays. 

Font pairings emphasize slight negative tracking (`-0.02em` to `-0.01em`) on large headings to create a solid, architectural appearance. Body copy uses standard letter tracking with generous line-height ratios (1.4–1.5x) to maintain scanability through audit trails, JSON logs, and configuration matrices. Numerical data (IP addresses, SHA-256 hashes, timestamps, latency metrics) should enable tabular figures (`font-variant-numeric: tabular-nums`) to prevent horizontal jitter during real-time telemetry refreshes.

## Layout & Spacing

The layout is built on an enterprise 12-column responsive fluid grid designed for variable density views, collapsible side navigation bars, and wide multi-column audit panes.

- **Grid Architecture:**
  - Desktop (1280px+): 12 columns, 1.5rem (`gutter`) column separation, 2rem (`margin`) canvas inset.
  - Tablet (768px - 1279px): 8 columns, 1.25rem column separation, 1.5rem canvas inset.
  - Mobile (<768px): 4 columns, 1rem (`gutter-mobile`) column separation, 1rem (`margin-mobile`) canvas inset.

- **Density & Rhythm:**
  The system uses a strict 4px base increment. Spacing tokens govern internal layout rhythm:
  - `space-xs` (4px): Dense element gaps, badge insets, icon-to-text gaps.
  - `space-sm` (8px): Form input padding, button inner gaps, list row spacing.
  - `space-md` (16px): Structural component insets, container padding, standard stack gaps.
  - `space-lg` (24px): Card interior paddings, widget boundaries, section partitions.
  - `space-xl` (32px): Primary module divisions, top-level layout sections.

## Elevation & Depth

Visual hierarchy relies on crisp architectural 1px micro-borders (`#E5E7EB`) and subtle tonal contrast rather than heavy drop shadows. Surfaces sit flat and deliberate.

- **Level 0 (Base Canvas):** `#FFFFFF`, flat, no shadow.
- **Level 1 (Cards, Data Grids, Sub-panels):** `#FFFFFF` fill, 1px solid `#E5E7EB` outline, optional ambient resting shadow: `0 1px 2px 0 rgba(0, 0, 0, 0.04)`.
- **Level 2 (Dropdowns, Flyouts, Popovers):** `#FFFFFF` fill, 1px solid `#E5E7EB` outline, elevated shadow: `0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.04)`.
- **Level 3 (Modal Dialogs, Command Palettes):** `#FFFFFF` fill, 1px solid `#E5E7EB` outline, high-depth shadow: `0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)`. Backing scrim uses `rgba(17, 24, 39, 0.4)` with an optional subtle blur (`backdrop-filter: blur(2px)`).

## Shapes

The design system uses structured, disciplined roundedness (Level 2). This standard provides an intentional structural radius that feels modern and approachable while maintaining strict alignment across dense data dashboards.

- **Standard Containers & Cards:** 0.75rem (12px) to 1rem (16px) corner radius.
- **Interactive Controls (Inputs, Buttons, Dropdowns):** 0.5rem (8px) corner radius.
- **Micro UI (Badges, Status Chips):** 0.375rem (6px) or fully rounded pill for standalone binary status indicators.
- **Overlays & Dialogs:** 1rem (16px) corner radius with matching inner micro-border containment.

## Components

- **Buttons:**
  - *Primary:* `#2563EB` fill, white `#FFFFFF` text, 0.5rem radius, 1px border transparent. Hover: `#1D4ED8`. Focus: 2px offset ring in `#2563EB`.
  - *Secondary / Neutral:* `#FFFFFF` fill, `#111827` text, 1px solid `#E5E7EB` border. Hover: `#F9FAFB` surface with `#D1D5DB` border.
  - *Destructive:* `#FEF2F2` fill, `#DC2626` text, 1px solid `#FECACA` border. Hover: `#DC2626` solid fill, `#FFFFFF` text.

- **Input Fields & Selectors:**
  - Base input: `#FFFFFF` surface, 1px solid `#E5E7EB` border, 0.5rem radius, padding `0.5rem 0.75rem`. Text: `#111827`. Placeholder: `#9CA3AF`.
  - Focus state: Border color changes to `#2563EB` with an ambient 3px outer ring of `#EFF6FF` (`box-shadow: 0 0 0 3px #EFF6FF`).

- **Cards & Data Surfaces:**
  - Enclosed in 1px solid `#E5E7EB` with 0.75rem (12px) radiuses.
  - Card headers use optional `#F9FAFB` backgrounds with an interior bottom dividing border of 1px `#E5E7EB` to segment telemetry controls from data charts.

- **Status Badges & Verification Chips:**
  - Height 24px, 0.375rem (6px) radius, padding `0.125rem 0.5rem`, `label-sm` font.
  - *Verified State:* Background `#ECFDF5`, text `#065F46`, border 1px solid `#A7F3D0`.
  - *Monitored / Neutral State:* Background `#EFF6FF`, text `#1E40AF`, border 1px solid `#BFDBFE`.

- **Checkboxes & Radios:**
  - Dimensions 16px × 16px, 1px solid `#D1D5DB` resting state on `#FFFFFF`.
  - Selected state: `#2563EB` solid fill with white checkmark glyph. Checkbox corner radius 4px; radio corner radius 50% circular.

- **Data Tables & Log Viewers:**
  - Headers: `#F9FAFB` fill, uppercase `label-sm` text `#6B7280`, 1px solid `#E5E7EB` bottom border.
  - Rows: Height 40px (compact) to 48px (standard), alternating hover state `#F9FAFB`, selected state `#EFF6FF`.
  - Monospaced data displays: Inlined with `#F3F4F6` background, `#111827` text, 4px corner radius, padding `2px 6px`.