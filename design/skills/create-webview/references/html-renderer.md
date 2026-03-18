# HTML Renderer Reference

Detailed guide for Phase 3 — building the dynamic HTML slide renderer from JSON data.

## Architecture

The renderer follows a function-array pipeline pattern:

```
fetch('data.json') → parse → [renderCover, renderSummary, ...renderProjects, renderClosing] → DOM
```

Each slide type is an independent function that receives the full data object and returns either:
- An `HTMLElement` (single slide)
- An `Array<HTMLElement>` (multi-slide section, spread into pipeline)
- `null` (skip this slide — data not available)

### Function Array Pattern

```javascript
const slides = [
    renderCover,
    renderSummary,
    renderMetrics,
    ...renderProjects(data),  // returns array, spread into pipeline
    renderTimeline,
    renderClosing,
];

slides.forEach(fn => {
    const result = typeof fn === 'function' ? fn(data) : fn;
    if (result === null || result === undefined) return;
    if (Array.isArray(result)) {
        result.forEach(el => container.appendChild(el));
    } else {
        container.appendChild(result);
    }
});
```

### Null Guard Pattern

Every renderer must handle missing or empty data gracefully:

```javascript
function renderTimeline(data) {
    if (!data.timeline || !data.timeline.length) return null;
    // ... build slide
}
```

## Helper Functions

### el(tag, attrs, children)

DOM factory function. The backbone of all slide construction:

```javascript
function el(tag, attrs = {}, children = []) {
    const element = document.createElement(tag);
    Object.entries(attrs).forEach(([key, value]) => {
        if (key === 'className') element.className = value;
        else if (key === 'innerHTML') element.innerHTML = value;
        else if (key === 'textContent') element.textContent = value;
        else if (key === 'style' && typeof value === 'object') {
            Object.assign(element.style, value);
        } else {
            element.setAttribute(key, value);
        }
    });
    if (typeof children === 'string') {
        element.innerHTML = children;
    } else if (Array.isArray(children)) {
        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else if (child) {
                element.appendChild(child);
            }
        });
    }
    return element;
}
```

### slide(opts)

Slide container factory:

```javascript
let slideCount = 0;

function slide(opts = {}) {
    slideCount++;
    const num = String(slideCount).padStart(2, '0');
    const classes = ['slide', ...(opts.classes || [])].join(' ');
    const s = el('div', { className: classes });
    if (!opts.noNumber) {
        s.appendChild(el('div', { className: 'slide-number', textContent: num }));
    }
    return s;
}
```

### header(tag, title, subtitle)

Slide header with tag badge, title, and optional subtitle:

```javascript
function header(tag, title, subtitle) {
    return `
        <span class="tag">${tag}</span>
        <h2 class="slide-title">${title}</h2>
        ${subtitle ? `<p class="slide-subtitle">${subtitle}</p>` : ''}
    `;
}
```

### nextSlide()

Zero-padded slide counter (useful for tracking outside the slide function):

```javascript
function nextSlide() {
    slideCount++;
    return String(slideCount).padStart(2, '0');
}
```

## Component Patterns

### Metric Cards

Large KPI numbers with labels. Use for summary slides:

```javascript
function renderMetrics(data) {
    const s = slide({ classes: ['metrics-slide'] });
    s.innerHTML = header('Overview', 'Key Metrics');

    const grid = el('div', { className: 'metrics-grid' });

    const metrics = [
        { value: data.summary.total_items, label: 'Total Items', icon: '📊' },
        { value: formatCurrency(data.summary.total_value), label: 'Total Value', icon: '💰' },
    ];

    metrics.forEach(m => {
        grid.appendChild(el('div', { className: 'metric-card' }, [
            el('div', { className: 'metric-icon', textContent: m.icon }),
            el('div', { className: 'metric-value', textContent: m.value }),
            el('div', { className: 'metric-label', textContent: m.label }),
        ]));
    });

    s.appendChild(grid);
    return s;
}
```

CSS for metric cards:
```css
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 24px;
    margin-top: 32px;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
}
.metric-value {
    font-size: 3rem;
    font-weight: 700;
    color: var(--primary);
    margin: 8px 0;
}
.metric-label {
    font-size: 0.9rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}
```

### Bar Charts

Horizontal bars for category breakdowns:

```css
.bar-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 12px;
}
.bar-label {
    width: 140px;
    font-size: 0.85rem;
    color: var(--text-muted);
    text-align: right;
    flex-shrink: 0;
}
.bar-track {
    flex: 1;
    height: 28px;
    background: var(--surface-alt);
    border-radius: 6px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--primary-light));
    border-radius: 6px;
    transition: width 0.3s ease;
    display: flex;
    align-items: center;
    padding-left: 12px;
    font-size: 0.8rem;
    color: white;
    font-weight: 600;
}
```

### Timeline

Vertical timeline for chronological data:

```css
.timeline-container {
    position: relative;
    padding-left: 40px;
}
.timeline-container::before {
    content: '';
    position: absolute;
    left: 15px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--border);
}
.timeline-item {
    position: relative;
    margin-bottom: 24px;
    padding-left: 24px;
}
.timeline-item::before {
    content: '';
    position: absolute;
    left: -29px;
    top: 6px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--primary);
    border: 2px solid var(--bg);
}
.timeline-date {
    font-size: 0.8rem;
    color: var(--primary-light);
    font-weight: 600;
    margin-bottom: 4px;
}
.timeline-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}
.timeline-detail {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 4px;
}
```

### Detail Cards

Rich content cards for individual items:

```css
.detail-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}
.detail-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}
.detail-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
}
.detail-card-badge {
    font-size: 0.75rem;
    padding: 4px 12px;
    border-radius: 99px;
    font-weight: 600;
    white-space: nowrap;  /* CRITICAL: prevents badge from wrapping */
}
```

### Data Tables

Styled tables with alternating rows:

```css
.df-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8rem;
}
.df-table thead th {
    background: var(--surface-alt);
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.7rem;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 2px solid var(--border);
}
.df-table tbody tr:nth-child(even) {
    background: var(--surface);
}
.df-table tbody td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}
```

### Split Layout

Two-column layouts for comparison or detail+visual:

```css
.split-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-top: 24px;
}
.split-layout.aside-right {
    grid-template-columns: 2fr 1fr;
}
.split-layout.aside-left {
    grid-template-columns: 1fr 2fr;
}
```

## Multi-slide Pagination

For sections with many items (e.g., 20 projects), paginate into multiple slides:

```javascript
function renderProjects(data) {
    if (!data.projects || !data.projects.length) return [null];

    const ITEMS_PER_SLIDE = 4;
    const pages = [];

    for (let i = 0; i < data.projects.length; i += ITEMS_PER_SLIDE) {
        const batch = data.projects.slice(i, i + ITEMS_PER_SLIDE);
        const pageNum = Math.floor(i / ITEMS_PER_SLIDE) + 1;
        const totalPages = Math.ceil(data.projects.length / ITEMS_PER_SLIDE);

        const s = slide();
        s.innerHTML = header(
            'Projects',
            `Project Details`,
            pageNum > 1 ? `Page ${pageNum} of ${totalPages}` : null
        );

        batch.forEach(project => {
            s.appendChild(renderProjectCard(project));
        });

        pages.push(s);
    }

    return pages;
}
```

Use with spread in the function array: `...renderProjects(data)`

## Factory Pattern for Repeated Sections

When multiple data arrays share the same card layout, create a factory:

```javascript
function createCardRenderer(sectionKey, tag, title) {
    return function(data) {
        const items = data[sectionKey];
        if (!items || !items.length) return null;

        const s = slide();
        s.innerHTML = header(tag, title, `${items.length} items`);

        items.forEach(item => {
            s.appendChild(renderGenericCard(item));
        });

        return s;
    };
}

// Usage in function array:
const slides = [
    renderCover,
    createCardRenderer('infrastructure', 'Infra', 'Infrastructure Projects'),
    createCardRenderer('software', 'Software', 'Software Projects'),
    renderClosing,
];
```

## Typography Hierarchy

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Slide number | 0.75rem | 600 | var(--text-muted) |
| Tag badge | 0.7rem | 700 | var(--primary) on var(--primary-bg) |
| Slide title | 1.8rem | 800 | var(--text) |
| Slide subtitle | 1rem | 400 | var(--text-muted) |
| Metric value | 3rem | 700 | var(--primary) |
| Metric label | 0.9rem | 500 | var(--text-muted) |
| Card title | 1.1rem | 700 | var(--text) |
| Card body | 0.85rem | 400 | var(--text) |
| Table header | 0.7rem | 600 | var(--text-muted) |
| Table body | 0.8rem | 400 | var(--text) |
| Bar label | 0.85rem | 400 | var(--text-muted) |
| Bar value | 0.8rem | 600 | white |

## CSS Naming Conventions

Follow a BEM-like pattern:

- Block: `.metric-card`, `.bar-row`, `.timeline-item`, `.detail-card`
- Element: `.metric-card .metric-value`, `.detail-card .detail-card-header`
- Modifier: `.slide.cover-slide`, `.detail-card-badge.status-active`
- State: `.bar-fill` width set via inline style

Avoid deeply nested selectors. Keep specificity flat. Use CSS custom properties for theming.
