---
name: ndt4-foundation
description: >-
  Implements and reviews Notre Dame Web Theme v4 (NDT4) markup and CSS using
  Foundation guidance — accessibility, colors, CSS cascade layers, grid,
  responsive breakpoints, typography, utilities, and animations. Use when
  building Django templates, CMS plugin templates, site CSS, headers/footers,
  or when the user mentions NDT4, Conductor theme, webtheme.nd.edu, or ND brand
  styles.
---

# NDT4 Foundation

Apply the [NDT4 Foundation](https://webtheme.nd.edu/?path=/docs/foundation-about-foundation--docs) design system for all front-end work in this project. Detailed cheat sheets live in [reference.md](reference.md).

## When to use

- Creating or editing HTML/Django templates and CMS plugin render templates
- Writing site CSS overrides
- Porting v3 markup to v4
- Reviewing UI against ND brand / accessibility requirements

## Workflow

1. **Assets** — Ensure pages load NDT 4.0 CSS/JS from Conductor (not 3.0). Add `animate.css` only if using `.animate` classes.
2. **Compose with theme** — Prefer documented Foundation/Component classes and CSS variables over custom styling.
3. **Custom CSS** — Place overrides only in `@layer site { … }` after the theme layer order: `base, theme, utilities, print, site`.
4. **Layout** — Use mobile-first breakpoints and `.grid` / `.grid-{bp}-{n}` (see reference).
5. **Type & color** — Use `--font-heading` / `--font-default`; Brand Blue or Dark Gray for headings in body copy; do not recolor default text tokens.
6. **Accessibility** — Alt text, heading order, contextual links, WCAG AA contrast, keyboard targets, captions, `prefers-reduced-motion` for custom animation.
7. **Verify in a real browser** — Load the live page (localhost), take screenshots, check desktop + mobile, exercise interactions, and compare to the matching Storybook story. Do not accept template/CSS-only review.

## Do / Don’t

| Do | Don’t |
|----|--------|
| Use `.btn--cta`, `.card--news`, `.bg--brand-blue` | Invent parallel class names or hex palettes |
| Put site CSS in `@layer site` | Override theme with unlayered `!important` soup |
| Use `span.icon[data-icon]` | Hard-code one-off SVG icon systems when theme icons exist |
| Keep body lines ~70 characters; left-align body | Center long body copy for decoration |
| Match Storybook HTML for components | Copy NDT 3.0 header/nav class names |

## Official docs

- [About Foundation](https://webtheme.nd.edu/?path=/docs/foundation-about-foundation--docs)
- [Accessibility](https://webtheme.nd.edu/?path=/docs/foundation-accessibility--docs)
- [Colors](https://webtheme.nd.edu/?path=/docs/foundation-colors--docs)
- [CSS Layers](https://webtheme.nd.edu/?path=/docs/foundation-css-layers--docs)
- [Grid](https://webtheme.nd.edu/?path=/docs/foundation-grid--docs)
- [Breakpoints](https://webtheme.nd.edu/?path=/docs/foundation-responsive-breakpoints--docs)
- [Typography](https://webtheme.nd.edu/?path=/docs/foundation-typography--docs)
- [Utilities](https://webtheme.nd.edu/?path=/docs/foundation-utilities--docs)
- [Animations](https://webtheme.nd.edu/?path=/docs/foundation-animations--docs)
