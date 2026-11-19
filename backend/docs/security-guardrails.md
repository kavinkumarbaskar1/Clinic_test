# Security Guardrails

The first-release backend keeps security-sensitive configuration server-side.
Secrets, tokens, signing keys, provider credentials, and integration secrets
must be supplied through `CLINIC_` environment variables or the deployment
secret manager. They must not be committed to source files, persisted in
frontend bundles, or returned by API responses.

Staff identity remains provider-neutral. Backend code may pass trusted
`StaffActorContext` values into authorization helpers, but no staff identity
provider is selected here. Staff schedule access is deny-by-default until a
trusted backend authentication layer supplies an actor with an allowed role.

Audit events store event type, timestamp metadata, actor reference when one is
available, and non-sensitive resource references. Audit helpers reject metadata
keys that represent PHI, message bodies, tokens, or full patient identifiers.
Email reminder content and submitted patient messages belong in the appropriate
clinical or messaging system, not in audit metadata.

Production deployments must enforce encryption in transit with HTTPS/TLS for
all patient, staff, administrative, and integration traffic. Internal service
traffic should also use encrypted channels unless it is isolated inside a
trusted network boundary with compensating controls.

SQLite database files, write-ahead-log files, temporary files, and backups must
be encrypted at rest in production through encrypted volumes, managed disk
encryption, backup encryption, or an approved equivalent. Backup retention,
restore testing, and access control must follow the same sensitivity level as
the live database.
