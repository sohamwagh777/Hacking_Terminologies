/**
 * atlas-graph.js — Force-directed constellation graph canvas engine for LEXICON.
 * Pure Vanilla ES2022 module.
 * Optimized with spatial hashing, edge culling, and requestAnimationFrame.
 */

import { getAllTerms, getCategoryMeta, CATEGORY_META } from './data-loader.js';
import { openTermDetail } from './detail.js';

let canvas = null;
let ctx = null;
let container = null;
let tooltipEl = null;

let width = 0;
let height = 0;
let dpr = 1;

// Camera state
let camera = {
  x: 0,
  y: 0,
  scale: 1,
  targetScale: 1
};

// Interaction state
let isDragging = false;
let dragStart = { x: 0, y: 0 };
let cameraStart = { x: 0, y: 0 };
let hoveredNode = null;
let activeFilteredIds = null; // Set of term IDs or null
let isRunning = true;
let isPhysicsPaused = false;
let animFrameId = null;

// Graph data structures
let nodes = [];
let nodeMap = new Map();
let edges = [];
let stars = [];

// Spatial Hash for O(1) neighbor/hover lookups
const CELL_SIZE = 80;
let spatialHash = new Map();

/**
 * Initialize Atlas Canvas Graph
 */
export function initAtlasGraph() {
  container = document.getElementById('atlas-container');
  canvas = document.getElementById('atlas-canvas');
  tooltipEl = document.getElementById('atlas-tooltip');

  if (!canvas || !container) return;

  ctx = canvas.getContext('2d', { alpha: false });

  // Handle window resizing
  window.addEventListener('resize', handleResize);
  handleResize();

  // Generate starfield
  initStarfield();

  // Build graph nodes & edges
  buildGraph();

  // Setup input event listeners
  setupInteractions();

  // Setup visibility change (pause on tab blur)
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopAnimation();
    } else {
      startAnimation();
    }
  });

  // Start animation loop
  startAnimation();
}

function handleResize() {
  if (!container || !canvas) return;
  const rect = container.getBoundingClientRect();
  width = rect.width;
  height = rect.height;
  dpr = window.devicePixelRatio || 1;

  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  if (camera.x === 0 && camera.y === 0) {
    camera.x = width / 2;
    camera.y = height / 2;
  }
}

function initStarfield() {
  stars = [];
  const starCount = 180;
  for (let i = 0; i < starCount; i++) {
    stars.push({
      x: (Math.random() - 0.5) * 3000,
      y: (Math.random() - 0.5) * 3000,
      radius: Math.random() * 1.4 + 0.4,
      alpha: Math.random() * 0.7 + 0.2,
      speed: Math.random() * 0.02 + 0.005,
      twinkleOffset: Math.random() * Math.PI * 2
    });
  }
}

/**
 * Construct nodes and edges from dataset
 */
function buildGraph() {
  const terms = getAllTerms();
  if (!terms.length) return;

  nodes = [];
  nodeMap.clear();
  edges = [];

  // Define 10 cluster centers evenly spaced in a wide orbit
  const categoryKeys = Object.keys(CATEGORY_META);
  const clusterCenters = new Map();
  const orbitRadius = Math.min(width, height) * 0.75 + 160;

  categoryKeys.forEach((key, idx) => {
    const angle = (idx / categoryKeys.length) * Math.PI * 2 - Math.PI / 2;
    clusterCenters.set(key, {
      x: Math.cos(angle) * orbitRadius,
      y: Math.sin(angle) * orbitRadius
    });
  });

  // Create Node objects
  terms.forEach((term, index) => {
    const center = clusterCenters.get(term.category) || { x: 0, y: 0 };
    // Distribute with noise around cluster center
    const localAngle = Math.random() * Math.PI * 2;
    const localDist = Math.random() * 140 + 20;

    const baseRadius = 7 + (term.related ? Math.min(term.related.length, 6) * 1.5 : 0);
    const meta = getCategoryMeta(term.category);

    const node = {
      id: term.id,
      name: term.name,
      category: term.category,
      difficulty: term.difficulty,
      nature: term.nature,
      color: meta.color,
      glow: meta.glow,
      radius: baseRadius,
      x: center.x + Math.cos(localAngle) * localDist,
      y: center.y + Math.sin(localAngle) * localDist,
      vx: 0,
      vy: 0,
      targetCluster: center,
      pulsePhase: Math.random() * Math.PI * 2,
      related: term.related || []
    };

    nodes.push(node);
    nodeMap.set(term.id, node);
  });

  // Create Edges
  const edgeSet = new Set();
  terms.forEach(term => {
    const sourceNode = nodeMap.get(term.id);
    if (!sourceNode) return;

    (term.related || []).forEach(relId => {
      const targetNode = nodeMap.get(relId);
      if (!targetNode || sourceNode === targetNode) return;

      // Unique edge key regardless of direction
      const edgeKey = [sourceNode.id, targetNode.id].sort().join('::');
      if (!edgeSet.has(edgeKey)) {
        edgeSet.add(edgeKey);
        edges.push({
          source: sourceNode,
          target: targetNode,
          color: sourceNode.color
        });
      }
    });
  });

  // Run initial warm-up physics ticks to relax layout
  for (let step = 0; step < 70; step++) {
    updatePhysics(0.016, true);
  }
}

/**
 * Re-hash nodes into 2D spatial hash grid
 */
function updateSpatialHash() {
  spatialHash.clear();
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i];
    const cellX = Math.floor(node.x / CELL_SIZE);
    const cellY = Math.floor(node.y / CELL_SIZE);
    const key = `${cellX}:${cellY}`;

    if (!spatialHash.has(key)) {
      spatialHash.set(key, []);
    }
    spatialHash.get(key).push(node);
  }
}

/**
 * Physics simulation tick
 */
function updatePhysics(dt, warmup = false) {
  if (isPhysicsPaused && !warmup) return;

  const damping = 0.88;
  const clusterAttraction = 0.04;
  const edgeSpring = 0.05;
  const minDistance = 35;

  // 1. Cluster center attraction
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    const dx = n.targetCluster.x - n.x;
    const dy = n.targetCluster.y - n.y;
    n.vx += dx * clusterAttraction * 0.2;
    n.vy += dy * clusterAttraction * 0.2;
  }

  // 2. Node Repulsion via spatial hash
  updateSpatialHash();
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    const cellX = Math.floor(n.x / CELL_SIZE);
    const cellY = Math.floor(n.y / CELL_SIZE);

    // Check adjacent 3x3 neighborhood
    for (let ox = -1; ox <= 1; ox++) {
      for (let oy = -1; oy <= 1; oy++) {
        const key = `${cellX + ox}:${cellY + oy}`;
        const neighbors = spatialHash.get(key);
        if (!neighbors) continue;

        for (let j = 0; j < neighbors.length; j++) {
          const other = neighbors[j];
          if (n === other) continue;

          const dx = other.x - n.x;
          const dy = other.y - n.y;
          const distSq = dx * dx + dy * dy;

          if (distSq > 0 && distSq < CELL_SIZE * CELL_SIZE) {
            const dist = Math.sqrt(distSq);
            const force = (minDistance - dist) / (dist * 1.5);
            if (force > 0) {
              const fx = (dx / dist) * force * 1.2;
              const fy = (dy / dist) * force * 1.2;
              n.vx -= fx;
              n.vy -= fy;
            }
          }
        }
      }
    }
  }

  // 3. Edge Springs
  for (let i = 0; i < edges.length; i++) {
    const e = edges[i];
    const dx = e.target.x - e.source.x;
    const dy = e.target.y - e.source.y;
    const dist = Math.sqrt(dx * dx + dy * dy) || 1;
    const targetDist = 70;
    const force = (dist - targetDist) * edgeSpring * 0.1;

    const fx = (dx / dist) * force;
    const fy = (dy / dist) * force;

    e.source.vx += fx;
    e.source.vy += fy;
    e.target.vx -= fx;
    e.target.vy -= fy;
  }

  // 4. Update positions with damping
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    n.vx *= damping;
    n.vy *= damping;
    n.x += n.vx;
    n.y += n.vy;

    // Gentle floating oscillation
    if (!warmup) {
      n.pulsePhase += 0.025;
    }
  }
}

/**
 * Main render cycle
 */
function render(timestamp) {
  if (!ctx) return;

  // Clear canvas with dark terminal background #050810
  ctx.save();
  ctx.scale(dpr, dpr);

  ctx.fillStyle = '#050810';
  ctx.fillRect(0, 0, width, height);

  // Draw animated parallax starfield
  renderStarfield(timestamp);

  // Transform to camera coordinates
  ctx.save();
  ctx.translate(camera.x, camera.y);
  ctx.scale(camera.scale, camera.scale);

  // Calculate viewport boundaries in world space for edge/node culling
  const vLeft = -camera.x / camera.scale - 100;
  const vTop = -camera.y / camera.scale - 100;
  const vRight = (width - camera.x) / camera.scale + 100;
  const vBottom = (height - camera.y) / camera.scale + 100;

  // Draw Edges (Filaments)
  renderEdges(vLeft, vTop, vRight, vBottom);

  // Draw Nodes (Constellations)
  renderNodes(vLeft, vTop, vRight, vBottom, timestamp);

  ctx.restore();
  ctx.restore();
}

function renderStarfield(time = 0) {
  ctx.fillStyle = '#ffffff';
  for (let i = 0; i < stars.length; i++) {
    const s = stars[i];
    // Parallax shift based on camera
    const px = (s.x + camera.x * 0.15) % width;
    const py = (s.y + camera.y * 0.15) % height;
    const screenX = px < 0 ? px + width : px;
    const screenY = py < 0 ? py + height : py;

    const twinkle = Math.sin(time * s.speed + s.twinkleOffset) * 0.35 + 0.65;
    ctx.globalAlpha = s.alpha * twinkle;
    ctx.beginPath();
    ctx.arc(screenX, screenY, s.radius, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1.0;
}

function renderEdges(vLeft, vTop, vRight, vBottom) {
  for (let i = 0; i < edges.length; i++) {
    const e = edges[i];
    const s = e.source;
    const t = e.target;

    // Viewport Culling
    if ((s.x < vLeft && t.x < vLeft) ||
        (s.x > vRight && t.x > vRight) ||
        (s.y < vTop && t.y < vTop) ||
        (s.y > vBottom && t.y > vBottom)) {
      continue;
    }

    const isConnectedToHovered = hoveredNode && (s === hoveredNode || t === hoveredNode);
    let alpha = 0.18;
    let lineWidth = 0.8;

    if (isConnectedToHovered) {
      alpha = 0.9;
      lineWidth = 2.0;
    } else if (activeFilteredIds) {
      const sMatch = activeFilteredIds.has(s.id);
      const tMatch = activeFilteredIds.has(t.id);
      if (!sMatch && !tMatch) {
        alpha = 0.04;
      } else if (sMatch && tMatch) {
        alpha = 0.35;
        lineWidth = 1.2;
      }
    }

    ctx.strokeStyle = s.color;
    ctx.globalAlpha = alpha;
    ctx.lineWidth = lineWidth;

    ctx.beginPath();
    ctx.moveTo(s.x, s.y);
    ctx.lineTo(t.x, t.y);
    ctx.stroke();
  }
  ctx.globalAlpha = 1.0;
}

function renderNodes(vLeft, vTop, vRight, vBottom, time) {
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];

    // Viewport Culling
    if (n.x < vLeft || n.x > vRight || n.y < vTop || n.y > vBottom) {
      continue;
    }

    const isHovered = (n === hoveredNode);
    const isFiltered = activeFilteredIds && !activeFilteredIds.has(n.id);
    const isAdjacent = hoveredNode && (hoveredNode.related.includes(n.id) || n.related.includes(hoveredNode.id));

    // Dynamic pulsating radius
    const pulse = Math.sin(n.pulsePhase) * 1.2;
    const currentRadius = (n.radius + (isHovered ? 4 : 0) + pulse);

    let alpha = 1.0;
    if (isFiltered) {
      alpha = 0.18;
    } else if (hoveredNode && !isHovered && !isAdjacent) {
      alpha = 0.35;
    }

    ctx.globalAlpha = alpha;

    // Outer Glow Halo
    if (isHovered || isAdjacent || (!isFiltered && activeFilteredIds)) {
      const gradient = ctx.createRadialGradient(n.x, n.y, 1, n.x, n.y, currentRadius * 2.8);
      gradient.addColorStop(0, n.color);
      gradient.addColorStop(1, 'transparent');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(n.x, n.y, currentRadius * 2.8, 0, Math.PI * 2);
      ctx.fill();
    }

    // Node Core
    ctx.fillStyle = isHovered ? '#ffffff' : n.color;
    ctx.beginPath();
    ctx.arc(n.x, n.y, currentRadius, 0, Math.PI * 2);
    ctx.fill();

    // Inner Specular Dot
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(n.x - currentRadius * 0.3, n.y - currentRadius * 0.3, currentRadius * 0.28, 0, Math.PI * 2);
    ctx.fill();

    // Text Label: Show when hovered, adjacent, or zoomed in
    const shouldShowLabel = isHovered || isAdjacent || (camera.scale > 0.95 && !isFiltered);
    if (shouldShowLabel) {
      ctx.font = isHovered ? 'bold 12px "JetBrains Mono", monospace' : '10px "JetBrains Mono", monospace';
      ctx.fillStyle = isHovered ? '#00ffcc' : '#e0e6ed';
      ctx.textAlign = 'center';
      ctx.fillText(n.name, n.x, n.y + currentRadius + 12);
    }
  }

  ctx.globalAlpha = 1.0;
}

/**
 * Main animation loop
 */
function loop(timestamp) {
  if (!isRunning) return;

  updatePhysics(0.016);
  render(timestamp);

  animFrameId = requestAnimationFrame(loop);
}

export function startAnimation() {
  if (!isRunning) {
    isRunning = true;
    animFrameId = requestAnimationFrame(loop);
  }
}

export function stopAnimation() {
  isRunning = false;
  if (animFrameId) {
    cancelAnimationFrame(animFrameId);
    animFrameId = null;
  }
}

/**
 * Handle user interactions: drag, zoom, hover, click
 */
function setupInteractions() {
  if (!canvas) return;

  // Pointer Down (Pan drag start)
  canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    dragStart = { x: e.clientX, y: e.clientY };
    cameraStart = { x: camera.x, y: camera.y };
    canvas.style.cursor = 'grabbing';
  });

  // Pointer Move (Pan or Hover)
  window.addEventListener('mousemove', (e) => {
    if (isDragging) {
      const dx = e.clientX - dragStart.x;
      const dy = e.clientY - dragStart.y;
      camera.x = cameraStart.x + dx;
      camera.y = cameraStart.y + dy;
    } else {
      handlePointerHover(e);
    }
  });

  // Pointer Up (End Drag or Click)
  window.addEventListener('mouseup', (e) => {
    if (isDragging) {
      const dx = Math.abs(e.clientX - dragStart.x);
      const dy = Math.abs(e.clientY - dragStart.y);
      isDragging = false;
      canvas.style.cursor = hoveredNode ? 'pointer' : 'grab';

      // If barely moved, treat as click
      if (dx < 5 && dy < 5 && hoveredNode) {
        openTermDetail(hoveredNode.id);
      }
    }
  });

  // Zoom by Wheel
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.12 : 0.89;
    zoomAt(e.clientX, e.clientY, zoomFactor);
  }, { passive: false });

  // Touch Interactions
  let touchStartDist = 0;
  canvas.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      isDragging = true;
      dragStart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      cameraStart = { x: camera.x, y: camera.y };
    } else if (e.touches.length === 2) {
      isDragging = false;
      touchStartDist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
    }
  });

  canvas.addEventListener('touchmove', (e) => {
    if (e.touches.length === 1 && isDragging) {
      const dx = e.touches[0].clientX - dragStart.x;
      const dy = e.touches[0].clientY - dragStart.y;
      camera.x = cameraStart.x + dx;
      camera.y = cameraStart.y + dy;
    } else if (e.touches.length === 2) {
      const dist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
      if (touchStartDist > 0) {
        const factor = dist / touchStartDist;
        const midX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        const midY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        zoomAt(midX, midY, factor);
        touchStartDist = dist;
      }
    }
  });

  canvas.addEventListener('touchend', () => {
    isDragging = false;
    touchStartDist = 0;
  });

  // UI Control buttons
  const zoomInBtn = document.getElementById('atlas-zoom-in');
  const zoomOutBtn = document.getElementById('atlas-zoom-out');
  const resetBtn = document.getElementById('atlas-reset-view');

  if (zoomInBtn) {
    zoomInBtn.addEventListener('click', () => zoomAt(width / 2, height / 2, 1.25));
  }
  if (zoomOutBtn) {
    zoomOutBtn.addEventListener('click', () => zoomAt(width / 2, height / 2, 0.8));
  }
  if (resetBtn) {
    resetBtn.addEventListener('click', resetView);
  }
}

function zoomAt(clientX, clientY, factor) {
  const rect = canvas.getBoundingClientRect();
  const mouseX = clientX - rect.left;
  const mouseY = clientY - rect.top;

  const newScale = Math.max(0.28, Math.min(3.2, camera.scale * factor));
  const scaleChange = newScale / camera.scale;

  camera.x = mouseX - (mouseX - camera.x) * scaleChange;
  camera.y = mouseY - (mouseY - camera.y) * scaleChange;
  camera.scale = newScale;
}

export function resetView() {
  camera.scale = 1;
  camera.x = width / 2;
  camera.y = height / 2;
}

function handlePointerHover(e) {
  if (!canvas) return;
  const rect = canvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  // Convert to world space
  const worldX = (mouseX - camera.x) / camera.scale;
  const worldY = (mouseY - camera.y) / camera.scale;

  // Spatial search for closest node
  const cellX = Math.floor(worldX / CELL_SIZE);
  const cellY = Math.floor(worldY / CELL_SIZE);

  let closest = null;
  let minDistance = 20 / camera.scale;

  for (let ox = -1; ox <= 1; ox++) {
    for (let oy = -1; oy <= 1; oy++) {
      const key = `${cellX + ox}:${cellY + oy}`;
      const cellNodes = spatialHash.get(key);
      if (!cellNodes) continue;

      for (let i = 0; i < cellNodes.length; i++) {
        const n = cellNodes[i];
        const dist = Math.hypot(n.x - worldX, n.y - worldY);
        if (dist <= n.radius + 6 && dist < minDistance) {
          closest = n;
          minDistance = dist;
        }
      }
    }
  }

  hoveredNode = closest;
  canvas.style.cursor = closest ? 'pointer' : (isDragging ? 'grabbing' : 'grab');

  if (tooltipEl) {
    if (closest) {
      const meta = getCategoryMeta(closest.category);
      tooltipEl.innerHTML = `
        <div class="tooltip-header" style="color: ${meta.color};">${meta.icon} ${meta.name}</div>
        <div class="tooltip-title">${closest.name}</div>
        <div class="tooltip-meta">${closest.related.length} related links • ${closest.difficulty}</div>
      `;
      tooltipEl.style.left = `${e.clientX + 14}px`;
      tooltipEl.style.top = `${e.clientY + 14}px`;
      tooltipEl.style.display = 'block';
    } else {
      tooltipEl.style.display = 'none';
    }
  }
}

/**
 * Filter graph nodes based on active search/category results
 */
export function filterGraph(results) {
  if (!results || results.length === getAllTerms().length) {
    activeFilteredIds = null;
  } else {
    activeFilteredIds = new Set(results.map(r => r.id));
  }
}
