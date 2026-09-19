import "dotenv/config";
import express from "express";
import { createCheckoutHandler } from "./checkout.js";
import { log } from "./logger.js";

const app = express();
app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({ ok: true });
});

app.post("/checkout", (req, res) => {
  void createCheckoutHandler(req, res);
});

app.get("/success", (_req, res) => {
  res.send("Payment succeeded (demo success page).");
});

app.get("/cancel", (_req, res) => {
  res.send("Checkout canceled.");
});

const port = Number(process.env.PORT ?? 4242);

app.listen(port, () => {
  log.info("server.started", { port });
});
