# Mentor guide — how we work together

You are **not** pretending to be a senior software engineer. You are becoming someone who can **design, build, and debug Stripe integrations** in Node/TypeScript. That is a different (and reachable) goal.

## What I will do as your mentor

- **Right-size** tasks so you finish something every 1–2 weeks
- **Tell you when to stop watching courses** and write 10 lines of code
- **Unblock async/Promises** with tiny exercises before big projects
- **Connect** lab work to your deal and IE title conversation
- **Be honest** when something is optional vs required

## What you bring

- Stripe product/API context (you already have this)
- ~5 protected hours per week
- Willingness to say “I don’t understand this yet” early

## Rules (non-negotiable)

1. **One focus per week** — no new Scrimba course until the week’s milestone is done
2. **Explain aloud** — after each study block, explain the idea in 2 sentences (even alone)
3. **45-minute stuck rule** — then ask for help with a **specific** snippet or error message
4. **Git push = progress** — beats “module 12/80”

## Phase 0 — “Not an engineer yet” (you are here)

Goal: comfort with **async** and reading small TS files. **Do not rush Project A** until Phase 0 checks pass.

### Phase 0 exit checklist

- [ ] I can draw sync vs async on paper (call stack vs “later”)
- [ ] I wrote `retry` from memory in a blank file (compare once to `drills/async/retry.ts`)
- [ ] I wrote `mapWithConcurrency` from memory OR explained every line of the reference
- [ ] I read [javascript.info — Promise basics](https://javascript.info/promise-basics) and [async/await](https://javascript.info/async-await)
- [ ] I completed one Scrimba async section using **pause-and-retype** (not watch-only)

**Estimated time:** 2–3 weeks at 5 h/week if async is hard; 1 week if it clicks.

## Phase 1 — First shippable integration (Project A)

Only after Phase 0.

- Run Project A with **your** test key
- One successful Checkout in the browser
- Repeat the same `curl` with the same `Idempotency-Key` and notice the same session id

## Phase 2 — Webhooks (Project B)

- `stripe listen` + one triggered event in logs
- Explain to someone (or write in weekly log): why we dedupe `event.id`

## Phase 3 — Deal + title (Project C + manager doc)

- Fill `docs/deal-bridge/` for one real surface
- Complete `docs/manager-align.md` conversation
- One runbook section from real pain

## Weekly message template (paste to your mentor / agent)

```
Week N:
- Hours spent: 
- Phase 0 / 1 / 2:
- Done this week:
- Stuck on (exact error or concept):
- Next week ONE goal:
```

## Resources map

See [LEARNING-RESOURCES.md](./LEARNING-RESOURCES.md) for links and Scrimba discipline.
