#!/usr/bin/env python3
"""
Convert the Cuyahoga fiscal report markdown to HTML with table of contents and anchor links.
"""

import re
import markdown
from pathlib import Path

def create_html_template():
    """Create the HTML template for the report."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Suburban Exploitation or Urban Drain? - Full Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .navigation {
            background: #667eea;
            padding: 20px 40px;
            text-align: center;
        }
        
        .navigation a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            padding: 10px 20px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        
        .navigation a:hover {
            background-color: rgba(255,255,255,0.2);
        }
        
        .content {
            display: flex;
            min-height: 80vh;
        }
        
        .sidebar {
            width: 300px;
            background: #f1f3f5;
            padding: 30px 20px;
            border-right: 1px solid #dee2e6;
            position: sticky;
            top: 0;
            height: fit-content;
            max-height: 100vh;
            overflow-y: auto;
        }
        
        .sidebar h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        
        .toc {
            list-style: none;
        }
        
        .toc li {
            margin: 8px 0;
        }
        
        .toc a {
            color: #495057;
            text-decoration: none;
            font-size: 0.9em;
            line-height: 1.4;
            display: block;
            padding: 5px 0;
            border-left: 3px solid transparent;
            padding-left: 10px;
            transition: all 0.3s;
        }
        
        .toc a:hover {
            color: #667eea;
            border-left-color: #667eea;
            padding-left: 15px;
        }
        
        .toc .toc-h2 {
            font-weight: 600;
        }
        
        .toc .toc-h3 {
            padding-left: 20px;
            font-size: 0.85em;
        }
        
        .toc .toc-h4 {
            padding-left: 30px;
            font-size: 0.8em;
            color: #6c757d;
        }
        
        .main-content {
            flex: 1;
            padding: 40px;
            max-width: calc(100% - 300px);
        }
        
        .main-content h1 {
            color: #2c3e50;
            font-size: 2.2em;
            margin: 40px 0 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        .main-content h2 {
            color: #2c3e50;
            font-size: 1.8em;
            margin: 35px 0 15px;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }
        
        .main-content h3 {
            color: #34495e;
            font-size: 1.4em;
            margin: 25px 0 10px;
        }
        
        .main-content h4 {
            color: #495057;
            font-size: 1.2em;
            margin: 20px 0 10px;
        }
        
        .main-content p {
            margin: 15px 0;
            text-align: justify;
        }
        
        .main-content ul, .main-content ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        
        .main-content li {
            margin: 8px 0;
        }
        
        .main-content blockquote {
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            font-style: italic;
        }
        
        .main-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .main-content table th,
        .main-content table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        
        .main-content table th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        
        .main-content table tr:hover {
            background: #f8f9fa;
        }
        
        .main-content code {
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .main-content pre {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid #dee2e6;
        }
        
        .main-content strong {
            color: #2c3e50;
        }
        
        .main-content a {
            color: #667eea;
            text-decoration: none;
        }
        
        .main-content a:hover {
            text-decoration: underline;
        }
        
        .footer {
            background: #2c3e50;
            color: white;
            padding: 30px 40px;
            text-align: center;
        }
        
        .footer-links {
            margin-top: 15px;
        }
        
        .footer-links a {
            color: #667eea;
            text-decoration: none;
            margin: 0 15px;
            transition: color 0.3s;
        }
        
        .footer-links a:hover {
            color: #764ba2;
        }
        
        .print-only {
            display: none;
        }
        
        @media print {
            .sidebar, .navigation {
                display: none;
            }
            
            .main-content {
                max-width: 100%;
                padding: 20px;
            }
            
            .print-only {
                display: block;
            }
            
            .container {
                box-shadow: none;
            }
        }
        
        @media (max-width: 768px) {
            .content {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                position: relative;
                max-height: none;
            }
            
            .main-content {
                max-width: 100%;
                padding: 20px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
            
            .navigation a {
                display: block;
                margin: 5px 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Suburban Exploitation or Urban Drain?</h1>
            <div class="subtitle">Fiscal Flows in Cuyahoga County - Full Research Report</div>
        </div>
        
        <div class="navigation">
            <a href="index.html">Interactive Dashboard</a>
            <a href="report.pdf">Download PDF</a>
            <a href="#methodology">Methodology</a>
            <a href="#conclusion">Conclusion</a>
        </div>
        
        <div class="content">
            <div class="sidebar">
                <h3>Table of Contents</h3>
                {{ toc }}
            </div>
            
            <div class="main-content">
                {{ content }}
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 Cuyahoga County Fiscal Flows Research</p>
            <div class="footer-links">
                <a href="index.html">Interactive Dashboard</a>
                <a href="report.pdf">Download PDF</a>
                <a href="#methodology">Methodology</a>
                <a href="mailto:contact@research.example.com">Contact Researchers</a>
            </div>
        </div>
    </div>
</body>
</html>"""

def create_anchor_slug(text):
    """Create URL-friendly anchor from heading text."""
    # Remove markdown formatting
    text = re.sub(r'[*_`]', '', text)
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def convert_markdown_to_html():
    """Convert the markdown report to HTML with TOC and anchors."""
    
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
            'abbr'
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
    
    # Get the table of contents
    toc_html = md.toc
    
    # Create the full HTML document
    template = create_html_template()
    full_html = template.replace('{{ content }}', html_content)
    full_html = full_html.replace('{{ toc }}', toc_html)
    
    # Write the HTML file
    output_file = dist_dir / 'report.html'
    output_file.write_text(full_html, encoding='utf-8')
    
    print(f"✅ Generated HTML report: {output_file}")
    
    # Also copy the source markdown to dist for reference
    (dist_dir / 'cuyahoga-fiscal-report.md').write_text(content, encoding='utf-8')
    
    return output_file, md.toc_tokens

if __name__ == '__main__':
    try:
        html_file, toc_tokens = convert_markdown_to_html()
        print(f"HTML conversion completed successfully: {html_file}")
        print(f"Generated {len(toc_tokens)} table of contents entries")
    except Exception as e:
        print(f"❌ Error converting markdown to HTML: {e}")
        exit(1)