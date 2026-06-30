---
name: Agro-Modernist
colors:
  surface: '#e8fff0'
  surface-dim: '#b8e4cc'
  surface-bright: '#e8fff0'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#d1fee5'
  surface-container: '#ccf8df'
  surface-container-high: '#c6f2da'
  surface-container-highest: '#c1ecd4'
  on-surface: '#002114'
  on-surface-variant: '#404943'
  inverse-surface: '#0e3727'
  inverse-on-surface: '#cffbe2'
  outline: '#707973'
  outline-variant: '#bfc9c1'
  surface-tint: '#2c694e'
  primary: '#0f5238'
  on-primary: '#ffffff'
  primary-container: '#2d6a4f'
  on-primary-container: '#a8e7c5'
  inverse-primary: '#95d4b3'
  secondary: '#954a00'
  on-secondary: '#ffffff'
  secondary-container: '#ff850d'
  on-secondary-container: '#602e00'
  tertiary: '#5f4200'
  on-tertiary: '#ffffff'
  tertiary-container: '#7d5800'
  on-tertiary-container: '#ffd388'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#b1f0ce'
  primary-fixed-dim: '#95d4b3'
  on-primary-fixed: '#002114'
  on-primary-fixed-variant: '#0e5138'
  secondary-fixed: '#ffdcc6'
  secondary-fixed-dim: '#ffb784'
  on-secondary-fixed: '#301400'
  on-secondary-fixed-variant: '#713700'
  tertiary-fixed: '#ffdea9'
  tertiary-fixed-dim: '#f9bc47'
  on-tertiary-fixed: '#271900'
  on-tertiary-fixed-variant: '#5e4100'
  background: '#e8fff0'
  on-background: '#002114'
  surface-variant: '#c1ecd4'
typography:
  headline-1:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-1-mobile:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-2:
    fontFamily: Playfair Display
    fontSize: 36px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-3:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.3'
  body-large:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-medium:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-small:
    fontFamily: Be Vietnam Pro
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
  label-bold:
    fontFamily: Be Vietnam Pro
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
  button:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  huge: 64px
---

## Brand & Style
The design system is engineered for "Kisan Sathi," balancing the technical precision of smart farming with the organic reliability of the agricultural sector. The brand personality is **Professional, Trustworthy, and Modern**, aiming to evoke a sense of growth, stability, and data-driven confidence.

The visual style follows a **Corporate / Modern** approach with high-performance utility. It prioritizes clarity and legibility to ensure the UI remains functional under diverse outdoor lighting conditions. By blending sophisticated serif headings with geometric sans-serif UI elements, the system bridges the gap between traditional agricultural wisdom and cutting-edge ag-tech.

## Colors
This design system utilizes an agriculture-inspired palette. The **Forest Green** serves as the primary anchor for brand identity and primary actions. **Harvest Orange** is reserved for high-priority secondary actions and warning states, while **Golden Wheat** provides a warm accent for data visualizations and highlights.

The color system is built for accessibility; high-contrast ratios between text and background surfaces are mandatory. In dark mode, the palette shifts to a deep navy-charcoal base to reduce glare during night-time field monitoring.

## Typography
Typography is used to establish a clear hierarchy between editorial-style data summaries and functional interface controls. 

- **Headings (Playfair Display):** Used for page titles and section headers to convey authority and tradition.
- **UI & Body (Be Vietnam Pro):** Chosen as a modern substitute for Poppins, offering superior legibility and a friendly, contemporary feel for data-heavy agricultural inputs and dashboards.
- **Scale:** All font sizes follow a modular scale. Mobile headings are stepped down to prevent overflow, while body sizes remain large enough for easy reading on handheld devices in the field.

## Layout & Spacing
The layout follows a **Fluid Grid** system based on a 4px baseline rhythm. This ensures all components—from small buttons to large data cards—align to a consistent vertical and horizontal cadence.

- **Desktop:** 12-column grid with generous 64px outer margins to focus the user's eye on the central dashboard content.
- **Mobile:** Single column layout with 16px margins to maximize horizontal real estate.
- **Rhythm:** Use `md` (16px) for internal component padding and `lg` (24px) for spacing between distinct UI blocks.

## Elevation & Depth
This design system uses **Tonal Layers** combined with **Ambient Shadows** to create a structured sense of depth. 

- **Background:** The lowest layer, using the neutral-light or neutral-dark background tokens.
- **Cards/Surfaces:** Elevated using a subtle, diffused shadow (0px 4px 20px rgba(0,0,0,0.05)) to separate content from the background. 
- **Floating Elements:** Modals and dropdowns use a more pronounced shadow (0px 8px 32px rgba(0,0,0,0.12)) to indicate high-priority interaction.
- **Dark Mode Depth:** In dark mode, depth is expressed primarily through slight shifts in surface color (lighter grays for higher elevation) rather than heavy shadows.

## Shapes
The shape language is **Rounded**, utilizing a 16px (1rem) corner radius for primary containers and cards. This softens the technical nature of the application, making the tool feel more approachable and modern. Smaller elements like buttons and input fields follow a consistent 8px (0.5rem) radius to maintain a cohesive visual family.

## Components
Consistent component styling ensures the application remains intuitive for farmers who may be using the tool under physical constraints.

- **Buttons:** Primary buttons use the Forest Green background with white text. Secondary buttons use an Emerald outline. All buttons must have a minimum height of 48px to ensure they are touch-friendly.
- **Cards:** Cards are the primary container for data. They feature the 16px corner radius and the subtle ambient shadow. Use `md` (16px) internal padding.
- **Input Fields:** Use a solid 1px border (#DEE2E6 in light mode). On focus, the border transitions to Forest Green with a soft outer glow.
- **Chips/Badges:** Use for crop types or status updates. These should be semi-transparent versions of the status colors (e.g., 10% opacity Emerald for "Healthy" status).
- **Data Tables:** High-contrast row stripes for readability. Headers should use the `label-bold` typography style.
- **Weather/Status Widgets:** Use Golden Wheat and Harvest Orange to highlight critical environmental data like soil moisture and temperature alerts.