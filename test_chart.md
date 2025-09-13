# Test Chart Extension

This is a test of the Chart.js markdown extension.

## Revenue Comparison Chart

```chart
type: bar
title: Municipal Revenue Comparison
width: 800
height: 400
data:
  labels: 
    - Cleveland
    - Suburban Average
  datasets:
    - label: Municipal Income Tax ($ millions)
      data: [538.5, 45.2]
      backgroundColor: 
        - "#667eea"
        - "#764ba2"
options:
  scales:
    y:
      beginAtZero: true
      title:
        display: true
        text: Revenue ($ millions)
```

## Property Tax Distribution

```chart
type: doughnut
title: Cleveland Property Tax Distribution
width: 600
height: 400
data:
  labels:
    - Cleveland Schools (67.6%)
    - County (16.8%)
    - City (9.3%)
    - Library (6.4%)
  datasets:
    - data: [67.551, 16.782, 9.254, 6.413]
      backgroundColor:
        - "#667eea"
        - "#764ba2"
        - "#f093fb"
        - "#f5576c"
options:
  plugins:
    legend:
      position: bottom
```

This demonstrates the chart extension working with YAML configuration.