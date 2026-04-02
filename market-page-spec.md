# Character Engine — Market-Specific Landing Page Spec

## Pattern
Each market page follows the SAME structure as the main characterengine.live page but rewrites every section through the lens of a specific buyer. The CSS files (base.css, style.css) are shared — referenced from the parent directory via `../base.css` and `../style.css`.

## Page Structure (every page must have all of these sections)

1. **Header** — Same as main page. Logo links to `/` (the main Character Engine page). Nav CTA: "Book a Discovery Call" linking to #book.

2. **Hero** — Market-specific headline and subline. Badge says "Character Engine for [MARKET]". Two CTAs: "Book a Discovery Call" (#book) and "See What's Possible" (#examples).

3. **The Problem** — Market-specific pain points. Left column: 2-3 paragraphs describing the specific problem this market faces without characters. Right column: 4 stat cards (same layout as main page, but with market-relevant stats/proof points).

4. **Three Pillars** — Build Memory / Build Brand Authority / Blur Reality — same three pillars but each description rewritten for the specific market. Use the same icons and card structure.

5. **What We Build (for [Market])** — Same 2-column layout. Left: intro text tailored to market. Right: 8 service items, same titles but descriptions rewritten for market context.

6. **Use Cases** — REPLACES the Character Roster section. Instead of showing characters, show 3 specific use case cards for this market. Each card has a title, description, and "what it looks like" bullet points. Use the same `.character-card` styling but adapt the inner content.

7. **Two Paths** — Same structure (Build Your Own / License Ours) but descriptions tailored to the market.

8. **How It Works** — Same 4 steps, same structure. Minor copy tweaks if needed for market context.

9. **Final CTA** — Market-specific headline. "Book a 30-minute discovery call. We'll explore what a living character can do for your [market-specific thing]." Link: https://calendly.com/mornings-mitl

10. **Footer** — Includes two sections:
    - "Character Engine is also for:" with links to ALL other market pages
    - "MiTL Network" links: Character Engine (/), MiTL Studio, Mornings in the Lab

## Technical Requirements
- Each page lives in its own folder: `/ecommerce/index.html`, `/realestate/index.html`, etc.
- CSS references: `<link rel="stylesheet" href="../base.css">` and `<link rel="stylesheet" href="../style.css">`
- Font link same as main page
- Same JS at bottom for theme toggle, header scroll, and fade-in observer
- Logo href should be `../` to go back to main page
- All internal anchor links use # (same page)
- data-theme="dark" default
- All sections use the same CSS classes as the main page

## Footer HTML Template
```html
<footer class="footer">
  <div class="container">
    <div style="text-align: center; margin-bottom: var(--space-6);">
      <div class="section-label" style="margin-bottom: var(--space-3);">Character Engine Is Also For</div>
      <div style="display: flex; flex-wrap: wrap; gap: var(--space-3); justify-content: center;">
        <a href="../ecommerce/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">E-Commerce</a>
        <a href="../realestate/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">Real Estate</a>
        <a href="../restaurants/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">Restaurants</a>
        <a href="../fitness/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">Fitness</a>
        <a href="../podcasters/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">Podcasters</a>
        <a href="../agencies/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">Agencies</a>
        <a href="../creators/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">Creators</a>
        <a href="../saas/" class="btn btn--ghost" style="font-size: var(--text-xs); padding: var(--space-2) var(--space-4);">SaaS</a>
      </div>
    </div>
    <div style="display: flex; align-items: center; justify-content: space-between; padding-top: var(--space-4); border-top: 1px solid var(--color-border);">
      <div class="footer-text">&copy; 2026 MiTL Studio. Character Engine.</div>
      <div class="footer-links">
        <a href="../">Character Engine</a>
        <a href="https://mitl.studio" target="_blank" rel="noopener noreferrer">MiTL Studio</a>
        <a href="https://mornings.live" target="_blank" rel="noopener noreferrer">Mornings in the Lab</a>
      </div>
    </div>
  </div>
</footer>
```

NOTE: Each page should EXCLUDE its own link from the "Also For" section. E.g., the ecommerce page should not link to itself.
