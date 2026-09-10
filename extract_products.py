#!/usr/bin/env python3
"""
HTML to Hugo converter for Performance Sailing Products
Extracts product/parts entries from HTML and generates Hugo content files
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple
import json

class ProductExtractor:
    def __init__(self, html_content: str):
        self.html = html_content
        self.main_heading = ""
        self.sections = []
    
    def extract_main_heading(self) -> str:
        """Extract main heading, handling HTML tags within it"""
        # Match productHeading div, capturing everything between opening and closing tags
        match = re.search(r'<div[^>]*class="[^"]*productHeading[^"]*"[^>]*>(.*?)</div>', self.html, re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Remove any HTML tags but keep text
            text = re.sub(r'<[^>]+>', '', text)
            return text
        
        # Try partsHeading
        match = re.search(r'<div[^>]*class="[^"]*partsHeading[^"]*"[^>]*>(.*?)</div>', self.html, re.DOTALL)
        if match:
            text = match.group(1).strip()
            text = re.sub(r'<[^>]+>', '', text)
            return text
        
        return ""
    
    def extract_intro_content(self) -> str:
        """Extract the original intro block that appears before the first product group or section heading."""
        heading_patterns = [
            r'<div[^>]*class="[^"]*productHeading[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*partsHeading[^"]*"[^>]*>(.*?)</div>'
        ]

        for pattern in heading_patterns:
            heading_match = re.search(pattern, self.html, re.DOTALL)
            if not heading_match:
                continue

            start_idx = heading_match.start()
            trailing_html = self.html[heading_match.end():]

            # Find the earliest content boundary after the heading: either the first
            # product/parts sub-heading or the first product separator.
            subheading_match = re.search(r'<div[^>]*class="[^"]*(?:product|parts)SubHeading[^"]*"[^>]*>', trailing_html, re.DOTALL)
            product_start_match = re.search(r'<hr class="(?:product|parts)"\s*/?>', trailing_html, re.DOTALL)

            boundary_start = None
            if subheading_match:
                boundary_start = subheading_match.start()
            if product_start_match and (boundary_start is None or product_start_match.start() < boundary_start):
                boundary_start = product_start_match.start()

            if boundary_start is not None:
                end_idx = heading_match.end() + boundary_start
                intro_html = self.html[start_idx:end_idx]
                return intro_html.strip()

        return ""

    def extract_sections(self) -> List[Dict]:
        """Extract sections between sectionSeparators with their sub-headings"""
        sections = []
        
        # Find content area
        content_match = re.search(r'<div id="ContentDiv"[^>]*>.*?<div class="(?:product|parts)"[^>]*>(.*?)</div>\s*<div class="span-24">', self.html, re.DOTALL)
        if not content_match:
            return sections
        
        content_area = content_match.group(1)
        
        # Split by sectionSeparator to find sections
        separator_splits = re.split(r'<hr class="sectionSeparator"\s*/?>', content_area)
        
        for section_html in separator_splits[1:]:  # Skip first element before first separator
            # Extract sub-heading from this section
            heading_match = re.search(r'<div[^>]*class="[^"]*(?:product|parts)SubHeading[^"]*"[^>]*>(.*?)</div>', section_html, re.DOTALL)
            if heading_match:
                sub_heading = heading_match.group(1).strip()
                # Clean HTML tags
                sub_heading = re.sub(r'<[^>]+>', '', sub_heading)
                sub_heading = re.sub(r'^\s*<span[^>]*>', '', sub_heading)
                sub_heading = re.sub(r'</span>\s*$', '', sub_heading)
            else:
                # No heading found, use generic name based on section count
                sub_heading = None
            
            products = self.extract_products_from_section(section_html)
            if products:
                # If no sub-heading was found, use a default name
                if sub_heading is None:
                    sub_heading = f"Products {len(sections) + 1}" if len(sections) > 0 else "Products"
                
                sections.append({
                    'sub_heading': sub_heading,
                    'products': products
                })
        
        return sections
    
    def extract_products_from_section(self, section_html: str) -> List[Dict]:
        """Extract individual product entries from a section, handling both product and parts separators"""
        products = []
        
        # Split by both <hr class="product" /> and <hr class="parts" />
        product_blocks = re.split(r'<hr class="(?:product|parts)"\s*/?>', section_html)
        
        for block in product_blocks[1:]:  # Skip first empty element
            block_stripped = block.strip()
            if not block_stripped:
                continue
            
            # Check if this is a table (descriptive entry)
            if '<table' in block_stripped:
                # This is a descriptive entry with a table
                product = self.parse_descriptive_block(block)
            else:
                # This is a simple product entry
                product = self.parse_product_block(block)
            
            if product:
                products.append(product)
        
        return products
    
    def normalize_path(self, path: str) -> str:
        """Convert relative paths to absolute paths by prepending /"""
        if path and not path.startswith('/'):
            return '/' + path
        return path
    
    def normalize_html_links(self, html: str) -> str:
        """Normalize relative href and src attributes in HTML to absolute paths and convert detail page links"""
        # Mapping of old detail page HTML filenames to new detail page URLs
        detail_page_mapping = {
            '19mmCCMount.html': '/detail/19mmccmount/',
            '22mmCCMount.html': '/detail/22mmccmount/',
            '22mmCCMountProtoype.html': '/detail/22mmccmountprotoype/',
            '22mmStdCCMountProtoype.html': '/detail/22mmstdccmountprotoype/',
            '5.5sqmMainsailRigging.html': '/detail/5.5sqmmainsailrigging/',
            'CascadeControlSystems.html': '/detail/cascadecontrolsystems/',
            'DN_ChainstitchMainsheets.html': '/detail/dn_chainstitchmainsheets/',
            'HiTechChainstitchMainsheetPrototype.html': '/detail/hitechchainstitchmainsheetprototype/',
            'IceSafetyPicks.html': '/detail/icesafetypicks/',
            'MiniSkeeterMainsheetBlocks.html': '/detail/miniskeetermainsheetblocks/',
            'PSP010.html': '/detail/psp010/',
            'PSP011.html': '/detail/psp011/',
            'PSP012.html': '/detail/psp012/',
            'PSP501.html': '/detail/psp501/',
            'PSP600.html': '/detail/psp600/',
            'StaSetChainstitchMainsheet.html': '/detail/stasetchainstitchmainsheet/'
        }
        
        # Normalize href attributes
        def normalize_href(match):
            href = match.group(1)
            if not href:
                return f'href="{href}"'
            
            # Check if this is a detail page link that needs mapping
            for old_url, new_url in detail_page_mapping.items():
                if old_url in href:
                    # Replace old filename with new detail page URL
                    href = href.replace(old_url, new_url)
                    return f'href="{href}"'
            
            # Standard path normalization for other links
            if href and not href.startswith('/') and not href.startswith('http'):
                href = '/' + href
            return f'href="{href}"'
        
        # Normalize src attributes  
        def normalize_src(match):
            src = match.group(1)
            if src and not src.startswith('/') and not src.startswith('http'):
                src = '/' + src
            return f'src="{src}"'
        
        html = re.sub(r'href="([^"]*)"', normalize_href, html)
        html = re.sub(r'src="([^"]*)"', normalize_src, html)
        return html
    
    
    def parse_descriptive_block(self, block_html: str) -> Dict:
        """Parse a descriptive entry block (tables, complex content)"""
        # Normalize relative links and image paths to absolute paths
        normalized_html = self.normalize_html_links(block_html)

        # Extract only the descriptive HTML block, stopping before the next section separator.
        start_match = re.search(r'<div class="span-20[^>]*parts[^>]*>', normalized_html)
        content_html = ""
        if start_match:
            content_start = normalized_html[start_match.start():]
            clear_match = re.search(r'<div class="span-20 clear">', content_start)
            if clear_match:
                content_html = content_start[:clear_match.start()].strip()
            else:
                content_html = content_start.strip()

        product = {
            'type': 'descriptive',
            'heading': '',
            'content': content_html,
            'image': '',
            'imageWidth': '',
            'imageHeight': ''
        }

        # Try to extract an image from the descriptive block
        img_match = re.search(r'<img[^>]*src="([^"]*)"[^>]*width="(\d+)"[^>]*height="(\d+)"', normalized_html)
        if img_match:
            product['image'] = img_match.group(1)
            product['imageWidth'] = img_match.group(2)
            product['imageHeight'] = img_match.group(3)

        return product
    
    def parse_product_block(self, block_html: str) -> Dict:
        """Parse a single product/part entry block"""
        product = {
            'type': 'simple',
            'image': '',
            'imageWidth': '100',
            'imageHeight': '100',
            'name': '',
            'description': '',
            'price': '',
            'link': '',
            'contactUrl': '/contact/'
        }
        
        # Extract image
        img_match = re.search(r'<img[^>]*src="([^"]*)"[^>]*width="(\d+)"[^>]*height="(\d+)"', block_html)
        if img_match:
            src = img_match.group(1)
            if 'placeholder' not in src:
                product['image'] = self.normalize_path(src)
                product['imageWidth'] = img_match.group(2)
                product['imageHeight'] = img_match.group(3)
        
        # Extract product name (productName class)
        name_match = re.search(r'<span class="productName">([^<]+)</span>', block_html)
        if name_match:
            product['name'] = name_match.group(1).strip()
        
        # Extract full description - all content in the span-14 div
        desc_pattern = r'<div class="span-14[^>]*>(.*?)</div>\s*<div class="span-2 right productPrice"'
        desc_match = re.search(desc_pattern, block_html, re.DOTALL)
        if desc_match:
            desc_html = desc_match.group(1).strip()
            
            # Normalize relative links to absolute paths
            desc_html = self.normalize_html_links(desc_html)
            
            # Extract link if present
            link_match = re.search(r'<a href="([^"]+)">Click here', desc_html)
            if link_match:
                product['link'] = link_match.group(1)  # Already normalized
            
            # Store the full HTML description (will be rendered with safeHTML)
            product['description'] = desc_html
        
        # Extract price
        price_pattern = r'<div class="span-2 right productPrice">([^<]+(?:<[^>]+>[^<]+</[^>]+>)*)'
        price_match = re.search(price_pattern, block_html, re.DOTALL)
        if price_match:
            price_html = price_match.group(1).strip()
            # Remove contact us div if present
            price_text = re.sub(r'<div class="ContactUsOrder".*?</div>', '', price_html, flags=re.DOTALL)
            product['price'] = price_text.strip()
        
        return product if (product['name'] or product['description']) else None

def generate_hugo_content(file_name: str, title: str, main_heading: str, sections: List[Dict], intro_content: str = "") -> str:
    """Generate Hugo markdown content from extracted data using front matter for structured data"""
    
    # Clean up title
    title = title.replace('_', ' ')
    # Remove HTML entities and symbols if present
    title = title.replace('®', '(R)')
    
    # Build front matter with sections data
    front_matter_lines = [
        "---",
        f'title: "{title}"',
        f'description: "{main_heading}"',
        "date: 2026-08-30",
        "draft: false",
        "type: products",
        "sections:"
    ]
    
    # Add sections to front matter
    for i, section in enumerate(sections):
        front_matter_lines.append(f'  - heading: "{section["sub_heading"]}"')
        front_matter_lines.append(f'    count: {len(section["products"])}')
        front_matter_lines.append('    items:')
        for j, product in enumerate(section['products']):
            front_matter_lines.append(f'      - type: {product.get("type", "simple")}')
            if product.get('name'):
                name = product['name'].replace('"', '\\"')
                front_matter_lines.append(f'        name: "{name}"')
            if product.get('description'):
                # Store full description, properly escaped for YAML
                desc = product['description'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                front_matter_lines.append(f'        description: "{desc}"')
            if product.get('content'):
                front_matter_lines.append('        content: |')
                for line in product['content'].splitlines():
                    front_matter_lines.append(f'          {line}')
            if product.get('image'):
                front_matter_lines.append(f'        image: "{product["image"]}"')
            if product.get('price'):
                price = product['price'].replace('"', '\\"')
                front_matter_lines.append(f'        price: "{price}"')
    
    front_matter_lines.append("---")
    front_matter = '\n'.join(front_matter_lines)
    
    # Build markdown content with intro HTML preserved from the original source page
    content_lines = [front_matter]

    if intro_content.strip():
        content_lines.append("\n" + intro_content.strip() + "\n")

    return '\n'.join(content_lines)


def convert_html_file(input_file: str, output_dir: str, data_dir: str) -> None:
    """Convert a single HTML file to Hugo markdown with extracted data"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    extractor = ProductExtractor(html_content)
    main_heading = extractor.extract_main_heading()
    intro_content = extractor.extract_intro_content()
    sections = extractor.extract_sections()
    
    # Generate output filename
    base_name = Path(input_file).stem
    output_file = os.path.join(output_dir, f"_index.md")
    
    # Generate content
    content = generate_hugo_content(base_name, base_name.replace('_', ' '), main_heading, sections, intro_content)
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Write markdown content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Write extracted data as JSON in data directory for reference
    data_file = os.path.join(data_dir, f"{base_name}.json")
    os.makedirs(data_dir, exist_ok=True)
    data_to_save = {
        'title': base_name.replace('_', ' '),
        'main_heading': main_heading,
        'sections': sections
    }
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2)
    
    print(f"Converted {input_file} -> {output_file}")
    print(f"  Main heading: {main_heading}")
    print(f"  Sections: {len(sections)}")
    for sec in sections:
        print(f"    - {sec['sub_heading']}: {len(sec['products'])} products")

def main():
    source_dir = r"c:\Users\Geoff\PSP_Claude_Port\PerfSailingProd_www"
    output_base = r"c:\Users\Geoff\PSP_Claude_Port\PerfSailingProd2026\content"
    data_base = r"c:\Users\Geoff\PSP_Claude_Port\PerfSailingProd2026\data"
    
    # Find all Product_*.html and Parts_*.html files
    product_files = []
    parts_files = []
    
    for file in os.listdir(source_dir):
        if file.startswith("Products_") and file.endswith(".html"):
            product_files.append(os.path.join(source_dir, file))
        elif file.startswith("Parts_") and file.endswith(".html"):
            parts_files.append(os.path.join(source_dir, file))
    
    print(f"Found {len(product_files)} product files and {len(parts_files)} parts files\n")
    
    # Convert products
    print("Converting Product files:")
    for file in sorted(product_files):
        try:
            base_name = Path(file).stem
            output_dir = os.path.join(output_base, "products", base_name)
            data_dir = os.path.join(data_base, "products")
            convert_html_file(file, output_dir, data_dir)
        except Exception as e:
            print(f"  Error converting {file}: {e}")
            import traceback
            traceback.print_exc()
    
    # Convert parts
    print("\nConverting Parts files:")
    for file in sorted(parts_files):
        try:
            base_name = Path(file).stem
            output_dir = os.path.join(output_base, "parts", base_name)
            data_dir = os.path.join(data_base, "parts")
            convert_html_file(file, output_dir, data_dir)
        except Exception as e:
            print(f"  Error converting {file}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
