# CLAUDE.md - Production Jinja2 Theme

This file provides guidance to Claude Code (claude.ai/code) when working with the production Jinja2 theme.

> **Note**: This is part of a dual-setup project. See the root `/zid-theme/CLAUDE.md` for the complete development workflow including the HTML prototype workspace.

## Project Overview

This is the production Jinja2-based e-commerce theme called "soft-theme-vitrin" for the Zid platform. This theme supports RTL languages and includes comprehensive e-commerce functionality.

## Architecture

### Template Structure
- **layout.jinja**: Main layout template with head, CSS variables, and basic structure
- **header.jinja/footer.jinja**: Reusable header and footer components
- **templates/**: Page templates for different views (product, category, cart, account, etc.)
- **sections/**: Reusable content sections (sliders, product grids, galleries, etc.)
- **components/**: Smaller reusable UI components (product cards, breadcrumbs, pagination, etc.)

### Schema-Driven Configuration
Each template has a corresponding `.schema.json` file that defines:
- Customizable settings and their types (text, color, image, select, etc.)
- Multilingual labels (Arabic/English)
- Field validation and options

### Asset Management
- **assets/**: Static files (CSS, JS, images, fonts)
- CSS uses CSS custom properties for theming (--primary-color, etc.)
- jQuery-based interactions with plugins like Slick slider, PhotoSwipe, Toastr
- Bootstrap for responsive grid and components

### Internationalization
- **locale/ar/**: Arabic translation files (.po/.mo format)
- Bilingual schema definitions with "ar" and "en" keys
- RTL support via CSS and Bootstrap RTL classes
- Font selection supports Arabic typography (Changa, Cairo, Amiri, etc.)

## Key Files

### Core Templates
- `layout.jinja`: Main HTML structure with configurable fonts, colors, and branding
- `templates/product.jinja`: Product detail page with gallery, variants, reviews
- `templates/category.jinja`: Product listing with filters and pagination
- `templates/cart.jinja`: Shopping cart functionality
- `templates/home.jinja`: Homepage with sections

### Configuration Schemas
- `layout.schema.json`: Theme-wide settings (fonts, colors, logos)
- `sections/*.schema.json`: Section-specific settings (titles, product selections, styling)

### JavaScript Features
- Product gallery with zoom and lightbox
- Shopping cart functionality with AJAX
- Slide-out mobile menu
- Product filtering and search
- Loyalty points integration

## Development Guidelines

### Template Editing
- Use Jinja2 syntax for templating
- Follow existing naming conventions for variables and includes
- Respect the schema-driven configuration system
- Include both Arabic and English labels in schema files

### CSS Modifications
- Use CSS custom properties for theme colors
- Follow existing Bootstrap and custom CSS structure
- Maintain RTL compatibility
- Keep responsive design principles

### Asset Handling
- Place static assets in the `assets/` directory
- Use `asset_url` filter for asset references
- Version assets with query parameters when needed
- Optimize images for web usage

### Schema Configuration
- Define settings in corresponding `.schema.json` files
- Include multilingual labels (ar/en)
- Use appropriate field types (color, image, text, select, etc.)
- Group related settings logically

## No Build Process

This is a template-based project without a build system. Changes to templates and assets are directly used by the platform. There are no npm scripts for building, testing, or linting - the package.json is minimal.