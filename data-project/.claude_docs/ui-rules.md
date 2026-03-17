# Task Management System — UI Rules & Design Contract

> This is the authoritative reference for anyone writing a component, reviewing
> a pull request, or debugging a layout issue. If a decision isn't documented
> here, it should be discussed and then added here.

---

## Core Philosophy

The UI has one non-negotiable requirement above all others: **it must feel
equally at home in Hebrew and English.** This shapes every layout decision
made in this document. We do not retrofit RTL as an afterthought. We design
for both directions simultaneously, using CSS Logical Properties as the default.

---

## Direction & RTL Support

### The Rule: Logical Properties Everywhere

Never write `left`, `right`, `margin-left`, `padding-right`, `border-left`,
`text-align: left`, etc. in component stylesheets. Always use their logical
equivalents:

| ❌ Physical (forbidden in components) | ✅ Logical (required)         |
|---------------------------------------|-------------------------------|
| `margin-left`                         | `margin-inline-start`         |
| `padding-right`                       | `padding-inline-end`          |
| `border-left`                         | `border-inline-start`         |
| `left: 0`                             | `inset-inline-start: 0`       |
| `text-align: left`                    | `text-align: start`           |
| `text-align: right`                   | `text-align: end`             |
| `flex-direction: row`                 | Stays as-is (flex is OK)      |

The `dir` attribute is set on `<html>` by the i18n provider on mount and
whenever the user switches languages. All logical properties respond automatically.

### Directional Icons

Icons that imply a direction (arrows, chevrons, "back" buttons, list bullets,
drag handles) must be visually mirrored in RTL. Use the utility class
`.flip-rtl`, which applies `transform: scaleX(-1)` under `[dir="rtl"]`.

Icons that do not carry directionality (checkmarks, stars, avatars, status
dots) must **not** be flipped.
```tsx
// ✅ Correct — back arrow flips in RTL
<ArrowLeftIcon className="flip-rtl" />

// ✅ Correct — checkmark never flips
<CheckIcon />
```

### Hebrew Typography

- **Font:** Heebo (Google Fonts) for Hebrew. System font stack for Latin.
  The CSS font stack is: `'Heebo', 'Segoe UI', system-ui, sans-serif`.
- **Line height:** Increase to `1.7` for Hebrew body text (Hebrew letters
  have taller descenders).
- **Letter spacing:** Never apply `letter-spacing` to Hebrew text — it
  breaks readability.

---

## Component Rules

### Forms & Inputs

- All `<input>` and `<textarea>` elements must set `dir="auto"` so the
  browser infers direction from the typed content. This ensures a Hebrew
  user typing in a search box gets right-aligned text automatically.
- Validation error messages appear **below** the input (`margin-block-start`),
  never beside it, so they reflow correctly in both directions.
- Labels are always associated via `htmlFor`/`id` — never implicit wrapping.

### Data Tables

- Column order must be defined in a configuration object, not hardcoded in
  JSX. The RTL config reverses the visual column order automatically.
- Sort indicator arrows use `.flip-rtl`.
- Numeric columns (IDs, counts, dates) are always `dir="ltr"` regardless of
  page direction, to preserve natural numeral reading order.

### Modals & Drawers

- Modals are centered — no directional adjustment needed.
- Slide-in drawers use `inset-inline-end: 0` for the "detail panel" pattern
  (opens from the end of the reading direction, which is left in RTL and
  right in LTR).

### Buttons

- Never rely on icon position within a button for meaning. If an icon
  appears "before" the label in LTR, use `gap` in a flex row — it will
  automatically mirror in RTL.
- Button minimum width: `88px`. No text truncation inside buttons.

---

## Color & Theming

The design token system uses CSS custom properties. All components consume
tokens — never raw hex values.
```css
:root {
  --color-brand-primary:   #2563EB;
  --color-brand-secondary: #7C3AED;
  --color-surface-base:    #FFFFFF;
  --color-surface-raised:  #F8FAFC;
  --color-surface-overlay: #F1F5F9;
  --color-border-subtle:   #E2E8F0;
  --color-border-default:  #CBD5E1;
  --color-text-primary:    #0F172A;
  --color-text-secondary:  #475569;
  --color-text-disabled:   #94A3B8;
  --color-status-todo:     #64748B;
  --color-status-inprog:   #2563EB;
  --color-status-blocked:  #DC2626;
  --color-status-done:     #16A34A;
  --color-focus-ring:      #3B82F6;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
```

Dark mode overrides are applied under `[data-theme="dark"]` on `<html>`.

---

## Spacing Scale

We use an 8px base grid. Valid spacing values: `4, 8, 12, 16, 24, 32, 48, 64px`.
Deviations require a comment explaining why.

---

## Accessibility Baseline

- All interactive elements must be keyboard-focusable with a visible
  `--color-focus-ring` outline (never `outline: none` without a replacement).
- Color is never the only way to convey information (always pair with text
  or icon).
- Minimum touch target: 44×44px on mobile.
- Every image has meaningful `alt` text or `alt=""` if decorative.
- All status labels (task status, priority) include an `aria-label` with
  the full text value.

---

## What We Intentionally Avoid

- CSS `float` — Flexbox and Grid only.
- Fixed pixel widths on containers — use `max-width` with `width: 100%`.
- Physical directional properties in component code (`left`, `right`,
  `margin-left`, etc.).
- `!important` outside of reset stylesheets.
- Inline styles for anything that belongs in the design token system.