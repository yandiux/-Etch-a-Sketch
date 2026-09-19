import type { Request, Response } from "express";
import type Stripe from "stripe";
import { randomUUID } from "crypto";
import { stripe } from "./stripe.js";
import { log } from "./logger.js";

type CheckoutBody = {
  priceId?: string;
  quantity?: number;
  /** Client-supplied key groups retries into one Stripe object */
  idempotencyKey?: string;
  customerEmail?: string;
};

export async function createCheckoutHandler(
  req: Request,
  res: Response,
): Promise<void> {
  const requestId = (req.headers["x-request-id"] as string) ?? randomUUID();
  const body = req.body as CheckoutBody;

  const successUrl =
    process.env.CHECKOUT_SUCCESS_URL ?? "http://localhost:4242/success";
  const cancelUrl =
    process.env.CHECKOUT_CANCEL_URL ?? "http://localhost:4242/cancel";

  const idempotencyKey =
    body.idempotencyKey ?? (req.headers["idempotency-key"] as string) ?? requestId;

  log.info("checkout.create.start", {
    requestId,
    idempotencyKey,
    priceId: body.priceId,
  });

  try {
    let sessionParams: Stripe.Checkout.SessionCreateParams;

    if (body.priceId) {
      sessionParams = {
        mode: "payment",
        line_items: [
          {
            price: body.priceId,
            quantity: body.quantity ?? 1,
          },
        ],
        success_url: successUrl,
        cancel_url: cancelUrl,
        customer_email: body.customerEmail,
      };
    } else {
      // Demo-friendly default when no Price exists yet (test mode)
      sessionParams = {
        mode: "payment",
        line_items: [
          {
            price_data: {
              currency: "usd",
              product_data: { name: "IE Lab Demo Item" },
              unit_amount: 2000,
            },
            quantity: 1,
          },
        ],
        success_url: successUrl,
        cancel_url: cancelUrl,
        customer_email: body.customerEmail,
      };
    }

    const session = await stripe.checkout.sessions.create(sessionParams, {
      idempotencyKey,
    });

    log.info("checkout.create.success", {
      requestId,
      idempotencyKey,
      stripeRequestId: session.lastResponse?.requestId,
      sessionId: session.id,
    });

    res.status(201).json({
      requestId,
      idempotencyKey,
      sessionId: session.id,
      url: session.url,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    log.error("checkout.create.failed", {
      requestId,
      idempotencyKey,
      error: message,
    });
    res.status(502).json({ requestId, error: message });
  }
}
