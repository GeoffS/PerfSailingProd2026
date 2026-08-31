# Hugo SSG Conversion - Performance Sailing Products

## Project Summary

Successfully converted the Performance Sailing Products static website from HTML to a Hugo Static Site Generator (SSG) structure, with automated extraction of product and parts entries into reusable templates.

## Structure Overview

### Directory Layout

```
PerfSailingProd2026/
├── content/
│   ├── products/
│   │   ├── Products_blokart/
│   │   │   └── _index.md
│   │   ├── Products_CamMounts/
│   │   │   └── _index.md
│   │   ├── Products_DN/
│   │   │   └── _index.md
│   │   └── Products_MiniSketer/
│   │       └── _index.md
│   └── parts/
│       ├── Parts_Nautos/
│       │   └── _index.md
│       ├── Parts_Ratchets/
│       │   └── _index.md
│       └── Parts_Viadana/
│           └── _index.md
├── data/
│   ├── products/
│   │   ├── Products_blokart.json
│   │   ├── Products_CamMounts.json
│   │   ├── Products_DN.json
│   │   └── Products_MiniSketer.json
│   └── parts/
│       ├── Parts_Nautos.json
│       ├── Parts_Ratchets.json
│       └── Parts_Viadana.json
├── themes/psp/
│   └── layouts/
│       ├── _default/
│       │   ├── baseof.html
│       │   └── sidebar.html
│       ├── partials/
│       │   ├── simple-product-entry.html
│       │   ├── descriptive-entry.html
│       │   └── section-heading.html
│       ├── products/
│       │   └── section.html
│       └── parts/
│           └── section.html
├── public/
│   ├── products/
│   │   ├── products_blokart/index.html
│   │   ├── products_cammounts/index.html
│   │   ├── products_dn/index.html
│   │   └── products_minisketer/index.html
│   └── parts/
│       ├── parts_nautos/index.html
│       ├── parts_ratchets/index.html
│       └── parts_viadana/index.html
├── hugo.toml
└── extract_products.py
```

## How It Works

### 1. Content Extraction (`extract_products.py`)

The extraction script performs these steps:

1. **Parses HTML files** from `PerfSailingProd_www` directory
2. **Extracts main headings** (e.g., "DN Iceboat Products:")
3. **Finds section separators** marked by `<hr class="sectionSeparator" />`
4. **Extracts sub-headings** (e.g., "Standard Products:")
5. **Identifies product entries** between `<hr class="product" />` or `<hr class="parts" />` tags
6. **Parses two types of entries**:
   - **Simple product entries**: Image, name, description, price
   - **Descriptive entries**: Complex content like tables with optional images
7. **Generates Hugo content files** with YAML front matter containing structured data
8. **Stores extracted data** as JSON in the data directory for reference

### 2. Front Matter Structure

Each generated markdown file uses YAML front matter to store the structured product data:

```yaml
---
title: "Products DN"
description: "DN Iceboat Products:"
date: 2026-08-30
draft: false
type: products
sections:
  - heading: "Standard Products:"
    count: 3
    items:
      - type: simple
        name: "Product Name"
        description: "Product description..."
        image: "products/image.jpg"
        price: "$XX + Shipping"
      - type: descriptive
        heading: "Optional heading"
        content: "<table>...</table>"
        image: "parts/image.jpg"
---
```

### 3. Hugo Templates

#### Base Template (`baseof.html`)
- Defines the overall page structure
- Sets up HTML head with stylesheets
- Defines banner and layout
- Uses `block` directives for sidebar and main content

#### Section Layouts
- `layouts/products/section.html` - Renders product pages with products CSS classes
- `layouts/parts/section.html` - Renders parts pages with parts CSS classes
- Both iterate over `.Params.sections` from front matter
- Render products with proper HTML structure matching original design

#### Rendering Logic
Each section layout:
1. Renders sidebar navigation
2. Iterates over sections from front matter
3. For each section:
   - Displays sub-heading
   - Renders section separator
   - Loops through items and renders based on type:
     - **Simple**: Image div, description div, price div
     - **Descriptive**: Full HTML content div

### 4. Data Files

JSON data files in `data/` directory store the complete extracted data for reference:

```json
{
  "title": "Products DN",
  "main_heading": "DN Iceboat Products:",
  "sections": [
    {
      "sub_heading": "Standard Products:",
      "products": [
        {
          "type": "simple",
          "name": "...",
          "description": "...",
          "image": "...",
          "price": "...",
          "link": "...",
          "contactUrl": "/contact/"
        }
      ]
    }
  ]
}
```

## Entry Types

### Simple Product Entry
Used for standard product listings with:
- Thumbnail image (100x100)
- Product name  
- Description text
- Optional link to detail page
- Price information
- Optional contact/order button

**Example HTML rendering:**
```html
<hr class="product" />
<div class="span-1 clear spacer">.</div>
<div class="span-3 push-1 product">
  <img class="tn" src="products/image.jpg" width="100" height="100" />
</div>
<div class="span-14 product">
  <p>Description...</p>
</div>
<div class="span-2 right productPrice">
  Price + Shipping
</div>
```

### Descriptive Product Entry  
Used for complex entries like parts lists with:
- Tables with item numbers, descriptions, pricing
- Optional images
- Multi-row complex content

**Example:** Parts_Viadana.html "22mm Ball-Bearing Blocks" section with product table

## Generation Process

To regenerate content after modifying the extraction script:

```bash
cd PerfSailingProd2026
python extract_products.py
hugo build
```

This will:
1. Parse all `Products_*.html` and `Parts_*.html` files
2. Create section directories with `_index.md` files
3. Store extracted data in `data/` directory
4. Generate static HTML in `public/` directory

## CSS Framework

The site uses the **Blueprint CSS Framework** for layout:
- `span-4` - 4 column sidebar
- `span-20` - 20 column main content
- `span-24` - Full width
- Product/parts specific classes for styling

## Headings Extracted

### Product Headings
- `productHeading` - Main category heading
- `productSubHeading` - Section sub-heading (e.g., "Standard Products")

### Parts Headings  
- `partsHeading` - Main category heading
- `partsSubHeading` - Section sub-heading (e.g., "Blocks")

## Next Steps

To further enhance this Hugo setup:

1. **Create home page layout** - `layouts/index.html` for category listings
2. **Add section/taxonomy layouts** - For product browsing by category
3. **Create detail pages** - Individual product pages linked from main listings
4. **Copy static assets** - CSS, images, JavaScript to `static/` directory
5. **Configure base URL** - Update `baseURL` in `hugo.toml` for your domain
6. **Add navigation** - Create about, contact pages
7. **Build theme CSS** - Customize or extend Blueprint styling

## Files Generated

- **7 Product Pages** - DN, blokart, Mini-Skeeter, Camera Mounts
- **3 Parts Pages** - Ratchets, Viadana, Nautos
- **22 total HTML pages** including section index pages
- **7 data files** with extracted product information

All HTML files maintain the original layout structure and CSS classes for compatibility with existing stylesheets.
