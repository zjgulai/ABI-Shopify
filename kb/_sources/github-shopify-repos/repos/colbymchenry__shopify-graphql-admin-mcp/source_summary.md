---
title: GitHub Source Summary - colbymchenry/shopify-graphql-admin-mcp
type: source_snapshot
source: https://github.com/colbymchenry/shopify-graphql-admin-mcp
captured_at: 2026-06-28T08:57:42+0800
verification_status: local_readonly_snapshot
---

# colbymchenry/shopify-graphql-admin-mcp

- priority: P2
- bucket: MCP/Admin GraphQL
- target_nodes: 10, 07, 91
- default_branch: `main`
- head_sha_prefix: `241ce3408f00`
- readme: `README.md` / sha256 `890af93b256c6f78`
- license: `not_found` / hint `unknown` / sha256 `not_found`
- risk_note: community MCP; admin GraphQL live-write risk high

## README Signals
- # shopify-graphql-admin-mcp
- MCP server providing full access to Shopify's Admin GraphQL API. Introspects the live schema on startup so it's always up-to-date with the latest API version — no stale docs, no embeddings needed.
- ## Features
- - **Raw GraphQL execution** — run any query or mutation against the Admin API
- - **Live schema introspection** — search and explore the full GraphQL schema (2,700+ types) directly from your AI assistant
- - **29 convenience tools** — typed, no-GraphQL-needed CRUD for products, collections, metaobjects, metafields, customers, orders, and inventory
- ## Quick Start
- # With a legacy access token
- npx shopify-graphql-admin-mcp --store mystore.myshopify.com --access-token shpat_xxxxx
- # With OAuth client credentials (Dev Dashboard app)
- npx shopify-graphql-admin-mcp --store mystore.myshopify.com --client-id YOUR_ID --client-secret YOUR_SECRET
- ## Tools

## Boundary
This is a local read-only source snapshot. It is not a license grant, implementation endorsement, or permission to use live Shopify credentials.
