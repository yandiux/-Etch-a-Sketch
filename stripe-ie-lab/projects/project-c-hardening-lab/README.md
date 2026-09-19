# Project C — Integration hardening lab (weeks 5–8)

Clone **one pain point** from your live deal: retries, rate limits, partial failures, and observability.

## Starter scope

1. Import shared patterns from [../../drills/async/retry.ts](../../drills/async/retry.ts) into your API client wrapper.
2. Add integration tests against [stripe-mock](https://github.com/stripe/stripe-mock) (Docker):

```bash
docker run --rm -it -p 12111-12112:12111-12112 stripe/stripe-mock:latest
```

Point `STRIPE_API_BASE` at `http://localhost:12111` in test env only.

3. Fill in [RUNBOOK.md](./RUNBOOK.md) for your scenario.

## Suggested layout (you extend)

```
project-c-hardening-lab/
  src/
    StripeClientWrapper.ts   # composition over subclassing
    errors.ts                # IntegrationError with isRetryable
  tests/
    checkout.integration.test.ts
  RUNBOOK.md
```

## IE checklist

- [ ] Exponential backoff on retryable Stripe errors (429, 5xx)
- [ ] Idempotency keys on all create paths
- [ ] Webhook lag / failure runbook
- [ ] Tests that run in CI without live keys
