# Usage Guide for Hugo SSG - Performance Sailing Products

## Quick Start

### Building the Site

```bash
cd PerfSailingProd2026
hugo build
```

Output will be generated in the `public/` directory.

### Previewing the Site

```bash
hugo server
```

Then open http://localhost:1313 in your browser.

## Modifying Content

### Adding/Updating a Product

1. Edit the corresponding markdown file:
   - Product: `content/products/Products_*/index.md`
   - Parts: `content/parts/Parts_*/index.md`

2. Modify the front matter sections array:

```yaml
sections:
  - heading: "Section Name"
    count: 1
    items:
      - type: simple
        name: "Product Name"
        image: "products/image.jpg"
        imageWidth: "100"
        imageHeight: "100"
        description: "Product description"
        price: "$99.99 + Shipping"
        link: "/detail-page/"
```

3. Rebuild: `hugo build`

### Adding a New Product Category

1. Create new directory:
   ```bash
   mkdir -p content/products/Products_NewCategory
   ```

2. Create `_index.md` with front matter containing sections

3. Create corresponding data file in `data/products/Products_NewCategory.json`

4. Rebuild: `hugo build`

## Extraction and Re-import

### Re-extract from Original HTML

If the original HTML files change, re-run the extraction:

```bash
python extract_products.py
hugo build
```

This will:
1. Parse all Products_*.html and Parts_*.html from PerfSailingProd_www
2. Regenerate content files with updated data
3. Store extracted data in data/ directory

## Theme Customization

### Changing Styles

1. CSS files are in original source, reference them in templates:
   - Blueprint CSS: `blueprint/screen.css`
   - Custom styles: `GSSTstyle.css`

2. To use local CSS:
   - Copy to `static/css/`
   - Update paths in `themes/psp/layouts/_default/baseof.html`

### Adding New Sections

Create new layout file in `themes/psp/layouts/` following the pattern:

```html
{{ define "sidebar" }}
  <!-- Navigation -->
{{ end }}

{{ define "main" }}
  <!-- Content -->
{{ end }}
```

### Modifying the Sidebar

Edit the `define "sidebar"` block in:
- `themes/psp/layouts/products/section.html`
- `themes/psp/layouts/parts/section.html`
- `themes/psp/layouts/_default/sidebar.html`

## Front Matter Reference

### Product Item Fields

```yaml
items:
  - type: simple|descriptive        # Entry type
    name: string                     # Product name (optional for descriptive)
    description: string              # Product description or HTML content
    image: string                    # Image path (optional)
    imageWidth: string              # Image width (default: 100)
    imageHeight: string             # Image height (default: 100)
    price: string                   # Price text (HTML allowed)
    link: string                    # Link to detail page (optional)
    contactUrl: string              # Contact/order link (default: /contact/)
    content: string                 # For descriptive type: full HTML content
    style: string                   # Optional CSS style attribute
```

## Hugo Commands Reference

- `hugo build` - Build production site
- `hugo server` - Local development server
- `hugo server -D` - Include draft posts in preview
- `hugo list all` - List all content with details
- `hugo version` - Show Hugo version

## Directory Structure Explanation

### content/
Hugo looks for markdown files here. Files ending with `_index.md` become section pages.

### data/
Data files in YAML/JSON/TOML format accessed in templates via `.Site.Data`.

### public/
Generated static HTML output. Ready to deploy.

### static/
Static files (images, CSS, JS) copied as-is to public/.

### themes/psp/
Custom Hugo theme with layouts and partials.

## Troubleshooting

### Pages Not Generating

1. Check `hugo list all` to see if content is recognized
2. Verify `_index.md` is in correct directory structure
3. Ensure front matter is valid YAML

### Styling Issues

1. Check if CSS files are being served (check browser console)
2. Verify CSS file paths in baseof.html
3. Check if `baseURL` in hugo.toml needs adjustment for relative paths

### Data Not Rendering

1. Verify `.Params.sections` is being populated (check source)
2. Check template `{{ range .Params.sections }}` logic
3. Ensure markdown file has proper YAML front matter

## Performance Tips

- Use `hugo build` for production (faster than `hugo server`)
- Enable minification: `hugo --minify`
- Run garbage collection: `hugo build --gc`
- Check performance: `hugo --templateMetrics`

## Deployment

### To a Web Server

1. Build: `hugo build`
2. Upload contents of `public/` to web server
3. Ensure base URL matches server domain in `hugo.toml`

### To GitHub Pages

1. Build: `hugo build`
2. Commit `public/` directory
3. Configure GitHub Pages to serve from the branch

## Resources

- Hugo Documentation: https://gohugo.io/documentation/
- Markdown Guide: https://www.markdownguide.org/
- Blueprint CSS: http://blueprintcss.org/

## Support Files

- `HUGO_CONVERSION_GUIDE.md` - Technical overview of the conversion
- `extract_products.py` - Python script to extract and convert HTML
- `hugo.toml` - Hugo configuration file
