# Architecture Requirements Document (ARD)

## Document Metadata

- **Product/Application:** Online Patient Scheduling and Reminders
- **Document ID:** ARD-OPS
- **Version:** 0.1
- **Status:** Draft
- **Architecture Owner:** TBD
- **Contributors:** Product Owner, Technical Lead, Security Reviewer, Engineering Lead
- **Last Updated:** 2026-11-19
- **Reference PRD:** `PRD.md`

---

## 1. Architecture Summary

Online Patient Scheduling and Reminders will be implemented as a responsive React web application backed by a FastAPI service and SQLite database for the first release. The architecture supports patient self-service booking and rescheduling for standard follow-up and routine visits, staff daily schedule visibility, and email reminder orchestration.

The key architecture drivers are HIPAA-aligned handling of appointment-related protected health information, instant booking confirmation without double-booking, online rescheduling up to 24 hours before appointment time, and a focused small-business first-release scope. Several production-critical decisions remain open, including hosting, scheduling system system-of-record strategy, patient and staff authentication, email delivery provider, observability, CI/CD, security scanning, and rollback posture.

## 2. Architecture Drivers

- PRD-FR-001 — Patients must be able to book eligible standard follow-up and routine appointments online from available clinic slots.
- PRD-FR-002 — The system must prevent double-booking when patients compete for the same slot.
- PRD-FR-003 — The system must clearly show no-availability states when eligible slots are full.
- PRD-FR-004 — The system must block urgent or emergency symptom paths from routine online booking.
- PRD-FR-005 — Patients must be able to reschedule eligible appointments online up to 24 hours before appointment time.
- PRD-FR-006 — The system must send email appointment reminders according to configured first-release timing.
- PRD-FR-007 — Staff must have a single daily schedule view.
- PRD-FR-008 — Staff should be able to filter the daily schedule by provider and appointment type.
- PRD-NFR-001 — The system must collect only minimum necessary patient information.
- PRD-NFR-002 — Protected health information must be encrypted in transit and at rest.
- PRD-NFR-003 — Staff schedule access must be restricted through role-based access controls.
- PRD-NFR-004 — Patients should be able to complete booking in under 3 minutes under normal load.
- PRD-NFR-005 — Booking pages should load in under 2 seconds under normal load.
- PRD-NFR-006 — The system should be available 99.5% monthly excluding planned maintenance.
- CON-001 — First-release scope must remain focused for a small business.
- CON-002 — The clinic operates in healthcare and must meet HIPAA requirements.
- CON-003 — Online booking must exclude urgent and emergency care.
- CON-004 — Online booking must exclude new patient intake appointments.
- CON-005 — Reminder channel scope is email only for the first release.
- CON-006 — Target release date is TBD.
- CON-007 — Scheduling system integration or replacement approach is TBD.
- CON-008 — Accessibility standard is TBD.

## 3. Architecture Principles

1. Minimize protected health information collection, storage, and exposure across all patient and staff workflows.
2. Prefer explicit transactional controls for appointment slot confirmation so users never receive duplicate confirmations for the same capacity.
3. Reuse established repository and platform patterns where appropriate.
4. Keep presentation, orchestration, domain, integration, and persistence concerns separated.
5. Treat unresolved production decisions as blocking architecture questions before production launch.
6. Ensure auditability of scheduling, rescheduling, reminder, and staff access workflows without logging sensitive message content.

## 4. System Context

### 4.1 Actors

- Patient — Books eligible routine/follow-up appointments online, reschedules eligible appointments, and receives email reminders.
- Front-Desk Staff Member — Views the daily schedule and filters by provider or appointment type.
- Clinic Administrator — Defines operational policies such as eligible appointment types, office hours, provider availability, urgent/emergency handling, and reminder timing.
- Email Delivery System — Sends appointment reminder emails; provider and interface are TBD.
- Scheduling System — Holds or synchronizes clinic appointment availability and bookings; system-of-record approach is TBD.
- Identity Provider — Authenticates staff and/or patients if selected; provider and approach are TBD.

### 4.2 External Systems

| ID | System | Purpose | Interface | Owner |
|---|---|---|---|---|
| EXT-001 | Scheduling System | Provides availability and receives confirmed or rescheduled appointments; system-of-record strategy TBD | REST/Event/File/TBD | Clinic / TBD vendor |
| EXT-002 | Email Delivery System | Sends appointment reminder emails and returns delivery status | REST/SMTP/TBD | TBD provider |
| EXT-003 | Staff Identity Provider | Authenticates staff and supplies role information if selected | OIDC/SAML/TBD | Clinic / TBD provider |
| EXT-004 | Patient Identity or Verification Service | Verifies patient access for booking and rescheduling if selected | Email token/OIDC/TBD | Clinic / TBD provider |
| EXT-005 | Hosting Platform | Runs React, FastAPI, SQLite storage, backups, and secrets | Managed cloud/on-prem/TBD | TBD |

## 5. Technology Stack

| Layer | Technology | Version/Constraint | Rationale |
|---|---|---|---|
| Frontend | React | Version TBD | Supports responsive patient and staff web workflows with clear separation from backend APIs. |
| Backend | FastAPI | Version TBD | Provides Python-based API layer for booking, rescheduling, reminders, staff schedule views, and integration adapters. |
| Data | SQLite | First release; requires transaction locking, encrypted storage, backups, and documented scale limits | Selected by stakeholder for first release; must be constrained to prevent double-booking and protect PHI. |
| Hosting | TBD | Must support HIPAA requirements, encryption, secrets handling, backups, monitoring, and signed BAA if cloud-hosted | Hosting model remains an open architecture question. |
| Email | TBD | Email-only reminders; provider must support required privacy/security posture | PRD limits reminder channel to email, but delivery architecture is unresolved. |
| Authentication | TBD | Must support patient access policy and staff RBAC | Patient and staff identity approaches are unresolved. |

## 6. Logical Architecture

### 6.1 Components

#### COMP-001 — Patient Web Application

- **Responsibility:** Provides patient-facing booking, no-availability, urgent/emergency block, and rescheduling flows.
- **Inputs:** Appointment type selection, patient minimum necessary scheduling information, selected slot, reschedule token or identity context, urgent/emergency screening response.
- **Outputs:** Booking requests, rescheduling requests, availability queries, user-facing confirmation or denial messages.
- **Dependencies:** COMP-002, COMP-006, COMP-008.
- **Repository Area:** `frontend/`

#### COMP-002 — Scheduling API

- **Responsibility:** Exposes booking, rescheduling, availability, and staff schedule APIs; enforces domain rules and coordinates persistence/integrations.
- **Inputs:** Requests from React application, scheduler job triggers, identity context, configuration data.
- **Outputs:** Confirmed appointments, rescheduled appointments, errors, schedule query responses, audit events.
- **Dependencies:** COMP-003, COMP-004, COMP-005, COMP-006, COMP-007, EXT-001.
- **Repository Area:** `backend/`

#### COMP-003 — Appointment Domain Service

- **Responsibility:** Enforces eligible appointment type rules, urgent/emergency exclusions, 24-hour rescheduling cutoff, provider availability, and double-booking prevention.
- **Inputs:** Appointment type, provider availability, appointment state, requested slot, patient scheduling data.
- **Outputs:** Domain decisions, confirmed appointment changes, rejected booking/rescheduling attempts.
- **Dependencies:** COMP-004, COMP-007, EXT-001.
- **Repository Area:** `backend/app/domain/`

#### COMP-004 — SQLite Persistence Layer

- **Responsibility:** Stores appointment, reminder, audit, configuration, and operational state needed by the first release.
- **Inputs:** Domain entities, audit events, reminder events, configuration changes.
- **Outputs:** Persisted and queried data for APIs, reminder jobs, and staff schedule views.
- **Dependencies:** Encrypted storage, backup mechanism TBD, transaction locking.
- **Repository Area:** `backend/app/persistence/`

#### COMP-005 — Reminder Scheduler

- **Responsibility:** Identifies appointments requiring email reminders at configured timing and records reminder attempts and delivery status.
- **Inputs:** Appointment records, reminder timing configuration, email delivery results.
- **Outputs:** Reminder send requests, reminder status records, audit events.
- **Dependencies:** COMP-004, COMP-007, EXT-002.
- **Repository Area:** `backend/app/reminders/`

#### COMP-006 — Identity and Access Adapter

- **Responsibility:** Implements patient access decision and staff RBAC once identity approach is selected.
- **Inputs:** Patient verification context TBD, staff authentication context TBD, role assignments.
- **Outputs:** Authorization decisions, user context, access-denied responses, audit events.
- **Dependencies:** EXT-003, EXT-004.
- **Repository Area:** `backend/app/security/`

#### COMP-007 — Audit Logging Service

- **Responsibility:** Records security-relevant and scheduling-relevant events according to finalized audit scope without storing sensitive message content.
- **Inputs:** Booking, rescheduling, reminder, staff access, authentication, authorization, and administrative events.
- **Outputs:** Audit log records for compliance review and incident investigation.
- **Dependencies:** COMP-004, observability tooling TBD.
- **Repository Area:** `backend/app/audit/`

#### COMP-008 — Staff Schedule Web Application

- **Responsibility:** Provides staff daily schedule view and filters by provider and appointment type.
- **Inputs:** Staff identity context, selected date, provider filter, appointment type filter.
- **Outputs:** Filtered daily schedule and access-denied states.
- **Dependencies:** COMP-002, COMP-006.
- **Repository Area:** `frontend/`

#### COMP-009 — Integration Adapter Layer

- **Responsibility:** Encapsulates scheduling system, email provider, identity provider, hosting, and future external-system integrations.
- **Inputs:** Domain requests and provider-specific configuration.
- **Outputs:** Provider calls, provider responses, normalized integration errors.
- **Dependencies:** EXT-001, EXT-002, EXT-003, EXT-004, EXT-005.
- **Repository Area:** `backend/app/integrations/`

### 6.2 Data Flow

1. Patient uses COMP-001 to search eligible appointment types and available slots through COMP-002.
2. COMP-002 invokes COMP-003 to validate appointment eligibility, urgent/emergency exclusions, and availability rules.
3. COMP-003 uses COMP-004 and, once decided, EXT-001 integration to check or maintain schedule state.
4. Patient submits a booking request; COMP-003 confirms the appointment inside a transaction with slot-level protection to prevent double-booking.
5. COMP-004 stores the appointment and COMP-007 records the booking audit event.
6. COMP-005 reads upcoming appointments and configured reminder timing, sends email reminders through EXT-002, and records delivery status.
7. Staff uses COMP-008 to request the daily schedule through COMP-002; COMP-006 enforces RBAC and COMP-004 returns appointments filtered by provider or appointment type.
8. Patient rescheduling follows the same availability and transaction path, additionally enforcing the 24-hour cutoff before replacing the original appointment time.

## 7. Architecture Decisions

### ARD-DEC-001 — React and FastAPI Application Stack

- **Status:** Accepted
- **Related Requirements:** PRD-FR-001, PRD-FR-005, PRD-FR-007, PRD-FR-008, PRD-NFR-004, PRD-NFR-005

**Decision**

Use React for the patient and staff web experiences, FastAPI for backend APIs and orchestration, and keep frontend, backend, domain, integration, security, and persistence concerns separated.

**Rationale**

The approved stack was selected by the stakeholder and supports responsive web workflows, API-based separation, and focused first-release implementation.

**Consequences**

- Enables independent frontend and backend testing.
- Requires API contracts between React and FastAPI.
- Requires deployment model, hosting, CI/CD, and observability decisions before production.

**Alternatives Considered**

- Server-rendered web application — not selected because stakeholder specified React and FastAPI.
- Low-code scheduling platform — not selected because stakeholder specified a custom React/FastAPI/SQLite stack.

### ARD-DEC-002 — SQLite First-Release Persistence with Guardrails

- **Status:** Accepted
- **Related Requirements:** PRD-FR-001, PRD-FR-002, PRD-FR-005, PRD-NFR-002, PRD-NFR-006

**Decision**

Use SQLite for first-release persistence with transaction locking, encrypted storage, backups, and documented scale limits.

**Rationale**

SQLite was selected by the stakeholder for the first release. Because the product handles appointment-related PHI and instant confirmations, SQLite usage must include explicit concurrency, encryption, backup, and scale constraints.

**Consequences**

- Simplifies first-release operations for a small clinic.
- Requires careful transaction design to prevent double-booking.
- May constrain concurrent usage and future scale.
- Backup and rollback posture remains open and must be resolved before production.

**Alternatives Considered**

- PostgreSQL or managed relational database for production — recommended from a scalability perspective but not selected for first release.
- SQLite as development-only storage — not selected because stakeholder accepted SQLite for first release.

### ARD-DEC-003 — Scheduling System Strategy Deferred

- **Status:** Proposed
- **Related Requirements:** PRD-FR-001, PRD-FR-005, PRD-FR-007, PRD-NFR-006

**Decision**

Keep scheduling system architecture TBD and document it as an open architecture question. The design must support a pluggable scheduling integration adapter so the first release can integrate with an existing system, use the product database as system of record, or support another decided pattern.

**Rationale**

The approved PRD explicitly leaves the scheduling integration or replacement approach unresolved.

**Consequences**

- Prevents premature coupling to an unknown scheduling system.
- Leaves migration, reconciliation, source of truth, and operational support unresolved.
- Blocks final production architecture until decided.

**Alternatives Considered**

- Existing scheduling system as system of record — recommended but not accepted.
- Product database as system of record — possible but not accepted.
- Standalone schedule with manual reconciliation — possible but not accepted.

### ARD-DEC-004 — Email-Only Reminder Channel with Provider Deferred

- **Status:** Proposed
- **Related Requirements:** PRD-FR-006, PRD-NFR-001, PRD-NFR-002

**Decision**

Implement reminder orchestration for email only, but keep email delivery architecture and provider TBD.

**Rationale**

The PRD constrains reminder scope to email only and excludes SMS and patient portal notifications. The provider decision is unresolved.

**Consequences**

- Keeps reminder channel scope focused.
- Requires an email provider or SMTP decision before reminder implementation is production-ready.
- Requires delivery logging and privacy review of message content.

**Alternatives Considered**

- HIPAA-capable transactional email provider under signed BAA — recommended but not accepted.
- Clinic SMTP server — possible but not accepted.
- Direct local SMTP from application server — not recommended due to deliverability and operational concerns.

### ARD-DEC-005 — Authentication and Authorization Deferred with RBAC Required

- **Status:** Proposed
- **Related Requirements:** PRD-FR-005, PRD-FR-007, PRD-FR-008, PRD-NFR-003

**Decision**

Keep patient identity and staff authentication approaches TBD while requiring role-based authorization for staff schedule access.

**Rationale**

The PRD mandates staff RBAC, but the user deferred patient and staff identity approach decisions.

**Consequences**

- Requires identity abstraction in the backend.
- Blocks detailed access-flow design for rescheduling and staff schedule views.
- Requires a later decision before implementation can complete security acceptance.

**Alternatives Considered**

- Magic-link patient verification — recommended but not accepted.
- Managed staff identity provider — recommended but not accepted.
- Application-managed accounts — possible but not accepted.

### ARD-DEC-006 — HIPAA-Aligned Minimum Necessary and Encryption Controls

- **Status:** Accepted
- **Related Requirements:** PRD-NFR-001, PRD-NFR-002, PRD-NFR-003

**Decision**

Design all data collection, storage, transmission, authorization, logging, and retention practices to support HIPAA-aligned handling of appointment-related PHI.

**Rationale**

The clinic operates in healthcare and must meet HIPAA requirements. The PRD explicitly requires minimum necessary information, encryption in transit and at rest, and role-based staff access.

**Consequences**

- All collected fields need documented scheduling or reminder purpose.
- Application, database, backups, logs, and integrations must avoid unnecessary PHI exposure.
- Compliance validation is required before production launch.

**Alternatives Considered**

- Treat appointment metadata as non-sensitive — rejected because appointment-related patient information can be PHI.

### ARD-DEC-007 — Deployment, Observability, Testing, and Supply Chain Deferred

- **Status:** Proposed
- **Related Requirements:** PRD-NFR-002, PRD-NFR-004, PRD-NFR-005, PRD-NFR-006

**Decision**

Keep deployment/CI/CD, observability, testing quality gates, dependency/CVE scanning, SBOM, and rollback posture TBD and document them as open architecture questions.

**Rationale**

The user explicitly deferred these decisions during the architecture interview.

**Consequences**

- ARD can define quality needs from PRD targets, but production-readiness gates remain unresolved.
- Security reviewer and engineering lead must resolve open questions before production approval.

**Alternatives Considered**

- Containerized application with automated build, test, security scan, and manual production approval — recommended but not accepted.
- Structured logs, metrics, health checks, and alerts without PHI — recommended but not accepted.
- Dependency/CVE scanning blocking high and critical findings plus SBOM generation — recommended but not accepted.

## 8. API and Integration Architecture

### ARD-API-001 — Availability Search API

- **Type:** REST
- **Operation/Topic:** `GET /api/availability`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** TBD pending patient identity decision
- **Versioning:** URL path versioning to be added if backward-incompatible changes are introduced; first release may use unversioned internal API.

**Request/Input Contract**

Query parameters: appointment type identifier, requested date range, optional provider identifier, and patient context if required by finalized identity design.

**Response/Output Contract**

Available slot list with slot identifier, provider identifier, appointment type identifier, start time, end time, and no-availability state when no eligible slots exist.

**Error Handling**

Return validation errors for unsupported appointment types, access errors if identity is required and absent, and safe no-availability responses when slots cannot be offered. Do not expose internal scheduling or PHI details in error messages.

### ARD-API-002 — Appointment Booking API

- **Type:** REST
- **Operation/Topic:** `POST /api/appointments`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** TBD pending patient identity decision
- **Versioning:** URL path versioning to be added if backward-incompatible changes are introduced; first release may use unversioned internal API.

**Request/Input Contract**

Minimum necessary patient scheduling fields, appointment type identifier, selected slot identifier, urgent/emergency screening response, email address for reminders, and patient identity/verification context if required.

**Response/Output Contract**

Confirmed appointment identifier, appointment date/time, appointment type, provider identifier if applicable, reminder enrollment status, or rejection reason.

**Error Handling**

Use transaction-controlled confirmation. If a slot is no longer available, return a conflict response and prompt the patient to choose another slot. If urgent/emergency symptoms are indicated, block confirmation and return non-booking guidance configured by clinic policy. Booking operation must be idempotency-aware using a client request identifier or equivalent mechanism before production.

### ARD-API-003 — Appointment Rescheduling API

- **Type:** REST
- **Operation/Topic:** `POST /api/appointments/{appointment_id}/reschedule`
- **Provider:** COMP-002
- **Consumers:** COMP-001
- **Authentication:** TBD pending patient identity decision
- **Versioning:** URL path versioning to be added if backward-incompatible changes are introduced; first release may use unversioned internal API.

**Request/Input Contract**

Appointment identifier, selected replacement slot identifier, patient identity/verification context, and client request identifier or equivalent idempotency token.

**Response/Output Contract**

Updated appointment identifier, new appointment date/time, prior appointment reference, reminder enrollment status, or rejection reason.

**Error Handling**

Reject rescheduling when appointment time is 24 hours or less away, when the replacement slot is unavailable, or when authorization fails. Reschedule changes must be atomic so the original appointment is not released unless the replacement slot is confirmed.

### ARD-API-004 — Staff Daily Schedule API

- **Type:** REST
- **Operation/Topic:** `GET /api/staff/schedule/daily`
- **Provider:** COMP-002
- **Consumers:** COMP-008
- **Authentication:** TBD pending staff authentication decision; must support staff RBAC
- **Versioning:** URL path versioning to be added if backward-incompatible changes are introduced; first release may use unversioned internal API.

**Request/Input Contract**

Schedule date, optional provider filter, optional appointment type filter, and authenticated staff context.

**Response/Output Contract**

Daily appointment list with minimum necessary staff-visible appointment details, provider, appointment type, time, and reminder status if authorized by finalized RBAC policy.

**Error Handling**

Deny access for unauthenticated or unauthorized users. Return empty filtered results when no matching appointments exist. Record staff access according to finalized audit scope.

### ARD-API-005 — Reminder Delivery Integration

- **Type:** REST | File | SMTP | TBD
- **Operation/Topic:** `TBD reminder send operation`
- **Provider:** EXT-002
- **Consumers:** COMP-005
- **Authentication:** TBD pending email provider decision
- **Versioning:** Provider-specific; TBD.

**Request/Input Contract**

Reminder recipient email address, appointment reference, scheduled reminder timing, and minimum necessary message content.

**Response/Output Contract**

Provider message identifier, accepted/rejected status, delivery/bounce status where available, and timestamp.

**Error Handling**

Retry policy, dead-letter handling, delivery failure visibility, and PHI-safe provider error logging are TBD pending email delivery architecture decision.

### ARD-API-006 — Scheduling System Integration

- **Type:** REST | Event | File | TBD
- **Operation/Topic:** `TBD scheduling availability and appointment operation`
- **Provider:** EXT-001 or COMP-002 depending on system-of-record decision
- **Consumers:** COMP-003, COMP-009
- **Authentication:** TBD pending scheduling system decision
- **Versioning:** Provider-specific or internal API versioning; TBD.

**Request/Input Contract**

Availability query, appointment create/update, provider availability, appointment type eligibility, and reconciliation payloads as required by finalized scheduling strategy.

**Response/Output Contract**

Available slots, confirmed appointments, updated appointments, conflicts, and synchronization status.

**Error Handling**

Conflict handling, retry rules, reconciliation procedures, and source-of-truth failure behavior are TBD pending scheduling architecture decision.

## 9. Data Architecture

### DATA-001 — Patient Scheduling Profile

- **Purpose:** Contains minimum necessary patient information required to book, reschedule, and remind patients about eligible appointments.
- **System of Record:** TBD pending scheduling system decision.
- **Classification:** Restricted
- **Retention:** According to clinic HIPAA record-retention policy; exact durations TBD.
- **Key Relationships:** Related to DATA-002 Appointment and DATA-003 Reminder Event.

### DATA-002 — Appointment

- **Purpose:** Represents an eligible routine or follow-up appointment booking or rescheduled appointment.
- **System of Record:** TBD pending scheduling system decision.
- **Classification:** Restricted
- **Retention:** According to clinic HIPAA record-retention policy; exact durations TBD.
- **Key Relationships:** Related to DATA-001 Patient Scheduling Profile, DATA-004 Provider, DATA-005 Appointment Type, and DATA-003 Reminder Event.

### DATA-003 — Reminder Event

- **Purpose:** Records configured reminder attempts, timestamps, provider status, and delivery status for email reminders.
- **System of Record:** Online Patient Scheduling and Reminders application unless email provider becomes authoritative for delivery status.
- **Classification:** Restricted
- **Retention:** According to clinic HIPAA record-retention policy; exact durations TBD.
- **Key Relationships:** Related to DATA-002 Appointment and DATA-001 Patient Scheduling Profile.

### DATA-004 — Provider

- **Purpose:** Identifies clinic providers used for availability and staff schedule filtering.
- **System of Record:** TBD pending scheduling system decision.
- **Classification:** Internal
- **Retention:** According to clinic operational policy; exact durations TBD.
- **Key Relationships:** Related to DATA-002 Appointment and DATA-006 Availability Slot.

### DATA-005 — Appointment Type

- **Purpose:** Defines which appointment types are eligible standard follow-up or routine visits and excludes new patient intake, urgent, and emergency care.
- **System of Record:** Clinic operational configuration or scheduling system; TBD.
- **Classification:** Internal
- **Retention:** According to clinic operational policy; exact durations TBD.
- **Key Relationships:** Related to DATA-002 Appointment and DATA-006 Availability Slot.

### DATA-006 — Availability Slot

- **Purpose:** Represents bookable provider capacity for eligible appointment types.
- **System of Record:** TBD pending scheduling system decision.
- **Classification:** Internal; Restricted when linked to a patient appointment.
- **Retention:** According to clinic operational and HIPAA record-retention policy; exact durations TBD.
- **Key Relationships:** Related to DATA-004 Provider, DATA-005 Appointment Type, and DATA-002 Appointment.

### DATA-007 — Audit Event

- **Purpose:** Supports compliance review and incident investigation for access and scheduling-related actions.
- **System of Record:** Online Patient Scheduling and Reminders application.
- **Classification:** Restricted
- **Retention:** According to clinic HIPAA record-retention policy; exact durations TBD.
- **Key Relationships:** Related to staff identity, patient identity where applicable, DATA-002 Appointment, and reminder actions.

### DATA-008 — Configuration

- **Purpose:** Stores clinic office hours, eligible appointment types, provider availability rules, urgent/emergency handling configuration, reminder timing, and feature settings.
- **System of Record:** Online Patient Scheduling and Reminders application or scheduling system; TBD by final scheduling strategy.
- **Classification:** Internal
- **Retention:** According to clinic operational policy; exact durations TBD.
- **Key Relationships:** Drives DATA-006 Availability Slot, DATA-002 Appointment, and DATA-003 Reminder Event behavior.

### Data Migration

- **Required:** TBD
- **Approach:** TBD pending scheduling system system-of-record decision. If integrating with an existing scheduling system, migration may be limited to configuration and synchronization setup. If the new product database becomes system of record for eligible visits, migration or reconciliation planning is required before launch.

## 10. Security Architecture

### ARD-SEC-001 — HIPAA-Aligned PHI Protection

- **Related Requirements:** PRD-NFR-001, PRD-NFR-002, PRD-NFR-003

The implementation must:

- Collect only minimum necessary patient information required for booking, rescheduling, and reminders.
- Encrypt protected health information in transit and at rest.
- Restrict staff schedule access using role-based access controls.
- Use a hosting and vendor model that supports HIPAA obligations, including a signed BAA where applicable.
- Protect SQLite database files, backups, logs, and exported data with encryption and restricted access.
- Document each patient-facing collected data field with its scheduling or reminder purpose.

The implementation must not:

- Store secrets in source code, logs, repositories, or unencrypted configuration.
- Log email message content, submitted PHI form content, or unnecessary patient details in application telemetry.
- Allow online booking for urgent or emergency symptoms.
- Allow online booking for new patient intake appointments.
- Send SMS or patient portal reminders in the first release.
- Permit staff schedule access without an authorized role.

### ARD-SEC-002 — Authentication and Authorization Deferred

- **Related Requirements:** PRD-NFR-003, PRD-FR-005, PRD-FR-007, PRD-FR-008

The implementation must:

- Provide an abstraction for patient identity/verification and staff authentication.
- Enforce staff RBAC before showing daily schedule data.
- Resolve patient rescheduling authorization before production use.

The implementation must not:

- Use shared staff accounts for production unless explicitly accepted through a security review.
- Allow unauthenticated or unauthorized staff access to the daily schedule.

### ARD-SEC-003 — Secrets and Configuration Protection

- **Related Requirements:** PRD-NFR-002

The implementation must:

- Use managed secrets service or encrypted environment secrets.
- Keep secrets out of code, logs, client-side bundles, and database records unless specifically designed for encrypted secret storage.
- Rotate secrets according to clinic or hosting-platform policy, with exact schedule TBD.

The implementation must not:

- Commit secrets to source control.
- Expose provider credentials to the React frontend.

### Security Controls

- **Authentication:** TBD for patients and staff; staff access must be authenticated before schedule access.
- **Authorization:** Role-based access control required for staff daily schedule views; patient authorization for rescheduling TBD.
- **Secrets Management:** Managed secrets service or encrypted environment secrets; no secrets in code or logs.
- **Encryption:** TLS or equivalent encrypted transport for all PHI in transit; encrypted SQLite storage, backups, and any PHI-bearing files at rest.
- **Audit Logging:** Scope TBD; must at minimum be able to support HIPAA-aligned review of staff access and scheduling-relevant actions once finalized.
- **Dependency/CVE Scanning:** TBD; blocking severity threshold unresolved.
- **SBOM:** TBD.

## 11. Reliability, Performance, and Scalability

### ARD-OPS-001 — Booking Completion Time

- **Target:** Eligible booking flow completes in under 3 minutes under normal load.
- **Validation Method:** Performance test of the patient booking journey using representative normal-load conditions and required patient information available.

### ARD-OPS-002 — Booking Page Load Time

- **Target:** Each booking page loads in under 2 seconds under normal load.
- **Validation Method:** Frontend performance test measuring page-load timing for patient booking pages under representative normal-load conditions.

### ARD-OPS-003 — Monthly Availability

- **Target:** 99.5% monthly availability excluding planned maintenance.
- **Validation Method:** Monthly uptime calculation from production monitoring or hosting platform availability records once observability and hosting are selected.

### ARD-OPS-004 — Double-Booking Prevention

- **Target:** Zero confirmed duplicate appointments for the same slot from concurrent online booking attempts.
- **Validation Method:** Concurrency test that submits competing booking requests for the same slot and verifies only one confirmation succeeds.

### ARD-OPS-005 — Rescheduling Atomicity

- **Target:** 100% of successful reschedules replace the original appointment with the new appointment atomically; no successful reschedule leaves both old and new appointments active.
- **Validation Method:** Integration test and database transaction test covering success, conflict, and failure paths.

### ARD-OPS-006 — SQLite Scale Limits

- **Target:** Documented first-release concurrency, database size, backup, and restore limits before production approval.
- **Validation Method:** Architecture review plus load and concurrency testing against expected first-release clinic usage once usage assumptions are available.

## 12. Observability

- **Logging:** TBD; logs must avoid PHI and secrets and should support troubleshooting booking, rescheduling, reminder, access, and integration failures.
- **Metrics:** TBD; metrics should support PRD KPIs, availability, page load time, booking completion time, reminder delivery status, and error rates once observability approach is selected.
- **Tracing:** TBD; tracing must not include PHI if implemented.
- **Alerting:** TBD; alerting thresholds and owners remain open.
- **Sensitive Data Restrictions:** Do not log submitted PHI, email message content, secrets, authentication tokens, or full patient identifiers unless explicitly approved through HIPAA-aligned security review.

## 13. Deployment Architecture

- **Environments:** TBD; expected needs include development, test, staging, and production, but environment model is not finalized.
- **Deployment Model:** TBD; containerized deployment was recommended but not accepted.
- **CI/CD:** TBD; build, test, security scan, approval, and release workflow not finalized.
- **Configuration Management:** Managed secrets service or encrypted environment secrets for sensitive configuration; non-sensitive configuration approach TBD.
- **Rollback:** TBD; rollback and backup posture for appointment data must be resolved before production.
- **Infrastructure as Code:** TBD; tool or standard not selected.

## 14. Testing Architecture

Required test levels:

- Unit tests
- Integration tests
- Contract tests
- End-to-end tests
- Security tests
- Performance tests, where applicable

Minimum quality expectations:

- **Coverage Threshold:** TBD pending testing quality gate decision.
- **Blocking Security Severity:** TBD pending supply-chain and security gate decision.
- **Required Build/Lint Checks:** TBD pending CI/CD and testing quality gate decision.

Additional required validation:

- Booking concurrency tests for PRD-FR-002.
- Rescheduling cutoff and atomicity tests for PRD-FR-005.
- PHI encryption validation for PRD-NFR-002.
- RBAC access-denial and access-allowance tests for PRD-NFR-003 once identity approach is selected.
- Performance validation for PRD-NFR-004 and PRD-NFR-005.
- Availability measurement approach for PRD-NFR-006 once hosting and observability are selected.

## 15. Architecture Constraints

- ARC-CON-001 — The clinic is a small business, so first-release scope must remain focused on booking, rescheduling, reminders, and daily schedule visibility.
- ARC-CON-002 — The clinic operates in healthcare and must meet HIPAA requirements.
- ARC-CON-003 — Online booking must exclude urgent and emergency care.
- ARC-CON-004 — Online booking must exclude new patient intake appointments.
- ARC-CON-005 — Reminder channel scope is email only for the first release.
- ARC-CON-006 — Target release date is TBD.
- ARC-CON-007 — Scheduling system integration or replacement approach is TBD.
- ARC-CON-008 — Accessibility standard is TBD.
- ARC-CON-009 — React, FastAPI, and SQLite are the selected first-release application stack.
- ARC-CON-010 — SQLite use requires transaction locking, encrypted storage, backups, and documented scale limits.
- ARC-CON-011 — Data retention must follow the clinic HIPAA record-retention policy, with exact durations TBD.
- ARC-CON-012 — Secrets must use a managed secrets service or encrypted environment secrets, with no secrets in code or logs.

## 16. Risks and Trade-offs

| ID | Risk/Trade-off | Impact | Mitigation |
|---|---|---|---|
| ARC-RISK-001 | Scheduling system strategy is unresolved | High impact to system of record, migration, reconciliation, and staff operations | Keep scheduling integration behind COMP-009 and resolve ARC-OQ-001 before production implementation is finalized |
| ARC-RISK-002 | Hosting model is unresolved for a HIPAA-regulated product | High impact to compliance, encryption, backup, BAA, monitoring, and operations | Resolve ARC-OQ-002 before production deployment decisions |
| ARC-RISK-003 | SQLite may limit concurrency, recoverability, and scale | Potential double-booking, downtime, or data-loss risk if not engineered carefully | Use transaction locking, encrypted storage, backups, documented scale limits, and concurrency tests |
| ARC-RISK-004 | Patient and staff identity approaches are unresolved | Blocks secure rescheduling and RBAC implementation details | Resolve ARC-OQ-003 and ARC-OQ-004 before security acceptance |
| ARC-RISK-005 | Email delivery provider and reminder timing are unresolved | Reminder feature cannot be production-ready | Resolve ARC-OQ-005 and ARC-OQ-006 before reminder launch |
| ARC-RISK-006 | Audit logging scope is unresolved | HIPAA-aligned review and incident investigation may be insufficient | Resolve ARC-OQ-008 with security reviewer before production |
| ARC-RISK-007 | Observability, testing gates, and supply-chain controls are unresolved | Production quality and security acceptance may be delayed | Resolve ARC-OQ-010, ARC-OQ-011, and ARC-OQ-012 before release approval |
| ARC-RISK-008 | Accessibility standard remains TBD | Patient-facing experience may not meet expected accessibility needs | Resolve ARC-OQ-015 before patient-facing release acceptance |

## 17. Open Architecture Questions

| ID | Question | Owner | Status | Decision/Due Date |
|---|---|---|---|---|
| ARC-OQ-001 | Will the product integrate with the existing scheduling system, replace it for eligible visits, or use a standalone schedule with manual reconciliation? | Product Owner / Technical Lead | Open | TBD |
| ARC-OQ-002 | What HIPAA-aligned hosting model and vendor will be used, including whether a signed BAA is required? | Product Owner / Technical Lead / Security Reviewer | Open | TBD |
| ARC-OQ-003 | What patient identity or verification approach will be used for booking and rescheduling? | Product Owner / Security Reviewer | Open | TBD |
| ARC-OQ-004 | What staff authentication provider and role mapping approach will be used for RBAC? | Technical Lead / Security Reviewer | Open | TBD |
| ARC-OQ-005 | What email delivery architecture and provider will send reminders and report delivery status? | Product Owner / Technical Lead | Open | TBD |
| ARC-OQ-006 | What email reminder timing should be configured for the first release? | Product Owner | Open | TBD |
| ARC-OQ-007 | What are the exact clinic HIPAA record-retention durations for appointments, reminders, audit events, and backups? | Product Owner / Security Reviewer | Open | TBD |
| ARC-OQ-008 | What audit logging scope is required for staff access, patient access, booking, rescheduling, reminders, and administrative changes? | Security Reviewer | Open | TBD |
| ARC-OQ-009 | What deployment, environment, CI/CD, infrastructure-as-code, rollback, backup, and restore model will be used? | Technical Lead / Engineering Lead | Open | TBD |
| ARC-OQ-010 | What observability stack, logging policy, metrics, tracing, alerting thresholds, and alert owners are required? | Technical Lead / Engineering Lead | Open | TBD |
| ARC-OQ-011 | What testing quality gate, coverage threshold, required build checks, lint checks, and release-blocking criteria will apply? | Engineering Lead | Open | TBD |
| ARC-OQ-012 | What dependency/CVE scanning threshold and SBOM requirement will apply? | Security Reviewer / Engineering Lead | Open | TBD |
| ARC-OQ-013 | What exact normal-load assumptions should be used to validate 3-minute booking completion and 2-second page loads? | Product Owner / Technical Lead | Open | TBD |
| ARC-OQ-014 | What migration or data reconciliation steps are required based on the scheduling system decision? | Product Owner / Technical Lead | Open | TBD |
| ARC-OQ-015 | What accessibility standard should apply to patient-facing booking and rescheduling? | Product Owner | Open | TBD |
| ARC-OQ-016 | Who is the named Architecture Owner for this ARD? | Product Owner | Open | TBD |

## 18. Feature Mapping

| Feature | Relevant Components | Decision IDs | Interface IDs | Security IDs |
|---|---|---|---|---|
| FEAT-001 | COMP-001, COMP-002, COMP-003, COMP-004, COMP-006, COMP-007, COMP-009 | ARD-DEC-001, ARD-DEC-002, ARD-DEC-003, ARD-DEC-006 | ARD-API-001, ARD-API-002, ARD-API-006 | ARD-SEC-001, ARD-SEC-002, ARD-SEC-003 |
| FEAT-002 | COMP-001, COMP-002, COMP-003, COMP-004, COMP-006, COMP-007, COMP-009 | ARD-DEC-001, ARD-DEC-002, ARD-DEC-003, ARD-DEC-005, ARD-DEC-006 | ARD-API-001, ARD-API-003, ARD-API-006 | ARD-SEC-001, ARD-SEC-002, ARD-SEC-003 |
| FEAT-003 | COMP-002, COMP-004, COMP-005, COMP-007, COMP-009 | ARD-DEC-001, ARD-DEC-004, ARD-DEC-006 | ARD-API-005 | ARD-SEC-001, ARD-SEC-003 |
| FEAT-004 | COMP-002, COMP-004, COMP-006, COMP-007, COMP-008, COMP-009 | ARD-DEC-001, ARD-DEC-003, ARD-DEC-005, ARD-DEC-006 | ARD-API-004, ARD-API-006 | ARD-SEC-001, ARD-SEC-002, ARD-SEC-003 |

## 19. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Solution Architect | TBD | Pending | TBD |
| Security Reviewer | TBD | Pending | TBD |
| Engineering Lead | TBD | Pending | TBD |