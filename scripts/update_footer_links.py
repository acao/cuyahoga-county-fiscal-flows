#!/usr/bin/env python3
"""
Update the webapp footer links to point to the correct sections in the generated report.
"""

import re
import markdown
from pathlib import Path

def extract_section_anchors():
    """Extract section anchors from the markdown file."""
    
    # Read the source markdown
    md_file = Path('cuyahoga-fiscal-report.md')
    if not md_file.exists():
        raise FileNotFoundError(f"Source file {md_file} not found")
    
    content = md_file.read_text(encoding='utf-8')
    
    # Configure markdown with TOC extension
    md = markdown.Markdown(
        extensions=['toc'],
        extension_configs={
            'toc': {
                'anchorlink': True,
                'title': 'Table of Contents',
                'toc_depth': 4,
                'permalink': True
            }
        }
    )
    
    # Convert to get TOC tokens
    md.convert(content)
    
    # Extract anchor mappings
    anchors = {}
    for token in md.toc_tokens:
        level = token['level']
        anchor = token['id']
        title = token['name']
        
        # Map common section names to anchors
        if 'methodology' in title.lower():
            anchors['methodology'] = anchor
        elif 'conclusion' in title.lower():
            anchors['conclusion'] = anchor
        elif 'data sources' in title.lower():
            anchors['data-sources'] = anchor
        elif 'policy' in title.lower() and 'recommendation' in title.lower():
            anchors['solutions'] = anchor
        elif 'appendix' in title.lower():
            if 'appendix a' in title.lower():
                anchors['appendix-a'] = anchor
            elif 'appendix b' in title.lower():
                anchors['appendix-b'] = anchor
    
    return anchors

def update_webapp_footer():
    """Update the webapp HTML file with correct footer links."""
    
    # Get section anchors
    anchors = extract_section_anchors()
    
    # Read the webapp HTML
    webapp_file = Path('index.html')
    if not webapp_file.exists():
        raise FileNotFoundError(f"Webapp file {webapp_file} not found")
    
    content = webapp_file.read_text(encoding='utf-8')
    
    # Define the new footer links
    footer_links_html = f'''
            <div class="footer-links">
                <a href="report.html">Download Full Report</a>
                <a href="report.html#{anchors.get('methodology', 'methodology-and-data-sources-comprehensive-research-framework')}">View Methodology</a>
                <a href="report.html#{anchors.get('appendix-b', 'appendix-b-works-cited')}">Data Sources</a>
                <a href="mailto:contact@research.example.com">Contact Researchers</a>
            </div>'''
    
    # Update the footer links section
    footer_pattern = r'<div class="footer-links">.*?</div>'
    updated_content = re.sub(
        footer_pattern, 
        footer_links_html.strip(), 
        content, 
        flags=re.DOTALL
    )
    
    # Also update the navigation links in the header
    nav_links_pattern = r'(<a href="https://claude\.ai/public/artifacts/[^"]*">Download Full Report</a>)'
    updated_content = re.sub(
        nav_links_pattern,
        '<a href="report.html">Download Full Report</a>',
        updated_content
    )
    
    # Ensure output directory exists and copy webapp
    dist_dir = Path('dist')
    dist_dir.mkdir(exist_ok=True)
    
    # Write updated webapp as index.html in dist
    output_file = dist_dir / 'index.html'
    output_file.write_text(updated_content, encoding='utf-8')
    
    print(f"✅ Updated webapp with correct footer links: {output_file}")
    print(f"🔗 Found anchors: {list(anchors.keys())}")
    
    return output_file, anchors

if __name__ == '__main__':
    try:
        output_file, anchors = update_webapp_footer()
        print(f"Footer links updated successfully: {output_file}")
        print(f"Generated {len(anchors)} anchor links")
    except Exception as e:
        print(f"❌ Error updating footer links: {e}")
        exit(1)