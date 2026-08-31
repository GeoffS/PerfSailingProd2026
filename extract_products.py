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
    
    def parse_descriptive_block(self, block_html: str) -> Dict:
        """Parse a descriptive entry block (tables, complex content)"""
        product = {
            'type': 'descriptive',
            'heading': '',
            'content': block_html.strip(),
            'image': '',
            'imageWidth': '',
            'imageHeight': ''
        }
        
        # Try to extract an image from the descriptive block
        img_match = re.search(r'<img[^>]*src="([^"]*)"[^>]*width="(\d+)"[^>]*height="(\d+)"', block_html)
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
                product['image'] = src
                product['imageWidth'] = img_match.group(2)
                product['imageHeight'] = img_match.group(3)
        
        # Extract product name (productName class)
        name_match = re.search(r'<span class="productName">([^<]+)</span>', block_html)
        if name_match:
            product['name'] = name_match.group(1).strip()
        
        # Extract description - the paragraph after image
        desc_pattern = r'<div class="span-14[^>]*>.*?<p>(.*?)</p>'
        desc_match = re.search(desc_pattern, block_html, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            # Extract link if present
            link_match = re.search(r'<a href="([^"]+)">Click here', desc)
            if link_match:
                product['link'] = link_match.group(1)
            product['description'] = desc
        
        # Extract price
        price_pattern = r'<div class="span-2 right productPrice">([^<]+(?:<[^>]+>[^<]+</[^>]+>)*)'
        price_match = re.search(price_pattern, block_html, re.DOTALL)
        if price_match:
            price_html = price_match.group(1).strip()
            # Remove contact us div if present
            price_text = re.sub(r'<div class="ContactUsOrder".*?</div>', '', price_html, flags=re.DOTALL)
            product['price'] = price_text.strip()
        
        return product if (product['name'] or product['description']) else None

def generate_hugo_content(file_name: str, title: str, main_heading: str, sections: List[Dict]) -> str:
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
                # Escape for YAML
                desc = product['description'][:100].replace('"', '\\"').replace('\n', ' ')
                front_matter_lines.append(f'        description: "{desc}..."')
            if product.get('image'):
                front_matter_lines.append(f'        image: "{product["image"]}"')
            if product.get('price'):
                price = product['price'].replace('"', '\\"')
                front_matter_lines.append(f'        price: "{price}"')
    
    front_matter_lines.append("---")
    front_matter = '\n'.join(front_matter_lines)
    
    # Build markdown content with sections
    content_lines = [front_matter]
    
    if main_heading:
        content_lines.append(f"\n## {main_heading}\n")
    
    for section in sections:
        content_lines.append(f"\n### {section['sub_heading']}\n")
        
        for product in section['products']:
            if product.get('type') == 'descriptive':
                # For descriptive entries (tables, etc), note that the raw content is available
                content_lines.append("**Detailed Entry** (Table/Complex Content)\n")
            else:
                # Simple product entry summary
                if product.get('name'):
                    content_lines.append(f"- **{product['name']}**")
                if product.get('price'):
                    content_lines.append(f"  - Price: {product['price']}")
        
        content_lines.append("")
    
    return '\n'.join(content_lines)


def convert_html_file(input_file: str, output_dir: str, data_dir: str) -> None:
    """Convert a single HTML file to Hugo markdown with extracted data"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    extractor = ProductExtractor(html_content)
    main_heading = extractor.extract_main_heading()
    sections = extractor.extract_sections()
    
    # Generate output filename
    base_name = Path(input_file).stem
    output_file = os.path.join(output_dir, f"_index.md")
    
    # Generate content
    content = generate_hugo_content(base_name, base_name.replace('_', ' '), main_heading, sections)
    
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
