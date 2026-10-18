/**
 * detail.js — Slide-over detail panel and bottom sheet for LEXICON.
 * Pure Vanilla ES2022 module.
 */

import { getTermById, getCategoryMeta } from './data-loader.js';
import { navigateToTerm } from './router.js';

let detailPanel = null;
let backdrop = null;
let breadcrumbsEl = null;
let contentEl = null;
let historyStack = [];

/**
 * Initialize detail panel DOM references and event listeners
 */
export function initDetailPanel() {
  detailPanel = document.getElementById('detail-panel');
  backdrop = document.getElementById('panel-backdrop');
  breadcrumbsEl = document.getElementById('detail-breadcrumbs');
  contentEl = document.getElementById('detail-content');

  const closeBtn = document.getElementById('detail-close-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeDetail);
  }

  if (backdrop) {
    backdrop.addEventListener('click', closeDetail);
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isDetailOpen()) {
      closeDetail();
    }
  });
}

export function isDetailOpen() {
  return detailPanel && detailPanel.classList.contains('open');
}

/**
 * Open detail panel for a term ID, tracking breadcrumbs
 */
export function openTermDetail(termId, pushHistory = true) {
  if (!detailPanel) initDetailPanel();

  const term = getTermById(termId);
  if (!term) {
    console.warn(`Term not found: ${termId}`);
    return;
  }

  if (pushHistory) {
    if (historyStack.length === 0 || historyStack[historyStack.length - 1] !== term.id) {
      historyStack.push(term.id);
    }
  }

  renderBreadcrumbs();
  renderTerm(term);

  detailPanel.classList.add('open');
  if (backdrop) backdrop.classList.add('open');
  detailPanel.setAttribute('aria-hidden', 'false');

  // Announce to router or URL
  navigateToTerm(term.id);
}

export function closeDetail() {
  if (!detailPanel) return;
  detailPanel.classList.remove('open');
  if (backdrop) backdrop.classList.remove('open');
  detailPanel.setAttribute('aria-hidden', 'true');
  historyStack = [];
}

function renderBreadcrumbs() {
  if (!breadcrumbsEl) return;
  breadcrumbsEl.innerHTML = '';

  if (historyStack.length <= 1) {
    breadcrumbsEl.style.display = 'none';
    return;
  }

  breadcrumbsEl.style.display = 'flex';

  const backBtn = document.createElement('button');
  backBtn.className = 'crumb-back-btn';
  backBtn.innerHTML = '← Back';
  backBtn.title = 'Go back to previous term';
  backBtn.addEventListener('click', () => {
    historyStack.pop(); // Remove current
    const prevId = historyStack[historyStack.length - 1];
    if (prevId) {
      openTermDetail(prevId, false);
    } else {
      closeDetail();
    }
  });
  breadcrumbsEl.appendChild(backBtn);

  const trailSpan = document.createElement('div');
  trailSpan.className = 'crumb-trail';

  historyStack.forEach((id, idx) => {
    const t = getTermById(id);
    if (!t) return;

    if (idx > 0) {
      const sep = document.createElement('span');
      sep.className = 'crumb-sep';
      sep.textContent = ' / ';
      trailSpan.appendChild(sep);
    }

    const crumb = document.createElement('button');
    crumb.className = `crumb-item ${idx === historyStack.length - 1 ? 'active' : ''}`;
    crumb.textContent = t.name;
    crumb.addEventListener('click', () => {
      historyStack = historyStack.slice(0, idx + 1);
      openTermDetail(id, false);
    });
    trailSpan.appendChild(crumb);
  });

  breadcrumbsEl.appendChild(trailSpan);
}

function renderTerm(term) {
  if (!contentEl) return;

  const meta = getCategoryMeta(term.category);
  const diffClass = `diff-${term.difficulty.toLowerCase()}`;

  // Nature badges
  const natureWords = term.nature.split(/\s+/);
  const natureBadges = natureWords
    .map(w => `<span class="nature-badge nature-${w.toLowerCase()}">${w.toUpperCase()}</span>`)
    .join(' ');

  // Related terms chips
  const relatedChips = term.related.map(relId => {
    const relTerm = getTermById(relId);
    const relName = relTerm ? relTerm.name : relId;
    return `<button class="related-chip" data-term-id="${relId}">${escapeHtml(relName)} →</button>`;
  }).join('');

  // Links list
  const linksHtml = term.links.map(link => {
    const domain = extractDomain(link.url);
    return `
      <li class="resource-link-item">
        <a href="${escapeHtml(link.url)}" target="_blank" rel="noopener noreferrer" class="resource-link">
          <span class="link-title">${escapeHtml(link.title)}</span>
          <span class="link-domain">${domain} ↗</span>
        </a>
      </li>
    `;
  }).join('');

  // Example block
  let exampleHtml = '';
  if (term.example && term.example.trim()) {
    exampleHtml = `
      <div class="detail-section example-section">
        <div class="section-header">
          <span class="section-title">REAL-WORLD SNIPPET</span>
          <button class="copy-snippet-btn" id="copy-snippet-btn">Copy</button>
        </div>
        <pre class="code-block"><code id="code-snippet-body">${escapeHtml(term.example)}</code></pre>
      </div>
    `;
  }

  contentEl.innerHTML = `
    <div class="detail-header" style="border-left-color: ${meta.color};">
      <div class="badge-row">
        <span class="category-pill" style="border-color: ${meta.color}; color: ${meta.color}; background: ${meta.glow};">
          ${meta.icon} ${meta.name}
        </span>
        <span class="difficulty-pill ${diffClass}">
          ${term.difficulty.toUpperCase()}
        </span>
        <div class="nature-tags">
          ${natureBadges}
        </div>
      </div>
      <h2 class="detail-title" style="text-shadow: 0 0 16px ${meta.glow};">${escapeHtml(term.name)}</h2>
    </div>

    <div class="detail-section">
      <h4 class="section-title">MECHANISM & DEFINITION</h4>
      <p class="definition-text">${escapeHtml(term.definition)}</p>
    </div>

    <div class="detail-section why-matters-box" style="border-left-color: ${meta.color};">
      <h4 class="section-title why-title">⚠️ WHY IT MATTERS & RISK PROFILE</h4>
      <p class="why-text">${escapeHtml(term.why_matters)}</p>
    </div>

    ${exampleHtml}

    <div class="detail-section">
      <h4 class="section-title">RELATED CONCEPTS (${term.related.length})</h4>
      <div class="related-chips-grid">
        ${relatedChips}
      </div>
    </div>

    <div class="detail-section">
      <h4 class="section-title">READ MORE & DOCUMENTATION</h4>
      <ul class="resource-links-list">
        ${linksHtml}
      </ul>
    </div>
  `;

  // Attach event listeners to related chips
  contentEl.querySelectorAll('.related-chip').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const targetId = e.currentTarget.getAttribute('data-term-id');
      if (targetId) openTermDetail(targetId, true);
    });
  });

  // Attach copy button handler
  const copyBtn = contentEl.querySelector('#copy-snippet-btn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const code = term.example || '';
      navigator.clipboard.writeText(code).then(() => {
        copyBtn.textContent = 'COPIED!';
        copyBtn.classList.add('copied');
        setTimeout(() => {
          copyBtn.textContent = 'Copy';
          copyBtn.classList.remove('copied');
        }, 2000);
      }).catch(err => {
        console.error('Copy failed', err);
      });
    });
  }
}

function extractDomain(url) {
  try {
    return new URL(url).hostname.replace('www.', '');
  } catch {
    return 'external';
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
