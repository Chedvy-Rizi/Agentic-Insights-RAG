# Task Management System - UI Design System and Rules

## Design Philosophy

The Task Management System UI is designed with a user-centric approach, prioritizing accessibility, clarity, and efficiency. The design supports both LTR (Left-to-Right) and RTL (Right-to-Left) languages, with primary focus on Hebrew language support for regional users.

## RTL (Right-to-Left) Support

### Implementation Strategy

#### HTML/CSS RTL Configuration
```html
<!-- Set direction attribute for RTL languages -->
<html dir="rtl" lang="he">
<!-- or -->
<div dir="ltr" lang="en">
```

#### CSS Approach
- Use logical properties instead of physical properties
- `margin-inline-start` instead of `margin-left`
- `padding-inline-end` instead of `padding-right`
- `inset-inline-start` instead of `left`
- `flex-direction: row-reverse` for RTL-specific layouts

#### React Component Example
```javascript
// Use CSS modules with RTL support
import styles from './TaskCard.module.css';

// Or use inline styles with conditional logic
const containerStyle = {
  direction: isRTL ? 'rtl' : 'ltr',
  marginInlineStart: '1rem',
  paddingInlineEnd: '2rem'
};
```

### RTL-Specific Components
- **Input Fields**: Text cursor and validation icons positioned accordingly
- **Buttons**: Icons and text alignment adjusted for RTL
- **Menus**: Dropdown menus expand in correct direction
- **Navigation**: Sidebar and breadcrumbs flow right-to-left
- **Modals**: Content and controls aligned properly
- **Data Tables**: Column order and scrolling direction optimized

### Language Switching
- Language toggle in user preferences
- Persistent storage of language choice (localStorage)
- Dynamic CSS class switching: `.rtl` and `.ltr`
- Translation files for Hebrew and English content

## Color Palette

### Primary Color Scheme
- **Primary Blue**: `#001f3f` (Navy Blue)
  - Primary action buttons
  - Links and interactive elements
  - Header background
  - Active states

### Secondary Colors
- **Accent Color**: `#0074D9` (Bright Blue)
  - Highlights and hover states
  - Secondary buttons
  - Active navigation items
  
- **Success Color**: `#2ECC40` (Green)
  - Completed tasks
  - Success messages
  - Positive actions
  
- **Warning Color**: `#FF851B` (Orange)
  - Pending actions
  - Warnings
  - Moderate priority items

- **Danger Color**: `#FF4136` (Red)
  - Delete actions
  - Error messages
  - Critical issues
  - High priority items

### Neutral Colors
- **Dark Gray**: `#111111` (Text and heavy elements)
- **Medium Gray**: `#AAAAAA` (Secondary text and borders)
- **Light Gray**: `#F1F1F1` (Backgrounds and subtle elements)
- **White**: `#FFFFFF` (Primary backgrounds)

### Color Usage Examples
```css
/* Primary Button */
.btn-primary {
  background-color: #001f3f;
  color: #FFFFFF;
  border: none;
}

/* Task Status - Done */
.task-status-done {
  background-color: #2ECC40;
  color: #FFFFFF;
}

/* Priority - High */
.priority-high {
  color: #FF4136;
  border-left: 4px solid #FF4136;
}

/* Error Message */
.error-message {
  background-color: #FFF0F0;
  color: #FF4136;
  border-left: 4px solid #FF4136;
}
```

## Typography

### Font Stack
```css
/* Primary Font */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;

/* For Hebrew Support (RTL) */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Open Sans', 'Arial', sans-serif;
```

### Font Sizes and Weights

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| Display/Hero | 32px | 700 | Page titles |
| Heading 1 | 28px | 700 | Section headings |
| Heading 2 | 24px | 600 | Subsection headings |
| Heading 3 | 20px | 600 | Component headings |
| Body Large | 16px | 400 | Main content |
| Body Regular | 14px | 400 | Secondary content |
| Body Small | 12px | 400 | Metadata, captions |
| Label | 12px | 600 | Form labels, badges |
| Code | 13px | 400 | Code snippets (monospace) |

### Line Heights
- Headers: 1.2
- Body text: 1.5
- Compact text: 1.3

## Component Library Guidelines

### Layout Components

#### Container
- Max-width: 1200px
- Padding: 1rem (mobile), 2rem (desktop)
- Centered with `margin: 0 auto`

#### Grid System
- 12-column grid
- Responsive breakpoints:
  - Mobile: 320px - 640px (1 column)
  - Tablet: 641px - 1024px (2 columns)
  - Desktop: 1025px+ (3+ columns)

#### Spacing Scale
- Base unit: 8px
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px

### Form Components

#### Text Input
```css
.form-input {
  padding: 12px 16px;
  border: 1px solid #AAAAAA;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #001f3f;
  box-shadow: 0 0 0 3px rgba(0, 31, 63, 0.1);
}
```

#### Button Variants

**Primary Button**
```css
.btn-primary {
  background-color: #001f3f;
  color: #FFFFFF;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #0074D9;
}

.btn-primary:active {
  transform: scale(0.98);
}
```

**Secondary Button**
```css
.btn-secondary {
  background-color: transparent;
  color: #001f3f;
  padding: 12px 24px;
  border: 2px solid #001f3f;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary:hover {
  background-color: #F1F1F1;
}
```

**Danger Button**
```css
.btn-danger {
  background-color: #FF4136;
  color: #FFFFFF;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
}

.btn-danger:hover {
  background-color: #CC2E28;
}
```

#### Form Labels
```css
.form-label {
  font-size: 12px;
  font-weight: 600;
  color: #111111;
  margin-bottom: 8px;
  display: block;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

### Card Component
```css
.card {
  background-color: #FFFFFF;
  border: 1px solid #F1F1F1;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s, border-color 0.3s;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  border-color: #AAAAAA;
}
```

### Navigation Components

#### Header
- Height: 64px
- Background: #001f3f
- Text Color: #FFFFFF
- Contains logo, navigation menu, user menu

#### Sidebar
- Width: 280px (collapsible to 64px)
- Background: #F1F1F1
- Border-right: 1px solid #AAAAAA
- Active item: Background #001f3f, text #FFFFFF

#### Breadcrumb
```css
.breadcrumb {
  font-size: 12px;
  color: #AAAAAA;
}

.breadcrumb a {
  color: #001f3f;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}
```

### Task-Specific Components

#### Task Card
- Background: #FFFFFF
- Border: 1px solid #F1F1F1
- Padding: 16px
- Priority indicator: Left border (4px)
- Status badge: Top-right corner
- Min-height: 100px

#### Status Badge
```css
.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-todo {
  background-color: #F1F1F1;
  color: #111111;
}

.status-in-progress {
  background-color: #0074D9;
  color: #FFFFFF;
}

.status-done {
  background-color: #2ECC40;
  color: #FFFFFF;
}
```

#### Priority Indicator
```css
.priority-indicator {
  width: 4px;
  height: 100%;
  border-radius: 4px 0 0 4px;
}

.priority-low {
  background-color: #2ECC40;
}

.priority-medium {
  background-color: #FF851B;
}

.priority-high {
  background-color: #FF4136;
}

.priority-critical {
  background-color: #B10DC9;
}
```

### Modal Component
- Background overlay: rgba(0, 0, 0, 0.5)
- Modal background: #FFFFFF
- Min-width: 400px
- Max-width: 600px
- Border-radius: 8px
- Padding: 24px
- Close button: Top-right, 24px from edges

## Responsive Design Breakpoints

```javascript
const breakpoints = {
  mobile: '320px',
  tablet: '768px',
  desktop: '1024px',
  wide: '1440px'
};

// Usage in CSS
@media (max-width: 767px) {
  /* Mobile styles */
}

@media (min-width: 768px) and (max-width: 1023px) {
  /* Tablet styles */
}

@media (min-width: 1024px) {
  /* Desktop styles */
}
```

## Accessibility Guidelines

### WCAG 2.1 Compliance (Level AA)
- Color contrast ratio: 4.5:1 for normal text, 3:1 for large text
- Keyboard navigation support
- ARIA labels for interactive elements
- Semantic HTML (buttons, links, form elements)
- Focus indicators visible (outline or border)

### Implementation
```html
<!-- Form with ARIA labels -->
<label for="task-title">Task Title *</label>
<input 
  id="task-title"
  type="text"
  aria-required="true"
  aria-describedby="title-hint"
  placeholder="Enter task title"
/>
<small id="title-hint">Task title must be between 3 and 100 characters</small>

<!-- Button with ARIA attributes -->
<button 
  type="button"
  aria-label="Delete task"
  aria-confirm="Are you sure you want to delete this task?"
>
  Delete
</button>
```

## Animation and Transitions

### Standard Transitions
- Duration: 0.3s
- Easing: `ease-in-out`
- Properties: `background-color`, `border-color`, `color`, `box-shadow`

### Micro-interactions
- Button click: 100ms scale animation
- Hover effects: Smooth color/shadow transition
- Page transitions: 200ms fade
- Toast notifications: Slide in from top (300ms)

## Dark Mode (Future Enhancement)

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #111111;
    --bg-secondary: #1a1a1a;
    --text-primary: #FFFFFF;
    --text-secondary: #AAAAAA;
    --border-color: #333333;
  }
}
```

## Component Documentation

Each component should include:
- Props interface
- Usage examples
- RTL considerations
- Accessibility notes
- Responsive behavior
- Styling customization

