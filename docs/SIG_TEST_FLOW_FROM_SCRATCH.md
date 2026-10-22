# SIG Module Test Flow (From Scratch)

This document provides a complete test runbook for SIG functionality, including:
- member application and approval
- observer application and approval
- SIG login/dashboard
- meeting creation and document lifecycle
- internal consultations
- events
- admin moderation and access controls

Use this as a QA checklist before release.

---

## 1) Prerequisites

- Project setup is complete.
- Database is running and reachable.
- You can run Django management commands.
- Mail sending is configured (or you can verify generated credentials in DB/logs for local testing).

Run these commands first:

```bash
python3 manage.py migrate
python3 manage.py runserver
```

---

## 2) Test Users and Sessions

Use separate browser sessions:
- **Session A (Admin/Super Admin)**: normal window
- **Session B (SIG Member)**: incognito/private window
- **Session C (Optional second member)**: second incognito for visibility checks

Admin login endpoint:
- `http://localhost:8000/Adminn/`

SIG member login endpoint:
- `http://localhost:8000/siglogin/`

---

## 3) Admin Access Rules (Current Behavior)

Admin routes (meeting management, SIG moderation, members module, etc.) require elevated role.

Current accepted roles in `ig_account.role`:
- `super_admin`
- `admin` (legacy compatibility)

If access fails, verify role and status in DB:
- role is `admin` or `super_admin`
- status is `1`

---

## 4) Fresh Start Checklist (Optional but Recommended)

If you want a fully clean test:
- Remove old test users, meetings, consultations, events.
- Keep one valid admin/super admin account.

Minimal SQL checks (run carefully in your DB client):
- verify role values in `ig_account`
- verify pending rows in SIG request tables
- verify `core_meeting`, `core_internalconsultation`, `core_meetingdocument` are available

---

## 5) Public SIG Application Flows

### 5.1 Apply as SIG Member

1. Open: `http://localhost:8000/apply/sig-member/`
2. Fill form with test data:
   - first/last name
   - email/mobile
   - organization/designation/state
   - target SIGs
   - bio/linkedin
3. Submit.

Expected:
- Success message shown.
- New row in `core_sigmemberrequest` with status `pending`.

### 5.2 Apply as Observer

1. Open: `http://localhost:8000/apply/observer/`
2. Fill required fields.
3. Submit.

Expected:
- Success message shown.
- New row in `core_observerrequest` with status `pending`.

---

## 6) SIG Moderation (Admin)

1. Login in Session A via `http://localhost:8000/Adminn/`
2. Open: `http://localhost:8000/dashboard/sig-moderation/`

### 6.1 Approve Member Application

1. In pending member list, click **Approve**.

Expected:
- Member request status becomes `approved`.
- Django auth user is created.
- SIG profile is created and linked.
- Credentials email is sent (or verify in local logs/DB flow).

### 6.2 Reject Member Application

Expected:
- Member request status becomes `rejected`.
- Rejection email path executes.

### 6.3 Approve/Reject Observer

Expected:
- Observer request status updates accordingly.
- Notification email flow executes when email exists.

---

## 7) SIG Member Login and Dashboard Access

1. Use approved member credentials in Session B.
2. Login at: `http://localhost:8000/siglogin/`

Expected:
- Login success.
- Redirect to: `http://localhost:8000/sig_dashboard/`

Access control checks:
- Anonymous user opening `/sig_dashboard/` should be blocked/redirected.
- Non-SIG users should not access SIG dashboard.

---

## 8) Create Meetings (Admin)

1. In Session A, open: `http://localhost:8000/add_meeting`
2. Create meetings for each type:
   - `FI`
   - `TPS` (used as SIG-IPS tab)
   - `DNN`
   - `Joint`
3. For each meeting, test optional fields:
   - agenda file
   - minutes/record file
   - supporting document
   - meeting link

Expected:
- Meeting appears in listing table.
- Files and links are stored.
- SIG dashboard tabs show meetings in correct section.

---

## 9) Meeting Document Upload by Member

1. Session B opens SIG dashboard.
2. Go to any meeting tab.
3. Upload contribution using **Upload Contribution** form.

Expected:
- Upload succeeds with pending message.
- Uploader sees own pending item with status badge.
- Other members should not see pending file until approval.

---

## 10) Meeting Document Moderation (Admin)

1. Session A opens:
   - `http://localhost:8000/dashboard/documents/moderation/`
2. Approve pending document.

Expected:
- Status becomes `approved`.
- Document visible to all SIG members on meeting card.

Reject test:
- Reject should remove/reject item as implemented.

---

## 11) Internal Consultations

Internal consultations are separate from public stakeholder flow and available in SIG dashboard consultation tab.

### 11.1 Create Consultation (Admin via Django Admin)

1. Open: `http://localhost:8000/admin/core/internalconsultation/`
2. Add consultation with:
   - title
   - description
   - sig_type (`FI` / `TPS` / `DNN`)
   - future deadline
   - status `open`
   - optional brief document

Expected:
- Consultation appears in SIG dashboard **SIG Consultations** tab.

### 11.2 Submit Consultation Response (Member)

1. Session B opens consultations tab.
2. Submit:
   - designation
   - organization
   - response text
   - optional file

Expected:
- Success message shown.
- Row created in `core_internalconsultationresponse`.

Negative checks:
- missing required fields should show validation error.
- closed consultation should not accept new response.

---

## 12) SIG Events

### 12.1 Create SIG events (member dashboard)

SIG members see scheduled items from **`core.SIGEvent`**, managed in the admin shell (separate from public **Events** / `ig_events`).

1. Log in as super admin, open **SIG Events** in the sidebar (`/sig-events/`).
2. **Add SIG Event** — set title, description, date/time (use a **future** datetime for “upcoming” and a **past** datetime in another row to confirm filtering), optional join URL, type, and SIG scope.

The legacy **Events** menu item (`admin_events` / `ig_events`) is unchanged for public site events.

### 12.2 Verify on Dashboard

In Session B (approved SIG member), open **SIG Events** tab.

Expected:
- Upcoming `SIGEvent` rows are visible (`event_datetime >= now`).
- Past `SIGEvent` rows are not shown in this list.
- **Open Meeting Link** appears when join URL is set.

---

## 13) Tab-by-Tab Dashboard Validation

Check each tab renders without template errors:
- SIG-FI
- SIG-IPS
- SIG-DNN
- SIG Joint Meetings
- SIG Consultations
- SIG Events

Verify:
- content cards load
- official documents display correctly
- member uploads follow approval rules
- forms submit and show messages

---

## 14) Security and Permission Checks

### 14.1 Admin Routes

Verify only elevated admin can access:
- `/add_meeting`
- `/dashboard/sig-moderation/`
- `/dashboard/documents/moderation/`
- members/admin management routes

### 14.2 Member Routes

Verify:
- SIG dashboard is not public.
- observer/non-member cannot log in as SIG member.

---

## 15) Recommended Test Data Matrix

- 2 member applications (approve 1, reject 1)
- 2 observer applications (approve 1, reject 1)
- 4 meetings (FI/TPS/DNN/Joint)
- at least 1 consultation per SIG type
- 3 **SIG** events (`/sig-events/`, `core.SIGEvent`: 2 future, 1 past)
- 2 member document uploads (approve 1, reject 1)

---

## 16) Quick Smoke Test (5-10 Minutes)

1. Admin login works.
2. Create one FI meeting with agenda file.
3. Approve one pending SIG member.
4. Member login works and opens dashboard.
5. Member uploads one meeting doc.
6. Admin approves uploaded doc.
7. Member sees approved doc publicly in meeting tab.
8. Member submits one consultation response.
9. SIG Events tab shows upcoming `SIGEvent` (not past-dated rows).

If all pass, core SIG flow is healthy.

---

## 17) Known Mapping Notes

- Dashboard tab label uses **SIG-IPS**, backend meeting type value is currently `TPS`.
- Admin custom login and Django admin are different systems; use correct login for the target panel.

