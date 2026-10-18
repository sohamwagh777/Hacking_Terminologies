/**
 * router.js — Hash-based client router for LEXICON.
 * Supports deep linking: #/atlas?term=idor, #/index?term=xss, #/paths?category=auth-access&term=mfa
 * Pure Vanilla ES2022 module.
 */

import { openTermDetail, closeDetail, isDetailOpen } from './detail.js';

let activeView = 'atlas';
let viewChangeCallbacks = [];

export function initRouter() {
  window.addEventListener('hashchange', handleRoute);
  // Initial route
  handleRoute();
}

export function onViewChange(callback) {
  viewChangeCallbacks.push(callback);
}

export function getActiveView() {
  return activeView;
}

export function navigate(hash) {
  if (window.location.hash !== hash) {
    window.location.hash = hash;
  } else {
    handleRoute();
  }
}

export function navigateToView(viewName) {
  const currentParams = getHashParams();
  let newHash = `#/${viewName}`;
  const searchParams = new URLSearchParams();

  if (currentParams.term) {
    searchParams.set('term', currentParams.term);
  }
  if (currentParams.category && viewName === 'paths') {
    searchParams.set('category', currentParams.category);
  }

  const queryString = searchParams.toString();
  if (queryString) {
    newHash += `?${queryString}`;
  }

  navigate(newHash);
}

export function navigateToTerm(termId) {
  const currentParams = getHashParams();
  const searchParams = new URLSearchParams();

  searchParams.set('term', termId);
  if (currentParams.category && activeView === 'paths') {
    searchParams.set('category', currentParams.category);
  }

  navigate(`#/${activeView}?${searchParams.toString()}`);
}

export function getHashParams() {
  const hash = window.location.hash || '#/atlas';
  const qIdx = hash.indexOf('?');
  const params = {};

  if (qIdx !== -1) {
    const qs = hash.slice(qIdx + 1);
    const sp = new URLSearchParams(qs);
    for (const [k, v] of sp.entries()) {
      params[k] = v;
    }
  }

  return params;
}

function handleRoute() {
  let hash = window.location.hash || '#/atlas';
  if (!hash.startsWith('#/')) {
    hash = '#/atlas';
  }

  const qIdx = hash.indexOf('?');
  const pathPart = qIdx !== -1 ? hash.slice(2, qIdx) : hash.slice(2);
  const params = getHashParams();

  // Route matching
  let view = 'atlas';
  let category = params.category || null;

  if (pathPart.startsWith('index')) {
    view = 'index';
  } else if (pathPart.startsWith('paths') || pathPart.startsWith('path/')) {
    view = 'paths';
    if (pathPart.startsWith('path/')) {
      category = pathPart.slice(5);
    }
  } else {
    view = 'atlas';
  }

  activeView = view;

  // Notify listeners to update views (ATLAS / INDEX / PATHS)
  viewChangeCallbacks.forEach(cb => {
    try {
      cb({ view, category, termId: params.term, params });
    } catch (err) {
      console.error('Router callback error:', err);
    }
  });

  // Handle deep-linked term detail
  if (params.term) {
    openTermDetail(params.term, false);
  } else if (isDetailOpen()) {
    closeDetail();
  }
}
