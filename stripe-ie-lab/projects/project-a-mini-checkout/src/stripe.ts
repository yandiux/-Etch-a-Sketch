import Stripe from "stripe";

const secretKey = process.env.STRIPE_SECRET_KEY;

if (!secretKey) {
  throw new Error("STRIPE_SECRET_KEY is required. Copy .env.example to .env");
}

export const stripe = new Stripe(secretKey, {
  typescript: true,
});
