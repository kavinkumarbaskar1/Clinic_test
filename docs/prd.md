# Product Requirements Document (PRD)

> Replace all placeholder values. Keep requirement IDs stable after approval so downstream ARD and feature specifications retain traceability.

## Document Metadata

- **Product/Application:** Online Patient Scheduling and Reminders
- **Document ID:** PRD-OPS
- **Version:** 0.1
- **Status:** Draft
- **Owner:** TBD
- **Contributors:** TBD
- **Last Updated:** 2026-11-19

---

## 1. Executive Summary

This product enables patients at a small healthcare clinic to book and reschedule eligible appointments online, receive email reminders, and reduce reliance on phone-only booking during office hours. The first release focuses on standard follow-up and routine visit types, with instant confirmation from available clinic slots.

The expected value is fewer lost bookings outside office hours, a more convenient patient experience, and a unified daily schedule view for staff. Because the clinic operates in healthcare and is subject to HIPAA, the product must protect appointment-related patient information through minimum-necessary data collection, encryption, and role-based access.

## 2. Problem Statement

The clinic loses bookings because patients can only book appointments by phone during office hours. Patients who want to book after hours may abandon scheduling, delay care, or leave messages that are not converted into appointments. Evidence is not yet available; the baseline for after-hours lost-booking impact must be measured during discovery.

## 3. Product Vision

Patients can self-serve eligible appointment booking and rescheduling online at any time, receive timely appointment reminders by email, and rely on clear guidance when online booking is not appropriate. Staff can view the day’s schedule in one place and filter it by provider or appointment type.

## 4. Goals and Success Measures

### 4.1 Goals

- Reduce lost bookings outside office hours.
- Allow patients to book standard follow-up and routine visits online.
- Allow patients to reschedule eligible appointments online up to 24 hours before the appointment.
- Send appointment reminders by email.
- Give staff a single daily schedule view with provider and appointment-type filtering.
- Maintain HIPAA-aligned handling of appointment-related patient information.

### 4.2 Success Measures

| ID | Measure | Baseline | Target | Measurement Method |
|---|---|---:|---:|---|
| KPI-001 | Number of online bookings made outside office hours | TBD | TBD | Booking analytics segmented by timestamp outside clinic office hours |
| KPI-002 | Percentage of eligible routine/follow-up bookings completed online | TBD | TBD | Scheduling analytics by appointment type and booking channel |
| KPI-003 | Email reminder delivery success rate | TBD | TBD | Email delivery logs and bounced-message reporting |
| KPI-004 | Staff daily schedule usage | TBD | TBD | Staff access logs for daily schedule view and filters |

## 5. Scope

### 5.1 In Scope

- Online booking for standard follow-up and routine visit appointment types.
- Instant confirmation from available clinic slots.
- Online patient rescheduling up to 24 hours before the appointment.
- Email appointment reminders.
- Staff daily schedule view in one place.
- Staff filtering by provider and appointment type.
- Prevention of double-booking when multiple patients select the same slot.
- Display of no-availability states when eligible slots are full.
- Blocking online booking for urgent or emergency symptoms.
- HIPAA controls for minimum necessary information, encryption, and role-based access.

### 5.2 Out of Scope

- New patient intake appointment booking online.
- Urgent or emergency care booking online.
- Insurance coordinator workflows.
- Billing staff workflows.
- SMS reminders.
- Patient portal notifications.
- Staff approval workflow for every eligible booking.

## 6. Personas and Users

### PERSONA-001 — Patient Booking or Managing an Appointment

- **Description:** A patient who needs to book or reschedule a standard follow-up or routine visit without calling during office hours.
- **Primary Need:** Book or reschedule an eligible appointment online at a convenient time.
- **Key Pain Point:** Phone-only booking during office hours causes missed opportunities and inconvenience.

### PERSONA-002 — Front-Desk Staff Member

- **Description:** Clinic staff member responsible for monitoring the daily appointment schedule.
- **Primary Need:** See the day’s appointments in one place and filter them by provider or appointment type.
- **Key Pain Point:** Schedule visibility is fragmented or harder to manage when appointments are not shown in one consolidated view.

## 7. Assumptions and Dependencies

### Assumptions

- ASM-001 — The clinic will define which appointment types qualify as standard follow-up and routine visits before launch.
- ASM-002 — Patients using online booking can provide the minimum necessary information required to schedule eligible appointments.
- ASM-003 — Clinic office hours are defined so after-hours bookings can be measured.

### Dependencies

- DEP-001 — Scheduling system dependency is TBD.
- DEP-002 — Email delivery capability is required for appointment reminders.
- DEP-003 — Clinic operational policies are required for eligible appointment types, office hours, provider availability, and urgent/emergency symptom handling.
- DEP-004 — HIPAA-aligned security and privacy implementation is required before production launch.

## 8. Functional Requirements

### PRD-FR-001 — Online Eligible Appointment Booking

- **Priority:** Must
- **Feature:** FEAT-001
- **Persona:** PERSONA-001

**Requirement**

The system shall allow patients to book standard follow-up and routine visit appointments online from available clinic slots.

**Business Rationale**

Patients currently can only book by phone during office hours, which contributes to lost bookings outside office hours.

**Acceptance Criteria**

1. Given an eligible appointment type has available slots, when a patient selects a slot and submits valid required information, then the appointment is confirmed instantly.
2. Given an appointment type is not standard follow-up or routine, when a patient attempts to book it online, then the system does not allow online booking for that appointment type.
3. Given a booking is confirmed, when staff view the daily schedule, then the appointment appears in the appropriate day’s schedule.

---

### PRD-FR-002 — Real-Time Slot Protection

- **Priority:** Must
- **Feature:** FEAT-001
- **Persona:** PERSONA-001

**Requirement**

The system shall prevent double-booking when two patients attempt to book the same appointment slot.

**Business Rationale**

Instant confirmation is only safe if the system prevents multiple patients from receiving confirmation for the same clinic capacity.

**Acceptance Criteria**

1. Given two patients attempt to confirm the same available slot, when the first confirmation succeeds, then the second patient cannot confirm that same slot.
2. Given the selected slot is no longer available, when the patient submits the booking, then the system displays that the slot is unavailable and prompts the patient to choose another available slot.

---

### PRD-FR-003 — No-Availability State

- **Priority:** Must
- **Feature:** FEAT-001
- **Persona:** PERSONA-001

**Requirement**

The system shall show a clear no-availability state when all eligible slots are full.

**Business Rationale**

Patients need a clear outcome when no eligible appointments can be booked online, rather than encountering ambiguity or failed booking attempts.

**Acceptance Criteria**

1. Given no eligible slots are available, when a patient searches for an eligible appointment, then the system displays that no appointments are available.
2. Given no eligible slots are available, when the no-availability state is displayed, then the system does not present unavailable slots as bookable.

---

### PRD-FR-004 — Urgent and Emergency Booking Block

- **Priority:** Must
- **Feature:** FEAT-001
- **Persona:** PERSONA-001

**Requirement**

The system shall block online booking for urgent or emergency symptoms.

**Business Rationale**

Urgent or emergency needs are explicitly out of scope for online booking and require appropriate guidance outside the routine scheduling flow.

**Acceptance Criteria**

1. Given a patient indicates urgent or emergency symptoms, when they attempt to book online, then the system prevents appointment booking through the routine online flow.
2. Given online booking is blocked for urgent or emergency symptoms, then no routine or follow-up appointment is confirmed from that flow.

---

### PRD-FR-005 — Online Rescheduling

- **Priority:** Must
- **Feature:** FEAT-002
- **Persona:** PERSONA-001

**Requirement**

The system shall allow patients to reschedule eligible appointments online up to 24 hours before the appointment.

**Business Rationale**

Online rescheduling reduces dependence on phone access while preserving a clinic policy boundary close to the appointment time.

**Acceptance Criteria**

1. Given an eligible appointment is more than 24 hours away, when a patient selects an available replacement slot and confirms rescheduling, then the original appointment is replaced by the new appointment time.
2. Given an eligible appointment is 24 hours or less away, when a patient attempts to reschedule online, then the system prevents online rescheduling.
3. Given rescheduling succeeds, when staff view the daily schedule, then the old time no longer shows the appointment and the new time shows it.

---

### PRD-FR-006 — Email Appointment Reminders

- **Priority:** Must
- **Feature:** FEAT-003
- **Persona:** PERSONA-001

**Requirement**

The system shall send appointment reminders by email according to the reminder timing configured for the first release.

**Business Rationale**

Email reminders support appointment attendance and keep patients informed without adding SMS or portal notification scope.

**Acceptance Criteria**

1. Given an appointment has a valid patient email address and reminder timing is configured, when the configured reminder time occurs, then the system sends an email reminder for that appointment.
2. Given an email reminder is sent, when delivery logging is reviewed, then the reminder event is recorded with appointment reference, timestamp, and delivery status.
3. Given SMS and portal notifications are out of scope, when reminders are sent, then the system sends email reminders only.

---

### PRD-FR-007 — Staff Daily Schedule View

- **Priority:** Must
- **Feature:** FEAT-004
- **Persona:** PERSONA-002

**Requirement**

The system shall provide staff with a single view of the day’s schedule.

**Business Rationale**

Staff need the day’s schedule in one place to monitor clinic operations and appointments booked online.

**Acceptance Criteria**

1. Given staff open the daily schedule view, when appointments exist for that day, then all appointments for that day are displayed in one view.
2. Given a patient books or reschedules an appointment online, when staff refresh or reopen the daily schedule view, then the updated appointment appears on the correct day.

---

### PRD-FR-008 — Staff Schedule Filtering

- **Priority:** Should
- **Feature:** FEAT-004
- **Persona:** PERSONA-002

**Requirement**

The system shall allow staff to filter the daily schedule by provider and appointment type.

**Business Rationale**

Filtering helps staff quickly find relevant daily appointments without expanding first-release scope to editing, cancellation, or manual appointment creation.

**Acceptance Criteria**

1. Given staff are viewing the daily schedule, when they select a provider filter, then only appointments matching that provider are displayed.
2. Given staff are viewing the daily schedule, when they select an appointment-type filter, then only appointments matching that appointment type are displayed.
3. Given staff clear filters, then the full daily schedule is displayed again.

## 9. Non-Functional Requirements

### PRD-NFR-001 — Minimum Necessary Patient Information

- **Category:** Privacy
- **Priority:** Must

**Requirement**

The system shall collect only the minimum necessary patient information required to book, reschedule, and remind patients about eligible appointments.

**Acceptance Criteria**

1. Given the patient booking or rescheduling flow is reviewed, then each collected data field has a documented scheduling or reminder purpose.

---

### PRD-NFR-002 — Protected Health Information Encryption

- **Category:** Security
- **Priority:** Must

**Requirement**

The system shall encrypt protected health information in transit and at rest.

**Acceptance Criteria**

1. Given patient appointment data is transmitted, then the transmission uses encrypted transport.
2. Given patient appointment data is stored, then the stored data is encrypted at rest.

---

### PRD-NFR-003 — Role-Based Staff Access

- **Category:** Security
- **Priority:** Must

**Requirement**

The system shall restrict staff schedule access using role-based access controls.

**Acceptance Criteria**

1. Given a user without an authorized staff role attempts to access the daily schedule, then access is denied.
2. Given a user with an authorized staff role accesses the daily schedule, then access is permitted according to their assigned role.

---

### PRD-NFR-004 — Booking Completion Time

- **Category:** Performance
- **Priority:** Should

**Requirement**

The system shall allow patients to complete booking in under 3 minutes under normal load.

**Acceptance Criteria**

1. Given normal load test conditions, when a patient has required information available and completes a successful eligible booking flow, then the flow can be completed in under 3 minutes.

---

### PRD-NFR-005 — Booking Page Load Time

- **Category:** Performance
- **Priority:** Should

**Requirement**

The system shall load booking pages in under 2 seconds under normal load.

**Acceptance Criteria**

1. Given normal load test conditions, when a patient opens each booking page, then the page loads in under 2 seconds.

---

### PRD-NFR-006 — Monthly Availability

- **Category:** Availability
- **Priority:** Should

**Requirement**

The system shall be available 99.5% monthly excluding planned maintenance.

**Acceptance Criteria**

1. Given a completed calendar month, when availability is calculated excluding planned maintenance, then uptime is at least 99.5%.

## 10. User Journeys

### JOURNEY-001 — Patient Books an Eligible Appointment Online

1. Patient opens the online booking flow outside or during office hours.
2. Patient selects a standard follow-up or routine visit appointment type.
3. Patient selects an available slot and submits valid required information.
4. System confirms the appointment instantly and records it on the clinic schedule.
5. Patient receives email reminder according to configured timing.

**Related Requirements:** PRD-FR-001, PRD-FR-002, PRD-FR-003, PRD-FR-004, PRD-FR-006, PRD-NFR-001, PRD-NFR-002

### JOURNEY-002 — Patient Reschedules an Eligible Appointment

1. Patient accesses an eligible appointment more than 24 hours before the appointment time.
2. Patient selects an available replacement slot.
3. System confirms the rescheduled appointment.
4. Staff daily schedule reflects the updated appointment time.

**Related Requirements:** PRD-FR-005, PRD-FR-007, PRD-NFR-001, PRD-NFR-002

### JOURNEY-003 — Staff Reviews the Day’s Schedule

1. Staff member with an authorized role opens the daily schedule view.
2. System displays all appointments for the day in one place.
3. Staff filters the schedule by provider or appointment type.
4. System displays only matching appointments until filters are cleared.

**Related Requirements:** PRD-FR-007, PRD-FR-008, PRD-NFR-003

## 11. Feature Breakdown

### FEAT-001 — Online Appointment Booking

- **Summary:** Patients book standard follow-up and routine visits online with instant confirmation from available clinic slots, including double-booking prevention and no-availability handling.
- **Priority:** Must
- **Related Requirements:** PRD-FR-001, PRD-FR-002, PRD-FR-003, PRD-FR-004, PRD-NFR-001, PRD-NFR-002, PRD-NFR-004, PRD-NFR-005, PRD-NFR-006
- **Expected Spec File:** `specs/FEAT-001-online-appointment-booking.spec.md`

### FEAT-002 — Online Rescheduling

- **Summary:** Patients reschedule eligible appointments online up to 24 hours before the appointment.
- **Priority:** Must
- **Related Requirements:** PRD-FR-005, PRD-NFR-001, PRD-NFR-002, PRD-NFR-004, PRD-NFR-005, PRD-NFR-006
- **Expected Spec File:** `specs/FEAT-002-online-rescheduling.spec.md`

### FEAT-003 — Email Appointment Reminders

- **Summary:** Patients receive appointment reminders by email using first-release reminder timing once defined.
- **Priority:** Must
- **Related Requirements:** PRD-FR-006, PRD-NFR-001, PRD-NFR-002
- **Expected Spec File:** `specs/FEAT-003-email-appointment-reminders.spec.md`

### FEAT-004 — Staff Daily Schedule View

- **Summary:** Staff view the day’s appointments in one place and filter by provider or appointment type.
- **Priority:** Must
- **Related Requirements:** PRD-FR-007, PRD-FR-008, PRD-NFR-003, PRD-NFR-006
- **Expected Spec File:** `specs/FEAT-004-staff-daily-schedule-view.spec.md`

## 12. Constraints

- CON-001 — The clinic is a small business, so first-release scope must remain focused on booking, rescheduling, reminders, and daily schedule visibility.
- CON-002 — The clinic operates in healthcare and must meet HIPAA requirements.
- CON-003 — Online booking must exclude urgent and emergency care.
- CON-004 — Online booking must exclude new patient intake appointments.
- CON-005 — Reminder channel scope is email only for the first release.
- CON-006 — Target release date is TBD.
- CON-007 — Scheduling system integration or replacement approach is TBD.
- CON-008 — Accessibility standard is TBD.

## 13. Risks

| ID | Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| RISK-001 | Baseline and target for after-hours booking improvement are not yet defined | High | Medium | Measure baseline during discovery and set target before launch |
| RISK-002 | Scheduling system dependency is unresolved | High | Medium | Decide integration, replacement, or standalone reconciliation approach before implementation planning |
| RISK-003 | Reminder timing is unresolved | Medium | Medium | Define reminder timing before configuring reminder workflows |
| RISK-004 | HIPAA controls are insufficiently implemented | High | Medium | Require privacy, security, encryption, and role-based access validation before production launch |
| RISK-005 | Patients attempt to use routine booking for urgent or emergency needs | High | Medium | Block urgent/emergency symptom paths from online routine booking |

## 14. Open Questions

| ID | Question | Owner | Status | Decision/Due Date |
|---|---|---|---|---|
| OQ-001 | What is the measured baseline for after-hours lost bookings and online booking volume? | Product Owner | Open | TBD |
| OQ-002 | What target should define first-release success for after-hours online bookings? | Product Owner | Open | TBD |
| OQ-003 | What targets should be set for percentage of eligible bookings online, email delivery success, and staff daily schedule usage? | Product Owner | Open | TBD |
| OQ-004 | What is the target release date or launch window? | Product Owner | Open | TBD |
| OQ-005 | Will the product integrate with the existing scheduling system, replace it for eligible visits, or use a standalone schedule with manual reconciliation? | Product Owner / Technical Lead | Open | TBD |
| OQ-006 | What email reminder timing should be used in the first release? | Product Owner | Open | TBD |
| OQ-007 | What accessibility standard should apply to patient-facing booking and rescheduling? | Product Owner | Open | TBD |
| OQ-008 | What training and support materials are required for staff and patients? | Product Owner | Open | TBD |
| OQ-009 | What rollout approach should be used: pilot, phased, or full launch? | Product Owner | Open | TBD |
| OQ-010 | What migration or data reconciliation steps are required based on the scheduling system decision? | Product Owner / Technical Lead | Open | TBD |

## 15. Release and Rollout Considerations

- **Target Release:** TBD
- **Rollout Approach:** TBD
- **Migration Considerations:** TBD pending scheduling system dependency decision.
- **Training/Support Considerations:** TBD

## 16. Definition of Product Success

The product is successful when:

- Patients can book standard follow-up and routine visits online with instant confirmation from available clinic slots.
- Patients can reschedule eligible appointments online up to 24 hours before the appointment.
- Email reminders are sent according to defined first-release timing.
- Staff can see the day’s schedule in one place and filter by provider or appointment type.
- After-hours online booking success is measured against a discovery baseline and target once defined.
- All Must-priority requirements are accepted.
- Required quality, security, and compliance outcomes are evidenced.

## 17. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Product Owner | TBD | Pending | TBD |
| Business Sponsor | TBD | Pending | TBD |