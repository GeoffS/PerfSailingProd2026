# Usage Guide

## Quick start

### Build the site

```bash
cd PerfSailingProd2026
hugo build
```

### Preview locally

```bash
hugo server
```

Then open http://localhost:1313 in your browser.

## Current content structure

The current Hugo site includes:

- products sections in `content/products/`
- parts sections in `content/parts/`
- project pages in `content/projects/`
- detail pages in `content/detail/`

The generated site output is in `public/`.

## Regeneration workflow

If the legacy source HTML changes, regenerate the Hugo content with:

```bash
python extract_products.py
python extract_detail_pages.py
hugo build
```

### What each script does

- `extract_products.py` rebuilds the product and parts section pages from the legacy static HTML
- `extract_detail_pages.py` rebuilds the detail pages and normalizes HTML references

## Updating existing section content

### Product and parts pages

The content for products and parts is stored in files such as:

- `content/products/Products_DN/_index.md`
- `content/products/Products_blokart/_index.md`
- `content/parts/Parts_Ratchets/_index.md`

Edit those Markdown files directly if you want to adjust the rendered content, then rebuild:

```bash
hugo build
```

## Working with detail pages

Detail pages live in `content/detail/`, for example:

- `content/detail/psp600.md`
- `content/detail/stasetchainstitchmainsheet.md`

If the source HTML file in `PerfSailingProd_www` changes, rerun:

```bash
python extract_detail_pages.py
hugo build
```

This is the safest way to refresh the converted detail pages after any source changes.

## Project pages

Project content currently lives in `content/projects/` and is rendered using the standard site layout.

Examples:

- `content/projects/blokart-5.5m-mainsheet.md`
- `content/projects/blokart-mainsheet-cleat.md`
- `content/projects/dn-composite-mainsheet.md`
- `content/projects/ice-safety-picks.md`

## Theme customization

The custom theme is in `themes/psp/`.

Common edit locations:

- `themes/psp/layouts/_default/baseof.html` — shared HTML shell
- `themes/psp/layouts/_default/single.html` — generic single-page layout
- `themes/psp/layouts/products/section.html` — product section rendering
- `themes/psp/layouts/parts/single.html` — parts content rendering
- `themes/psp/layouts/detail/single.html` — detail page rendering

## Styling

The site uses the Blueprint CSS framework and the original static CSS files remain in the project.

Relevant static assets live in:

- `static/blueprint/`
- `static/GSSTstyle.css`
- `static/images/`
- `static/misc/`

## Common maintenance tasks

### Refresh all generated content

```bash
python extract_products.py
python extract_detail_pages.py
hugo build
```

### Preview changes

```bash
hugo server
```

### Check the current content inventory

```bash
hugo list all
```

## Troubleshooting

### Pages render incorrectly

1. confirm the source HTML in `PerfSailingProd_www` is correct
2. rerun `python extract_detail_pages.py`
3. rebuild with `hugo build`
4. inspect the generated output in `public/`

### Broken links

1. check whether the target page is generated in `content/`
2. verify the alias or URL mapping in the generated markdown
3. rebuild the site after any source or layout updates

### Hugo warning about taxonomy layout

This warning appears in the current build output:

```text
found no layout file for "html" for kind "taxonomy"
```

It is non-blocking. The build still succeeds and pages still render correctly.

## Deployment

To deploy the generated site:

1. run `hugo build`
2. upload the contents of `public/` to your hosting environment
3. ensure the site is served from the correct root path if your host is not using `/`

## Resources

- [README.md](README.md)
- [HUGO_CONVERSION_GUIDE.md](HUGO_CONVERSION_GUIDE.md)
- [COMPLETION_REPORT.md](COMPLETION_REPORT.md)

---

*Updated September 11, 2026*