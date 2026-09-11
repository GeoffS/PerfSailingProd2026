# Performance Sailing Products Hugo Site

## Status

✅ Hugo conversion is in place and the generated site has been verified. The current build succeeds, and recent work restored the missing content and formatting fidelity across the migrated detail pages, project pages, and section pages.

## What this project contains

This Hugo project now includes:

- Products sections for DN Iceboat, blokart, Mini-Skeeter, and Camera Mounts
- Parts sections for Ratchets, Viadana, and Nautos
- Project pages for the existing static site projects
- Detail pages converted from the legacy HTML files
- Shared layouts and static assets that preserve the original site structure and styling

## Current verified build state

The last verification run succeeded:

```bash
python extract_detail_pages.py
hugo build
```

Fresh build output showed:

- Pages: 36
- Static files: 456
- Aliases: 27
- Build completed successfully

There is one non-blocking warning remaining:

- Hugo reports no taxonomy layout for kind `taxonomy` (`found no layout file for "html" for kind "taxonomy"`)

This warning does not stop the site from building or serving correctly.

## Quick start

```bash
# rebuild the full site
hugo build

# preview locally
hugo server
```

Open http://localhost:1313 to preview the generated site.

## Scripts and source files

| File | Purpose |
|------|---------|
| `extract_products.py` | Converts the legacy HTML product/parts pages into Hugo section content |
| `extract_detail_pages.py` | Converts legacy detail pages into Hugo markdown and normalizes HTML references |
| `hugo.toml` | Hugo configuration |
| `content/` | Generated content for products, parts, projects, and detail pages |
| `themes/psp/layouts/` | Theme templates and shared page layouts |
| `static/` | Copied static assets such as CSS, images, and misc files |
| `public/` | Generated site output |

## Latest migration improvements reflected in this build

Recent work completed for the migrated site includes:

- restored the home page content from the original site
- corrected product links so they point to the new Hugo detail pages
- added missing intro/section content for generated product and parts pages
- restored the Projects navigation block and added the missing project pages
- fixed page rendering issues on project pages
- repaired malformed generated detail page content
- normalized detail-page HTML paths and references
- regenerated all detail pages after the shared converter fix

## Documentation

- [HUGO_CONVERSION_GUIDE.md](HUGO_CONVERSION_GUIDE.md) — technical conversion and architecture notes
- [USAGE_GUIDE.md](USAGE_GUIDE.md) — current content update and maintenance workflow
- [COMPLETION_REPORT.md](COMPLETION_REPORT.md) — current project status and verification summary

## Project structure

```text
PerfSailingProd2026/
├── content/
│   ├── _index.md
│   ├── products/
│   ├── parts/
│   ├── projects/
│   └── detail/
├── data/
├── static/
├── themes/psp/
├── public/
├── extract_products.py
├── extract_detail_pages.py
├── hugo.toml
├── README.md
├── HUGO_CONVERSION_GUIDE.md
├── USAGE_GUIDE.md
├── COMPLETION_REPORT.md
├── LICENSE
└── .gitignore
```

## Regeneration workflow

If the legacy source HTML changes, regenerate content with:

```bash
python extract_products.py
python extract_detail_pages.py
hugo build
```

## Requirements

- Hugo 0.165.0 or newer (current project was built with Hugo 0.165.0)
- Python 3.x

## Notes

- The current site is serving from Hugo content generated from the original static source.
- Detail pages now render using the same site layout framework as the rest of the site.
- The remaining taxonomy warning is cosmetic and does not affect the generated site output.

---

*Updated September 11, 2026*