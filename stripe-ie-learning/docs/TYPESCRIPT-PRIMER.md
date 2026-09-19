# TypeScript primer — zero assumed knowledge

You already use **JavaScript** ideas (variables, functions, objects). **TypeScript is JavaScript plus labels on data** so your editor catches mistakes before you run code.

You do **not** need to master TypeScript before Phase 0. Learn **async JS first**, then read this in **one week** when you open Project A.

---

## Mental model (one sentence)

> TypeScript describes **what shape** values have (string, number, object with fields); the computer **erases** those labels when the code runs — it is still JavaScript underneath.

---

## The only syntax you need for Project A/B

### 1. Types on variables and parameters

```typescript
const name: string = "checkout";
const port: number = 4242;

function greet(user: string): string {
  return `Hello, ${user}`;
}
```

Read `: string` as “must be text”, `: number` as “must be a number”, after `): string` as “this function returns text”.

### 2. Objects — `interface` or `type`

```typescript
type CheckoutBody = {
  priceId?: string;   // ? = optional
  quantity?: number;
};
```

This matches JSON bodies on API routes. Optional `?` means the field might be missing.

### 3. `import` / `export`

Same as modern JS modules. You will see:

```typescript
import { log } from "./logger.js";
export async function createCheckoutHandler() { ... }
```

The `.js` in the path is a TypeScript + Node quirk — the file on disk is still `.ts`.

### 4. `async` / `await`

Identical to JavaScript. Types only add what the Promise **resolves to**:

```typescript
async function load(): Promise<{ id: string }> {
  return { id: "cs_123" };
}
```

### 5. `unknown` and narrowing (when you see errors)

```typescript
catch (err) {
  const message = err instanceof Error ? err.message : "Unknown error";
}
```

You will copy this pattern for API errors — no need to invent it.

---

## What you can ignore for now

- Generics deep dives (`<T>` everywhere)
- `enum`, decorators, advanced utility types
- Strict compiler flags debate
- Converting class hierarchies from OOP courses

---

## 90-minute desk path (after Phase 0 async)

Do in one or two sittings with a laptop:

1. Read [TS Handbook — Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) (stop at **union types**)
2. Read [TS Handbook — Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html) (interfaces vs types — skim)
3. Open `projects/project-a-mini-checkout/src/checkout.ts` and label every `: Something` you see using the handbook
4. Change nothing; run `npm run typecheck` and notice errors only appear when types lie

**Commute (no laptop):** read Everyday Types on your phone; do not install anything on the bus.

---

## When TypeScript feels scary

Ask: **“What shape is this JSON?”** Write a `type` with those fields. That is 80% of IE TypeScript.

If stuck, paste the file and error in your weekly mentor message — that is normal at your stage.
