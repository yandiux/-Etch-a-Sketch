import type { Request, Response } from "express";
import Stripe from "stripe";
import { EventStore } from "./event-store.js";
import { handleStripeEvent } from "./handlers.js";
import { log } from "./logger.js";

export function createWebhookHandler(stripe: Stripe, store: EventStore) {
  return (req: Request, res: Response): void => {
    const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
    if (!webhookSecret) {
      res.status(500).json({ error: "STRIPE_WEBHOOK_SECRET not configured" });
      return;
    }

    const signature = req.headers["stripe-signature"];
    if (!signature || typeof signature !== "string") {
      res.status(400).json({ error: "Missing Stripe-Signature header" });
      return;
    }

    const rawBody = req.body as Buffer;
    if (!Buffer.isBuffer(rawBody)) {
      res.status(400).json({ error: "Expected raw body buffer" });
      return;
    }

    let event: Stripe.Event;
    try {
      event = stripe.webhooks.constructEvent(rawBody, signature, webhookSecret);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Invalid signature";
      log.warn("webhook.signature.invalid", { error: message });
      res.status(400).json({ error: message });
      return;
    }

    if (store.hasProcessed(event.id)) {
      log.info("webhook.duplicate", { eventId: event.id, type: event.type });
      res.json({ received: true, duplicate: true });
      return;
    }

    try {
      handleStripeEvent(event);
      store.markProcessed(event.id, event.type);
      log.info("webhook.processed", { eventId: event.id, type: event.type });
      res.json({ received: true });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Handler failed";
      log.error("webhook.handler.failed", {
        eventId: event.id,
        type: event.type,
        error: message,
      });
      // Return 500 so Stripe retries — handler must stay idempotent (event id dedupe)
      res.status(500).json({ error: message });
    }
  };
}
