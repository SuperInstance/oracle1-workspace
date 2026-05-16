# intent-inference — Rebirth Doc

> Reverse-engineers productive lane from agent behavior. Created 2026-05-07.

## What It Is

A TypeScript service that monitors agent behavior across the Cocapn Fleet and infers the *intent* behind successful actions — not motivation, but structure. Given a sequence of actions that produced verified output, what constraints were implicitly satisfied? The system produces a `ProductiveLane` model that tells the fleet what the user is trying to accomplish and what to work on proactively.

## Forgotten Gold

### 1. FleetBridge — Intent-Driven Fleet Orchestration

The `fleet_bridge.ts` is the most powerful component: it doesn't just *read* intent, it **tells other agents what to work on**. It writes goal tiles to PLATO's `intent_signals` room, sends focus directives to the Murmur worker in `murmur_directives` room, and posts briefings to `casey_briefings` for human notification. This creates a push-based workflow where inferred intent drives the entire fleet. The confidence thresholds (0.5 = broadcast goal, 0.7 = focus murmur, 0.85 = alert Casey) create graceful escalation.

### 2. Goal Engagement Prediction

The `predictGoalEngagement()` method in FleetBridge uses simulation-first prediction: before broadcasting a goal, predict whether user engagement will increase, file the prediction to PLATO with a Lamport clock, then later confirm or supersede with actual engagement data. This mirrors constraint-inference's prediction pattern — suggesting a fleet-wide design pattern of "predict before acting, confirm after observing."

### 3. Observer Architecture

Four independent observers (NavigationObserver, DeliberationObserver, MurmurObserver, PlatoObserver) each fetch from different PLATO rooms and produce typed `IntentSignal` objects. This clean separation means new signal sources can be added by writing a new observer class — no changes needed to the inference engine. The signals are sorted by timestamp and processed as a unified stream.

### 4. Signal Type Taxonomy

The `IntentSignal` type system defines 8 signal types: `page_view`, `tile_read`, `captain_override`, `captain_confirm`, `murmur_expand`, `murmur_skip`, `text_deleted`, `navigation_away`. The `text_deleted` type is particularly insightful — what a user types and deletes is often a stronger signal than what they actually send. The `navigation_away` + `from_page` captures drift patterns. This taxonomy is a complete model of user interaction signals that could be published as a shared type library.

### 5. Productive Lane Multi-Dimensional Model

The `ProductiveLane` model captures: primary goals, avoided topics, navigation patterns, peak hours, preferred theorems, preferred strategies, override patterns, and confidence score. It models the user as a multi-dimensional persona with rich structure — not just "the user wants to do X" but "the user works on X, avoids Y, prefers EXPLORE strategy, engages most at 2-4 AM, navigates in patterns." This could power extremely personalized agent behavior.

## Why It Matters Now

The FleetBridge is the missing link between intent inference and fleet action. The observer architecture is a reusable pattern. The signal taxonomy should be a shared type (`@cocapn/intent-signal-types`). The productive lane model could drive personalized agent delegation that adapts to Casey's working patterns, time-of-day preferences, and topic focus shifts.
