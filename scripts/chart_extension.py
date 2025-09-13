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
                        'callback': 'function(value) { return typeof value === "number" ? value.toLocaleString() : value; }'
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


# Chart.js templates for common chart types
CHART_TEMPLATES = {
    'revenue_comparison': {
        'type': 'bar',
        'title': 'Municipal Revenue Comparison',
        'width': 800,
        'height': 400,
        'data': {
            'labels': ['Cleveland', 'Suburban Average'],
            'datasets': [{
                'label': 'Municipal Income Tax ($ millions)',
                'data': [538.5, 45.2],
                'backgroundColor': ['#667eea', '#764ba2']
            }]
        },
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {
                        'display': True,
                        'text': 'Revenue ($ millions)'
                    }
                }
            }
        }
    },
    
    'property_tax_distribution': {
        'type': 'doughnut',
        'title': 'Cleveland Property Tax Distribution',
        'width': 600,
        'height': 400,
        'data': {
            'labels': ['Cleveland Schools (67.6%)', 'County (16.8%)', 'City (9.3%)', 'Library (6.4%)'],
            'datasets': [{
                'data': [67.551, 16.782, 9.254, 6.413],
                'backgroundColor': ['#667eea', '#764ba2', '#f093fb', '#f5576c']
            }]
        },
        'options': {
            'plugins': {
                'legend': {
                    'position': 'bottom'
                }
            }
        }
    },
    
    'economic_development_investment': {
        'type': 'bar',
        'title': 'County Economic Development Investment by Region',
        'width': 800,
        'height': 400,
        'data': {
            'labels': ['Cleveland', 'Inner Ring Suburbs', 'Outer Ring Suburbs'],
            'datasets': [{
                'label': 'Investment ($ millions)',
                'data': [89.2, 33.1, 21.7],
                'backgroundColor': ['#667eea', '#764ba2', '#f093fb']
            }]
        },
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {
                        'display': True,
                        'text': 'Investment ($ millions)'
                    }
                },
                'x': {
                    'title': {
                        'display': True,
                        'text': 'Region'
                    }
                }
            }
        }
    },
    
    'employment_flows': {
        'type': 'line',
        'title': 'Regional Employment Flow to Cleveland',
        'width': 800,
        'height': 400,
        'data': {
            'labels': ['Healthcare', 'Downtown Core', 'Universities', 'Total'],
            'datasets': [{
                'label': 'Total Employment',
                'data': [72000, 127000, 15200, 214200],
                'borderColor': '#667eea',
                'backgroundColor': 'rgba(102, 126, 234, 0.1)',
                'tension': 0.4
            }, {
                'label': 'Suburban Residents',
                'data': [51120, 99060, 9576, 147000],
                'borderColor': '#764ba2',
                'backgroundColor': 'rgba(118, 75, 162, 0.1)',
                'tension': 0.4
            }]
        },
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {
                        'display': True,
                        'text': 'Number of Jobs'
                    }
                }
            }
        }
    }
}


def get_chart_template(template_name, **kwargs):
    """Get a chart template with optional parameter overrides."""
    if template_name not in CHART_TEMPLATES:
        raise ValueError(f"Unknown chart template: {template_name}")
    
    template = CHART_TEMPLATES[template_name].copy()
    
    # Apply any overrides
    for key, value in kwargs.items():
        if key in template:
            template[key] = value
    
    return template