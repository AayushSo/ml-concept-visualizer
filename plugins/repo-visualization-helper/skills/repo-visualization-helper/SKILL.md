---
name: repo-visualization-helper
description: Create, improve, and review standalone HTML visualizer pages for ml-concept-visualizer while keeping the catalog, metadata, and checks consistent.
---

# Repo Visualization Helper

Use this skill when the user wants to add a new visualizer, revise an existing one,
or review a page for quality in this repository.

## Repo Context

- This repo is a collection of standalone HTML visualizers for ML, deep learning,
  computer architecture, GPU/CUDA, TPU, and performance topics.
- Most pages are single-file educational experiences with embedded HTML, CSS, and JS.
- Changes usually matter when they improve:
  - conceptual correctness
  - explanation quality
  - interaction design
  - state handling
  - responsive behavior
  - navigation and discoverability

## Default Workflow

1. Read the target page fully before editing.
   - Inspect the title, H1, controls, interaction flow, and any canvas logic.

2. If the task adds or renames a visualizer:
   - Update `index.html` so the page is discoverable.
   - Ensure the catalog title and description match the page purpose.
   - If an old URL should keep working, leave a redirect stub.

3. Keep the page repo-native:
   - Prefer a single self-contained HTML file unless the user asks for a broader refactor.
   - Preserve the repo’s teaching-first style: explain what the learner is seeing,
     not just what the code is doing.
   - Favor clear labels, readable controls, and visual feedback over decorative complexity.

4. Check metadata consistency:
   - Align filename, `<title>`, H1, and catalog label around one canonical concept name.
   - Add a concise catalog description if the page is linked from `index.html`.

5. Check responsiveness and interaction quality:
   - Avoid obvious desktop-only fixed-size layouts unless the page truly requires them.
   - For canvas-heavy pages, make sure resize behavior is intentional.
   - If a canvas has explicit dimensions, verify whether it should redraw on window resize.

6. Run repo checks after meaningful changes:

```bash
python3 scripts/check-consistency.py
python3 scripts/smoke-test-catalog.py
```

7. When asked for a review:
   - Prioritize correctness bugs, interaction regressions, missing explanations,
     broken catalog integration, and responsive layout risks.

## Review Checklist

When reviewing or refining a visualizer, pay special attention to:

- Is the concept name consistent across filename, title, H1, and index entry?
- Does the first screen communicate what the learner should notice?
- Are controls labeled in domain language rather than only implementation terms?
- Does the page remain usable on smaller screens?
- If the page uses canvas, does resizing preserve usability?
- Are there obvious broken local links, missing H1/title, or catalog drift?

## Preferred Output Style

- For implementation tasks: make the code changes directly and summarize the learner-facing outcome.
- For review tasks: list findings first, ordered by severity, with file references.
- For catalog-related tasks: mention both page-level changes and `index.html` updates.
