Type: #type/meta
Area: #area/meta
Keyword:
Date created: [[2026-04-13]]

---

Append-only chronological record of all Bloom operations. Each entry starts with `## [YYYY-MM-DD] operation | Title` so the log is greppable: `grep "^## \[" wiki/_meta/log.md | tail -5`.

## [2026-05-04] ingest | HTTP Protocol for Backend Engineers

Video transcript covering HTTP fundamentals for backend engineers. Covers statelessness and client-server model, HTTP versions (1.0 through 3), message structure, header categories (request, general, representation, security), methods and idempotency, CORS same-origin policy and pre-flight flows, status codes, conditional caching with ETag/Last-Modified, content negotiation and compression, persistent connections, multipart/chunked transfers, and TLS/HTTPS. Connects to existing sources on caching and Postgres backend engineering.

## [2026-05-04] query | what-is-http

Explained HTTP as a stateless request-response protocol. Covered core design (statelessness, client-server), HTTP versions, message structure, methods/idempotency, status codes, CORS, caching, content negotiation, and TLS/HTTPS. Sources: [[HTTP Protocol for Backend Engineers]]. Connections to [[Caching Fundamentals]] and [[Postgres for Backend Engineers]].
