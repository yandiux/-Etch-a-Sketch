# Project B — Webhook worker

Verify `Stripe-Signature`, handle key events, and **dedupe by `event.id`** before returning 2xx.

## Setup

```bash
npm install
cp .env.example .env
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_WEBHOOK_SECRET=whsec_... (from Stripe CLI or Dashboard endpoint)
npm run dev
```

Listens on `http://localhost:4243/webhook`.

## Stripe CLI forwarding (recommended)

Install [Stripe CLI](https://stripe.com/docs/stripe-cli), then:

```bash
stripe login
stripe listen --forward-to localhost:4243/webhook
```

Copy the `whsec_...` signing secret into `.env` as `STRIPE_WEBHOOK_SECRET`.

Trigger test events:

```bash
stripe trigger checkout.session.completed
stripe trigger payment_intent.payment_failed
```

Watch JSON logs for `webhook.processed` and handler lines.

## ngrok alternative

```bash
ngrok http 4243
```

Create a webhook endpoint in the [Dashboard](https://dashboard.stripe.com/test/webhooks) pointing to `https://YOUR_SUBDOMAIN.ngrok.io/webhook`, select events, and use the endpoint signing secret in `.env`.

## Idempotency

`processed_events` SQLite table stores `event_id`. Duplicates log `webhook.duplicate` and still return 200—Stripe may retry the same event.

## Fixture replay

For unsigned local experiments (expect 400 unless you set a valid signature):

```bash
npm run test:replay -- fixtures/sample-event.json
```

Prefer `stripe trigger` for end-to-end signature verification.

## IE checklist (Project B)

| Item | Implemented |
|------|-------------|
| Raw body for signature | Yes |
| `constructEvent` verification | Yes |
| Durable dedupe before 2xx | Yes |
| Handlers for `checkout.session.completed`, `payment_intent.payment_failed` | Yes |
| Stripe CLI / ngrok docs | Yes |

## Next

Project C: retries, rate limits, stripe-mock tests — [../project-c-hardening-lab](../project-c-hardening-lab/)
