---
version: "alpha"
name: "Lumen — Voice Reader"
description: "Lumen Voice Hero Section is designed for introducing a product with clear above-the-fold messaging. Key features include headline hierarchy, supporting copy, and a primary call-to-action. It is suitable for homepage hero areas and campaign landing pages."
colors:
  primary: "#64748B"
  secondary: "#94A3B8"
  tertiary: "#CBD5E1"
  neutral: "#FFFFFF"
  background: "#FFFFFF"
  surface: "#070709"
  text-primary: "#94A3B8"
  text-secondary: "#FFFFFF"
  border: "#FFFFFF"
  accent: "#64748B"
typography:
  headline-lg:
    fontFamily: "Inter"
    fontSize: "36px"
    fontWeight: 600
    lineHeight: "40px"
    letterSpacing: "-0.025em"
  body-md:
    fontFamily: "Inter"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "22.75px"
  label-md:
    fontFamily: "Inter"
    fontSize: "14px"
    fontWeight: 500
    lineHeight: "20px"
rounded:
  md: "8px"
  full: "9999px"
spacing:
  base: "4px"
  sm: "1px"
  md: "2px"
  lg: "4px"
  xl: "6px"
  gap: "6px"
  card-padding: "9px"
  section-padding: "24px"
components:
  button-primary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "6px"
  button-secondary:
    textColor: "#E2E8F0"
    rounded: "{rounded.md}"
    padding: "6px"
  button-link:
    textColor: "{colors.secondary}"
    typography: "{typography.label-md}"
    rounded: "0px"
    padding: "0px"
  card:
    rounded: "16px"
    padding: "24px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Full Bleed
  - Framing: Glassy
  - Grid: Strong

## Colors

The color system uses dark mode with #64748B as the main accent and #FFFFFF as the neutral foundation.

- **Primary (#64748B):** Main accent and emphasis color.
- **Secondary (#94A3B8):** Supporting accent for secondary emphasis.
- **Tertiary (#CBD5E1):** Reserved accent for supporting contrast moments.
- **Neutral (#FFFFFF):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #FFFFFF; Surface: #070709; Text Primary: #94A3B8; Text Secondary: #FFFFFF; Border: #FFFFFF; Accent: #64748B

## Typography

Typography relies on Inter across display, body, and utility text.

- **Headlines (`headline-lg`):** Inter, 36px, weight 600, line-height 40px, letter-spacing -0.025em.
- **Body (`body-md`):** Inter, 14px, weight 400, line-height 22.75px.
- **Labels (`label-md`):** Inter, 14px, weight 500, line-height 20px.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, full bleed structural frame before changing ornament or component styling. Use 4px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / full bleed composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Full Bleed
- **Base unit:** 4px
- **Scale:** 1px, 2px, 4px, 6px, 8px, 12px, 16px, 20px
- **Section padding:** 24px, 56px, 88px
- **Card padding:** 9px, 10px, 18px, 24px
- **Gaps:** 6px, 8px, 12px, 16px

## Elevation & Depth

Depth is communicated through glass, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as glass first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Glass
- **Borders:** 1px #FFFFFF
- **Shadows:** rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(255, 0, 170, 0.4) 0px 0px 40px -8px; rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 1px 3px 0px, rgba(0, 0, 0, 0.1) 0px 1px 2px -1px
- **Blur:** 6px, 20px, 24px

### Techniques
- **Gradient border shell:** Use a thin gradient border shell around the main card. Wrap the surface in an outer shell with 1px padding and a 24px radius. Drive the shell with linear-gradient(140deg, rgba(255, 0, 170, 0.35), rgba(0, 229, 255, 0.25), rgba(255, 255, 255, 0.05)) so the edge reads like premium depth instead of a flat stroke. Keep the actual stroke understated so the gradient shell remains the hero edge treatment. Inset the real content surface inside the wrapper with a slightly smaller radius so the gradient only appears as a hairline frame.

## Shapes

Shapes rely on a tight radius system anchored by 8px and scaled across cards, buttons, and supporting surfaces. Icon geometry should stay compatible with that soft-to-controlled silhouette.

Use the radius family intentionally: larger surfaces can open up, but controls and badges should stay within the same rounded DNA instead of inventing sharper or pill-only exceptions.

- **Corner radii:** 8px, 12px, 16px, 23px, 24px, 9999px
- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Anchor interactions to the detected button styles. Reuse the existing card surface recipe for content blocks.

### Buttons
- **Primary:** background #070709, text #FFFFFF, radius 9999px, padding 6px, border 0px solid rgb(229, 231, 235).
- **Secondary:** text #E2E8F0, radius 8px, padding 6px, border 1px solid rgba(255, 255, 255, 0.08).
- **Links:** text #94A3B8, radius 0px, padding 0px, border 0px solid rgb(229, 231, 235).

### Cards and Surfaces
- **Card surface:** border 1px solid rgba(255, 255, 255, 0.06), radius 16px, padding 24px, shadow none, blur 6px.

### Iconography
- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do
- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 4px rhythm.
- Do reuse the Glass surface treatment consistently across cards and controls.
- Do keep corner radii within the detected 8px, 12px, 16px, 23px, 24px, 9999px family.

### Don't
- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected moderate motion intensity without a deliberate reason.

## Motion

Motion feels controlled and interface-led across text, layout, and section transitions. Timing clusters around 150ms. Easing favors ease and cubic-bezier(0.4. Hover behavior focuses on color and text changes. Scroll choreography uses GSAP ScrollTrigger for section reveals and pacing.

**Motion Level:** moderate

**Durations:** 150ms

**Easings:** ease, cubic-bezier(0.4, 0, 0.2, 1)

**Hover Patterns:** color, text

**Scroll Patterns:** gsap-scrolltrigger

## WebGL

Reconstruct the graphics as a ambient background using alpha, antialias, custom shaders. The effect should read as technical and meditative: perspective grid field with black and sparse spacing. Build it from grid lines + depth fade so the effect reads clearly. Animate it as slow breathing pulse. Interaction can react to the pointer, but only as a subtle drift. Preserve dom fallback.

**Id:** webgl

**Label:** WebGL

**Stack:** WebGL

**Insights:**
  - **Scene:**
    - **Value:** Ambient background
  - **Effect:**
    - **Value:** Perspective grid field
  - **Primitives:**
    - **Value:** Grid lines + depth fade
  - **Motion:**
    - **Value:** Slow breathing pulse
  - **Interaction:**
    - **Value:** Pointer-reactive drift
  - **Render:**
    - **Value:** alpha, antialias, custom shaders

**Techniques:** Perspective grid, Breathing pulse, Pointer parallax, Shader gradients, DOM fallback

**Code Evidence:**
  - **JS reference:**
    - **Language:** js
    - **Snippet:**
      ```
      import { Renderer, Program, Mesh, Color, Triangle } from 'https://cdn.jsdelivr.net/npm/ogl@1.0.0/+esm';

      const MAX_STRANDS = 12, MAX_COLORS = 8;
      const VERT = `#version 300 es
      in vec2 position;
      void main(){ gl_Position = vec4(position,0.0,1.0); }`;
      ```
  - **Renderer setup:**
    - **Language:** js
    - **Snippet:**
      ```
      in vec2 position;
      void main(){ gl_Position = vec4(position,0.0,1.0); }`;
      const FRAG = `#version 300 es
      precision highp float;
      uniform float uTime; uniform vec2 uResolution;
      uniform vec3 uColors[${MAX_COLORS}]; uniform int uColorCount; uniform int uStrandCount;
      uniform float uSpeed,uAmplitude,uWaviness,uThickness,uGlow,uTaper,uSpread,uHueShift,uIntensity,uOpacity,uScale,uSaturation;
      out vec4 fragColor; const float PI=3.14159265;
      …
      ```
