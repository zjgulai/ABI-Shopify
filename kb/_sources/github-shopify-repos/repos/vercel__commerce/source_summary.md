---
title: GitHub Source Summary - vercel/commerce
type: source_snapshot
source: https://github.com/vercel/commerce
captured_at: 2026-06-28T08:57:42+0800
verification_status: local_readonly_snapshot
---

# vercel/commerce

- priority: P2
- bucket: Generic commerce architecture
- target_nodes: 02, 06
- default_branch: `main`
- head_sha_prefix: `3761e52e60df`
- readme: `README.md` / sha256 `b9d78355cc850960`
- license: `not_found` / hint `unknown` / sha256 `not_found`
- risk_note: high quality but not Shopify-native; use only as architecture reference

## README Signals
- # Next.js Commerce
- ## Providers
- Vercel will only be actively maintaining a Shopify version [as outlined in our vision and strategy for Next.js Commerce](https://github.com/vercel/commerce/pull/966).
- Vercel is happy to partner and work with any commerce provider to help them get a similar template up and running and listed below. Alternative providers should be able to fork this repository and swap out the `lib/sh...
- - Shopify (this repository)
- - [Fourthwall](https://github.com/FourthwallHQ/vercel-commerce) ([Demo](https://vercel-storefront.fourthwall.app/))
- ## Integrations
- ## Running locally
- > Note: You should not commit your `.env` file or it will expose secrets that will allow others to control your Shopify store.
- 1. Install Vercel CLI: `npm i -g vercel`
- 1. Connect to the existing `commerce-shopify` project.
- ## Vercel, Next.js Commerce, and Shopify Integration Guide

## Boundary
This is a local read-only source snapshot. It is not a license grant, implementation endorsement, or permission to use live Shopify credentials.
