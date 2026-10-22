# SIG Module — Requirements vs Current Implementation

This document maps the product requirements (see source spec) to the **IG-portal** codebase as of the review date. It is intended for planning: what is already in place, what is partial, and what remains to build.

**Scope:** Public SIG area, applications, member login, SIG dashboard, meetings, consultations, events, and admin workflows.  
**Code references:** `core/views.py`, `core/urls.py`, `templates/core/sig.html`, `templates/core/SIG/*`, `ig_account` (MySQL), Django models `ObserverRequest`, `SIGObserver`, etc.

---

## Legend

| Status | Meaning |
|--------|---------|
| **Done** | Largely matches the requirement |
| **Partial** | Some behaviour or UI exists; gaps remain |
| **Not done** | Missing or only placeholder / wrong wiring |
| **N/A** | Optional or out of scope for this pass |

---

## 1. Public page (no login)

| Requirement | Status | Notes |
|-------------|--------|--------|
| **A. Static information** — What is IG, what is NIXI SIG portal, SIGs (FI, IPS, DNN), Member vs Observer | **Partial** | `sig` → `core/sig.html` has narrative about SIGs and three SIG cards (DNN, IPS, FI). There is **no dedicated** block for “What is Internet Governance” or “NIXI SIG portal” as separate sections; **Member vs Observer** roles are not clearly explained on-page. |
| **B. SIG listing (3 SIGs)** | **Done** | FI, IPS, DNN are shown with short descriptions (`core/sig.html`). Naming aligns with spec (IPS/DNN/FI). |
| **C. SIG members list (per SIG, admin-approved)** | **Not done** | No dynamic list of approved members grouped by SIG on the public page. |
| **D. CTAs — Apply as Observer, Apply as SIG Member, SIG Member Login** | **Partial** | Buttons exist but wiring is inconsistent: hero uses `{% url 'login' %}` (general login) rather than **`siglogin`**; “Become a Member”, “Attend as an Observer”, and “Join a SIG” **all point to `sigregister`** — there is **no separate observer application** route on the public site. |

---

## 2. Apply as observer (form + pending + admin approval)

| Requirement | Status | Notes |
|-------------|--------|--------|
| Fields: name, email, mobile, org, designation, state, single SIG (FI/IPS/DNN), reason | **Not done** (public) | `ObserverForm` + `ObserverRequest` model exist (`core/forms.py`, `core/models.py`) and are available in **Django `/admin/`**, but there is **no URL/view** that renders `ObserverForm` for anonymous users. The form fields also **differ** from the spec (e.g. `work_experience` / `linkedin` vs `designation`, `state`, `reason to attend`). |
| Flow: submit → DB → **Pending** → admin approval | **Partial** | Data can be managed via Django admin if a public form existed; **no integrated** custom admin portal flow for `ObserverRequest` was found (only `SIGObserver`/legacy admin registrations). |

---

## 3. Apply as SIG member (form + pending + admin approval)

| Requirement | Status | Notes |
|-------------|--------|--------|
| Fields: name, email, mobile, org, designation, state, **multi-SIG**, bio, LinkedIn | **Not done** | `sigregister` (`core/SIG/sigregister.html` + `sigregister` view) only collects **full name, email, mobile, password** — not organization, designation, state, multi-select SIGs, bio, or LinkedIn. |
| Flow: pending → admin approval | **Partial / different** | Registration uses **email OTP**: account is `status=0` until OTP, then **`status=1`**. That is **email verification**, not an admin “pending application” gate. A separate **`ig_account`** path with `application_type` / `application_status` exists for **`admin_membership_requests`** (custom admin), but **`sigregister` does not** set those fields in the reviewed insert. |

---

## 4. SIG member login

| Requirement | Status | Notes |
|-------------|--------|--------|
| Email + password; **only approved** members | **Partial** | `siglogin` authenticates against `ig_account` with `role='member'` and `status=1`. There is **no check** on `application_status='approved'` in the login query, so “approval” is not enforced the same way as in the spec if you rely on a separate approval column. |
| Redirect → **dashboard** | **Not done** | On success, redirect is **`home`**, not `sig_dashboard` (unless `next` is passed). |

---

## 5. SIG dashboard (logged-in members)

| Requirement | Status | Notes |
|-------------|--------|--------|
| All members see **all SIGs** (not restricted per SIG) | **N/A / unknown** | `sig_dashboard` is a **placeholder**; there is no implemented restriction logic to evaluate. |
| Tabs/sections: FI, IPS, DNN, Joint meetings, Consultations, Events | **Not done** | `core/SIG/sig_dashboard.html` shows static cards (hard-coded numbers) and a minimal profile block — **no tabs**, no per-SIG content, no joint meetings / consultations / events feeds. |

---

## 6. SIG meetings (per SIG + joint)

| Requirement | Status | Notes |
|-------------|--------|--------|
| Display: date, agenda file, minutes/MOM, supporting docs | **Partial** | **Admin** side: `admin_meetings` + `ig_meetings` with `agenda_file`, `record_file`, `document_file` (`views.py`). **Member-facing** listing inside SIG dashboard with the same structure was **not found**. |
| Member: upload extra doc → pending → visible after admin approval | **Not done** | No dedicated member upload + approval workflow for meeting-linked documents was identified. |
| Admin: manage agenda, minutes, supporting docs, approve uploads | **Partial** | Admin meetings UI exists; **member upload approval** not implemented as above. |

---

## 7. SIG consultations (isolated from main Stakeholder Engagement)

| Requirement | Status | Notes |
|-------------|--------|--------|
| **Not** linked to main website Stakeholder Engagement; **separate DB** | **Not done** | Consultation comments for logged-in members use **`stakeholder_consultations`** / related tables (`submit_comment` in `views.py`) — i.e. **same ecosystem as the main portal**, not a separate SIG-only module. |
| Dashboard-only, SIG members only; admin creates topics; member responses | **Partial** | Members must be logged in to comment (`member_uuid`); **admin** manages stakeholder consultations globally. There is **no** separate “SIG consultations” product with its own schema and UI as specified. |

---

## 8. SIG events

| Requirement | Status | Notes |
|-------------|--------|--------|
| Upcoming dates, meeting links (Zoom/Meet) | **Partial** | **`ig_events`** and public `events` / `event_detail` exist; they are **not clearly scoped** as SIG-only or per-SIG inside a SIG dashboard. |
| Inside SIG dashboard | **Not done** | No SIG-events section wired into `sig_dashboard`. |

---

## 9. Admin panel (custom IG admin + Django admin)

| Requirement | Status | Notes |
|-------------|--------|--------|
| Approve/reject **observer** applications | **Partial** | `ObserverRequest` / `SIGObserver` in **Django admin**; **custom** `admin-dashboard` flow for observer list/approve was **not** found (membership requests are **`ig_account`**-based). |
| Approve/reject **member** applications | **Partial** | **`admin_membership_requests`** supports applications with `application_type` set and status updates — aligns **if** registration flows populate those columns (current **`sigregister`** path does not). |
| Manage SIG members list | **Partial** | **`admin_member`** can add/list members in `ig_account`; not necessarily aligned with “approved SIG member” semantics only. |
| Meetings, documents, consultations, events, approve member uploads | **Partial** | Meetings + stakeholder consultations + events have admin UIs; **SIG-isolated** consultations and **meeting upload approvals** are missing (see above). |

---

## 10. Core backend entities (spec vs codebase)

| Entity (spec) | In codebase? | Comment |
|-----------------|--------------|---------|
| Users (member / observer / admin) | **Partial** | `ig_account` (members, admin session), Django `User` for staff, `ObserverRequest`/`SIGObserver` for observers — **multiple patterns**, not one unified model. |
| SIGs | **Partial** | Represented as labels in HTML/forms (`SIG_CHOICES`, SIG cards); **no `SIG` table** driving membership. |
| Applications (observer / member) | **Partial** | Observer model exists; member applications via **`ig_account`** fields when used; **sigregister** is minimal OTP signup. |
| Meetings | **Yes** | `ig_meetings` + admin UI. |
| Documents | **Partial** | Meeting files in admin; member-upload pipeline incomplete. |
| Consultations | **Yes (shared)** | `stakeholder_consultations` — **not** SIG-isolated. |
| Responses | **Partial** | `consultation_comments` (and related) via `submit_comment`; not SIG-specific. |
| Events | **Yes** | `ig_events`. |

---

## 11. Key rules (spec compliance)

| Rule | Status |
|------|--------|
| SIG consultation ≠ Stakeholder Engagement | **Not met** — same consultation/comment pipeline used for members today. |
| All SIG members can see all SIGs | **Not implemented** (dashboard content missing). |
| Observer has **no** dashboard access | **Partial** — observer flow not on public site; if observer used Django user, behaviour not aligned with spec without explicit block. |
| Member uploads require admin approval | **Not met** for meetings (see §6). |
| Multi-SIG membership | **Not met** — no multi-select SIG membership model in `sigregister`. |
| Public page ≠ dashboard content | **Partial** — public SIG page exists; dashboard is placeholder, so separation is not really exercised. |

---

## Suggested implementation order (high level)

1. **Clarify identity model:** Single source of truth for SIG member vs observer (`ig_account` vs dedicated tables) and fields for `application_status` / multi-SIG.
2. **Public page:** Fix CTAs (`siglogin` vs `login`); add IG/NIXI copy; add **observer** vs **member** forms (separate URLs); add **approved member directory** per SIG (read-only API or queryset).
3. **Applications:** Expand `sigregister` (or replace) to match member spec; implement observer form + pending + **custom admin** approval (mirror `admin_membership_requests`).
4. **`siglogin`:** Enforce approved-only if using application workflow; redirect to **`sig_dashboard`** by default.
5. **`sig_dashboard`:** Build tabs and feed data: meetings (member view), **new** SIG consultations (new tables), SIG-scoped or global events as per product decision.
6. **SIG consultations:** New models + admin + member UI; **stop** reusing `stakeholder_consultations` if policy requires isolation.
7. **Meetings:** Member views + optional uploads + admin approval queue.

---

## Appendix — Quick file map

| Area | Primary locations |
|------|-------------------|
| Public SIG | `core/sig.html`, `views.sig` |
| Member register / login | `views.sigregister`, `views.verify_otp`, `views.siglogin`, `templates/core/SIG/sigregister.html`, `siglogin.html` |
| Member dashboard | `views.sig_dashboard`, `templates/core/SIG/sig_dashboard.html`, `sig_base.html` |
| Observer (model only) | `core/models.py` (`ObserverRequest`), `core/forms.py` (`ObserverForm`) |
| Admin membership | `views.admin_membership_requests`, `templates/admin/admin-membership-requests.html` |
| Admin meetings | `views.admin_meetings`, `ig_meetings` |
| Stakeholder / comments | `stakeholder_consultations`, `views.submit_comment` |
| Events | `ig_events`, `views.events`, `event_detail` |

---

*Generated from repository review; adjust dates and ticket links as the product evolves.*
