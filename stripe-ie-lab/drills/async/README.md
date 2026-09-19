# Async / Promise drills (weeks 1–2)

Spend **15–20 minutes per drill**, then redo the next day without opening the solution.

## Files

| File | Skill |
|------|--------|
| [retry.ts](./retry.ts) | Backoff retry around flaky API calls |
| [concurrency-limit.ts](./concurrency-limit.ts) | `mapWithConcurrency` — max N Stripe retrieves in flight |
| [promise-styles.ts](./promise-styles.ts) | Callback → `.then` → `async/await` |

## How to run

From repo root:

```bash
npx tsx stripe-ie-lab/drills/async/retry.ts
npx tsx stripe-ie-lab/drills/async/concurrency-limit.ts
```

## Practice mode

1. Copy a file to `retry.practice.ts` (etc.).
2. Delete the function body.
3. Re-implement from the spec in comments.
4. Compare **one** difference to the reference—not line-by-line copy.

## IE tie-in

- **Retry:** use for idempotent GETs or creates **with** idempotency keys—not blind retries on non-idempotent updates.
- **Concurrency limit:** avoids rate limits when reconciling many PaymentIntents.
- **`Promise.all`:** fine for independent reads; dangerous for money movement unless each step is isolated and idempotent.

## Optional: read Stripe SDK

In `node_modules/stripe/esm/`, pick one resource method and trace how it returns a `Promise` and attaches `lastResponse.requestId`.
