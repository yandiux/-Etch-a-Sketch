# Stripe Integration Engineer Learning Lab

Project-first Node/TypeScript practice aligned with integration engineer (IE) work: checkout APIs, webhooks, idempotency, and async patterns.

## Projects

| Project | Folder | Status |
|---------|--------|--------|
| A — Mini checkout backend | [project-a-mini-checkout](./projects/project-a-mini-checkout/) | Ready to run |
| B — Webhook worker | [project-b-webhook-worker](./projects/project-b-webhook-worker/) | Ready to run |
| C — Integration hardening lab | [project-c-hardening-lab](./projects/project-c-hardening-lab/) | Starter + runbook template |

## Async drills

Hands-on Promise exercises used in weeks 1–2: [drills/async](./drills/async/)

## Mentor path (start here if you’re not “an engineer yet”)

- [Mentor guide — phases, rules, weekly template](./docs/MENTOR-GUIDE.md)
- [Learning resources — Scrimba + javascript.info order](./docs/LEARNING-RESOURCES.md)

## Job bridge & career

- [Deal integration notes template](./docs/deal-bridge/integration-surface-template.md)
- [Weekly 1h job-bridge log](./docs/deal-bridge/weekly-bridge-log-template.md)
- [Manager alignment — IE title outcomes](./docs/manager-align.md)

## Scrimba protocol

When using Scrimba Pro: max ~90 min/week, only async/fetch modules, and **pause every 3–5 minutes** to re-implement the last snippet in a blank file. See each project README for the current milestone before starting new course modules.

## Quick start

```bash
cd projects/project-a-mini-checkout
cp .env.example .env
# Add STRIPE_SECRET_KEY from https://dashboard.stripe.com/test/apikeys
npm install
npm run dev
```

Then create a checkout session:

```bash
curl -s -X POST http://localhost:4242/checkout \
  -H 'Content-Type: application/json' \
  -d '{"priceId":"price_xxx"}' | jq
```

Replace `price_xxx` with a test Price ID from your Dashboard, or use `lineItems` as documented in Project A README.
