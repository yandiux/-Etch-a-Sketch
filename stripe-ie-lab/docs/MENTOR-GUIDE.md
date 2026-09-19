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

Goal: comfort with **async JavaScript**. TypeScript is **not** part of Phase 0.

You do **not** need to know TypeScript yet. Project A is written in TS, but you only open it **after** Phase 0 + the [90-minute TypeScript primer](./TYPESCRIPT-PRIMER.md). Until then, all drills are plain `.ts` files you can treat like JS with extra labels.

**Do not rush Project A** until Phase 0 checks pass.

### Phase 0 exit checklist

- [ ] I can draw sync vs async on paper (call stack vs “later”)
- [ ] I wrote `retry` from memory in a blank file (compare once to `drills/async/retry.ts`)
- [ ] I wrote `mapWithConcurrency` from memory OR explained every line of the reference
- [ ] I read [javascript.info — Promise basics](https://javascript.info/promise-basics) and [async/await](https://javascript.info/async-await)
- [ ] I completed one Scrimba async section using **pause-and-retype** (not watch-only)

**Estimated time:** 2–3 weeks at 5 h/week if async is hard; 1 week if it clicks.

## Phase 0.5 — TypeScript (about 90 minutes, after Phase 0)

- Read [TYPESCRIPT-PRIMER.md](./TYPESCRIPT-PRIMER.md)
- Handbook: [Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) (commute-friendly)
- **Do not** start a full TS video course

## Phase 1 — First shippable integration (Project A)

Only after Phase 0 **and** Phase 0.5.

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

## GitHub + how we work day to day

### Do you need to push to GitHub?

**Yes, eventually — but for learning, not for show.** Git is how you (and I) see progress: drills, notes, small commits. You do **not** need a public repo or a perfect history.

**Recommended setup**

1. Create a **private** GitHub repo, e.g. `stripe-ie-learning` (free private repos are fine).
2. Copy the `stripe-ie-lab/` folder into it (or merge the PR from this workspace if that repo is yours).
3. Work on **`main`** or short branches like `week-1-async` — no need for fancy git flow while learning.
4. Commit small and often:
   - `drills/async/retry.practice.ts`
   - filled weekly log under `docs/deal-bridge/logs/`
   - Project A when you reach Phase 1

**Never commit:** `.env`, `sk_live_`, `sk_test_` in code, customer names, deal details you cannot share. Use `.env` (already gitignored in projects).

### How you and I (Cursor / Cloud Agent) work together

This is **not** a live daily standup. It works like a mentor you message when you do the work:

1. You do the **weekly block** (Phase 0 reading, Scrimba, one drill).
2. You **push to your private repo** (optional but good habit).
3. You send a message with the **weekly template** (above) + paste errors or `@` files from your repo.
4. I respond with: what to fix, what to skip, and **one goal** for next week — not a new course list.

If you open this project in Cursor on the same repo, I can read your files and edit with you. If you only chat without a repo, paste code snippets and error text — that still works, but GitHub helps.

### What about the PR in this workspace?

The lab was added on branch `cursor/ie-learning-lab-22f2` in `-Etch-a-Sketch`. If that repo is just a sandbox:

- **Copy** `stripe-ie-lab/` to your **own private repo** and treat that as home base.
- If it *is* your repo, merge the PR when you want and clone locally to your machine.

### Minimum rhythm

| When | Action |
|------|--------|
| After each study session | Save file locally; commit if you use Git |
| Once per week | Push to GitHub + send weekly template here |
| When stuck 45+ min | Message with exact error + what you tried |

Progress = **files you wrote** + **weekly message**, not hours of video.
