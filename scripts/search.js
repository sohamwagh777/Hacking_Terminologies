/**
 * search.js — Global search and category filtering for LEXICON.
 * Pure Vanilla ES2022 module.
 */

import { searchTerms, getAllTerms, CATEGORY_META } from './data-loader.js';
import { openTermDetail } from './detail.js';

let searchInput = null;
let categoryFilter = null;
let countBadge = null;
let listeners = [];

/**
 * Initialize search controls and keyboard shortcuts
 */
export function initSearch() {
  searchInput = document.getElementById('global-search-input');
  categoryFilter = document.getElementById('category-filter-select');
  countBadge = document.getElementById('search-results-count');

  if (categoryFilter) {
    // Populate category filter options
    categoryFilter.innerHTML = '<option value="all">All Domains (10)</option>';
    for (const [key, meta] of Object.entries(CATEGORY_META)) {
      const opt = document.createElement('option');
      opt.value = key;
      opt.textContent = `${meta.icon} ${meta.name}`;
      categoryFilter.appendChild(opt);
    }

    categoryFilter.addEventListener('change', () => {
      triggerSearch();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      triggerSearch();
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        searchInput.value = '';
        searchInput.blur();
        triggerSearch();
      } else if (e.key === 'Enter') {
        const results = getCurrentResults();
        if (results.length > 0) {
          openTermDetail(results[0].id);
        }
      }
    });
  }

  // Global keyboard shortcut '/' to focus search
  window.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== searchInput) {
      // Don't trigger if user is typing in another input
      if (!['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      }
    }
  });

  // Initial trigger
  triggerSearch();
}

export function onSearchChange(callback) {
  listeners.push(callback);
}

export function getCurrentQuery() {
  return searchInput ? searchInput.value.trim() : '';
}

export function getCurrentCategory() {
  return categoryFilter ? categoryFilter.value : 'all';
}

export function setCategoryFilter(category) {
  if (categoryFilter) {
    categoryFilter.value = category;
    triggerSearch();
  }
}

export function setSearchQuery(query) {
  if (searchInput) {
    searchInput.value = query;
    triggerSearch();
  }
}

export function getCurrentResults() {
  const q = getCurrentQuery();
  const cat = getCurrentCategory();
  return searchTerms(q, cat);
}

function triggerSearch() {
  const query = getCurrentQuery();
  const category = getCurrentCategory();
  const results = searchTerms(query, category);
  const total = getAllTerms().length || 198;

  if (countBadge) {
    if (query || category !== 'all') {
      countBadge.textContent = `${results.length} / ${total} terms`;
      countBadge.classList.add('filtered');
    } else {
      countBadge.textContent = `${total} terms`;
      countBadge.classList.remove('filtered');
    }
  }

  listeners.forEach(cb => {
    try {
      cb({ query, category, results });
    } catch (err) {
      console.error('Search listener error:', err);
    }
  });
}
