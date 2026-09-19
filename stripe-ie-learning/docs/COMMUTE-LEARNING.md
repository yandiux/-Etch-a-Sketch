# Commute learning (bus, no laptop)

Use dead time to **understand** ideas. **Typing code** still happens at a desk — that is what avoids tutorial hell.

## Golden rule

| On the bus | At home (even 20 min) |
|------------|------------------------|
| Read, listen, predict answers | Re-type one tiny example from memory |
| One section = one idea | One file in `drills/async/` |

If you only commute-study all week, do **one** 20-minute desk session before Friday.

---

## Best reads (phone browser)

Work through in order; bookmark where you stop.

1. **[javascript.info — Promises](https://javascript.info/promise-basics)** → chaining → error handling → [async/await](https://javascript.info/async-await)  
   *Best ROI for IE. Read slowly; cover the “why not callbacks?” parts.*

2. **[MDN — Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)**  
   *Reference when you forget `all` vs `allSettled`.*

3. **[Stripe Docs — How webhooks work](https://docs.stripe.com/webhooks)** (skim once, re-read before Project B)  
   *You know the business side; this is the delivery/retry mental model.*

4. **[Stripe Docs — Idempotent requests](https://docs.stripe.com/api/idempotent_requests)**  
   *Short; read twice on separate commutes.*

5. **Internal Stripe** (if you have mobile access): one solved integration note or design doc from a similar deal — 10 min, not Slack rabbit holes.

## Short video (offline: download in YouTube Premium if you use it)

- Search: **“JavaScript event loop Philip Roberts”** (~15 min, once)  
- Search: **“Promises in 100 seconds Fireship”** (overview only, then read javascript.info)

Cap commute video at **~20 min/day** — longer tends to feel productive without sticking.

## Podcasts / audio (optional)

- **[Syntax](https://syntax.fm/)** — pick episodes on **async** or **Node** (not every episode; browse titles).  
- **[JS Party](https://changelog.com/jsparty)** — same: choose async/Node/API topics only.

Audio is good for **motivation and vocabulary**, not for learning syntax — pair with javascript.info.

## Flashcard-style habits (no app required)

In Notes on your phone, keep running lists:

- **“I learned”** — one sentence after each commute read  
- **“I predict”** — before revealing MDN/docs, guess what `await` in try/catch does  
- **“IE tie-in”** — one line: “This matters because webhooks…”

Review Sunday for 5 minutes before the week.

## What NOT to do on the bus

- New Scrimba modules (you need to type along)  
- Starting a second course app  
- LeetCode / algorithm grind (wrong path for IE)  
- Long React tutorials unless your deal requires React  

## Suggested weekly commute budget

~30–45 min/day × 5 ≈ 2.5–4 h of **reading/listening**.  
Matches ~5 h/week total if desk time covers drills + one small commit.

## 2-week commute plan (Phase 0)

| Day | Commute focus |
|-----|----------------|
| Mon | javascript.info promise-basics |
| Tue | promise-chaining + error handling |
| Wed | async/await chapter |
| Thu | Stripe idempotent requests + webhook overview |
| Fri | Re-read hardest paragraph; write 3 quiz questions in Notes |
| Mon | MDN Promise methods (`all`, `allSettled`) |
| Tue | Re-read async/await; explain event loop video |
| Wed–Fri | Your choice: repeat weak chapter or Stripe webhooks deep read |

Desk that week: `retry.practice.ts` + weekly log in `docs/deal-bridge/logs/`.
