import re

from django import forms
from django.core.exceptions import ValidationError

from .models import ObserverRequest, Event, SIGMemberRequest

FIRST_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z.'-]*(?: [A-Za-z][A-Za-z.'-]*)?$")
LAST_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z.'-]*$")
MOBILE_RE = re.compile(r"^[0-9]{10}$")

FIRST_NAME_HELP = (
    "Use letters only. One space is allowed between the first and middle name. "
    "A hyphen, apostrophe, or full stop is allowed."
)
LAST_NAME_HELP = (
    "Use letters only, with no spaces. A hyphen, apostrophe, or full stop is allowed."
)
MOBILE_HELP = "Enter a 10-digit mobile number."


def collect_name_errors(first_name, last_name):
    errors = []
    first_name = (first_name or "").strip()
    last_name = (last_name or "").strip()
    if not first_name:
        errors.append("First name is required.")
    elif not FIRST_NAME_RE.fullmatch(first_name):
        errors.append(FIRST_NAME_HELP)
    if last_name and not LAST_NAME_RE.fullmatch(last_name):
        errors.append(LAST_NAME_HELP)
    return errors


def _checked_first_name(value):
    value = (value or "").strip()
    if not FIRST_NAME_RE.fullmatch(value):
        raise ValidationError(FIRST_NAME_HELP)
    return value


def _checked_last_name(value):
    value = (value or "").strip()
    if value and not LAST_NAME_RE.fullmatch(value):
        raise ValidationError(LAST_NAME_HELP)
    return value


def apply_identity_attrs(form):
    if "first_name" in form.fields:
        form.fields["first_name"].widget.attrs.update({
            "pattern": r"[A-Za-z][A-Za-z.'\-]*(?: [A-Za-z][A-Za-z.'\-]*)?",
            "maxlength": "80",
            "title": FIRST_NAME_HELP,
        })
    if "last_name" in form.fields:
        form.fields["last_name"].widget.attrs.update({
            "pattern": r"[A-Za-z][A-Za-z.'\-]*",
            "maxlength": "80",
            "title": LAST_NAME_HELP,
        })
    if "mobile" in form.fields:
        form.fields["mobile"].widget.attrs.update({
            "inputmode": "numeric",
            "pattern": "[0-9]{10}",
            "maxlength": "10",
            "title": MOBILE_HELP,
        })


class PersonNameMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_identity_attrs(self)

    def clean_first_name(self):
        return _checked_first_name(self.cleaned_data.get("first_name"))

    def clean_last_name(self):
        return _checked_last_name(self.cleaned_data.get("last_name"))

SIG_CHOICES = [
    ("Internet Protocols & Standards", "Internet Protocols & Standards"),
    ("Domain Names & Related Issues", "Domain Names & Related Issues"),
    ("Future of Internet", "Future of Internet"),
]


class ObserverForm(PersonNameMixin, forms.ModelForm):
    mobile = forms.RegexField(
        regex=r"^[0-9]{10}$",
        help_text=MOBILE_HELP,
        error_messages={"invalid": MOBILE_HELP},
    )

    sig = forms.ChoiceField(choices=SIG_CHOICES)

    class Meta:
        model = ObserverRequest
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "organization",
            "designation",
            "state",
            "reason",
            "sig",
            "work_experience",
            "linkedin",
        ]
        widgets = {
            "work_experience": forms.Textarea(attrs={"rows": 3}),
            "reason": forms.Textarea(attrs={"rows": 3}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "desc",
            "event_datetime",
            "type",
            "join",
            "flyer",
        ]
        widgets = {
            "event_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "desc": forms.Textarea(attrs={"rows": 4}),
        }

class SIGMemberForm(PersonNameMixin, forms.ModelForm):

    SIG_CHOICES = [
        ("", "Select SIG"),
        ("SIG – DNN", "SIG – DNN (Domain Names & Numbers)"),
        ("SIG – IPS", "SIG – IPS (Internet Protocols & Standards)"),
        ("SIG – FI", "SIG – FI (Future of Internet)"),
    ]

    mobile = forms.RegexField(
        regex=r"^[0-9]{10}$",
        help_text=MOBILE_HELP,
        error_messages={"invalid": MOBILE_HELP},
    )

    target_sigs = forms.ChoiceField(
        choices=SIG_CHOICES,
        required=True,
        label="Choose the SIG you want to apply to"
    )

    class Meta:
        model = SIGMemberRequest

        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "organization",
            "designation",
            "state",
            "target_sigs",
            "bio",
            "linkedin",
        ]

        widgets = {

            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "mobile": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "organization": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "designation": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "target_sigs": forms.Select(attrs={
                "class": "form-control"
            }),

            "bio": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control"
            }),

            "linkedin": forms.URLInput(attrs={
                "class": "form-control"
            }),
        }

