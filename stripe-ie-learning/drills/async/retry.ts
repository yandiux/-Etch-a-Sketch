/**
 * Drill: implement retry without a library.
 * Run: npx tsx drills/async/retry.ts
 */

export type RetryOptions = {
  maxAttempts: number;
  backoffMs: number;
};

export async function retry<T>(
  fn: () => Promise<T>,
  options: RetryOptions,
): Promise<T> {
  const { maxAttempts, backoffMs } = options;
  let lastError: unknown;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt === maxAttempts) {
        break;
      }
      await sleep(backoffMs * attempt);
    }
  }

  throw lastError;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// --- self-test (remove or cover with tests when practicing) ---

async function demo(): Promise<void> {
  let calls = 0;
  const result = await retry(
    async () => {
      calls += 1;
      if (calls < 3) {
        throw new Error("transient");
      }
      return "ok";
    },
    { maxAttempts: 5, backoffMs: 10 },
  );
  console.log("retry demo:", result, "calls:", calls);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  demo().catch(console.error);
}
