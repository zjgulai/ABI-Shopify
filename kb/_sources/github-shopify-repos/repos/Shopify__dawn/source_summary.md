---
title: GitHub Source Summary - Shopify/dawn
type: source_snapshot
source: https://github.com/Shopify/dawn
captured_at: 2026-06-28T08:57:42+0800
verification_status: local_readonly_snapshot
---

# Shopify/dawn

- priority: P0
- bucket: Theme
- target_nodes: 02, 03, 06
- default_branch: `main`
- head_sha_prefix: `83d5e6b4094d`
- readme: `README.md` / sha256 `c8bed296b25969d8`
- license: `LICENSE.md` / hint `custom/copyright` / sha256 `189bbb2c31786bdb`
- risk_note: official reference theme; source-available/license must be respected

## README Signals
- # Dawn
- [Theme Store submission](#theme-store-submission) |
- Dawn represents a HTML-first, JavaScript-only-as-needed approach to theme development. It's Shopify's first source available theme with performance, flexibility, and [Online Store 2.0 features](https://www.shopify.com...
- * **Lean, fast, and reliable:** Functionality and design defaults to “no” until it meets this requirement. Code ships on quality. Themes must be built with purpose. They shouldn’t support each and every feature in Sho...
- * **Server-rendered:** HTML must be rendered by Shopify servers using Liquid. Business logic and platform primitives such as translations and money formatting don’t belong on the client. Async and on-demand rendering ...
- You can find a more detailed version of our theme code principles in the [contribution guide](https://github.com/Shopify/dawn/blob/main/.github/CONTRIBUTING.md#theme-code-principles).
- ## Getting started
- We recommend using Dawn as a starting point for theme development. [Learn more on Shopify.dev](https://shopify.dev/themes/getting-started/create).
- > If you're building a theme for the Shopify Theme Store, then you can use Dawn as a starting point. However, the theme that you submit needs to be [substantively different from Dawn](https://shopify.dev/themes/store/...
- Please note that the main branch may include code for features not yet released. The "stable" version of Dawn is available in the theme store.
- ## Staying up to date with Dawn changes
- Say you're building a new theme off Dawn but you still want to be able to pull in the latest changes, you can add a remote `upstream` pointing to this Dawn repository.

## Boundary
This is a local read-only source snapshot. It is not a license grant, implementation endorsement, or permission to use live Shopify credentials.
