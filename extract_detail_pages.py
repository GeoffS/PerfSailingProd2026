#!/usr/bin/env python3
"""
Convert detail HTML pages to Hugo content files
"""

import re
import os
from pathlib import Path
from typing import Dict, Tuple

def extract_detail_page(html_content: str, filename: str) -> Tuple[str, str]:
    """Extract title and content from detail page"""
    
    # Extract title from title tag
    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    title = title_match.group(1) if title_match else filename.replace('.html', '')
    
    # Extract main content from infoPage div
    content_match = re.search(r'<div class="infoPage">(.*?)</div>\s*</div>\s*<div class="span-24">', html_content, re.DOTALL)
    if content_match:
        content_html = content_match.group(1).strip()
        # Normalize relative paths to absolute
        content_html = re.sub(r'href="([^"]*)"(?!:/)', r'href="/\1', content_html)
        content_html = re.sub(r'src="([^"]*)"(?!:/)', r'src="/\1', content_html)
        return title, content_html
    
    return title, ""

def create_hugo_file(filename: str, title: str, content: str, content_dir: str):
    """Create a Hugo markdown file"""
    # Generate a slug from filename
    slug = filename.replace('.html', '').lower()
    original_filename = filename.replace('.html', '')
    
    # Create front matter with alias to redirect from original filename
    front_matter = f"""---
title: "{title}"
date: 2026-08-31
draft: false
type: detail
aliases:
  - /{original_filename}.html
---
"""
    
    # Combine front matter with content wrapped in raw HTML
    hugo_content = front_matter + f"\n{{% raw %}}\n{content}\n{{% endraw %}}\n"
    
    # Write file
    output_path = Path(content_dir) / f"{slug}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(hugo_content)
    
    print(f"Created {output_path}")
    return str(output_path)

def main():
    source_dir = Path("../PerfSailingProd_www")
    content_dir = Path("content/detail")
    
    # Create content directory
    content_dir.mkdir(parents=True, exist_ok=True)
    
    # List of detail pages to convert (excluding main product/parts pages)
    detail_pages = [
        "19mmCCMount.html",
        "22mmCCMount.html", 
        "22mmCCMountProtoype.html",
        "22mmStdCCMountProtoype.html",
        "5.5sqmMainsailRigging.html",
        "CascadeControlSystems.html",
        "DN_ChainstitchMainsheets.html",
        "HiTechChainstitchMainsheetPrototype.html",
        "IceSafetyPicks.html",
        "MiniSkeeterMainsheetBlocks.html",
        "PSP010.html",
        "PSP011.html",
        "PSP012.html",
        "PSP501.html",
        "PSP600.html",
        "StaSetChainstitchMainsheet.html",
    ]
    
    for page in detail_pages:
        file_path = source_dir / page
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            title, content = extract_detail_page(html_content, page)
            if content:
                create_hugo_file(page, title, content, content_dir)
                print(f"  Processed: {page} -> {title}")

if __name__ == '__main__':
    main()
