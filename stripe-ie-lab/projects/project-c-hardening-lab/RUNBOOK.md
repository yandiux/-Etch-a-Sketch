# Runbook template — fill for your deal

## Service

- **Name:**
- **Owner:**
- **Stripe mode:** test / live

## Symptom: Webhook lag > ___ minutes

1. Check Stripe Dashboard → Developers → Webhooks → event delivery logs for this endpoint.
2. Confirm worker health: `GET /health` on Project B server.
3. Inspect SQLite (or prod store): `SELECT * FROM processed_events ORDER BY processed_at DESC LIMIT 20;`
4. Verify `STRIPE_WEBHOOK_SECRET` matches the active endpoint (CLI vs Dashboard vs ngrok URL rotation).

## Symptom: Duplicate fulfillment

1. Confirm dedupe key is **`event.id`**, not object id alone.
2. Search logs for `webhook.duplicate` — should be safe no-ops.
3. Ensure handler returns 500 only before `markProcessed` completes.

## Symptom: Elevated 402 / card errors

1. Distinguish merchant misconfiguration vs integration bug (metadata, connected account, etc.).
2. Pull `payment_intent.payment_failed` events for sample `last_payment_error.code`.

## Escalation

- **Internal:**
- **Stripe support / TAM:**

## Test IDs used in last rehearsal

| Object | ID | Notes |
|--------|-----|-------|
| | | |
