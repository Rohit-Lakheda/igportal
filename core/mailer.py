"""
Centralized email-sending utility for IG Portal.

Provides a single function, pref_send_mail(), used across the site to
send all outgoing notification emails (welcome, registration,
submissions, etc.) from one consistent place instead of duplicating
send_mail() calls everywhere.
"""

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


# ======================================================
# EMAIL TEMPLATES
# Add a new entry here whenever a new email type is needed.
# {placeholders} are filled from the `member` dict / extra kwargs.
# ======================================================
EMAIL_TEMPLATES = {
    "welcome": {
        "subject": "Welcome to IG Portal",
        "message": (
            "Dear {name},\n\n"
            "Welcome to the Bharat Internet Governance Sphere (IG Portal)! "
            "Your account has been created successfully.\n\n"
            "Email: {email}\n\n"
            "Regards,\n"
            "IG Portal Team"
        ),
    },
    "research_submit": {
        "subject": "Research Paper Submitted Successfully",
        "message": (
            "Dear {name},\n\n"
            "Thank you for submitting your research paper \"{title}\" "
            "to the IG Portal. It is now under review.\n\n"
            "Regards,\n"
            "IG Portal Team"
        ),
    },
    "blog_submit": {
        "subject": "Blog Article Submitted Successfully",
        "message": (
            "Dear {name},\n\n"
            "Thank you for submitting your blog article \"{title}\" "
            "to the IG Portal. It is now under editorial review.\n\n"
            "Regards,\n"
            "IG Portal Team"
        ),
    },
    "sig_register": {
        "subject": "SIG Registration Received",
        "message": (
            "Dear {name},\n\n"
            "Your SIG registration request has been received.\n\n"
            "Regards,\n"
            "IG Portal Team"
        ),
    },
    "sig_apply": {
        "subject": "SIG Member Application Received",
        "message": (
            "Dear {name},\n\n"
            "Your SIG membership application has been received and is "
            "pending admin approval.\n\n"
            "Regards,\n"
            "IG Portal Team"
        ),
    },
}

# Templates for which the admin should also get a copy, so pending
# approval items don't go unnoticed.
ADMIN_NOTIFY_TEMPLATES = {"sig_apply", "research_submit"}


def get_client_ip(request):
    """Best-effort extraction of the requester's IP address."""
    if not request:
        return "Unknown"
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "Unknown")


def pref_send_mail(temp_id, member, body="", request=None, notify_admin=False, **extra):
    """
    Centralized email sender for IG Portal.

    Args:
        temp_id (str): Key identifying which template to use (see
                        EMAIL_TEMPLATES above).
        member (dict):  Must include at least "email"; may include
                        "name" and any other fields the template needs.
        body (str):     Optional — overrides the default template
                        message entirely, if provided.
        request:        The Django request object (optional) — used to
                        automatically attach IP address + timestamp.
        notify_admin:   If True, also sends a copy to the admin email
                        (useful for approval-pending templates).
        **extra:        Any additional values needed to fill template
                        placeholders (e.g. title="My Paper").

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    template = EMAIL_TEMPLATES.get(temp_id)
    if not template:
        logger.error("pref_send_mail: unknown temp_id '%s'", temp_id)
        return False

    if not member or not member.get("email"):
        logger.error(
            "pref_send_mail: member email missing for temp_id '%s'", temp_id
        )
        return False

    context = {**member, **extra}
    subject = template["subject"]

    try:
        message = body if body else template["message"].format(**context)
    except KeyError as e:
        logger.error(
            "pref_send_mail: missing field %s for temp_id '%s'", e, temp_id
        )
        return False

    # Append audit-trail footer (action name + timestamp + IP).
    timestamp = timezone.now().strftime("%d %b %Y, %I:%M %p")
    ip_address = get_client_ip(request)
    message += (
        f"\n\n---\n"
        f"Action: {temp_id}\n"
        f"Time: {timestamp}\n"
        f"IP Address: {ip_address}\n"
    )

    recipient_list = [member["email"]]
    if notify_admin and temp_id in ADMIN_NOTIFY_TEMPLATES:
        admin_email = getattr(settings, "ADMIN_NOTIFY_EMAIL", None)
        if admin_email:
            recipient_list.append(admin_email)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info("pref_send_mail: sent '%s' to %s", temp_id, recipient_list)
        return True
    except Exception as e:
        logger.error(
            "pref_send_mail: FAILED to send '%s' to %s - %s",
            temp_id, recipient_list, e
        )
        return False