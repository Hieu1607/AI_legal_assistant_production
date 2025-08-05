from prometheus_client import Counter, Histogram

# Define metrics
REQUEST_COUNTER = Counter(
    "http_requests_total", "Total http requests", ["method", "endpoint", "status_code"]
)
d = Histogram(
    "request_latency_seconds", "Histogram of request latency", ["method", "endpoint"]
)
GEMINI_TOKENS = Counter(
    "gemini_tokens_total", "Total tokens used in Gemini API", ["type"]
)
