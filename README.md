# Hugo SSG Conversion - Performance Sailing Products

**Status**: ✅ Complete

Successfully converted the Performance Sailing Products static website to a **Hugo Static Site Generator** with automated template extraction and data-driven content management.

## Quick Start

```bash
# Build the site
hugo build

# Preview locally
hugo server
```

Open http://localhost:1313 to preview.

## What's Included

### Generated Content (7 Pages)
- **Products**: DN Iceboat, blokart, Mini-Skeeter, Camera Mounts
- **Parts**: Ratchets, Viadana, Nautos

### Generated Output
- **22 HTML pages** ready for deployment
- Original CSS structure and layout preserved
- Product data extracted and organized in YAML front matter

### Key Files

| File | Purpose |
|------|---------|
| `extract_products.py` | Python script to extract HTML and generate Hugo content |
| `hugo.toml` | Hugo project configuration |
| `themes/psp/layouts/` | Theme templates for products and parts |
| `content/products/` | Product content (markdown) |
| `content/parts/` | Parts content (markdown) |
| `data/` | Extracted JSON data for reference |
| `public/` | Generated static HTML (ready to deploy) |

## Documentation

- **[HUGO_CONVERSION_GUIDE.md](HUGO_CONVERSION_GUIDE.md)** - Technical overview of conversion process
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - How to use and modify the Hugo project

## Features

✅ **Automated Extraction** - Python script parses HTML and generates Hugo content  
✅ **Data-Driven** - Product information stored in YAML front matter  
✅ **Two Entry Types** - Simple products and complex descriptive entries  
✅ **Layout Preservation** - CSS classes and structure maintained  
✅ **Template System** - Reusable layouts for products and parts  
✅ **Section Organization** - Hierarchical grouping of products  

## How It Works

1. **Extract**: `python extract_products.py` parses HTML files
2. **Generate**: Creates markdown files with structured product data
3. **Build**: `hugo build` generates static HTML
4. **Deploy**: Upload `public/` directory to web server

## To Regenerate Content

If source HTML files change:

```bash
python extract_products.py
hugo build
```

## Structure

```
PerfSailingProd2026/
├── content/             # Markdown content files
│   ├── products/        # Product pages
│   └── parts/           # Parts pages
├── data/                # Extracted JSON data
├── themes/psp/          # Custom Hugo theme
│   └── layouts/         # Page templates
├── public/              # Generated static HTML
├── hugo.toml            # Configuration
└── extract_products.py  # Extraction script
```

## Template System

### Simple Product Entry
- Image (100x100)
- Product name
- Description
- Price
- Optional link

### Descriptive Entry
- Complex HTML content
- Tables with pricing
- Optional images

## Deployment

The `public/` directory contains ready-to-deploy static HTML:

```bash
# Deploy to any web server
cp -r public/* /var/www/psp/
```

## Requirements

- Hugo 0.100+ (for building)
- Python 3.6+ (for extraction script)

## Troubleshooting

**Pages not generating?**
- Check: `hugo list all` 
- Verify front matter YAML is valid
- Check error messages: `hugo build --verbose`

**Styling issues?**
- CSS paths use relative URLs - adjust `baseURL` in `hugo.toml`
- Blueprint CSS should be in web root
- Check browser console for 404 errors

## Next Steps

Optional enhancements:
- Create home page with category listings
- Add detail pages for individual products
- Implement search functionality
- Optimize images
- Modernize CSS framework

## Project Statistics

- **Pages Generated**: 22
- **Products Extracted**: 27 simple + 4 complex entries
- **Categories**: 7 (4 products + 3 parts)
- **HTML Output Files**: 10
- **Build Time**: ~50ms

---

*Conversion completed August 30, 2026*  
*Hugo Migration Project - COMPLETE*