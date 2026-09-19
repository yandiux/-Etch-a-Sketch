# Project A — Mini checkout backend

Express + TypeScript + Stripe Checkout Session with **idempotency keys** and **structured JSON logging**.

## Prerequisites

- Node 20+
- [Stripe test API key](https://dashboard.stripe.com/test/apikeys)

## Setup

```bash
npm install
cp .env.example .env
# Set STRIPE_SECRET_KEY=sk_test_...
npm run dev
```

Server listens on `http://localhost:4242`.

## Create a checkout session

**Option 1 — dynamic line item (no Price ID required):**

```bash
curl -s -X POST http://localhost:4242/checkout \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: demo-checkout-001' \
  -d '{"customerEmail":"you@example.com"}' | jq
```

**Option 2 — existing test Price:**

```bash
curl -s -X POST http://localhost:4242/checkout \
  -H 'Content-Type: application/json' \
  -d '{"priceId":"price_REPLACE_ME","quantity":1}' | jq
```

Open the `url` field in a browser and pay with test card `4242 4242 4242 4242`.

## Idempotency

Repeat the same request with the same `Idempotency-Key` (or `idempotencyKey` in JSON). Stripe returns the **same** Checkout Session instead of creating duplicates—critical for safe retries from your merchant’s backend.

## IE checklist (Project A)

| Item | Implemented |
|------|-------------|
| Test mode keys via env | Yes |
| Idempotency on create | Yes |
| Structured logs (`requestId`, Stripe request id) | Yes |
| Clear error response on API failure | Yes |
| README + `.env.example` | Yes |

## Next

Project B adds webhooks and event deduplication: [../project-b-webhook-worker](../project-b-webhook-worker/)
