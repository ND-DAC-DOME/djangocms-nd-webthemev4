# NDT4 Foundation reference

Condensed from [webtheme.nd.edu Foundation](https://webtheme.nd.edu/?path=/docs/foundation-about-foundation--docs). Prefer Storybook for full examples.

## CDN assets

| Asset | URL |
|-------|-----|
| CSS | `https://conductor.nd.edu/stylesheets/themes/ndt/4.0/ndt.css` |
| JS | `https://conductor.nd.edu/javascripts/themes/ndt/4.0/ndt.js` |
| Animations | `https://conductor.nd.edu/stylesheets/themes/ndt/4.0/animate.css` |

## CSS cascade layers

```css
@layer base, theme, utilities, print, site;
```

`site` is empty in the theme — reserved for project overrides.

## Breakpoints (mobile-first)

| Token | Query |
|-------|--------|
| xs | default (&lt; 480px) |
| sm | `width >= 30em` (480px) |
| md | `width >= 48em` (768px) |
| ml | `width >= 60em` (960px) |
| lg | `width >= 80em` (1280px) |
| xl | `width >= 90em` (1440px) |
| xxl | `width >= 100em` (1600px) |

## Grid

```html
<div class="grid grid-sm-2 grid-md-3 grid-xl-6">…</div>
```

| Feature | Classes |
|---------|---------|
| Columns | `.grid-{xs\|sm\|md\|ml\|lg\|xl\|xxl}-{1-6}` |
| Span | `.span-{bp}-{n}`, `.span-full` / `.full` |
| Order | `.order-{bp}-{n}` |
| Gap | `.grid-gap-{xs\|sm\|md\|lg\|xl}`, `.no-gap` |
| Default gap | `--grid-gap` (2rem) |

## Typography CSS variables

```css
--font-default: GP, "Helvetica Neue", Helvetica, Arial, Verdana, sans-serif;
--font-heading: Garamond-Pro, "Adobe Garamond", Garamond, Georgia, "Times New Roman", Times, serif;
```

| Face | Usage |
|------|--------|
| Garamond Premier Pro | Page/section titles, blockquotes (`--font-heading`) |
| Galaxie Polaris (GP) | Site title, card titles, news/events snippets, body (`--font-default`) |

Heading colors in body copy: Brand Blue or Dark Gray; white on dark backgrounds. Soft Dark Gray for body. Do not alter default font colors. Body ~70 characters/line.

## Color usage

- Brand palette primary; secondary/tertiary ≤ ~25% of page color usage.
- WCAG AA: 4.5:1 normal text; 3:1 large text.
- Common variables: `--brand-blue` `#0C2340`, `--brand-gold` `#AE9142`, `--brand-green` `#0A843D`, `--sky-blue` `#E1E8F2`, `--warm-white` `#F8F4EC`, `--link-blue` `#0A67BC`.

### Background classes (examples)

`.bg--white`, `.bg--gray-*`, `.bg--black`, `.bg--sky-blue{,-light,-dark}`, `.bg--warm-white`, `.bg--brand-blue{,-bright,-light,-dark}`

Modifiers: `.bg--gradient`, `.bg--to-{bottom,bottom-right,bottom-left,left,top,top-left,top-right}`, `.bg--transparent`, `.bg--full-bleed`, `.bg--dark`, `.bg--light`.

## Animation classes

Base: `.animate`

| Class | Effect |
|-------|--------|
| `.animate--fade-in` | Fade in |
| `.animate--fade-in-up` | Fade + move up |
| `.animate--fade-in-left` | Fade + move left |
| `.animate--fade-in-right` | Fade + move right |
| `.animate--move-up` | Move up |
| `.animate--move-down` | Move down |
| `.animate--move-left` | Move left |
| `.animate--move-right` | Move right |

Custom animation CSS must be wrapped in:

```css
@media (prefers-reduced-motion: no-preference) { … }
```

Keep animations short (typically &lt; 500ms), purposeful; avoid excessive motion.

## Key utilities

| Area | Examples |
|------|----------|
| Visibility | `.hidden`, `.invisible`, `.visually-hidden`, `.visually-hidden-{md\|ml\|lg\|xl\|xxl}` |
| Columns | `.col--sm`, `.col--md`, `.col--lg`, `.col--xl`, `.col--c`, `.col--screen` |
| Spacing | `.m-0`–`.m-2`, `.p-*`, `.mi-gutter`, logical `.mbs-*` / `.mie-*` / `.pbs-*` |
| Text | `.text-start`, `.text-center`, `.text-end`, `.text-pretty`, `.text-balance` |
| Display | `.d-flex`, `.d-grid`, `.d-none`, `.d-block`, `.position-sticky` |
| Flex | `.flex-row`, `.flex-column`, `.flex-wrap`, `.justify-center`, `.align-center` |
| Object fit | `.object-fit-cover`, `.object-fit-contain`, … |

## Accessibility checklist

- [ ] Meaning not color-only; links underlined / distinct
- [ ] Image alt text present
- [ ] Logical heading order
- [ ] Contextual link text (no “click here”)
- [ ] Contrast AA
- [ ] Keyboard operable; adequate control size
- [ ] Video captions when needed
- [ ] `prefers-reduced-motion` respected for custom motion

## Storybook index

https://webtheme.nd.edu/?path=/docs/foundation-about-foundation--docs
