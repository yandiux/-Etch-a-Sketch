import "dotenv/config";
import express from "express";
import Stripe from "stripe";
import { EventStore } from "./event-store.js";
import { createWebhookHandler } from "./webhook.js";
import { log } from "./logger.js";

const secretKey = process.env.STRIPE_SECRET_KEY;
if (!secretKey) {
  throw new Error("STRIPE_SECRET_KEY is required");
}

const stripe = new Stripe(secretKey, { typescript: true });
const store = new EventStore(process.env.SQLITE_PATH ?? "./data/events.sqlite");

const app = express();

app.get("/health", (_req, res) => {
  res.json({ ok: true });
});

app.post(
  "/webhook",
  express.raw({ type: "application/json" }),
  createWebhookHandler(stripe, store),
);

const port = Number(process.env.PORT ?? 4243);
app.listen(port, () => {
  log.info("webhook.server.started", { port });
});
