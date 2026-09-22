# Security

Applies to any web application before a demo, a handoff, or a deployment. No exceptions,
no "just this once".

## The short list

**No secrets in anything the browser downloads.** Grep the whole tree for `sk_`,
`pk_live`, `AIza`, `Bearer`, `api_key`, `password`. Zero matches in any .html, .js or .css.
A key that genuinely must be public, like a publishable payment key, is restricted by
domain at the provider.

**Security headers on every response.**

```
Content-Security-Policy         start at default-src 'self', no wildcards, no unsafe-eval
Strict-Transport-Security       max-age=31536000; includeSubDomains
X-Frame-Options                 DENY
X-Content-Type-Options          nosniff
Referrer-Policy                 strict-origin-when-cross-origin
Permissions-Policy              lock the features you do not use
Cross-Origin-Opener-Policy      same-origin
Cache-Control: no-store         on any response carrying personal data
```

**Server-side validation on every endpoint.** Reject oversized bodies. Enforce maximum
lengths and numeric ranges. Validate path parameters against a pattern before you look
anything up. Client-side validation is a convenience, never a control.

**Rate limit every state-changing endpoint**, per IP, token bucket or sliding window.

**The static file server blocks source.** 404 on `*.py`, on state files, on dotfiles,
`.env` and `.git` included.

**Escape every user-supplied value before rendering.** No string concatenation into
innerHTML. Test with a script tag as a name.

**The server generates all IDs.** Never trust a client-supplied order number, session ID,
or anything that must be unique.

**No eval, no new Function, no document.write** with user input.

**CORS is not a wildcard in production.**

**Redact personal data in logs.** Never log full request bodies.

## Trackers and consent

Default to shipping none. If the client insists, nothing loads until the visitor opts in.
A banner that appears while the pixel has already fired is worse than no banner, because
it documents that you knew.

Name the tracking in the privacy policy. A policy that never mentions it is a failure.

## Test as an attacker before handoff

Submit a script tag. Try path traversal. Try an inflated total. Flood the rate limit. Curl
`/.env`, `/.git/config`, and your own server file. All of it must fail.
