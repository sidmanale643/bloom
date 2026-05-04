Type: #type/query
Area: #area/craft/engineering
Keyword: #keyword/http #keyword/web-protocols
Date created: [[2026-05-04]]
Question: what is http explain

---

## What HTTP Is

HTTP (Hypertext Transfer Protocol) is the application-layer protocol that governs how clients and servers communicate on the web. It is a **stateless, request-response protocol** — each request from a client contains all information needed for the server to process it, and the server retains no memory of past requests.

## Core Design Decisions

**Statelessness** is the defining property. Every request must carry authentication tokens, session identifiers, and resource locators because the server treats each request as independent. This buys simplicity and scalability (requests can be distributed across any server), but forces developers to implement continuity manually via cookies, session stores, or JWTs.

**Client-server model**: the client always initiates; the server always responds. No server-initiated push in standard HTTP/1.1.

## HTTP Versions

- **HTTP/1.0** — new TCP connection per request (high handshake overhead)
- **HTTP/1.1** — persistent connections (keep-alive), chunked transfer, improved caching
- **HTTP/2** — multiplexing, binary framing, HPACK header compression, server push
- **HTTP/3** — built on QUIC/UDP, eliminates head-of-line blocking, reduces connection latency

HTTPS is HTTP running over TLS encryption. TCP was chosen historically for guaranteed delivery, though HTTP only requires a reliable transport.

## Message Structure

**Request:**
- Method + Resource URL + HTTP version
- Headers (metadata key-value pairs)
- Blank line
- Body (optional)

**Response:**
- HTTP version + Status code + Reason phrase
- Headers
- Blank line
- Body (optional)

Headers are the remote control layer — client sends preferences (`Accept`, `Authorization`), server sends metadata (`Content-Type`, `Cache-Control`). They make HTTP extensible without changing the protocol itself.

## Methods and Idempotency

| Method | Intent | Idempotent? |
|--------|--------|-------------|
| GET | Retrieve resource | Yes |
| POST | Create resource | No |
| PUT | Replace resource entirely | Yes |
| PATCH | Partial update | No |
| DELETE | Remove resource | Yes |
| OPTIONS | Query server capabilities | Yes |

Idempotency is a contract. GET, PUT, DELETE should produce the same server state regardless of how many times called. Violating this (e.g., a GET that increments a counter) breaks caching and retries.

## Status Codes

- **1xx** — Informational (100 Continue, 101 Switching Protocols)
- **2xx** — Success (200 OK, 201 Created, 204 No Content)
- **3xx** — Redirection (301 Moved, 304 Not Modified)
- **4xx** — Client errors (400 Bad Request, 401 Unauthorized, 404 Not Found)
- **5xx** — Server errors (500 Internal Error, 502 Bad Gateway, 503 Unavailable)

Standardized codes create a universal error vocabulary — every HTTP client already understands them.

## Key Mechanisms

**CORS** — browsers enforce same-origin policy by default. CORS (Cross-Origin Resource Sharing) lets servers opt in to cross-origin requests via headers like `Access-Control-Allow-Origin`. Non-simple requests (custom headers, JSON content type, methods other than GET/POST/HEAD) trigger a pre-flight OPTIONS check first.

**Caching** — conditional requests use `ETag` and `Last-Modified` headers. Client sends `If-None-Match` or `If-Modified-Since`; server responds with 304 Not Modified (reuse cached) or 200 OK with fresh body. Manually managing ETags is error-prone; client-side libraries often provide better invalidation.

**Content negotiation** — client declares preferences via `Accept` (media type), `Accept-Language` (language), `Accept-Encoding` (compression like gzip). Same endpoint can serve different representations.

**Compression** — gzip typically achieves ~7x reduction on JSON payloads.

## Security

TLS (currently TLS 1.3) encrypts all data in transit, authenticates the server via certificates, and prevents eavesdropping/tampering. HTTPS is non-negotiable for any system handling sensitive data.

## Key Takeaways

- HTTP's statelessness is a feature: it enables horizontal scaling, but session continuity must be implemented at the application layer.
- Headers are the remote control — they let clients influence server behaviour without changing the URL, which is why HTTP has remained viable for three decades.
- Idempotency is a semantic contract; violating it breaks caching and retry safety.
- CORS is browser-enforced security; the server must explicitly opt in to cross-origin requests.
- Standardized status codes are a universal error vocabulary — custom conventions in response bodies ignore a standard every client already understands.

## Sources

- [[HTTP Protocol for Backend Engineers]]

## Connections

- [[Caching Fundamentals]] — ETag/Last-Modified conditional requests are the HTTP-level application of caching locality
- [[Postgres for Backend Engineers]] — HTTP methods map directly to CRUD operations