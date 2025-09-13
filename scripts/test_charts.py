#!/usr/bin/env python3
"""
Test script for the Chart.js markdown extension.
"""

import markdown
from pathlib import Path
from .chart_extension import ChartExtension

def test_chart_extension():
    """Test the chart extension with a simple markdown file."""
    
    # Read test markdown
    test_file = Path('test_chart.md')
    if not test_file.exists():
        print("❌ Test file not found")
        return False
    
    content = test_file.read_text()
    
    # Configure markdown with chart extension
    md = markdown.Markdown(
        extensions=[
            'toc',
            'tables',
            ChartExtension()
        ]
    )
    
    # Convert to HTML
    html = md.convert(content)
    
    # Write output for inspection
    output_file = Path('test_chart_output.html')
    
    # Create complete HTML document
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Chart Extension Test</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .chart-container {{ 
            background: white; 
            border: 1px solid #ddd; 
            border-radius: 8px; 
            padding: 20px; 
            margin: 20px 0; 
        }}
        .chart-error {{ 
            background: #fee; 
            border: 1px solid #fcc; 
            color: #c33; 
            padding: 15px; 
            border-radius: 5px; 
        }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    output_file.write_text(full_html)
    
    # Check if charts were processed
    if '<canvas id="chart_' in html and 'new Chart(' in html:
        print("✅ Chart extension test passed!")
        print(f"📄 Output written to: {output_file}")
        return True
    else:
        print("❌ Chart extension test failed!")
        print("❌ No chart elements found in output")
        return False

if __name__ == '__main__':
    test_chart_extension()