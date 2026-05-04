Type: #type/source
Area: #area/craft/engineering
Keyword: #keyword/http #keyword/web-protocols #keyword/api-design #keyword/cors #keyword/tls #keyword/caching
Date created: [[2026-05-04]]
Source: Video transcript (educational course on backend fundamentals)

---

## Overview

This is a comprehensive walkthrough of HTTP protocol fundamentals aimed at backend engineers. The speaker treats HTTP as the primary medium through which browsers and servers communicate, focusing on the concepts that appear in the majority of production codebases. The core argument is that HTTP is not merely a transport mechanism but a contract: it encodes statelessness, idempotency, content negotiation, and security policy into a standardised request-response grammar that every backend system must honour.

The transcript covers the protocol from first principles — why statelessness matters, how headers function as remote controls, why methods carry semantic intent, and how caching, CORS, compression, and TLS fit into the stack. It is practical rather than theoretical, using live demos to show request-response cycles, pre-flight checks, cache validation, and content negotiation in action.

## Notes

### Statelessness and the client-server model

Statelessness is the defining property of HTTP: the server retains no memory of past interactions. Every request must carry all information needed for processing — authentication tokens, session identifiers, resource locators — because the server treats each request as an independent, unrelated event.

This design buys two things:
- **Simplicity**: servers need not maintain session state, reducing resource consumption and architectural complexity.
- **Scalability**: requests can be distributed across any available server; if one crashes, no client state is lost.

The trade-off is that developers must implement continuity manually — via cookies, session stores, or JWT tokens — when interactions genuinely require memory (e.g., user login sessions, shopping carts).

The client-server model enforces a strict initiator-responder relationship: the client always opens the conversation, and the server always responds. There is no server-initiated push in standard HTTP/1.1 (though HTTP/2 introduced server push, which the speaker notes in passing).

### HTTP versions and transport

HTTP has evolved through several versions, each redefining connection efficiency:

**HTTP/1.0** opened a new TCP connection for every request-response pair, creating significant overhead from repeated handshakes.

**HTTP/1.1** introduced persistent connections (keep-alive), allowing multiple requests and responses over a single TCP connection. Chunked transfer encoding and improved caching mechanisms also arrived here.

**HTTP/2** added multiplexing (multiple concurrent streams over one connection), binary framing instead of text, header compression via HPACK, and server push.

**HTTP/3** is built on QUIC, which runs over UDP rather than TCP. This eliminates head-of-line blocking, reduces connection-establishment latency, and improves resilience to packet loss.

The speaker notes that HTTP does not strictly require TCP; it only requires a reliable transport. TCP was chosen historically because it guarantees delivery. HTTPS is simply HTTP with TLS encryption layered beneath it.

### Message structure

An HTTP message is either a request or a response, each with a rigid structure.

**Request:**
- Method (GET, POST, etc.) — the intent of the interaction
- Resource URL — what is being acted upon
- HTTP version
- Headers — metadata key-value pairs
- Blank line
- Body (optional) — payload data

**Response:**
- HTTP version
- Status code and reason phrase (e.g., 200 OK)
- Headers
- Blank line
- Body (optional)

Headers are the most flexible part of the protocol. They act as a remote control: the client sends instructions and preferences to the server, and the server sends metadata about the response back.

### Header categories

The speaker groups headers into four functional categories:

**Request headers** — sent by the client to describe the request environment. Examples: `User-Agent` (identifies the client software), `Authorization` (carries credentials), `Accept` (declares preferred content formats).

**General headers** — apply to both requests and responses, describing the message itself. Examples: `Date`, `Cache-Control`, `Connection`.

**Representation headers** — describe the format and encoding of the message body. Examples: `Content-Type` (media type), `Content-Length` (size in bytes), `Content-Encoding` (compression like gzip), `ETag` (unique identifier for caching).

**Security headers** — enforce browser security policies. Examples: `Strict-Transport-Security` (forces HTTPS), `Content-Security-Policy` (restricts resource loading to prevent XSS), `X-Frame-Options` (prevents clickjacking via iframes), `X-Content-Type-Options` (prevents MIME-type sniffing).

A key insight is HTTP's extensibility: new headers can be added without changing the underlying protocol. Custom headers (prefixed with `X-` historically) allow applications to layer their own semantics on top of the standard.

### Methods and idempotency

HTTP methods encode the *intent* of a request, not just its mechanics:

- **GET** — retrieve a resource; must not modify server state
- **POST** — create a new resource; non-idempotent by definition
- **PATCH** — partial update to an existing resource
- **PUT** — complete replacement of a resource (idempotent: replacing a resource with the same payload ten times yields the same result as once)
- **DELETE** — remove a resource (idempotent: deleting a non-existent resource yields the same end state as deleting it once)
- **OPTIONS** — query server capabilities; used in CORS pre-flight checks

Idempotency is a contract, not an enforcement. The protocol declares GET, PUT, and DELETE as idempotent, but it is the developer's responsibility to implement them that way. Violating this contract (e.g., a GET request that increments a counter) breaks caching, retries, and client expectations.

### CORS and the same-origin policy

Browsers enforce the same-origin policy: by default, a web page served from one origin (scheme + host + port) cannot make requests to a different origin. CORS (Cross-Origin Resource Sharing) is the mechanism that relaxes this restriction under server control.

The speaker distinguishes two flows:

**Simple request flow** — for requests that meet all of these conditions: method is GET, POST, or HEAD; only simple headers (no custom or authorization headers); content type is one of `application/x-www-form-urlencoded`, `multipart/form-data`, or `text/plain`. The browser sends the request directly, and the server must respond with `Access-Control-Allow-Origin` (and optionally other CORS headers). If the origin is not allowed, the browser blocks the response.

**Pre-flight request flow** — for everything else. The browser first sends an OPTIONS request (the pre-flight) to ask the server whether the actual request is permitted. The server responds with allowed origins, methods, and headers. Only if the pre-flight succeeds does the browser send the actual request. The demo shows a PUT request with `Authorization` and `Content-Type: application/json` triggering a pre-flight because it violates all three simple-request conditions.

### Response codes

HTTP status codes are a standardised vocabulary for communicating request outcomes. They are three-digit numbers grouped by first digit:

- **1xx** — Informational (e.g., 100 Continue, 101 Switching Protocols)
- **2xx** — Success (200 OK, 201 Created, 204 No Content)
- **3xx** — Redirection (301 Moved Permanently, 302 Found, 304 Not Modified)
- **4xx** — Client errors (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found)
- **5xx** — Server errors (500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable)

Before status codes, clients had to infer success or failure from response body structure, leading to inconsistent handling across platforms. Standardised codes enable universal error handling: a 401 triggers re-authentication, a 400 prompts form validation, a 503 triggers retry logic.

### Caching

HTTP caching reduces redundant data transfer by allowing clients to reuse previously fetched resources. The demo illustrates the conditional request pattern:

1. Initial request: server responds with `Cache-Control: max-age=10`, an `ETag` (hash of the response), and `Last-Modified` timestamp.
2. Subsequent request: client sends `If-None-Match` (with the cached ETag) and `If-Modified-Since` (with the cached timestamp).
3. If the resource is unchanged, server responds with **304 Not Modified** and no body. The client uses its cached version.
4. If the resource changed, server responds with **200 OK**, a new body, and updated cache headers.

The speaker notes that managing ETags manually in production is error-prone. If a server forgets to update an ETag after a change, clients will continue serving stale data. Modern client-side libraries (e.g., React Query) often provide more reliable caching with explicit invalidation strategies.

### Content negotiation and compression

Content negotiation is the mechanism by which client and server agree on the best format for exchanging data. Three dimensions are negotiated:

- **Media type** — `Accept: application/json` vs `Accept: text/xml`
- **Language** — `Accept-Language: en-US` vs `Accept-Language: es`
- **Encoding** — `Accept-Encoding: gzip, deflate` for compression

The demo shows a server responding with Spanish XML when the client requests it, demonstrating that the same endpoint can serve different representations based on headers.

HTTP compression (typically gzip) dramatically reduces payload size. In the demo, an 11,000-entry JSON file shrinks from 26 MB uncompressed to 3.8 MB with gzip — a ~7x reduction. The client decompresses the payload transparently.

### Persistent connections and keep-alive

HTTP/1.1 makes connections persistent by default: a single TCP connection can carry multiple request-response pairs. This eliminates the overhead of opening and closing connections for every interaction. The `Connection: keep-alive` header explicitly requests this behavior, and can specify timeouts or maximum request counts. `Connection: close` forces termination after the response.

### Handling large payloads

**Multipart requests** are used for file uploads. The body is divided into parts separated by a boundary string. Each part contains metadata (e.g., filename) followed by binary data. The `Content-Type: multipart/form-data; boundary=...` header tells the server how to parse the parts.

**Chunked transfer / text/event-stream** is used for streaming large responses. The server sets `Content-Type: text/event-stream` and `Connection: keep-alive`, then sends data in chunks over a sustained connection. The client appends each chunk until the stream ends. This is how real-time updates and large file downloads are handled without buffering the entire payload in memory.

### TLS and HTTPS

SSL was the original encryption protocol for HTTP. It has been superseded by TLS (currently TLS 1.3 is recommended) due to known vulnerabilities. HTTPS is simply HTTP running over a TLS-encrypted connection. TLS authenticates the server via certificates and encrypts all data in transit, preventing eavesdropping and tampering. The speaker emphasises that backend engineers do not need deep cryptography expertise, but must understand that HTTPS is non-negotiable for any system handling sensitive data.

## Key Takeaways

- HTTP's statelessness is a feature, not a limitation: it simplifies server architecture and enables horizontal scaling, but pushes session continuity into application-layer mechanisms like tokens and cookies.
- Headers function as a remote control layer, allowing clients to influence server behaviour without changing the URL or body; this extensibility is why HTTP has remained viable for three decades.
- Idempotency is a semantic contract: GET, PUT, and DELETE should produce the same server state regardless of how many times they are called; violating this breaks caching and retry safety.
- CORS is a browser-enforced security mechanism, not a server error; the server must explicitly opt in to cross-origin requests via response headers.
- Status codes create a universal error-handling vocabulary; inventing custom success/failure conventions in response bodies ignores a standard that every HTTP client already understands.
- HTTP caching via ETag and Last-Modified reduces bandwidth but requires careful server-side bookkeeping; client-side caching libraries often provide more predictable invalidation.
- Compression and persistent connections are not optional optimisations at scale — they are foundational to acceptable latency and throughput.

## Connections

- Connects to [[Caching Fundamentals]] — the ETag/Last-Modified conditional request pattern is the HTTP-level application of the same locality principle that drives all caching systems.
- Complements [[Postgres for Backend Engineers]] — the source assumes a REST API layer backed by a database, and the HTTP methods map directly to the CRUD queries demonstrated there.
- Could inform a future concept on "API Design as Protocol Contract" — the combination of methods, headers, status codes, and content negotiation forms a declarative interface that constrains both client and server behaviour.
