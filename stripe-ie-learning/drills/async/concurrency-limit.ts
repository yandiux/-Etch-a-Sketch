/**
 * Drill: fetch Stripe-like resources with a concurrency cap.
 * Replace `fetchOne` with stripe.paymentIntents.retrieve(id) in real code.
 *
 * Run: npx tsx drills/async/concurrency-limit.ts
 */

export async function mapWithConcurrency<T, R>(
  items: T[],
  concurrency: number,
  worker: (item: T, index: number) => Promise<R>,
): Promise<R[]> {
  if (concurrency < 1) {
    throw new Error("concurrency must be >= 1");
  }

  const results: R[] = new Array(items.length);
  let nextIndex = 0;

  async function runWorker(): Promise<void> {
    while (true) {
      const index = nextIndex;
      nextIndex += 1;
      if (index >= items.length) {
        return;
      }
      results[index] = await worker(items[index], index);
    }
  }

  const poolSize = Math.min(concurrency, items.length);
  await Promise.all(Array.from({ length: poolSize }, () => runWorker()));
  return results;
}

// --- demo: fake async fetches ---

async function fetchOne(id: string): Promise<{ id: string; amount: number }> {
  await sleep(50);
  return { id, amount: 1000 };
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function demo(): Promise<void> {
  const ids = ["pi_1", "pi_2", "pi_3", "pi_4", "pi_5", "pi_6"];
  const started = Date.now();
  const out = await mapWithConcurrency(ids, 3, (id) => fetchOne(id));
  console.log("concurrency demo ms:", Date.now() - started);
  console.log(out);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  demo().catch(console.error);
}
