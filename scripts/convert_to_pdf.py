#!/usr/bin/env python3
"""
Convert the Cuyahoga fiscal report markdown to PDF for download.
"""

import markdown
from pathlib import Path
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def create_pdf_css():
    """Create CSS specifically for PDF output."""
    return """
        @page {
            size: A4;
            margin: 1in;
            @top-center {
                content: "Suburban Exploitation or Urban Drain? - Fiscal Flows in Cuyahoga County";
                font-size: 10pt;
                color: #666;
            }
            @bottom-center {
                content: "Page " counter(page);
                font-size: 10pt;
                color: #666;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
        }
        
        .title-page {
            page-break-after: always;
            text-align: center;
            padding-top: 200px;
        }
        
        .title-page h1 {
            font-size: 32pt;
            margin-bottom: 30px;
            color: #2c3e50;
            line-height: 1.2;
        }
        
        .title-page .subtitle {
            font-size: 18pt;
            margin-bottom: 40px;
            color: #666;
            font-style: italic;
        }
        
        .title-page .meta {
            font-size: 12pt;
            color: #666;
            margin-top: 60px;
        }
        
        .toc {
            page-break-before: always;
            page-break-after: always;
        }
        
        .toc h2 {
            font-size: 20pt;
            margin-bottom: 30px;
            color: #2c3e50;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 10px;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 8px 0;
            padding-left: 0;
        }
        
        .toc a {
            text-decoration: none;
            color: #333;
            border-bottom: 1px dotted #ccc;
        }
        
        .toc .toc-h1 {
            font-weight: bold;
            font-size: 12pt;
            margin-top: 15px;
        }
        
        .toc .toc-h2 {
            font-weight: 600;
            margin-left: 15px;
        }
        
        .toc .toc-h3 {
            margin-left: 30px;
            font-size: 10pt;
        }
        
        .toc .toc-h4 {
            margin-left: 45px;
            font-size: 9pt;
            color: #666;
        }
        
        h1 {
            font-size: 22pt;
            margin: 40px 0 20px;
            color: #2c3e50;
            page-break-before: always;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 10px;
        }
        
        h1:first-of-type {
            page-break-before: auto;
        }
        
        h2 {
            font-size: 18pt;
            margin: 30px 0 15px;
            color: #2c3e50;
            page-break-after: avoid;
        }
        
        h3 {
            font-size: 14pt;
            margin: 25px 0 10px;
            color: #34495e;
            page-break-after: avoid;
        }
        
        h4 {
            font-size: 12pt;
            margin: 20px 0 10px;
            color: #495057;
            page-break-after: avoid;
        }
        
        p {
            margin: 12px 0;
            text-align: justify;
            orphans: 2;
            widows: 2;
        }
        
        ul, ol {
            margin: 12px 0;
            padding-left: 25px;
        }
        
        li {
            margin: 6px 0;
            page-break-inside: avoid;
        }
        
        blockquote {
            background: #f8f9fa;
            border-left: 4px solid #2c3e50;
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
            page-break-inside: avoid;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            page-break-inside: avoid;
        }
        
        table th,
        table td {
            padding: 8px 10px;
            text-align: left;
            border: 1px solid #dee2e6;
            font-size: 10pt;
        }
        
        table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        
        code {
            background: #f8f9fa;
            padding: 2px 4px;
            border-radius: 2px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }
        
        pre {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            overflow-wrap: break-word;
            margin: 15px 0;
            border: 1px solid #dee2e6;
            page-break-inside: avoid;
        }
        
        pre code {
            background: none;
            padding: 0;
        }
        
        strong {
            color: #2c3e50;
        }
        
        a {
            color: #2c3e50;
            text-decoration: underline;
        }
        
        .footnote {
            font-size: 9pt;
            color: #666;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        /* Appendix styling */
        .appendix h1 {
            border-bottom: 2px solid #666;
            color: #666;
        }
        
        .appendix h2 {
            color: #666;
        }
        
        /* Citation styling */
        .citation {
            font-size: 9pt;
            color: #666;
            margin: 5px 0;
        }
    """

def create_title_page():
    """Create a title page for the PDF."""
    return """
    <div class="title-page">
        <h1>Suburban Exploitation or Urban Drain?</h1>
        <div class="subtitle">Fiscal Flows in Cuyahoga County</div>
        <div class="meta">
            <p>A Comprehensive Analysis of Regional Economic Development and Municipal Finance</p>
            <p style="margin-top: 40px;">Generated: {date}</p>
            <p>Source: https://github.com/[username]/suburban-exploitation-paper</p>
        </div>
    </div>
    """.format(date="2024")

def process_markdown_for_pdf(content):
    """Process markdown content for better PDF formatting."""
    # Add page breaks before major sections
    content = content.replace('## 1. The Fiscal Federalism Debate', 
                            '<div class="page-break"></div>\n\n## 1. The Fiscal Federalism Debate')
    content = content.replace('## 2. Revenue Generation Analysis', 
                            '<div class="page-break"></div>\n\n## 2. Revenue Generation Analysis')
    content = content.replace('## 3. Public Investment Distribution Analysis', 
                            '<div class="page-break"></div>\n\n## 3. Public Investment Distribution Analysis')
    content = content.replace('## 4. Cleveland\'s Strategic Response', 
                            '<div class="page-break"></div>\n\n## 4. Cleveland\'s Strategic Response')
    content = content.replace('## 5. Regional Economic Development', 
                            '<div class="page-break"></div>\n\n## 5. Regional Economic Development')
    content = content.replace('## 6. Policy Implications and Recommendations', 
                            '<div class="page-break"></div>\n\n## 6. Policy Implications and Recommendations')
    content = content.replace('## 7. Methodology and Data Sources', 
                            '<div class="page-break"></div>\n\n## 7. Methodology and Data Sources')
    content = content.replace('## 8. Conclusion', 
                            '<div class="page-break"></div>\n\n## 8. Conclusion')
    content = content.replace('## Appendix A', 
                            '<div class="page-break appendix"></div>\n\n## Appendix A')
    content = content.replace('## Appendix B', 
                            '<div class="page-break appendix"></div>\n\n## Appendix B')
    
    return content

def convert_markdown_to_pdf():
    """Convert the markdown report to PDF."""
    
    # Ensure output directory exists
    dist_dir = Path('dist')
    dist_dir.mkdir(exist_ok=True)
    
    # Read the source markdown
    md_file = Path('cuyahoga-fiscal-report.md')
    if not md_file.exists():
        raise FileNotFoundError(f"Source file {md_file} not found")
    
    content = md_file.read_text(encoding='utf-8')
    
    # Process content for better PDF formatting
    content = process_markdown_for_pdf(content)
    
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
                'anchorlink': False,  # Don't need anchor links in PDF
                'title': 'Table of Contents',
                'toc_depth': 4,
                'permalink': False
            }
        }
    )
    
    # Convert markdown to HTML
    html_content = md.convert(content)
    
    # Create the complete HTML document for PDF
    title_page = create_title_page()
    toc_html = f'<div class="toc"><h2>Table of Contents</h2>{md.toc}</div>'
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Suburban Exploitation or Urban Drain? - Full Report</title>
    </head>
    <body>
        {title_page}
        {toc_html}
        {html_content}
    </body>
    </html>
    """
    
    # Create CSS
    css = CSS(string=create_pdf_css())
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Generate PDF
    output_file = dist_dir / 'report.pdf'
    html_doc = HTML(string=full_html)
    html_doc.write_pdf(
        output_file,
        stylesheets=[css],
        font_config=font_config
    )
    
    print(f"✅ Generated PDF report: {output_file}")
    return output_file

if __name__ == '__main__':
    try:
        pdf_file = convert_markdown_to_pdf()
        print(f"PDF conversion completed successfully: {pdf_file}")
    except Exception as e:
        print(f"❌ Error converting markdown to PDF: {e}")
        exit(1)