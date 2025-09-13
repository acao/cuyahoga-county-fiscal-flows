#!/usr/bin/env python3
"""
Convert the Cuyahoga fiscal report markdown to HTML with table of contents and anchor links.
Uses Jinja2 templates and unified styling.
"""

import re
import markdown
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def load_base_styles():
    """Load the base CSS styles."""
    styles_file = Path(__file__).parent / 'templates' / 'base_styles.css'
    return styles_file.read_text(encoding='utf-8')

def enhance_toc_with_depth_classes(toc_html):
    """Add depth classes to TOC for better styling."""
    # First, add toc-link class to all links
    toc_html = re.sub(r'<a href="#([^"]*)"([^>]*)>([^<]*)</a>', r'<a href="#\1"\2 class="toc-link">\3</a>', toc_html)
    
    # Track nesting level by counting ul depth
    lines = toc_html.split('\n')
    enhanced_lines = []
    ul_depth = 0
    
    for line in lines:
        # Update depth before processing the line
        ul_opens = line.count('<ul>')
        ul_closes = line.count('</ul>')
        
        # Process li tags with current depth
        if '<li>' in line:
            # Determine depth class based on current ul nesting level
            if ul_depth == 0:
                depth_class = 'toc-h1'
            elif ul_depth == 1:
                depth_class = 'toc-h2'
            elif ul_depth == 2:
                depth_class = 'toc-h3'
            else:
                depth_class = 'toc-h4'
            
            # Replace all li tags in this line with the appropriate class
            line = re.sub(r'<li>', f'<li class="{depth_class}">', line)
        
        # Update depth after processing
        ul_depth += ul_opens - ul_closes
        enhanced_lines.append(line)
    
    return '\n'.join(enhanced_lines)

def convert_markdown_to_html():
    """Convert the markdown report to HTML using Jinja2 templates."""
    
    # Ensure output directory exists
    dist_dir = Path('dist')
    dist_dir.mkdir(exist_ok=True)
    
    # Read the source markdown
    md_file = Path('cuyahoga-fiscal-report.md')
    if not md_file.exists():
        raise FileNotFoundError(f"Source file {md_file} not found")
    
    content = md_file.read_text(encoding='utf-8')
    
    # Configure markdown with extensions
    md = markdown.Markdown(
        extensions=[
            'toc',
            'tables',
            'fenced_code',
            'footnotes',
            'attr_list',
            'def_list',
            'abbr',
            'nl2br'  # Convert single newlines to <br> tags (GFM-style)
        ],
        extension_configs={
            'toc': {
                'anchorlink': True,
                'title': 'Table of Contents',
                'toc_depth': 4,
                'permalink': True
            }
        }
    )
    
    # Convert markdown to HTML
    html_content = md.convert(content)
    
    # Get and enhance the table of contents
    toc_html = enhance_toc_with_depth_classes(md.toc)
    
    # Load base styles
    base_styles = load_base_styles()
    
    # Setup Jinja2 environment
    template_dir = Path(__file__).parent / 'templates'
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report.html')
    
    # Known anchor IDs for navigation
    methodology_anchor = 'methodology-and-data-sources-comprehensive-research-framework'
    conclusion_anchor = '8-conclusion'
    
    # Render the template
    rendered_html = template.render(
        title='Suburban Exploitation or Urban Drain?',
        subtitle='Fiscal Flows in Cuyahoga County - Full Research Report',
        base_styles=base_styles,
        content=html_content,
        toc=toc_html,
        methodology_anchor=methodology_anchor,
        conclusion_anchor=conclusion_anchor
    )
    
    # Write the HTML file
    output_file = dist_dir / 'report.html'
    output_file.write_text(rendered_html, encoding='utf-8')
    
    print(f"✅ Generated HTML report: {output_file}")
    
    # Also copy the source markdown to dist for reference
    (dist_dir / 'cuyahoga-fiscal-report.md').write_text(content, encoding='utf-8')
    
    # Return info about generated content
    toc_count = len(md.toc_tokens) if hasattr(md, 'toc_tokens') else 0
    return output_file, toc_count

if __name__ == '__main__':
    try:
        html_file, toc_count = convert_markdown_to_html()
        print(f"HTML conversion completed successfully: {html_file}")
        print(f"Generated table of contents with {toc_count} entries")
    except Exception as e:
        print(f"❌ Error converting markdown to HTML: {e}")
        exit(1)