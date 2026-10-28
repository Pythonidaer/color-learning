# Color Learning

A growing reference for color vocabulary, interface design, and accessibility.

The site is in `dist/`. Run `python3 build.py` and `python3 notes_content.py`, then `python3 scripts/link-previews.py` to regenerate the HTML after editing content. Serve the repository with `python3 -m http.server 8000` and visit `/dist/`.

GitHub Actions publishes `dist/` to GitHub Pages.

## Link previews

Social previews follow the [toolkit publishing instructions](https://github.com/Pythonidaer/llm-instruction-toolkit/blob/main/design/publishing/link-previews.md), referenced in AGENTS.md. Every HTML page has its own title, description, canonical/Open Graph URL, 1200×630 PNG cover, image alternative text, and large-image social-card metadata in the initial HTML. Browser/touch icons and an image sitemap are included.

Configuration: preview-config.json. After editing or regenerating HTML:

```sh
python3 scripts/link-previews.py
python3 scripts/link-previews.py --check
```

GitHub Actions applies and validates these settings before deployment. The script is idempotent and leaves page bodies and styles unchanged. New pages require a configuration entry and a cover, so the checker catches incomplete coverage.

Images are committed under dist/assets/previews/. Their optional source tool is scripts/render-preview-images.py (Pillow and DejaVu fonts required; CI does not need those dependencies). Covers use neutral typography and existing site colors; the color covers use the existing burgundy mark with restrained warm/cool swatches. Change the versioned image URL when replacing an already shared image.

Sitemap: https://pythonidaer.github.io/color-learning/sitemap.xml

To inspect an actual platform's cached preview, paste a public page URL into https://www.linkedin.com/post-inspector/ or https://developers.facebook.com/tools/debug/ . These may require the user's account. Asset/metadata checks do not demonstrate that a social network has refreshed its preview, and Google controls indexing and search thumbnails. No social posts are created by these scripts.
