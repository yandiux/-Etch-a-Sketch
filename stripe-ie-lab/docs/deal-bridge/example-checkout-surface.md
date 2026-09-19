# Example — Checkout surface (sample job-bridge note)

_Fill with your real deal details; this shows the expected depth._

## Surface name

Hosted Checkout for one-time implementation fees

## Inputs

- Merchant admin clicks “Pay setup fee” in internal portal
- Backend `POST /internal/checkout` with `customerEmail`, optional `priceId`

## Outputs

- Stripe Checkout Session (`mode=payment`)
- Webhook: `checkout.session.completed` → mark deal stage “paid”

## Failure modes

| Failure | User impact | Detection | Mitigation |
|---------|-------------|-----------|------------|
| Missing idempotency key on retry | Duplicate sessions | Two sessions same email/minute | Require `Idempotency-Key` header |
| Webhook delay | UI stuck “pending” | Dashboard delivery lag | Poll session status + idempotent webhook |

## Stripe docs

- [Checkout quickstart](https://docs.stripe.com/checkout/quickstart)
- [Idempotent requests](https://docs.stripe.com/api/idempotent_requests)

## Test mode rehearsal

| Step | Test object ID | Date |
|------|----------------|------|
| Create session | cs_test_… | _your date_ |
| Pay 4242 card | pi_… | |

## Open questions

- Connect vs direct charge for this merchant?
