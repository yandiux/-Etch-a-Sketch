/**
 * Replays a saved event JSON to /webhook for local testing.
 * Real signatures require Stripe CLI or signing with whsec in code;
 * this script is for inspecting handler logs after `stripe trigger`.
 *
 * Usage: npm run test:replay -- path/to/event.json
 */
import fs from "node:fs";

const url = process.env.WEBHOOK_URL ?? "http://localhost:4243/webhook";
const file = process.argv[2];

if (!file) {
  console.error("Usage: npm run test:replay -- fixtures/sample-event.json");
  process.exit(1);
}

const body = fs.readFileSync(file);
const res = await fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Stripe-Signature": process.env.STRIPE_SIGNATURE ?? "t=0,v1=test",
  },
  body,
});

console.log("status", res.status);
console.log(await res.text());
