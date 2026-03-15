# Artboard Content Guidelines

## Standard artboard plan

| Artboard | File | Content |
|----------|------|---------|
| Foundations | `foundations.html` | Color palette swatches, typography scale, spacing tokens |
| Components | `components.html` | Buttons, cards, badges, form elements, nav items, icons |
| Hero & Navigation | `hero-navigation.html` | Navbar + hero section from the reference |
| Content Sections | `content-sections.html` | Middle sections (features, grids, testimonials, etc.) |
| Footer & CTA | `footer-cta.html` | Footer, CTA banners, bottom navigation |

Adjust based on the reference — if there are many sections, split further. If the page is simple, merge. The goal is 3-6 artboards, not more.

## Per-artboard guidelines

**Foundations:**
- Color palette: large swatches with hex values and role labels (Primary, Secondary, Accent, etc.)
- Typography: show the font at multiple sizes/weights with sample text
- Spacing: visual tokens showing the spacing scale
- This artboard is a reference sheet — prioritize clarity and readability over creativity

**Components:**
- Show each component in its variants (primary/secondary/outline buttons, card sizes, etc.)
- Group related components together with clear section labels
- Include hover/active states where relevant
- Maintain consistent spacing between component groups

**Hero & Navigation:**
- Recreate the navbar and hero section faithfully from the reference
- Use placeholder images (colored rectangles with subtle gradients from the palette) instead of real photos
- Keep the same proportions and spacing

**Content Sections:**
- Recreate each distinct section from the reference
- Maintain the same visual hierarchy and layout
- Use realistic placeholder text (lorem ipsum)

**Footer & CTA:**
- Recreate bottom sections faithfully
- Include all link groups, CTAs, and decorative elements

## Containment rules (non-negotiable)

Every artboard MUST:
- Fit within `width: 1440px` — nothing overflows horizontally
- Have clear visual separation between sections (use gaps, dividers, or background changes)
- Leave breathing room at edges — never place elements flush against the artboard boundary
- Ensure no element overlaps another unintentionally
