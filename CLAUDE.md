# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a research project analyzing fiscal flows in Cuyahoga County, Ohio, examining the relationship between suburban municipalities and Cleveland regarding revenue generation and public investment patterns. The project publishes automatically to GitHub Pages with:

- A comprehensive research report (`cuyahoga-fiscal-report.md`) - **SOURCE OF TRUTH** for all content
- An interactive web application (`fiscal-flows-webapp.html`) that visualizes the research findings
- Automated conversion to HTML with table of contents and anchor links
- PDF generation for download
- GitHub Pages deployment via GitHub Actions

## Content Management Strategy

**IMPORTANT**: `cuyahoga-fiscal-report.md` is the single source of truth for all report content. All exports (HTML, PDF) are generated from this markdown file.

### Making Content Changes
1. Edit only the `cuyahoga-fiscal-report.md` file
2. Commit changes to trigger automatic regeneration
3. GitHub Actions will automatically:
   - Convert markdown to HTML with TOC and anchor links
   - Generate PDF version
   - Update GitHub Pages site
   - Update webapp footer links to point to correct sections

## Development Environment

### Local Development
- Open `fiscal-flows-webapp.html` directly in a web browser
- For testing report conversions: `python scripts/convert_to_html.py` and `python scripts/convert_to_pdf.py`
- No server required for basic development

### Dependencies
- Python 3.8+ for conversion scripts
- See `requirements.txt` for Python dependencies (markdown, weasyprint, etc.)
- Chart.js (v4.4.0) CDN for data visualization

### Key Technologies
- Vanilla HTML5, CSS3, and JavaScript for webapp
- Python for markdown conversion scripts
- GitHub Actions for automated publishing
- GitHub Pages for hosting

## GitHub Pages Publishing Workflow

### Automated Publishing Process
1. **Trigger**: Push to main branch or manual workflow dispatch
2. **Content Generation**:
   - `scripts/convert_to_html.py` converts markdown to HTML with TOC and anchor links
   - `scripts/convert_to_pdf.py` generates PDF version for download
   - Updates webapp footer links to point to generated report sections
3. **Deployment**: GitHub Actions publishes to `gh-pages` branch
4. **Result**: Live site at `https://[username].github.io/suburban-exploitation-paper/`

### File Structure After Build
```
/
├── index.html (webapp - landing page)
├── report.html (generated from markdown with TOC)
├── report.pdf (generated PDF download)
├── assets/ (any additional resources)
└── cuyahoga-fiscal-report.md (source file)
```

### GitHub Actions Commands
- Test conversion scripts locally: `python scripts/convert_to_html.py`
- Manual workflow trigger: Available in GitHub Actions tab
- View build logs: Check Actions tab for detailed output

## Code Architecture

### Web Application Structure (`fiscal-flows-webapp.html`)
- **Single-file architecture**: All HTML, CSS, and JavaScript in one file
- **Tab-based interface**: 5 main sections (Revenue, Investment, Employment, Transit, Solutions)
- **Interactive elements**: Chart.js visualizations and a multiplier calculator slider
- **Responsive design**: CSS Grid and Flexbox for layout
- **Footer links**: Automatically updated to point to generated report sections

### Report Generation (`scripts/`)
- **`convert_to_html.py`**: Converts markdown to HTML with table of contents and anchor links
- **`convert_to_pdf.py`**: Generates PDF version using WeasyPrint
- **Dependencies**: markdown, markdown-extensions, weasyprint, python-markdown-toc

### Chart Types and Data
- Bar charts for municipal tax rates and employment distribution
- Pie/doughnut charts for investment and property tax distribution
- Line charts for ridership trends and TIF projections
- Radar chart for infrastructure benefits
- Interactive slider for economic multiplier calculations

### Styling Approach
- **CSS custom properties**: Gradient backgrounds and consistent color scheme
- **Animation effects**: Pulse animations and hover transitions
- **Component-based CSS**: Modular classes for cards, charts, and interactive elements

## Content Updates

### Adding New Research Data
1. **Update markdown file**: Edit `cuyahoga-fiscal-report.md` with new findings
2. **Update visualizations**: Modify chart data in `fiscal-flows-webapp.html` if needed
3. **Commit changes**: Automatic regeneration will update all exports
4. **Verify**: Check GitHub Pages site for updated content

### Adding New Sections
1. **Add to markdown**: Use proper heading structure for TOC generation
2. **Update footer links**: Scripts will automatically generate correct anchor links
3. **Test locally**: Run conversion scripts to verify output

## Research Context

This codebase supports academic research on fiscal federalism and regional economic development. When making changes:
- **Source of truth**: Always edit the markdown file first
- **Maintain accuracy**: Preserve data integrity across all formats
- **Scholarly tone**: Keep academic rigor in all generated outputs
- **Citations**: Ensure references are preserved in all export formats