#!/usr/bin/env python3
"""
Chart.js markdown extension for rendering charts from YAML configuration.
Supports both HTML and PDF output formats.
"""

import yaml
import json
import uuid
import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


class ChartPreprocessor(Preprocessor):
    """Preprocessor to find and extract chart blocks."""
    
    def run(self, lines):
        """Process markdown lines to find chart blocks."""
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for chart block start
            if line.strip() == '```chart':
                # Find the end of the chart block
                chart_lines = []
                i += 1
                
                while i < len(lines) and lines[i].strip() != '```':
                    chart_lines.append(lines[i])
                    i += 1
                
                # Parse YAML config
                if chart_lines:
                    try:
                        chart_config = yaml.safe_load('\n'.join(chart_lines))
                        chart_id = f"chart_{uuid.uuid4().hex[:8]}"
                        
                        # Store chart config for later processing
                        if not hasattr(self.md, 'chart_configs'):
                            self.md.chart_configs = {}
                        self.md.chart_configs[chart_id] = chart_config
                        
                        # Replace with placeholder
                        new_lines.append(f'<div class="chart-placeholder" data-chart-id="{chart_id}"></div>')
                        
                    except yaml.YAMLError as e:
                        # If YAML parsing fails, include error message
                        new_lines.append(f'<div class="chart-error">Chart configuration error: {e}</div>')
                
            else:
                new_lines.append(line)
            
            i += 1
        
        return new_lines


class ChartPostprocessor(Postprocessor):
    """Postprocessor to replace chart placeholders with actual Chart.js code."""
    
    def run(self, text):
        """Replace chart placeholders with Chart.js HTML."""
        if not hasattr(self.md, 'chart_configs'):
            return text
        
        # Find all chart placeholders
        placeholder_pattern = r'<div class="chart-placeholder" data-chart-id="([^"]+)"></div>'
        
        def replace_chart(match):
            chart_id = match.group(1)
            if chart_id in self.md.chart_configs:
                config = self.md.chart_configs[chart_id]
                return self._generate_chart_html(chart_id, config)
            return match.group(0)
        
        return re.sub(placeholder_pattern, replace_chart, text)
    
    def _generate_chart_html(self, chart_id, config):
        """Generate Chart.js HTML for a chart configuration."""
        
        # Extract chart properties
        chart_type = config.get('type', 'bar')
        title = config.get('title', 'Chart')
        width = config.get('width', 800)
        height = config.get('height', 400)
        data = config.get('data', {})
        options = config.get('options', {})
        
        # Set default options
        default_options = {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'title': {
                    'display': True,
                    'text': title,
                    'font': {'size': 16, 'weight': 'bold'}
                },
                'legend': {
                    'display': True,
                    'position': 'top'
                }
            },
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'ticks': {
                        # double quote usage should not be changed to prevent breaking js
                        'callback': "function(value) { return typeof value === 'number' ? value.toLocaleString() : value; }"
                    }
                }
            }
        }
        
        # Merge user options with defaults
        merged_options = self._deep_merge(default_options, options)
        
        # Create Chart.js configuration
        chart_config = {
            'type': chart_type,
            'data': data,
            'options': merged_options
        }
        
        # Convert to JSON (handle callback functions)
        config_json = json.dumps(chart_config, indent=2)
        
        # Handle JavaScript callbacks (they need to be functions, not strings)
        config_json = re.sub(
            r'"function\(([^)]*)\)\s*{\s*([^}]+)\s*}"',
            r'function(\1) { \2 }',
            config_json
        )
        
        # Generate HTML
        html = f"""
<div class="chart-container" style="position: relative; width: 100%; height: {height}px; margin: 20px 0;">
    <canvas id="{chart_id}" width="{width}" height="{height}"></canvas>
</div>
<script>
(function() {{
    // Wait for Chart.js to load
    function initChart() {{
        if (typeof Chart === 'undefined') {{
            setTimeout(initChart, 100);
            return;
        }}
        
        const ctx = document.getElementById('{chart_id}');
        if (ctx && !ctx.chart) {{
            const config = {config_json};
            ctx.chart = new Chart(ctx, config);
        }}
    }}
    
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initChart);
    }} else {{
        initChart();
    }}
}})();
</script>
"""
        return html
    
    def _deep_merge(self, dict1, dict2):
        """Deep merge two dictionaries."""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result


class ChartExtension(Extension):
    """Chart.js extension for Python-Markdown."""
    
    def extendMarkdown(self, md):
        """Register the extension with markdown."""
        md.preprocessors.register(
            ChartPreprocessor(md), 'chart_preprocessor', 27
        )
        md.postprocessors.register(
            ChartPostprocessor(md), 'chart_postprocessor', 0
        )


def makeExtension(**kwargs):
    """Create extension instance."""
    return ChartExtension(**kwargs)
