import type Stripe from "stripe";
import { log } from "./logger.js";

/** Side effects for your app would live here (fulfillment, CRM, etc.) */
export function handleStripeEvent(event: Stripe.Event): void {
  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object as Stripe.Checkout.Session;
      log.info("handler.checkout.session.completed", {
        eventId: event.id,
        sessionId: session.id,
        paymentStatus: session.payment_status,
      });
      break;
    }
    case "payment_intent.payment_failed": {
      const pi = event.data.object as Stripe.PaymentIntent;
      log.info("handler.payment_intent.payment_failed", {
        eventId: event.id,
        paymentIntentId: pi.id,
        lastPaymentError: pi.last_payment_error?.message,
      });
      break;
    }
    default:
      log.info("handler.ignored", { eventId: event.id, type: event.type });
  }
}
