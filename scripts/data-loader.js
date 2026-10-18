/**
 * data-loader.js — Data loading, indexing, and query services for LEXICON.
 * Pure Vanilla ES2022 module.
 */

export const CATEGORY_META = {
  'web-exploitation': {
    name: 'Web Exploitation',
    slug: 'web-exploitation',
    color: '#ff3366', // Hot crimson / neon pink
    glow: 'rgba(255, 51, 102, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(255, 51, 102, 0.12), transparent 70%)',
    icon: '⚡',
    description: 'Flaws, injection mechanisms, and perimeter boundary breaks targeting web applications.'
  },
  'auth-access': {
    name: 'Auth & Access',
    slug: 'auth-access',
    color: '#00ffcc', // Phosphor teal / cyan
    glow: 'rgba(0, 255, 204, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(0, 255, 204, 0.12), transparent 70%)',
    icon: '🔑',
    description: 'Authentication tokens, session integrity, privilege boundaries, and access control.'
  },
  'crypto-identity': {
    name: 'Crypto & Identity',
    slug: 'crypto-identity',
    color: '#9933ff', // Electric violet
    glow: 'rgba(153, 51, 255, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(153, 51, 255, 0.12), transparent 70%)',
    icon: '🔒',
    description: 'Cryptographic primitives, key management, hashing, signatures, and transport security.'
  },
  'data-databases': {
    name: 'Data & Databases',
    slug: 'data-databases',
    color: '#3399ff', // Cerulean blue
    glow: 'rgba(51, 153, 255, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(51, 153, 255, 0.12), transparent 70%)',
    icon: '🗄️',
    description: 'Relational storage engines, indexes, transactions, locking, and data integrity.'
  },
  'distributed-systems': {
    name: 'Distributed Systems',
    slug: 'distributed-systems',
    color: '#ffcc00', // Amber gold
    glow: 'rgba(255, 204, 0, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(255, 204, 0, 0.12), transparent 70%)',
    icon: '🌐',
    description: 'Consensus protocols, quorum mechanics, partition handling, and distributed concurrency.'
  },
  'messaging-streaming': {
    name: 'Messaging & Streaming',
    slug: 'messaging-streaming',
    color: '#ff6600', // Neon orange
    glow: 'rgba(255, 102, 0, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(255, 102, 0, 0.12), transparent 70%)',
    icon: '📨',
    description: 'Event queues, stream partitions, delivery semantics, and asynchronous pipelines.'
  },
  'http-networking': {
    name: 'HTTP & Networking',
    slug: 'http-networking',
    color: '#00e5ff', // High-contrast cyan
    glow: 'rgba(0, 229, 255, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(0, 229, 255, 0.12), transparent 70%)',
    icon: '📡',
    description: 'Internet protocols, headers, status codes, real-time channels, and DNS routing.'
  },
  'cloud-infra-ops': {
    name: 'Cloud Infra & Ops',
    slug: 'cloud-infra-ops',
    color: '#00ff66', // Phosphor terminal green
    glow: 'rgba(0, 255, 102, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(0, 255, 102, 0.12), transparent 70%)',
    icon: '☁️',
    description: 'VPCs, security groups, container runtimes, orchestration, and infrastructure deployment.'
  },
  'reliability-observability': {
    name: 'Reliability & Observability',
    slug: 'reliability-observability',
    color: '#ff00aa', // Neon magenta
    glow: 'rgba(255, 0, 170, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(255, 0, 170, 0.12), transparent 70%)',
    icon: '📊',
    description: 'Telemetry, SLOs, distributed tracing, profiling, fault isolation, and incident resilience.'
  },
  'secure-sdlc': {
    name: 'Secure SDLC',
    slug: 'secure-sdlc',
    color: '#33ffbb', // Mint cyan
    glow: 'rgba(51, 255, 187, 0.4)',
    wash: 'radial-gradient(ellipse at top left, rgba(51, 255, 187, 0.12), transparent 70%)',
    icon: '🛡️',
    description: 'Supply chain defense, CI/CD guardrails, image scanning, and version governance.'
  }
};

let termsCache = null;
let termsById = new Map();
let termsByCategory = new Map();

/**
 * Load terms from /data/terms.json
 */
export async function loadTerms() {
  if (termsCache) return termsCache;

  const response = await fetch('./data/terms.json');
  if (!response.ok) {
    throw new Error(`Failed to load terms: HTTP ${response.status}`);
  }

  const terms = await response.json();
  termsCache = terms;

  termsById.clear();
  termsByCategory.clear();

  for (const catKey of Object.keys(CATEGORY_META)) {
    termsByCategory.set(catKey, []);
  }

  for (const term of terms) {
    termsById.set(term.id, term);
    if (!termsByCategory.has(term.category)) {
      termsByCategory.set(term.category, []);
    }
    termsByCategory.get(term.category).push(term);
  }

  return termsCache;
}

export function getAllTerms() {
  return termsCache || [];
}

export function getTermById(id) {
  if (!id) return null;
  return termsById.get(id.toLowerCase()) || null;
}

export function getTermsByCategory(category) {
  return termsByCategory.get(category) || [];
}

export function getCategoryMeta(category) {
  return CATEGORY_META[category] || {
    name: category,
    slug: category,
    color: '#00ffcc',
    glow: 'rgba(0, 255, 204, 0.3)',
    wash: 'transparent',
    icon: '📌',
    description: ''
  };
}

/**
 * Perform search filtering by query string and optional category
 */
export function searchTerms(query, category = 'all') {
  const all = getAllTerms();
  const q = (query || '').trim().toLowerCase();

  return all.filter(term => {
    if (category !== 'all' && term.category !== category) {
      return false;
    }
    if (!q) return true;

    // Search in name, id, category, definition, nature, why_matters
    return (
      term.name.toLowerCase().includes(q) ||
      term.id.toLowerCase().includes(q) ||
      term.nature.toLowerCase().includes(q) ||
      term.category.toLowerCase().includes(q) ||
      term.definition.toLowerCase().includes(q) ||
      term.why_matters.toLowerCase().includes(q)
    );
  });
}
