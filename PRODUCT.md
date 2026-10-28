# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

AngularJS 1.4 + Bootstrap 3 + Flask static shell (`fancyhotel/templates/index.html`, `fancyhotel/static/views/*`, `controllers_v2.js`). MySQL backend (project requirement). No framework migration unless explicitly requested.

## Users

- **Customers** (`customer`): book rooms, manage masked payment cards, update/cancel reservations, submit and read location reviews after completed stays.
- **Managers** (`manager`): reservation/revenue/popularity reports, demand forecast, demand-based pricing rules, confirmation outbox.

Primary context: academic/demo deployment (CS 4400 / Tópicos Especiales II), local Docker at port 5001.

## Product Purpose

Online hotel reservation and operations portal for multi-location Fancy Hotel properties. Success means completing core workflows while logged in with correct role permissions and visible API outcomes (calendar, charts, masked cards, policies).

## Positioning

Combines guest self-service (reservation lifecycle + saved cards + feedback gates) with manager tooling that documents pricing/forecast rules instead of hiding them behind opaque models.

## Operating Context

- Demo credentials: customer `C0001`, manager `M0001`, password `password`.
- Locations: Atlanta, Charlotte, Savannah, Orlando, Miami.
- Room types: Single, Double, Suite.
- Confirmation delivery demonstrated via local outbox (no SMTP in demo).

## Capabilities and Constraints

- Auth with role persisted in `localStorage` (`fancyhotel.user`, `fancyhotel.role`).
- Dynamic availability calendar by location/month.
- Reservation create/update/cancel with stated refund policy on cancel.
- Payment API returns masked numbers; CVV never stored/displayed from API.
- Manager reports and Chart.js demand forecast.
- UI is not graded for course points but should remain maintainable on AngularJS 1.4.

## Brand Commitments

Product name **Fancy Hotel 4400**. Spanish UI copy acceptable for modernized fork; do not invent hotels, prices, or customer testimonials not backed by API data.

## Evidence on Hand

- Repository README and `docs/` (functional analysis, decisions).
- Synthetic/demo data from MySQL seed; charts and tables render live API JSON.
- Do not fabricate revenue benchmarks, press quotes, or third-party logos.

## Product Principles

1. Role clarity beats decorative chrome—customers and managers must never confuse portals.
2. Show policy and calculation rules in UI copy where the API implements them.
3. Preserve working routes and controllers; visual redesign must not break bindings.
4. Prefer accessible forms/tables (labels, focus, contrast, responsive tables).
5. Keep demo honesty: label synthetic/outbox behaviors explicitly.

## Accessibility & Inclusion

Target WCAG-minded contrast and keyboard focus on interactive controls; respect `prefers-reduced-motion`.
