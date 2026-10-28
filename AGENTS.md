# Color Learning project instructions

Deployable source is dist/. Preserve the existing vocabulary, notes, styling, navigation, and accessibility behavior. build.py and notes_content.py generate the HTML; run them from the repository root. GitHub Pages publishes dist/ from main.

Use plain descriptive copy, preserve keyboard focus and reduced motion, and do not add emoji or text-glyph substitute UI icons. Keep page bodies and CSS unchanged during metadata-only work.

## Link previews and publishing

Before deploying this website, apply the [LLM Instruction Toolkit link-preview guidance](https://github.com/Pythonidaer/llm-instruction-toolkit/blob/main/design/publishing/link-previews.md). Prepare appropriate page metadata and share images, preserve the intended audience and indexing policy, and verify deployed URLs. Report actual platform-preview observations separately from implementation and asset checks.

Preview configuration is preview-config.json. Run python3 scripts/link-previews.py after editing or regenerating HTML; use --check for a read-only validation. Keep page-specific descriptions, production URLs, and versioned share images aligned. Do not alter learning layouts or publish a social post as part of preview verification.
