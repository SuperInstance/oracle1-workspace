# cocapn-ai-web — Rebirth Doc

> Browser-native fleet demos showing captain deliberation, thinking strategies, constraint theory in the browser. Created 2026-05-07.

## What It Is

A collection of self-contained, zero-dependency HTML demos that bring Cocapn Fleet's constraint-theory ecosystem to life in the browser. Includes an Eisenstein drift-race hex lattice explorer, fleet murmur quality-gated insight streaming, fleet-spread captain topology, PLATO room protocol visualization, a GUARD constraint editor with FLUX-C bytecode mock compiler, and a full reverse-actualization truck concept.

## Forgotten Gold

### 1. The Reverse-Actualization "Truck" Philosophy

The deepest idea in this repo is the **truck paradigm** documented in `REVERSE-ACTUALIZATION.md` and `ROADMAP.md`. Classic AI: user asks → assistant answers. Truck: assistant always working → user steers away from unproductive tangents. The system flips the reactive model: **system writes, user reads**. Murmur runs in a background web worker without being triggered. Captain deliberation pre-reasons every decision before asked. PLATO becomes visible working memory, not hidden database. This philosophy should be the beating heart of the entire fleet, yet it lives only as a spec document — no service implements it end-to-end.

### 2. Ambient Briefing Loop (Phase 2)

`ROADMAP.md` Phase 2 and `AMBIENT-BRIEFING-SPEC.md` define the "12 things happened while you were away" briefing system. Idle detection state machine (ACTIVE → IDLE_PENDING → IDLE → BRIEFING_SENT). Four category briefings (Fleet, Math, Lane, Attention). Idempotency guards. Cached research. The `fleet-ambient-loop/` repo was planned but **never built**. This is the single highest-ROI missing piece in the entire fleet architecture.

### 3. Chrome Built-in AI APIs (Free, On-Device Intelligence)

`CHROME-AI-APIS.md` comprehensively documents Summarizer, Translator, LanguageDetector, Writer, and Rewriter APIs — all free and on-device in Chrome 138+. The demos use a cloud fallback (DeepSeek/z.ai) but the on-device path was **never wired up**. This means the fleet demos could run entirely offline, on-device, with zero API costs and zero network latency.

### 4. vdmo / PodiumJS Collaboration Opportunity

The SPEC.md documents a full collaboration path with PodiumJS author @vdmo: co-authored case studies, README showcase, feature requests. PodiumJS provides WebGPU-backed radar visualizations, agent ping effects, particle drift physics — but the actual demos ship with CSS fallbacks. The WebGPU visual layer was never implemented.

### 5. GUARD Constraint Playground (Phase E)

The `constraint-playground.js` module implements a full in-browser constraint programming IDE: syntax-highlighted GUARD editor, mock FLUX-C bytecode compiler with hex addresses, execution preview with input→output test cases, 4 example templates (Temperature, Door, Motor, Light). Phase F (real FLUX-C WASM compilation) was documented but never built.

## Why It Matters Now

The truck paradigm is the fleet's north star. The ambient briefing loop is the feature that makes the truck feel magical. Chrome AI APIs make it free and private. PodiumJS makes it visually stunning. These pieces were designed but never fully assembled. The wireframe exists; the building is still under construction.
