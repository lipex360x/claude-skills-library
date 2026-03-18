/* ==========================================================================
   Renderer — Data-Driven Presentation

   Architecture:
   - IIFE with fetch('data.json')
   - Helper functions: el(), slide(), header(), nextSlide()
   - Function array pipeline: each slide type = independent function
   - Null guard: missing data → skip slide (return null)
   ========================================================================== */

(function () {
    'use strict';

    const container = document.getElementById('slides');
    let slideCount = 0;

    // ---------- Helpers ----------

    /**
     * DOM factory — creates an element with attributes and children.
     * @param {string} tag - HTML tag name
     * @param {Object} attrs - Attributes (className, innerHTML, textContent, style, data-*, etc.)
     * @param {string|Array} children - HTML string or array of child elements/strings
     * @returns {HTMLElement}
     */
    function el(tag, attrs, children) {
        attrs = attrs || {};
        children = children || [];
        const element = document.createElement(tag);
        Object.entries(attrs).forEach(function (entry) {
            var key = entry[0], value = entry[1];
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
            children.forEach(function (child) {
                if (typeof child === 'string') {
                    element.appendChild(document.createTextNode(child));
                } else if (child) {
                    element.appendChild(child);
                }
            });
        }
        return element;
    }

    /**
     * Slide container factory.
     * @param {Object} opts - { classes: string[], noNumber: boolean }
     * @returns {HTMLElement}
     */
    function slide(opts) {
        opts = opts || {};
        slideCount++;
        var num = String(slideCount).padStart(2, '0');
        var classes = ['slide'].concat(opts.classes || []).join(' ');
        var s = el('div', { className: classes });
        if (!opts.noNumber) {
            s.appendChild(el('div', { className: 'slide-number', textContent: num }));
        }
        return s;
    }

    /**
     * Slide header with tag badge, title, and optional subtitle.
     * Returns HTML string — use with innerHTML.
     */
    function header(tag, title, subtitle) {
        return '<span class="tag">' + tag + '</span>' +
            '<h2 class="slide-title">' + title + '</h2>' +
            (subtitle ? '<p class="slide-subtitle">' + subtitle + '</p>' : '');
    }

    /**
     * Zero-padded slide counter.
     */
    function nextSlide() {
        slideCount++;
        return String(slideCount).padStart(2, '0');
    }

    // ---------- Slide Renderers ----------
    // Each function receives data and returns HTMLElement, Array<HTMLElement>, or null.

    /*
    function renderCover(data) {
        var s = slide({ classes: ['cover-slide'], noNumber: true });
        s.innerHTML = [
            '<h1 class="slide-title" style="font-size:2.5rem">' + data.meta.title + '</h1>',
            '<p class="slide-subtitle">' + (data.meta.subtitle || '') + '</p>',
            '<p class="slide-subtitle" style="margin-top:auto">' + data.meta.date + '</p>'
        ].join('');
        return s;
    }

    function renderSummary(data) {
        if (!data.summary) return null;
        var s = slide();
        s.innerHTML = header('Overview', 'Summary');
        // ... build summary content
        return s;
    }

    // Multi-slide example with pagination:
    function renderItems(data) {
        if (!data.items || !data.items.length) return [null];
        var ITEMS_PER_SLIDE = 4;
        var pages = [];
        for (var i = 0; i < data.items.length; i += ITEMS_PER_SLIDE) {
            var batch = data.items.slice(i, i + ITEMS_PER_SLIDE);
            var s = slide();
            s.innerHTML = header('Items', 'Item Details');
            batch.forEach(function(item) {
                // ... build item card
            });
            pages.push(s);
        }
        return pages;
    }

    function renderClosing(data) {
        var s = slide({ classes: ['closing-slide'] });
        s.innerHTML = '<h2 class="slide-title" style="text-align:center;margin:auto">' +
            (data.meta.company || 'Thank you') + '</h2>';
        return s;
    }
    */

    // ---------- Pipeline ----------

    fetch('data.json')
        .then(function (res) { return res.json(); })
        .then(function (data) {
            // Define the slide pipeline — order matters
            var pipeline = [
                // renderCover,
                // renderSummary,
                // ...renderItems(data),  // spread for multi-slide
                // renderClosing,
            ];

            pipeline.forEach(function (fn) {
                var result = typeof fn === 'function' ? fn(data) : fn;
                if (result === null || result === undefined) return;
                if (Array.isArray(result)) {
                    result.forEach(function (el) {
                        if (el) container.appendChild(el);
                    });
                } else {
                    container.appendChild(result);
                }
            });
        })
        .catch(function (err) {
            console.error('Failed to load data.json:', err);
            container.innerHTML = '<div class="slide" style="justify-content:center;align-items:center">' +
                '<h2 style="color:#ef4444">Error loading data.json</h2>' +
                '<p style="color:#888;margin-top:12px">' + err.message + '</p></div>';
        });

})();
