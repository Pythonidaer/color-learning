# Color Learning design decisions

## Link-preview guidance trial (October 27, 2026)

Applied llm-instruction-toolkit/design/publishing/link-previews.md to this public GitHub Pages site. Added the rule to AGENTS.md, a maintained preview configuration, idempotent standard-library metadata generation/checks, page-specific 1200×630 PNG images, browser icons, and an image sitemap. The deployment workflow prepares and validates preview metadata before uploading dist/.

Design: use the site's existing white/charcoal reading identity; preserve the site-specific mark and color accents in the covers. Covers are original code-rendered typography/layout assets using open DejaVu fonts, rather than replicas of the live font specimens or page screenshots. Brief page-specific titles/subtitles stay inside generous margins. Native page bodies, interactions, CSS, and roadmap geometry are unchanged. Existing public access/indexing behavior is preserved; no robots restrictions were removed and no private Site was made public. No unsupported rich-result markup or new manifest is needed for this scope.

Validation: all deployed HTML pages are configured; metadata identity tags are unique; canonical and Open Graph URLs align; production paths retain the repository subdirectory; PNG signatures/dimensions and icon assets pass checks. Reapplying the generator is byte-identical. Every HTML body is identical to its pre-change source. Actual platform preview selection and cache refresh remain distinct from these checks.

Deployment compatibility: updated actions/upload-pages-artifact from v3 to v4 to match the supported artifact generation used by the other learning site; retained its existing Pages environment and deployment flow.
