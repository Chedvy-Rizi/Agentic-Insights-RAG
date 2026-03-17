# UI Design System and Rules

## Overview

This document defines the comprehensive design system for the Task Management System, with special emphasis on RTL (Right-to-Left) Hebrew language support, accessibility, and consistent user experience across all platforms.

## Design Philosophy

### Core Principles
- **Accessibility First**: Ensure WCAG 2.1 AA compliance
- **RTL-Native Design**: Built from the ground up for Hebrew and other RTL languages
- **Consistency**: Maintain visual and interaction consistency across all components
- **Performance**: Optimize for fast loading and smooth interactions
- **Responsive**: Design for mobile-first, progressive enhancement

## Color System

### Primary Colors
- **Primary Dark**: `#001f3f` - Deep navy blue for primary actions and branding
- **Primary Light**: `#003366` - Lighter shade for hover states
- **Primary Accent**: `#004080` - Accent color for highlights

### Secondary Colors
- **Secondary**: `#6c757d` - Neutral gray for secondary actions
- **Success**: `#28a745` - Green for success states and confirmations
- **Warning**: `#ffc107` - Amber for warnings and cautions
- **Danger**: `#dc3545` - Red for errors and destructive actions
- **Info**: `#17a2b8` - Cyan for informational messages

### Neutral Colors
- **White**: `#ffffff` - Primary background color
- **Light Gray**: `#f8f9fa` - Subtle backgrounds and cards
- **Medium Gray**: `#e9ecef` - Borders and dividers
- **Dark Gray**: `#343a40` - Text and dark UI elements
- **Black**: `#000000` - High contrast text

### Semantic Color Usage
```css
/* Primary Actions */
.btn-primary { background-color: #001f3f; }
.btn-primary:hover { background-color: #003366; }

/* Status Indicators */
.status-success { color: #28a745; background-color: #d4edda; }
.status-warning { color: #856404; background-color: #fff3cd; }
.status-danger { color: #721c24; background-color: #f8d7da; }
.status-info { color: #0c5460; background-color: #d1ecf1; }
```

## Typography

### Font Stack
```css
/* Primary Hebrew-friendly font stack */
font-family: "Segoe UI", "Arial Hebrew", "Arial", sans-serif;

/* Monospace for code */
font-family: "Courier New", "Courier", monospace;
```

### Type Scale
- **Display 1**: 2.5rem (40px) - Page headers
- **Display 2**: 2rem (32px) - Section headers
- **Heading 1**: 1.75rem (28px) - Main headings
- **Heading 2**: 1.5rem (24px) - Sub-sections
- **Heading 3**: 1.25rem (20px) - Card titles
- **Heading 4**: 1.125rem (18px) - Small headings
- **Body Large**: 1.125rem (18px) - Important body text
- **Body**: 1rem (16px) - Standard body text
- **Body Small**: 0.875rem (14px) - Secondary text
- **Caption**: 0.75rem (12px) - Labels and metadata

### Font Weights
- **Light**: 300
- **Normal**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

### Line Height
- **Display**: 1.2
- **Headings**: 1.3
- **Body**: 1.5
- **Tight**: 1.2

## RTL (Right-to-Left) Support

### Direction Handling
```css
/* Base RTL support */
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}

/* Logical properties for RTL/LTR compatibility */
.margin-inline-start: 1rem;
.margin-inline-end: 1rem;
.padding-inline-start: 1rem;
.padding-inline-end: 1rem;
.border-inline-start: 1px solid #e9ecef;
.border-inline-end: 1px solid #e9ecef;
```

### Icon and Symbol Adaptation
- **Arrows**: Automatically reverse direction based on text direction
- **Chevrons**: Point left in RTL, right in LTR
- **Progress Indicators**: Flow from right to left in RTL mode
- **Navigation**: Menu items aligned to the right in RTL

### Text Alignment Rules
```css
/* RTL text alignment */
[dir="rtl"] .text-left { text-align: right; }
[dir="rtl"] .text-right { text-align: left; }
[dir="rtl"] .text-start { text-align: right; }
[dir="rtl"] .text-end { text-align: left; }
```

## Layout System

### Grid System
- **12-column responsive grid**
- **CSS Grid for complex layouts**
- **Flexbox for component-level layouts**
- **Container max-width**: 1200px

### Breakpoints
- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px - 1439px
- **Large Desktop**: 1440px+

### Spacing Scale
- **xs**: 0.25rem (4px)
- **sm**: 0.5rem (8px)
- **md**: 1rem (16px)
- **lg**: 1.5rem (24px)
- **xl**: 2rem (32px)
- **2xl**: 3rem (48px)
- **3xl**: 4rem (64px)

## Component Library

### Button System
```css
/* Primary Button */
.btn-primary {
  background-color: #001f3f;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: #003366;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 31, 63, 0.1);
}
```

### Button Variants
- **Primary**: Main actions with #001f3f background
- **Secondary**: Secondary actions with outline style
- **Ghost**: Minimal styling for icon buttons
- **Link**: Button styled as hyperlink
- **Sizes**: Small, Medium, Large

### Form Components
```css
/* Input Fields */
.form-input {
  border: 1px solid #e9ecef;
  border-radius: 0.375rem;
  padding: 0.75rem;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #001f3f;
  box-shadow: 0 0 0 3px rgba(0, 31, 63, 0.1);
}

[dir="rtl"] .form-input {
  text-align: right;
}
```

### Card Components
```css
.card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  border: 1px solid #e9ecef;
}

.card-header {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}
```

## Navigation Patterns

### Header Navigation
- **Logo**: Left in LTR, right in RTL
- **Primary Navigation**: Center-aligned
- **User Menu**: Right in LTR, left in RTL
- **Mobile Menu**: Hamburger icon positioned appropriately

### Sidebar Navigation
- **Desktop**: Fixed sidebar with collapsible sections
- **Mobile**: Slide-out drawer from appropriate side
- **Breadcrumbs**: RTL-aware breadcrumb navigation

### Footer Navigation
- **Links**: Horizontal layout with RTL support
- **Language Toggle**: Prominent language switcher
- **Contact Info**: Right-aligned in RTL

## Interaction Patterns

### Hover States
- **Buttons**: Subtle lift effect with shadow
- **Cards**: Border color change and slight elevation
- **Links**: Underline animation
- **Interactive Elements**: Cursor pointer and visual feedback

### Focus States
- **High Contrast**: 2px outline with #001f3f color
- **Visible Focus**: Always visible for accessibility
- **Skip Links**: Keyboard navigation support

### Loading States
- **Skeleton Loaders**: For content areas
- **Spinners**: For button actions
- **Progress Bars**: For multi-step processes
- **Shimmer Effects**: For dynamic content

## Accessibility Guidelines

### WCAG 2.1 AA Compliance
- **Color Contrast**: Minimum 4.5:1 for normal text
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Readers**: Proper ARIA labels and roles
- **Focus Management**: Logical tab order and focus trapping

### ARIA Implementation
```jsx
// Example accessible button
<button
  aria-label="מחק משימה"
  aria-describedby="delete-help"
  className="btn-ghost"
>
  <TrashIcon />
</button>
<div id="delete-help" className="sr-only">
  מחיקת המשימה הנבחרת לצמיתות
</div>
```

### Screen Reader Support
- **Hebrew Language Tag**: `lang="he"` on HTML element
- **Direction Indicators**: Proper `dir="rtl"` attributes
- **Alternative Text**: Descriptive alt text for images
- **Form Labels**: Explicit label associations

## Responsive Design

### Mobile-First Approach
- **Base Styles**: Mobile layout (320px+)
- **Progressive Enhancement**: Tablet and desktop enhancements
- **Touch Targets**: Minimum 44px tap targets
- **Thumb Zones**: Consider thumb reach on mobile

### Breakpoint-Specific Rules
```css
/* Mobile (default) */
.task-card {
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .task-card {
    padding: 1.5rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .task-card {
    padding: 2rem;
  }
}
```

## Animation and Transitions

### Motion Principles
- **Purposeful**: Animations should enhance understanding
- **Subtle**: Avoid distracting or excessive motion
- **Fast**: Keep animations under 300ms
- **Respectful**: Honor reduced motion preferences

### Transition Properties
```css
/* Standard transitions */
.transition-all {
  transition: all 0.2s ease-in-out;
}

.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease;
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .transition-all {
    transition: none;
  }
}
```

## Icon System

### Icon Library
- **Lucide React**: Primary icon library
- **Custom Icons**: Hebrew-specific cultural icons
- **SVG Format**: Scalable vector graphics
- **RTL Variants**: Direction-aware icon variants

### Icon Usage Rules
- **Consistent Size**: 16px, 20px, 24px standard sizes
- **Color Consistency**: Inherit text color or use semantic colors
- **Accessibility**: Include aria-label for icon-only buttons
- **Cultural Appropriateness**: Icons suitable for Hebrew-speaking users

## Brand Guidelines

### Logo Usage
- **Primary Logo**: Full color version on light backgrounds
- **Monochrome**: Single color for constrained contexts
- **Minimum Size**: 24px height for digital use
- **Clear Space**: Minimum 0.5x logo height clear space

### Voice and Tone
- **Professional**: Clear, concise, professional language
- **Helpful**: Encouraging and supportive messaging
- **Direct**: Straightforward instructions and feedback
- **Culturally Aware**: Hebrew idioms and cultural references

## Implementation Guidelines

### CSS Architecture
- **Utility-First**: Tailwind CSS for rapid development
- **Component-Based**: Styled components for complex UI
- **Design Tokens**: Centralized design system variables
- **CSS Custom Properties**: For theming and customization

### File Organization
```
src/
├── styles/
│   ├── globals.css
│   ├── components.css
│   └── utilities.css
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Card.tsx
│   └── layout/
│       ├── Header.tsx
│       └── Sidebar.tsx
└── hooks/
    ├── useRTL.ts
    └── useTheme.ts
```

### Code Standards
- **TypeScript**: Strict typing for all components
- **Props Interface**: Clear prop definitions with JSDoc
- **Storybook**: Component documentation and testing
- **Design Reviews**: Regular design system reviews

## Quality Assurance

### Design Review Checklist
- [ ] RTL layout works correctly
- [ ] Color contrast meets WCAG standards
- [ ] Keyboard navigation is functional
- [ ] Screen reader announcements are appropriate
- [ ] Responsive design works across breakpoints
- [ ] Loading states are implemented
- [ ] Error states are handled gracefully
- [ ] Micro-interactions enhance UX

### Testing Requirements
- **Visual Regression**: Automated visual testing
- **Accessibility**: Automated a11y testing
- **Cross-browser**: Browser compatibility testing
- **Device Testing**: Real device testing on mobile/tablet

## Future Enhancements

### Planned Improvements
- **Dark Mode**: Complete dark theme implementation
- **Advanced Theming**: User-customizable color schemes
- **Motion Design**: Sophisticated animation library
- **Voice UI**: Voice commands and responses
- **AR/VR Support**: Future augmented reality features

### Technology Roadmap
- **Design Tokens**: Centralized token management system
- **Component Library**: Published component library
- **Design System Automation**: Automated design sync
- **Performance Optimization**: Advanced performance monitoring
