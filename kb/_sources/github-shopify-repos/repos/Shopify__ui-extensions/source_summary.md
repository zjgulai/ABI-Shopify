---
title: GitHub Source Summary - Shopify/ui-extensions
type: source_snapshot
source: https://github.com/Shopify/ui-extensions
captured_at: 2026-06-28T08:57:42+0800
verification_status: local_readonly_snapshot
---

# Shopify/ui-extensions

- priority: P0
- bucket: Checkout/UI Extensions
- target_nodes: 06, 10, 91
- default_branch: `2026-07-rc`
- head_sha_prefix: `80040db41a35`
- readme: `README.md` / sha256 `0c943aa9b9e390ca`
- license: `LICENSE.md` / hint `custom/copyright` / sha256 `0873555e5ade346c`
- risk_note: extension examples can affect checkout/order surfaces; no live deployment without test store

## README Signals
- # UI Extensions
- This repo contains the public definition of Shopify’s UI extension API. App developers can use these libraries for a strongly-typed, optimized development experience that lets them focus on integrating their app’s fea...
- > **Note:** UI extensions are a [versioned API](https://shopify.dev/api/usage/versioning). This branch contains the APIs for the `2026-04-rc` API version. The following API versions are available as separate branches ...
- Shopify provides UI extension APIs via the [`@shopify/ui-extensions` package](./packages/ui-extensions/) which lets developers use a small, strongly-typed JavaScript API for creating UI extensions
- ## What are “UI extensions”?
- A UI extension is a JavaScript-based module that can hook in to client-side behaviors on any of Shopify’s first party UI surface areas. The most minimal definition of a UI extension has the following properties, which...
- - A `name` that is presented to merchants when interacting with the extension.
- - The [`target`](https://shopify.dev/docs/apps/app-extensions/configuration#targets) that the UI extension wishes to inject into. These are represented with string identifiers that describe the surface and responsibil...
- - What **imperative APIs** are provided by the host application, for reading and writing data relevant to the extension
- UI extensions are built on an open source project called, [remote-dom](https://github.com/Shopify/remote-dom), which allows them to render native UI elements while being safely sandboxed.
- > **Note:** If you are migrating from an API version prior to `2025-10`, you can follow the [migration guide](https://shopify.dev/docs/api/checkout-ui-extensions/2025-10/upgrading-to-2025-10).

## Boundary
This is a local read-only source snapshot. It is not a license grant, implementation endorsement, or permission to use live Shopify credentials.
