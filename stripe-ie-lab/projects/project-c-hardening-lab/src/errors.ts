/** IE-friendly errors for logs and HTTP mapping */

export class IntegrationError extends Error {
  readonly code: string;
  readonly httpStatus: number;
  readonly isRetryable: boolean;

  constructor(
    message: string,
    options: { code: string; httpStatus: number; isRetryable: boolean },
  ) {
    super(message);
    this.name = "IntegrationError";
    this.code = options.code;
    this.httpStatus = options.httpStatus;
    this.isRetryable = options.isRetryable;
  }
}

export function fromStripeStatus(statusCode: number, message: string): IntegrationError {
  const retryable = statusCode === 429 || statusCode >= 500;
  return new IntegrationError(message, {
    code: `stripe_http_${statusCode}`,
    httpStatus: statusCode >= 400 && statusCode < 600 ? statusCode : 502,
    isRetryable: retryable,
  });
}
