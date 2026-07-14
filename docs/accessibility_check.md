# Accessibility and Low-Bandwidth Check

## Current checks

| Area | Current implementation |
|---|---|
| Font size | Responsive headings and readable body text |
| Contrast | Dark text on light cards; high-contrast header and active tab |
| Mobile layout | KPI, chart, alert, and deployment grids collapse for smaller screens |
| Horizontal navigation | Tabs can scroll when the viewport is narrow |
| Non-colour cues | Risk labels use text as well as colour |
| Chart semantics | SVG charts include image roles and accessible labels |
| Images | Architecture diagrams have alternative text |
| Status feedback | API and action feedback use visible text |
| Animation | Limited to short toast transitions |
| Low bandwidth | No external CDN, font, analytics, or large frontend framework |
| Local operation | Dashboard and evidence can run on an institutional LAN |
| Offline edge behaviour | Readings buffer locally and retry after connectivity returns |

## Known gaps

- charts do not yet expose full tabular alternatives for every data point;
- keyboard focus styling should be strengthened before production;
- screen-reader testing has not been completed;
- the dashboard is currently English-only;
- a formal accessibility review with target users has not been completed.

## Production actions

1. Add visible `:focus` styles and verify full keyboard navigation.
2. Add accessible tables or downloadable CSV for chart data.
3. Test with Windows Narrator or NVDA.
4. Test at 200% zoom and common mobile widths.
5. Confirm colour contrast with an automated checker.
6. Add plain-language help and local-language support where user need is confirmed.
