/**
 * Drill: same logic three ways — callback → .then → async/await.
 * Practice by deleting implementations and rewriting from memory.
 */

type FetchCb = (
  id: string,
  cb: (err: Error | null, data?: { id: string }) => void,
) => void;

function fakeFetch(id: string): Promise<{ id: string }> {
  return new Promise((resolve) => {
    setTimeout(() => resolve({ id }), 10);
  });
}

// 1) Callback style (legacy integrations)
export function getLabelCallback(fetch: FetchCb, id: string, cb: (label: string) => void): void {
  fetch(id, (err, data) => {
    if (err || !data) {
      cb("unknown");
      return;
    }
    cb(`payment:${data.id}`);
  });
}

// 2) Promise chain
export function getLabelThen(id: string): Promise<string> {
  return fakeFetch(id).then((data) => `payment:${data.id}`);
}

// 3) async/await
export async function getLabelAsync(id: string): Promise<string> {
  const data = await fakeFetch(id);
  return `payment:${data.id}`;
}
