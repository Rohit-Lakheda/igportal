# ============================
# views.py
# ============================

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.urls import reverse
import re
import secrets
from datetime import date, datetime

from .models import (
    Event,
    Consultation,
    GroupMaster,
    DesignationMaster,
    SigMember,
    SIGProfile,
    SIGObserver,
    UserProfile,
)
from .forms import ObserverForm, EventForm


# ---------- helpers ----------
def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def is_super_admin_request(request):
    session_role = (request.session.get("admin_role") or "").strip().lower()
    # Backward-compatible: legacy installs may still use "admin".
    elevated_roles = {"super_admin", "admin"}
    return session_role in elevated_roles or (
        request.user.is_authenticated and request.user.is_superuser
    )


def generate_password():
    return secrets.token_urlsafe(10)


# ---------- public pages ----------
def base(request):
    return render(request, "base.html")


def home(request):
    feed = [
        {"text": "Upcoming Event: Internet Governance Workshop", "time": timezone.now()},
        {"text": "Open Consultation: ICP-2 V2 now live", "time": timezone.now()},
        {"text": "India@Global Forums: APNIC update published", "time": timezone.now()},
    ]
    return render(request, "core/home.html", {"feed": feed})

from collections import defaultdict


# def capacity(request):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id, name, about, photo, cohort
#             FROM capacity_building_profiles
#             ORDER BY cohort, id
#         """)
#         cols = [c[0] for c in cursor.description]
#         rows = [dict(zip(cols, r)) for r in cursor.fetchall()]

#     cohorts = defaultdict(list)
#     for r in rows:
#         cohorts[r["cohort"]].append(r)

#     return render(request, "core/capacity.html", {
#         "cohorts": dict(cohorts),
#         "MEDIA_URL": settings.MEDIA_URL
#     })


def capacity(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, about, photo, cohort
            FROM capacity_building_profiles
            ORDER BY cohort DESC, id DESC
        """)
        cols = [c[0] for c in cursor.description]
        rows = [dict(zip(cols, r)) for r in cursor.fetchall()]

    cohorts = defaultdict(list)
    for r in rows:
        cohorts[r["cohort"]].append(r)

    # Convert to sorted list (latest cohort first)
    cohort_list = sorted(cohorts.items(), key=lambda x: x[0], reverse=True)

    return render(request, "core/capacity.html", {
        "cohort_list": cohort_list,   # [(cohort, fellows), ...]
        "MEDIA_URL": settings.MEDIA_URL
    })

def cohort_fellows(request, cohort):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, about, photo
            FROM capacity_building_profiles
            WHERE cohort = %s
            ORDER BY id DESC
        """, [cohort])

        cols = [c[0] for c in cursor.description]
        fellows = [dict(zip(cols, r)) for r in cursor.fetchall()]

    return render(request, "core/cohort_fellows.html", {
        "cohort": cohort,
        "fellows": fellows,
        "MEDIA_URL": settings.MEDIA_URL
    })

def global_forums(request):
    """
    India at Global Forums — dummy content for policy tiles, positions, and carousel.
    Tile backgrounds use Wikimedia Commons media representing each forum’s official branding.
    """
    forum_topics = [
        {
            "id": "icann",
            "name": "ICANN",
            "tagline": "Internet identifiers, DNS & naming policy",
            "logo_variant": "wide",
            "bg_image": (
                "https://itp.cdn.icann.org/assets/images/www-static/logo/"
                "icann-logo-tagline-en_680x152.webp"
            ),
            "positions": [
                {
                    "date": "2025-03-01",
                    "title": "ccNSO guidance on DNS abuse metrics",
                    "summary": (
                        "India noted the need for metrics that respect national legal frameworks "
                        "and encouraged transparent reporting without duplicating local enforcement."
                    ),
                    "source_label": "ccNSO session (illustrative)",
                },
                {
                    "date": "2025-01-22",
                    "title": "New gTLD subsequent rounds — public comment",
                    "summary": (
                        "Submission emphasised affordability for applicants from developing economies "
                        "and clarity on geographic/cultural string protections."
                    ),
                    "source_label": "Public comment summary (dummy)",
                },
                {
                    "date": "2024-11-08",
                    "title": "GNSO policy development on privacy proxy services",
                    "summary": (
                        "Aligned with MeitY-led stakeholder consultations on balancing WHOIS utility "
                        "with data protection under Indian law."
                    ),
                    "source_label": "GNSO materials (illustrative)",
                },
            ],
        },
        {
            "id": "igf",
            "name": "Internet Governance Forum (IGF)",
            "tagline": "Multi-stakeholder dialogue on global Internet policy",
            "logo_variant": "tall",
            "bg_image": (
                "https://www.intgovforum.org/sites/default/files/igflogo2.png"
            ),
            "positions": [
                {
                    "date": "2025-02-18",
                    "title": "IGF 2025 thematic inputs — AI & connectivity",
                    "summary": (
                        "India highlighted inclusive AI governance, open standards, and "
                        "last-mile connectivity investments as national priorities."
                    ),
                    "source_label": "National IGF track (dummy)",
                },
                {
                    "date": "2024-12-05",
                    "title": "WSIS+20 review — development dimension",
                    "summary": (
                        "Stressed bridging digital divides, capacity building, and meaningful "
                        "participation for Global South delegations."
                    ),
                    "source_label": "WSIS coordination (illustrative)",
                },
                {
                    "date": "2024-09-14",
                    "title": "Cybersecurity & trust — main session intervention",
                    "summary": (
                        "Called for norms that strengthen resilience while respecting sovereignty "
                        "and cross-border cooperation on incident response."
                    ),
                    "source_label": "IGF session record (dummy)",
                },
            ],
        },
        {
            "id": "apnic",
            "name": "APNIC",
            "tagline": "Asia–Pacific Internet number resources",
            "bg_image": (
                "https://webdist.data.apnic.net/web-framework-theme/9.1.5/images/apnic.svg"
            ),
            "positions": [
                {
                    "date": "2025-01-30",
                    "title": "IPv6 deployment and measurement",
                    "summary": (
                        "Supported APNIC community efforts on accurate routing data and IPv6 "
                        "adoption reporting for the region, including Indian ISPs."
                    ),
                    "source_label": "APNIC conference workshop (dummy)",
                },
                {
                    "date": "2024-10-21",
                    "title": "RPKI and routing security",
                    "summary": (
                        "India reiterated commitment to ROA uptake and collaboration on "
                        "anti-hijack practices with neighbouring economies."
                    ),
                    "source_label": "Routing SIG (illustrative)",
                },
            ],
        },
        {
            "id": "itu",
            "name": "ITU",
            "tagline": "Telecommunication standardisation & development",
            "bg_image": (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/"
                "International_Telecommunication_Union_logo.svg/"
                "480px-International_Telecommunication_Union_logo.svg.png"
            ),
            "positions": [
                {
                    "date": "2025-02-27",
                    "title": "WTSA / standardisation priorities",
                    "summary": (
                        "Underlined interoperability, security-by-design, and reference to "
                        "existing multistakeholder Internet governance processes."
                    ),
                    "source_label": "Delegation brief (dummy)",
                },
                {
                    "date": "2024-08-19",
                    "title": "Development — digital public infrastructure",
                    "summary": (
                        "Shared India Stack–inspired lessons on identity, payments, and "
                        "consent-based data sharing for sustainable development goals."
                    ),
                    "source_label": "ITU-D forum (illustrative)",
                },
            ],
        },
        {
            "id": "w3c",
            "name": "W3C",
            "tagline": "Web standards & accessibility",
            "bg_image": (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/"
                "W3C_icon.svg/480px-W3C_icon.svg.png"
            ),
            "positions": [
                {
                    "date": "2025-03-12",
                    "title": "Web accessibility & Indian languages",
                    "summary": (
                        "Encouraged WCAG adoption in e-governance templates and Indic script "
                        "shaping improvements in browser engines."
                    ),
                    "source_label": "WAI community (dummy)",
                },
                {
                    "date": "2024-12-01",
                    "title": "Privacy-preserving web APIs",
                    "summary": (
                        "Contributed to discussion on advertising technology changes while "
                        "preserving user agency and regulatory alignment."
                    ),
                    "source_label": "WebPM WG note (illustrative)",
                },
            ],
        },
    ]

    for topic in forum_topics:
        topic["positions"] = sorted(
            topic["positions"],
            key=lambda p: p["date"],
            reverse=True,
        )
        for p in topic["positions"]:
            p["date_display"] = datetime.strptime(
                p["date"], "%Y-%m-%d"
            ).strftime("%d %b %Y")

    carousel_slides = [
        {
            "src": (
                "https://images.unsplash.com/photo-1526304760382-3591ee3c7604"
                "?auto=format&fit=crop&w=1600&q=80"
            ),
            "alt": "Delegates in a conference hall",
            "caption": "India’s engagement in multistakeholder Internet governance dialogues (illustrative).",
        },
        {
            "src": (
                "https://images.unsplash.com/photo-1540575467063-27aef4e929bd"
                "?auto=format&fit=crop&w=1600&q=80"
            ),
            "alt": "Panel discussion at a summit",
            "caption": "National and regional forums feeding into global policy tracks (dummy caption).",
        },
        {
            "src": (
                "https://images.unsplash.com/photo-1475721027785-f74eccf877e2"
                "?auto=format&fit=crop&w=1600&q=80"
            ),
            "alt": "Audience at a technology event",
            "caption": "Stakeholder consultations supporting India’s international positions (illustrative).",
        },
        {
            "src": (
                "https://images.unsplash.com/photo-1504384308090-c54be3855833"
                "?auto=format&fit=crop&w=1600&q=80"
            ),
            "alt": "Modern workspace with connectivity theme",
            "caption": "Capacity building and research inputs for global standards bodies (dummy).",
        },
    ]

    return render(
        request,
        "core/global.html",
        {
            "forum_topics": forum_topics,
            "carousel_slides": carousel_slides,
            "page": "global_forums",
        },
    )


def events(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, title, description, event_date,event_dateto,event_type, event_link, photo
            FROM ig_events
            ORDER BY event_date DESC
        """)
        columns = [c[0] for c in cursor.description]
        events = [dict(zip(columns, r)) for r in cursor.fetchall()]

    return render(request, "core/events.html", {"events": events,
        "MEDIA_URL": settings.MEDIA_URL,
        "page":'event_page'
        })


def _consultation_bucket(c, today):
    """
    Mutually exclusive bucket for public proceedings listing.
    Upcoming: open_date in the future.
    Pending: Draft (not yet published / awaiting go-live).
    Open: published and within submission window.
    Closed: Closed, Archived, or past close_date.
    """
    od, cd = c.get("open_date"), c.get("close_date")
    st = (c.get("status") or "").strip()

    if od and od > today:
        return "upcoming"
    if st == "Draft":
        return "pending"
    if st == "Open" and (cd is None or cd >= today):
        return "open"
    return "closed"


def consultations(request):
    today = date.today()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                id,
                title,
                description,
                open_date,
                close_date,
                organization,
                status
            FROM stakeholder_consultations
            WHERE category IS NULL OR LOWER(category) NOT LIKE 'sig%%'
            ORDER BY updated_at DESC
        """)

        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    open_proceedings = []
    closed_proceedings = []
    pending_proceedings = []
    upcoming_proceedings = []

    for c in rows:
        bucket = _consultation_bucket(c, today)
        if bucket == "open":
            open_proceedings.append(c)
        elif bucket == "closed":
            closed_proceedings.append(c)
        elif bucket == "pending":
            pending_proceedings.append(c)
        else:
            upcoming_proceedings.append(c)

    _far = date(2099, 12, 31)
    _past = date(1900, 1, 1)

    open_proceedings.sort(
        key=lambda x: (x.get("close_date") or _far, x.get("id", 0)),
    )
    closed_proceedings.sort(
        key=lambda x: (x.get("close_date") or _past, x.get("id", 0)),
        reverse=True,
    )
    pending_proceedings.sort(key=lambda x: x.get("id", 0), reverse=True)
    upcoming_proceedings.sort(
        key=lambda x: (x.get("open_date") or _far, x.get("id", 0)),
    )

    for c in rows:
        if c.get("close_date"):
            c["days_left"] = (c["close_date"] - today).days
        else:
            c["days_left"] = None

    return render(request, "core/consultations.html", {
        "open_proceedings": open_proceedings,
        "closed_proceedings": closed_proceedings,
        "pending_proceedings": pending_proceedings,
        "upcoming_proceedings": upcoming_proceedings,
        "today": today,
    })


def blogs(request):
    return render(request,"core/blogs.html")

from .models import BlogArticle
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_http_methods
from .models import BlogArticle
import bleach

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_IMAGE_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.webp'
]

# def blog_page(request):
#     t=request.POST.get('title')
#     print(t)
#     print("this funton is calling")
#     return redirect(blogs)



@require_http_methods(["GET", "POST"])
def blog_page(request):
    print('function calling')

    if request.method == "POST":
        print('yes received this')

        try:

            member_uuid = request.session.get('member_uuid')

            if not member_uuid:

                messages.error(
                    request,
                    'Please login first.'
                )

                return redirect('login')

            # =========================
            # GET DATA
            # =========================

            title = request.POST.get(
                'title',
                ''
            ).strip()

            article_type = request.POST.get(
                'article_type',
                ''
            ).strip()

            read_time = request.POST.get(
                'read_time',
                ''
            ).strip()

            tags = request.POST.get(
                'tags',
                ''
            ).strip()

            description = request.POST.get(
                'description',
                ''
            ).strip()

            content = request.POST.get(
                'content',
                ''
            ).strip()

            image = request.FILES.get('image')

            # =========================
            # VALIDATION
            # =========================

            if not title:

                messages.error(
                    request,
                    'Title is required.'
                )

                return redirect('blog_page')

            if len(title) < 10:

                messages.error(
                    request,
                    'Title must be minimum 10 characters.'
                )

                return redirect('blog_page')

            if len(description) < 30:

                messages.error(
                    request,
                    'Description must be minimum 30 characters.'
                )

                return redirect('blog_page')

            if len(content) < 200:

                messages.error(
                    request,
                    'Article content must be minimum 200 characters.'
                )

                return redirect('blog_page')

            # =========================
            # SANITIZE
            # =========================

            title = bleach.clean(
                title,
                strip=True
            )

            article_type = bleach.clean(
                article_type,
                strip=True
            )

            read_time = bleach.clean(
                read_time,
                strip=True
            )

            tags = bleach.clean(
                tags,
                strip=True
            )

            description = bleach.clean(
                description,
                strip=True
            )

            content = bleach.clean(
                content,
                tags=[],
                strip=True
            )

            # =========================
            # IMAGE VALIDATION
            # =========================

            if image:

                ext = os.path.splitext(
                    image.name
                )[1].lower()

                if ext not in ALLOWED_IMAGE_EXTENSIONS:

                    messages.error(
                        request,
                        'Only JPG, PNG and WEBP allowed.'
                    )

                    return redirect('blog_page')

                if image.size > MAX_IMAGE_SIZE:

                    messages.error(
                        request,
                        'Image size must be less than 2MB.'
                    )

                    return redirect('blog_page')

            # =========================
            # SAVE
            # =========================

            BlogArticle.objects.create(
                member_uuid=member_uuid,
                title=title,
                article_type=article_type,
                read_time=read_time,
                tags=tags,
                image=image,
                description=description,
                content=content,
                status='Pending'
            )

            messages.success(
                request,
                'Article submitted successfully.'
            )

            return redirect('blog_page')

        except Exception as e:

            print(e)

            messages.error(
                request,
                'Something went wrong.'
            )

            return redirect('blog_page')

    # =========================
    # GET ARTICLES
    # =========================

    articles = BlogArticle.objects.filter(
        status='Approved'
    ).order_by('-id')

    return render(
        request,
        'core/blogs.html',
        {
            'articles': articles
        }
    )







# def Proceedingsdtl(request, id):
#     today = date.today()

#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT
#                 id,
#                 title,
#                 description,
#                 open_date,
#                 close_date,
#                 organization,
#                 input_focus,
#                 proposals,
#                 contact_email,
#                 category,
#                 requester,
#                 status
#             FROM stakeholder_consultations
#             WHERE id = %s
#         """, [id])

#         row = cursor.fetchone()

#     if not row:
#         return render(request, "404.html", status=404)

#     columns = [
#         "id","title","description","open_date","close_date",
#         "organization","input_focus","proposals",
#         "contact_email","category","requester","status"
#     ]

#     c = dict(zip(columns, row))

#     # Days left calculation
#     if c["close_date"]:
#         c["days_left"] = (c["close_date"] - today).days
#     else:
#         c["days_left"] = None


#     return render(request, "core/Proceedingsdtl.html", {
#         "c": c,
#         "today": today
#     }) 



def Proceedingsdtl(request, id):
    today = date.today()

    # ---------- FETCH CONSULTATION ----------
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                id,
                title,
                description,
                open_date,
                close_date,
                organization,
                input_focus,
                proposals,
                contact_email,
                category,
                requester,
                status
            FROM stakeholder_consultations
            WHERE id = %s
              AND (category IS NULL OR LOWER(category) NOT LIKE 'sig%%')
        """, [id])

        row = cursor.fetchone()

    if not row:
        return render(request, "404.html", status=404)

    columns = [
        "id", "title", "description", "open_date", "close_date",
        "organization", "input_focus", "proposals",
        "contact_email", "category", "requester", "status"
    ]

    c = dict(zip(columns, row))

    # ---------- DAYS LEFT ----------
    if c["close_date"]:
        c["days_left"] = (c["close_date"] - today).days
    else:
        c["days_left"] = None

    already_commented = False
    user_comment = None

    # ---------- CHECK LOGIN + MAP UUID → USER ID ----------
    if request.session.get("member_uuid"):
        member_uuid = request.session["member_uuid"]

        with connection.cursor() as cursor:
            # Step 1: Get user_id from ig_account
            cursor.execute("""
                SELECT id
                FROM ig_account
                WHERE uuid = %s
                  AND role = 'Member'
                  AND status = 1
                LIMIT 1
            """, [member_uuid])

            user_row = cursor.fetchone()

        if user_row:
            user_id = user_row[0]

            with connection.cursor() as cursor:
                # Step 2: Fetch user's comment
                cursor.execute("""
                    SELECT designation, organization, comment, document_path, status, created_at
                    FROM consultation_comments
                    WHERE consultation_id = %s
                      AND user_id = %s
                    LIMIT 1
                """, [c["id"], user_id])

                comment_row = cursor.fetchone()
                if comment_row:
                    already_commented = True
                    user_comment = {
                        "designation": comment_row[0],
                        "organization": comment_row[1],
                        "comment": comment_row[2],
                        "document_path": comment_row[3],
                        "status": comment_row[4],
                        "created_at": comment_row[5]
                    }

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT document_name, document_path, uploaded_at
            FROM stakeholder_documents
            WHERE consultation_id = %s
            ORDER BY uploaded_at DESC
            """,
            [id],
        )
        consultation_docs = [
            {
                "document_name": r[0],
                "document_path": _stakeholder_document_url(r[1]),
                "uploaded_at": r[2],
            }
            for r in cursor.fetchall()
        ]

    return render(request, "core/Proceedingsdtl.html", {
        "c": c,
        "today": today,
        "already_commented": already_commented,
        "user_comment": user_comment,
        "consultation_docs": consultation_docs,
    })















# ---------- SIG observer ----------
def sig(request):
    return render(request, "core/sig.html")


@login_required
@user_passes_test(is_staff_user)
def create_sig_user(request):
    if request.method == "POST":
        email = request.POST.get("email").strip().lower()
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        mobile = request.POST.get("mobile")
        sig_role = request.POST.get("sig_role")

        # 🔒 EMAIL UNIQUE CHECK
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect("create_sig_user")

        # USERNAME SAFE GENERATION
        base_username = email.split("@")[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        password = generate_password()

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname,
            is_active=True,
        )

        # CREATE SIG PROFILE (ONE-TO-ONE SAFE)
        profile = SIGProfile.objects.create(
            user=user,
            mobile_number=mobile,
        )
        
        from core.models import SIG
        sig_roles = request.POST.getlist("sig_role")
        if not sig_roles and sig_role:
            sig_roles = [sig_role]
            
        for role_code in sig_roles:
            role_code = role_code.strip()
            if role_code:
                sig_obj, _ = SIG.objects.get_or_create(code=role_code, defaults={'name': role_code})
                profile.sigs.add(sig_obj)

        # 📧 SEND EMAIL (ONLY AFTER SUCCESS)
        send_mail(
            subject="Welcome to IG Portal – Login Credentials",
            message=(
                f"Dear {fname},\n\n"
                f"Your SIG account has been created successfully.\n\n"
                f"Login Details:\n"
                f"Username: {username}\n"
                f"Password: {password}\n\n"
                f"Login URL: {settings.SITE_URL}/login/\n\n"
                f"Please change your password after first login.\n\n"
                f"Regards,\nIG Portal Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "SIG user created successfully and email sent.")
        return redirect("create_sig_user")

    return render(request, "admin/create_sig_user.html")
# def create_sig_user(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         fname = request.POST.get("first_name")
#         lname = request.POST.get("last_name")
#         mobile = request.POST.get("mobile")
#         sig_role = request.POST.get("sig_role")

#         username = email.split("@")[0]
#         password = generate_password()

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "User already exists.")
#             return redirect("create_sig_user")

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             first_name=fname,
#             last_name=lname,
#         )

#         SIGProfile.objects.create(
#             user=user,
#             sig_role=sig_role,
#             mobile_number=mobile,
#         )

#         send_mail(
#             "Welcome to IG Portal",
#             f"Username: {username}\nPassword: {password}",
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#             fail_silently=True,
#         )

#         messages.success(request, "SIG user created successfully.")
#         return redirect("create_sig_user")

#     return render(request, "admin/create_sig_user.html")


@login_required
@user_passes_test(is_staff_user)
def admin_create_sig_member(request):
    return render(
        request,
        "core/admin_create_sig_member.html",
        {
            "groups": GroupMaster.objects.all(),
            "designations": DesignationMaster.objects.all(),
        },
    )


# ---------- auth ----------
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect("admin_dashboard" if user.is_staff else "home")

        messages.error(request, "Invalid credentials.")

    return render(request, "core/login.html")


def logout_view(request):
    auth_logout(request)   # ✅ correct alias
    return redirect("login")



# ---------- dashboard ----------


@login_required
def add_event(request):
    if not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect("home")

    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Event added successfully.")
        return redirect("events")

    return render(request, "core/add_event.html", {"form": form})


# ============================
# urls.py
# ============================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)

            if user.is_staff:
                return redirect("admin1_dashboard")  # ✅ URL NAME

            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "core/login.html")




def add_meeting(request):
    if not is_super_admin_request(request):
        messages.error(request, "Super admin access is required for this page.")
        return redirect("sigadmin")

    from .models import Meeting
    if request.method == "POST":
        action = request.POST.get("action", "create")
        if action == "delete":
            meeting_id = request.POST.get("meeting_id")
            meeting = Meeting.objects.filter(id=meeting_id).first()
            if not meeting:
                messages.error(request, "Meeting not found.")
                return redirect("add_meeting")
            meeting.delete()
            messages.success(request, "Meeting deleted successfully.")
            return redirect("add_meeting")

        title = request.POST.get("title")
        date_str = request.POST.get("date")
        sig_type = request.POST.get("sig_type")
        meeting_link = request.POST.get("meeting_link", "").strip()
        agenda = request.FILES.get("agenda")
        minutes = request.FILES.get("minutes")
        supporting_document = request.FILES.get("supporting_document")
        if title and date_str and sig_type and agenda and minutes and supporting_document:
            try:
                meeting_dt = datetime.fromisoformat(date_str)
            except ValueError:
                messages.error(request, "Invalid date format. Please choose a valid date and time.")
                return redirect("add_meeting")

            Meeting.objects.create(
                title=title,
                date=meeting_dt,
                sig_type=sig_type,
                meeting_link=meeting_link or None,
                agenda=agenda,
                minutes=minutes,
                supporting_document=supporting_document,
            )
            messages.success(request, "Meeting created successfully.")
            return redirect("add_meeting")
        else:
            messages.error(
                request,
                "Please provide title, meeting date, SIG type, agenda, minutes, and supporting document.",
            )
            
    meetings = Meeting.objects.all().order_by("-date")
    return render(request, "core/add_meeting.html", {"meetings": meetings})

@login_required
def member(request):
    return render(request, "core/member.html")

@login_required
def consultation(request):
    return render(request, "core/consultation.html")


# abhishek work


from django.shortcuts import render, redirect
from django.db import connection ,transaction
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from functools import wraps
import time
import math
import random, string
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import make_password
import uuid, random, string







    
def chortdtl(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM capacity_building_profiles WHERE id=%s",
            [id]
        )
        cols = [c[0] for c in cursor.description]
        row = cursor.fetchone()

    profile = dict(zip(cols, row)) if row else None

    return render(request, "core/chortdtl.html", {
        "profile": profile,
        "MEDIA_URL": settings.MEDIA_URL
    })

def about(request):
    return render(request, "core/about.html")

 

# def admin(request):
#     return render(request,'admin/admin-login.html')



MAX_ATTEMPTS = 5
LOCK_TIME_MINUTES = 30

# ------------------
# CUSTOM DECORATOR FOR ADMIN DASHBOARD
# ------------------
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if is_super_admin_request(request):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Super admin access is required.")
        return redirect('sigadmin')  # LOGIN_URL
    return _wrapped_view


# ------------------
# ADMIN LOGIN
# ------------------

@csrf_protect
def sigadmin(request):
    if request.method == "POST":
        login_input = request.POST.get("login", "").strip()
        password_input = request.POST.get("password", "").strip()

        if not login_input or not password_input:
            messages.error(request, "Email and password are required.")
            return render(request, 'admin/admin-login.html')

        # Fetch user
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, uuid, password_hash, role,
                       failed_attempts, locked_until
                FROM ig_account
                WHERE email = %s
                  AND LOWER(role) IN ('super_admin', 'admin')
                  AND status = 1
                LIMIT 1
            """, [login_input])
            row = cursor.fetchone()

        if not row:
            messages.error(request, "Invalid login credentials.")
            return render(request, 'admin/admin-login.html')

        user_id, uuid, password_hash, role, failed_attempts, locked_until = row

        # Convert locked_until to timezone-aware datetime
        if locked_until:
            locked_until = timezone.make_aware(locked_until)
            if locked_until > timezone.now():
                messages.error(request, f"Account temporarily locked. Try again after {locked_until}.")
                return render(request, 'admin/admin-login.html')

        # Check password
        if check_password(password_input, password_hash):
            # Login success
            request.session.flush()  # prevent session fixation
            request.session['admin_uuid'] = uuid
            request.session['admin_role'] = role
            request.session.set_expiry(60 * 60)  # 1 hour session

            # Reset failed attempts and last login
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ig_account
                    SET failed_attempts = 0,
                        locked_until = NULL,
                        last_login = %s
                    WHERE id = %s
                """, [timezone.now(), user_id])

            messages.success(request, "Login successful.")
            next_url = request.GET.get('next') or '/admin-dashboard/'  # LOGIN_REDIRECT_URL
            return redirect(next_url)

        # Password incorrect → increment failed attempts
        failed_attempts += 1
        lock_time = None
        if failed_attempts >= MAX_ATTEMPTS:
            lock_time = timezone.now() + timezone.timedelta(minutes=LOCK_TIME_MINUTES)
            messages.error(request, f"Too many failed attempts. Account locked until {lock_time}.")
        else:
            messages.error(request, "Invalid login credentials.")

        # Update DB
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE ig_account
                SET failed_attempts = %s,
                    locked_until = %s
                WHERE id = %s
            """, [failed_attempts, lock_time, user_id])

    return render(request, 'admin/admin-login.html')



@csrf_protect
def admin_profile(request):
    admin_uuid = request.session.get("admin_uuid")
    if not admin_uuid:
        return redirect("admin_login")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, email, role, company_name,
                   mobile, last_login, created_at
            FROM ig_account
            WHERE uuid=%s
            LIMIT 1
        """, [admin_uuid])
        user = cursor.fetchone()

    if not user:
        return redirect("admin_dashboard")

    user_id = user[0]
    sweet_message = None
    sweet_icon = None

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        with connection.cursor() as cursor:
            cursor.execute("SELECT password_hash FROM ig_account WHERE id=%s", [user_id])
            stored_hash = cursor.fetchone()[0]

        if not check_password(current_password, stored_hash):
            sweet_message = "Current password is incorrect."
            sweet_icon = "error"

        elif new_password != confirm_password:
            sweet_message = "New passwords do not match."
            sweet_icon = "error"

        elif len(new_password) < 6:
            sweet_message = "Password must be at least 6 characters."
            sweet_icon = "error"

        else:
            new_hash = make_password(new_password)
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ig_account
                    SET password_hash=%s,
                        updated_at=%s
                    WHERE id=%s
                """, [new_hash, timezone.now(), user_id])

            sweet_message = "Password updated successfully."
            sweet_icon = "success"

    return render(request, "admin/admin-user.html", {
        "user": user,
        "sweet_message": sweet_message,
        "sweet_icon": sweet_icon
    })





@admin_required
@csrf_protect
def admin_membership_requests(request):
    from .models import SIG, SIGMemberRequest, SIGProfile

    def approve_sig_member_request(member_req, custom_password=""):
        existing_user = User.objects.filter(email__iexact=member_req.email).first()

        if existing_user and hasattr(existing_user, "sigprofile"):
            return None, "This email is already mapped to an existing SIG profile."


        base_username = member_req.email.split("@")[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exclude(email__iexact=member_req.email).exists():
            username = f"{base_username}{counter}"
            counter += 1

        password = (custom_password or "").strip() or generate_password()
        if len(password) < 6:
            return None, "Password must be at least 6 characters."

        if existing_user:
            user = existing_user
            user.username = username
            user.first_name = member_req.first_name
            user.last_name = member_req.last_name
            user.is_active = True
            user.set_password(password)
            user.save()
        else:
            user = User.objects.create_user(
                username=username,
                email=member_req.email,
                password=password,
                first_name=member_req.first_name,
                last_name=member_req.last_name,
                is_active=True,
            )

        profile, _ = SIGProfile.objects.get_or_create(
            user=user,
            defaults={"mobile_number": member_req.mobile},
        )
        if member_req.mobile and profile.mobile_number != member_req.mobile:
            profile.mobile_number = member_req.mobile
            profile.save(update_fields=["mobile_number"])

        if member_req.target_sigs:
            sigs_list = [s.strip() for s in member_req.target_sigs.split(",") if s.strip()]
            for code in sigs_list:
                sig_obj, _ = SIG.objects.get_or_create(code=code, defaults={"name": code})
                profile.sigs.add(sig_obj)

        member_req.status = "approved"
        member_req.save(update_fields=["status"])

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE ig_account
                SET application_status='approved',
                    status=1,
                    updated_at=%s
                WHERE email=%s
                  AND LOWER(role)='member'
                """,
                [timezone.now(), member_req.email],
            )

        send_mail(
            subject="SIG Member Application Approved",
            message=(
                f"Dear {member_req.first_name},\n\n"
                "Your SIG membership application has been approved.\n"
                f"Username: {user.username}\n"
                f"Password: {password}\n\n"
                "Please login at: https://ig-portal.in/siglogin/\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_req.email],
            fail_silently=True,
        )
        return user, None

    search = request.GET.get("search", "")
    status = request.GET.get("status", "")

    query = """
        SELECT id, email, company_name, mobile,
               state, sig_selection,
               application_type, application_status, reason
        FROM ig_account
        WHERE application_type IS NOT NULL
    """

    params = []

    if search:
        query += " AND (email LIKE %s OR company_name LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    if status:
        query += " AND application_status=%s"
        params.append(status)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()

    users = [
        {
            "id": r[0],
            "email": r[1],
            "company_name": r[2],
            "mobile": r[3],
            "state": r[4],
            "sig_selection": r[5],
            "application_type": r[6],
            "application_status": r[7],
            "reason": r[8],
        }
        for r in rows
    ]

    if request.method == "POST":
        source = request.POST.get("source", "ig_account")

        if source == "sig_member_request":
            req_id = request.POST.get("request_id")
            action = request.POST.get("action")
            custom_password = request.POST.get("custom_password", "")
            member_req = get_object_or_404(SIGMemberRequest, id=req_id)

            if action == "approve":
                _, err = approve_sig_member_request(member_req, custom_password=custom_password)
                if err:
                    messages.error(request, err)
                else:
                    messages.success(request, f"Approved SIG profile for {member_req.first_name} {member_req.last_name}.")
            elif action == "reject":
                member_req.status = "rejected"
                member_req.save(update_fields=["status"])
                messages.success(request, "SIG member request rejected.")
            else:
                messages.error(request, "Invalid action.")

            return redirect("admin_membership_requests")

        user_id = request.POST.get("user_id")
        new_status = request.POST.get("status")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE ig_account
                SET application_status=%s,
                    status=%s
                WHERE id=%s
                """,
                [new_status, 1 if new_status == "approved" else 0, user_id],
            )

        return redirect("admin_membership_requests")

    sig_member_requests = SIGMemberRequest.objects.all().order_by("-submitted_at")
    if status in {"pending", "approved", "rejected"}:
        sig_member_requests = sig_member_requests.filter(status=status)

    return render(request, "admin/admin-membership-requests.html", {
        "users": users,
        "sig_member_requests": sig_member_requests,
        "search": search,
        "status": status
    })


@admin_required
@csrf_protect
def admin_sig_member_requests(request):
    from .models import SIGMemberRequest

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    qs = SIGMemberRequest.objects.all().order_by("-submitted_at")

    if search:
        qs = qs.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(organization__icontains=search)
        )
    if status in {"pending", "approved", "rejected"}:
        qs = qs.filter(status=status)

    if request.method == "POST":
        req_id = request.POST.get("request_id")
        action = request.POST.get("action")
        custom_password = request.POST.get("custom_password", "")
        member_req = get_object_or_404(SIGMemberRequest, id=req_id)

        # Reuse centralized flow by proxy posting to admin_membership_requests logic style.
        if action == "approve":
            # minimal duplicate logic to keep view independent
            existing_user = User.objects.filter(email__iexact=member_req.email).first()
            if existing_user and hasattr(existing_user, "sigprofile"):
                messages.error(request, "This email is already mapped to an existing SIG profile.")
                return redirect("admin_sig_member_requests")

            base_username = member_req.email.split("@")[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exclude(email__iexact=member_req.email).exists():
                username = f"{base_username}{counter}"
                counter += 1

            password = (custom_password or "").strip() or generate_password()
            if len(password) < 6:
                messages.error(request, "Password must be at least 6 characters.")
                return redirect("admin_sig_member_requests")

            if existing_user:
                user = existing_user
                user.username = username
                user.first_name = member_req.first_name
                user.last_name = member_req.last_name
                user.is_active = True
                user.set_password(password)
                user.save()
            else:
                user = User.objects.create_user(
                    username=username,
                    email=member_req.email,
                    password=password,
                    first_name=member_req.first_name,
                    last_name=member_req.last_name,
                    is_active=True,
                )

            from .models import SIG, SIGProfile
            profile, _ = SIGProfile.objects.get_or_create(
                user=user,
                defaults={"mobile_number": member_req.mobile},
            )
            if member_req.mobile and profile.mobile_number != member_req.mobile:
                profile.mobile_number = member_req.mobile
                profile.save(update_fields=["mobile_number"])
            if member_req.target_sigs:
                for code in [s.strip() for s in member_req.target_sigs.split(",") if s.strip()]:
                    sig_obj, _ = SIG.objects.get_or_create(code=code, defaults={"name": code})
                    profile.sigs.add(sig_obj)

            member_req.status = "approved"
            member_req.save(update_fields=["status"])
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ig_account
                    SET application_status='approved',
                        status=1,
                        updated_at=%s
                    WHERE email=%s
                      AND LOWER(role)='member'
                    """,
                    [timezone.now(), member_req.email],
                )
            send_mail(
                subject="SIG Member Application Approved",
                message=(
                    f"Dear {member_req.first_name},\n\n"
                    "Your SIG membership application has been approved.\n"
                    f"Username: {user.username}\n"
                    f"Password: {password}\n\n"
                    "Please login at: https://ig-portal.in/siglogin/\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_req.email],
                fail_silently=True,
            )
            messages.success(request, "SIG member request approved successfully.")
        elif action == "reject":
            member_req.status = "rejected"
            member_req.save(update_fields=["status"])
            messages.success(request, "SIG member request rejected.")
        else:
            messages.error(request, "Invalid action.")
        return redirect("admin_sig_member_requests")

    return render(
        request,
        "admin/sig-member-requests.html",
        {"sig_member_requests": qs, "search": search, "status": status},
    )

# ------------------
# ADMIN DASHBOARD
# ------------------

@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics and quick actions"""
    from django.db import connection
    from datetime import datetime, timedelta
    
    # Get statistics from database
    stats = {}
    
    # Total Events
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ig_events")
        stats['total_events'] = cursor.fetchone()[0]
    
    # Total Members
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ig_account WHERE role IN ('member', 'Member')")
        stats['total_members'] = cursor.fetchone()[0]
    
    # Pending Requests
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ig_account WHERE application_status = 'pending'")
        stats['pending_requests'] = cursor.fetchone()[0]
    
    # Total Consultations (using Django model)
    try:
        from .models import Consultation
        stats['total_consultations'] = Consultation.objects.count()
    except Exception:
        stats['total_consultations'] = 0

    # Research + open-source moderation queue (Django ORM)
    try:
        from .models import (
            OpenSourceContribution,
            OpenSourceProject,
            ResearchPaper,
            ResearchSpecificTopic,
        )

        stats["research_pending_topics"] = ResearchSpecificTopic.objects.filter(
            status=ResearchSpecificTopic.Status.PENDING
        ).count()
        stats["research_pending_papers"] = ResearchPaper.objects.filter(
            status=ResearchPaper.Status.PENDING
        ).count()
        stats["oss_pending_projects"] = OpenSourceProject.objects.filter(
            status=OpenSourceProject.Status.PENDING
        ).count()
        stats["oss_pending_contributions"] = OpenSourceContribution.objects.filter(
            status=OpenSourceContribution.Status.PENDING
        ).count()
        stats["research_queue_total"] = (
            stats["research_pending_topics"]
            + stats["research_pending_papers"]
            + stats["oss_pending_projects"]
            + stats["oss_pending_contributions"]
        )
    except Exception:
        stats["research_pending_topics"] = 0
        stats["research_pending_papers"] = 0
        stats["oss_pending_projects"] = 0
        stats["oss_pending_contributions"] = 0
        stats["research_queue_total"] = 0
    
    # Total Meetings
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ig_meetings")
        stats['total_meetings'] = cursor.fetchone()[0]
    
    # Recent Events (last 5)
    recent_events = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, description, event_date, created_at 
            FROM ig_events 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        columns = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            event_dict = dict(zip(columns, row))
            recent_events.append(event_dict)
    
    return render(request, 'admin/admin-dashboard.html', {
        **stats,
        'recent_events': recent_events
    })


def admin_logout(request):
    """
    Securely log out admin, flush session, and redirect to login page
    """
    # Optional: track logout time for audit
    admin_uuid = request.session.get('admin_uuid')

    # Flush session completely
    request.session.flush()

    # Expire session cookie immediately
    response = redirect('sigadmin')  # LOGIN_URL
    response.delete_cookie('sessionid')

    messages.success(request, "You have been logged out successfully.")
    return response

@admin_required
@csrf_protect
def admin_events(request):
    # ---------------- ADD EVENT ----------------
    if request.method == "POST" and 'add_event' in request.POST:
        description = request.POST.get("description", "").strip()
        event_link = request.POST.get("event_link", "").strip()
        event_date = request.POST.get("event_date", "").strip()
        photo = request.FILES.get("photo")

        if not description or not event_date:
            messages.error(request, "Description and Date are required.")
            return redirect('admin_events')

        photo_name = None
        if photo:
            from django.core.files.storage import default_storage
            photo_name = f"events/{int(timezone.now().timestamp())}_{photo.name}"
            default_storage.save(photo_name, photo)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO ig_events (description, event_link, photo, event_date, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [description, event_link, photo_name, event_date, timezone.now(), timezone.now()])

        messages.success(request, "Event added successfully.")
        return redirect('admin_events')

    # ---------------- UPDATE EVENT ----------------
    if request.method == "POST" and 'update_event' in request.POST:
        event_id = request.POST.get("event_id")
        description = request.POST.get("description", "").strip()
        event_link = request.POST.get("event_link", "").strip()
        event_date = request.POST.get("event_date", "").strip()
        photo = request.FILES.get("photo")

        if not description or not event_date:
            messages.error(request, "Description and Date are required.")
            return redirect('admin_events')

        photo_name = None
        if photo:
            from django.core.files.storage import default_storage
            photo_name = f"events/{int(timezone.now().timestamp())}_{photo.name}"
            default_storage.save(photo_name, photo)

        with connection.cursor() as cursor:
            if photo_name:
                cursor.execute("""
                    UPDATE ig_events
                    SET description=%s, event_link=%s, event_date=%s, photo=%s, updated_at=%s
                    WHERE id=%s
                """, [description, event_link, event_date, photo_name, timezone.now(), event_id])
            else:
                cursor.execute("""
                    UPDATE ig_events
                    SET description=%s, event_link=%s, event_date=%s, updated_at=%s
                    WHERE id=%s
                """, [description, event_link, event_date, timezone.now(), event_id])

        messages.success(request, "Event updated successfully.")
        return redirect('admin_events')

    # ---------------- DELETE EVENT ----------------
    if request.method == "POST" and 'delete_event' in request.POST:
        event_id = request.POST.get("event_id")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ig_events WHERE id=%s", [event_id])
        messages.success(request, "Event deleted successfully.")
        return redirect('admin_events')

    # ---------------- PAGINATION SETUP ----------------
    search = request.GET.get("search", "").strip()
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 10))
    offset = (page - 1) * per_page

    base_query = """
        FROM ig_events
        WHERE (%s = '' OR description LIKE %s OR title LIKE %s)
    """

    like = f"%{search}%"
    params = [search, like, like]

    # ---- Total Count ----
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) {base_query}", params)
        total_records = cursor.fetchone()[0]

    total_pages = math.ceil(total_records / per_page)
    page_range = range(1, total_pages + 1)

    # ---- Fetch Paginated Data ----
    sort = request.GET.get("sort", "event_date")
    direction = request.GET.get("direction", "desc")

    allowed_fields = ["title", "description", "event_date", "created_at"]
    if sort not in allowed_fields:
        sort = "event_date"

    if direction not in ["asc", "desc"]:
        direction = "desc"

    order_clause = f"{sort} {direction.upper()}"

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT id, title, description, event_link, photo, event_date, created_at, updated_at
                {base_query}
                ORDER BY {order_clause}
                LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        events = cursor.fetchall()

    # ---------------- RENDER ----------------
    return render(request, 'admin/admin-events.html', {
        "events": events,
        "search": search,
        "current_page": page,
        "page_range": page_range,
        "per_page": per_page,
        "per_page_options": [10, 20, 50, 100],
        "total_records": total_records,
    })

@admin_required
@csrf_protect
def admin_event_add(request):
    """
    Dedicated add page for ig_events (admin UI)
    """
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        event_link = request.POST.get("event_link", "").strip()
        event_date = request.POST.get("event_date", "").strip()
        event_date_to = request.POST.get("event_date_to", "").strip()
        event_type = request.POST.get("event_type", "").strip()
        photo = request.FILES.get("photo")

        if not title or not description or not event_date:
            messages.error(request, "Title, Description and Date are required.")
            return redirect("admin_event_add")

        # enforce DB title length (VARCHAR(100))
        MAX_TITLE_LEN = 100
        if len(title) > MAX_TITLE_LEN:
            messages.warning(
                request,
                f"Title was longer than {MAX_TITLE_LEN} characters and has been truncated."
            )
            title = title[:MAX_TITLE_LEN]

        # ig_events.description is VARCHAR(500) in MySQL � prevent DataError 1406
        MAX_DESC_LEN = 500
        if len(description) > MAX_DESC_LEN:
            messages.warning(
                request,
                f"Description was longer than {MAX_DESC_LEN} characters and has been truncated."
            )
            description = description[:MAX_DESC_LEN]

        photo_name = None
        if photo:
            from django.core.files.storage import default_storage
            photo_name = f"events/{int(timezone.now().timestamp())}_{photo.name}"
            default_storage.save(photo_name, photo)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ig_events (title, description, event_link, photo, event_date, event_dateto ,event_type, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)
                """,
                [title, description, event_link, photo_name, event_date ,event_date_to,event_type, timezone.now(), timezone.now()],
            )

        messages.success(request, "Event added successfully.")
        return redirect("admin_events")

    return render(request, "admin/admin-event-form.html", {"mode": "add", "event": None})

@admin_required
@csrf_protect
def admin_event_edit(request, event_id):
    """
    Dedicated edit page for ig_events (admin UI)
    """
    # Fetch existing event
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, description, event_link, photo, event_date,event_dateto,event_type, created_at, updated_at
            FROM ig_events
            WHERE id = %s
            """,
            [event_id],
        )
        row = cursor.fetchone()

    if not row:
        messages.error(request, "Event not found.")
        return redirect("admin_events")

    cols = ["id", "title", "description", "event_link", "photo", "event_date","event_dateto","event_type" ,"created_at", "updated_at"]
    event = dict(zip(cols, row))

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        event_link = request.POST.get("event_link", "").strip()
        event_date = request.POST.get("event_date", "").strip()
        photo = request.FILES.get("photo")

        if not title or not description or not event_date:
            messages.error(request, "Title, Description and Date are required.")
            return redirect("admin_event_edit", event_id=event_id)

        # Enforce title length
        MAX_TITLE_LEN = 100
        if len(title) > MAX_TITLE_LEN:
            messages.warning(
                request,
                f"Title was longer than {MAX_TITLE_LEN} characters and has been truncated."
            )
            title = title[:MAX_TITLE_LEN]

        # Enforce same DB length constraint on edit for description
        MAX_DESC_LEN = 500
        if len(description) > MAX_DESC_LEN:
            messages.warning(
                request,
                f"Description was longer than {MAX_DESC_LEN} characters and has been truncated."
            )
            description = description[:MAX_DESC_LEN]

        photo_name = None
        if photo:
            from django.core.files.storage import default_storage
            photo_name = f"events/{int(timezone.now().timestamp())}_{photo.name}"
            default_storage.save(photo_name, photo)

        with connection.cursor() as cursor:
            if photo_name:
                cursor.execute(
                    """
                    UPDATE ig_events
                    SET title=%s, description=%s, event_link=%s, event_date=%s, photo=%s, updated_at=%s
                    WHERE id=%s
                    """,
                    [title, description, event_link, event_date, photo_name, timezone.now(), event_id],
                )
            else:
                cursor.execute(
                    """
                    UPDATE ig_events
                    SET title=%s, description=%s, event_link=%s, event_date=%s, updated_at=%s
                    WHERE id=%s
                    """,
                    [title, description, event_link, event_date, timezone.now(), event_id],
                )

        messages.success(request, "Event updated successfully.")
        return redirect("admin_events")

    return render(request, "admin/admin-event-form.html", {"mode": "edit", "event": event})


@admin_required
@csrf_protect
def admin_event_delete(request, event_id):
    """
    Delete a single ig_events row and redirect back to listing
    """
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ig_events WHERE id=%s", [event_id])
        messages.success(request, "Event deleted successfully.")
    else:
        messages.error(request, "Invalid request method for delete.")

    return redirect("admin_events")


@admin_required
@csrf_protect
def admin_meetings(request):
    from .models import Meeting

    if request.method == "POST":
        action = request.POST.get("action", "create")
        if action == "delete":
            meeting_id = request.POST.get("meeting_id")
            meeting = Meeting.objects.filter(id=meeting_id).first()
            if not meeting:
                messages.error(request, "Meeting not found.")
                return redirect("admin_meetings")
            meeting.delete()
            messages.success(request, "Meeting deleted successfully.")
            return redirect("admin_meetings")

        if action == "edit":
            meeting_id = request.POST.get("meeting_id")
            meeting = Meeting.objects.filter(id=meeting_id).first()
            if not meeting:
                messages.error(request, "Meeting not found.")
                return redirect("admin_meetings")

            title = request.POST.get("title")
            date_str = request.POST.get("date")
            sig_type = request.POST.get("sig_type")
            meeting_link = request.POST.get("meeting_link", "").strip()
            agenda = request.FILES.get("agenda")
            minutes = request.FILES.get("minutes")
            supporting_document = request.FILES.get("supporting_document")

            if not (title and date_str and sig_type):
                messages.error(request, "Title, date and SIG type are required for update.")
                return redirect("admin_meetings")

            try:
                meeting_dt = datetime.fromisoformat(date_str)
            except ValueError:
                messages.error(request, "Invalid date format. Please choose a valid date and time.")
                return redirect("admin_meetings")

            meeting.title = title
            meeting.date = meeting_dt
            meeting.sig_type = sig_type
            meeting.meeting_link = meeting_link or None
            if agenda:
                meeting.agenda = agenda
            if minutes:
                meeting.minutes = minutes
            if supporting_document:
                meeting.supporting_document = supporting_document
            meeting.save()
            messages.success(request, "Meeting updated successfully.")
            return redirect("admin_meetings")

        title = request.POST.get("title")
        date_str = request.POST.get("date")
        sig_type = request.POST.get("sig_type")
        meeting_link = request.POST.get("meeting_link", "").strip()
        agenda = request.FILES.get("agenda")
        minutes = request.FILES.get("minutes")
        supporting_document = request.FILES.get("supporting_document")

        if title and date_str and sig_type and agenda and minutes and supporting_document:
            try:
                meeting_dt = datetime.fromisoformat(date_str)
            except ValueError:
                messages.error(request, "Invalid date format. Please choose a valid date and time.")
                return redirect("admin_meetings")

            Meeting.objects.create(
                title=title,
                date=meeting_dt,
                sig_type=sig_type,
                meeting_link=meeting_link or None,
                agenda=agenda,
                minutes=minutes,
                supporting_document=supporting_document,
            )
            messages.success(request, "Meeting created successfully.")
            return redirect("admin_meetings")
        else:
            messages.error(
                request,
                "Please provide title, meeting date, SIG type, agenda, minutes, and supporting document.",
            )

    search = request.GET.get("search", "").strip()
    meetings = Meeting.objects.all().order_by("-date")
    if search:
        meetings = meetings.filter(
            Q(title__icontains=search) | Q(sig_type__icontains=search)
        )

    return render(
        request,
        "admin/admin-meetings.html",
        {"meetings": meetings, "search": search, "total_records": meetings.count()},
    )



@admin_required
@csrf_protect
def admin_member(request):

    # ---------- ADD MEMBER ----------
    if request.method == "POST" and "add_member" in request.POST:

        email = request.POST.get("email", "").strip().lower()
        mobile = request.POST.get("mobile", "").strip()
        company = request.POST.get("company_name", "").strip()
        member_grp = request.POST.get("member_grp", "").strip()
        member_type = request.POST.get("member_type", "").strip()

        if not email or not mobile or not company:
            messages.error(request, "All fields are required.")
            return redirect("admin_member")

        with connection.cursor() as cursor:

            # ---------- CHECK DUPLICATE ----------
            cursor.execute(
                "SELECT id FROM ig_account WHERE email = %s LIMIT 1",
                [email]
            )
            if cursor.fetchone():
                messages.error(request, "Email already registered.")
                return redirect("admin_member")

            # ---------- PASSWORD ----------
            rand = ''.join(random.choices(string.digits, k=4))
            raw_password = f"{email}@{rand}"
            password_hash = make_password(raw_password)

            # ---------- UUID ----------
            user_uuid = str(uuid.uuid4())

            # ---------- INSERT ----------
            cursor.execute("""
                INSERT INTO ig_account
                (uuid, email, mobile, company_name, member_grp, member_type,
                 password_hash, role, status, created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, [
                user_uuid,
                email,
                mobile,
                company,
                member_grp,
                member_type,
                password_hash,
                "member",
                1,
                timezone.now()
            ])

        # ---------- SEND EMAIL ----------
        try:
            send_member_credentials_email(
                email=email,
                company=company,
                raw_password=raw_password
            )
            messages.success(
                request,
                "Member added successfully. Login credentials sent via email."
            )
        except Exception as e:
            messages.warning(
                request,
                f"Member added but email could not be sent. Error: {str(e)}"
            )

        return redirect("admin_member")

    # ---------- DELETE MEMBER ----------
    delete_id = request.GET.get("delete")
    if delete_id:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM ig_account WHERE id = %s AND role = 'member'",
                [delete_id]
            )
        messages.success(request, "Member deleted successfully.")
        return redirect("admin_member")

    # ---------- EDIT MEMBER ----------
    if request.method == "POST" and "edit_member" in request.POST:
        member_id = request.POST.get("member_id")
        email = request.POST.get("email", "").strip().lower()
        mobile = request.POST.get("mobile", "").strip()
        company = request.POST.get("company_name", "").strip()
        member_grp = request.POST.get("member_grp", "").strip()
        member_type = request.POST.get("member_type", "").strip()

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE ig_account
                SET email = %s,
                    mobile = %s,
                    company_name = %s,
                    member_grp = %s,
                    member_type = %s
                WHERE id = %s AND role = 'member'
            """, [email, mobile, company, member_grp, member_type, member_id])
        
        messages.success(request, "Member updated successfully.")
        return redirect("admin_member")

    # ---------- PAGINATION SETUP ----------
    import math
    search = request.GET.get("search", "").strip()
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    
    try:
        per_page = int(request.GET.get("per_page", 10))
    except ValueError:
        per_page = 10
        
    offset = (page - 1) * per_page

    base_query = """
        FROM ig_account
        WHERE role = 'member'
          AND (%s = '' OR email LIKE %s OR mobile LIKE %s OR company_name LIKE %s)
    """
    like = f"%{search}%"
    params = [search, like, like, like]

    # ---- Total Count ----
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) {base_query}", params)
        total_records = cursor.fetchone()[0]

    total_pages = math.ceil(total_records / per_page)
    if total_pages > 0 and page > total_pages:
        page = total_pages
        offset = (page - 1) * per_page
        
    page_range = range(1, total_pages + 1)

    # ---- Fetch Paginated Data ----
    sort = request.GET.get("sort", "id")
    direction = request.GET.get("direction", "desc")

    allowed_fields = ["id", "email", "mobile", "company_name", "member_grp", "member_type", "created_at"]
    if sort not in allowed_fields:
        sort = "id"

    if direction not in ["asc", "desc"]:
        direction = "desc"

    order_clause = f"{sort} {direction.upper()}"

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT id, email, mobile, company_name,
                   member_grp, member_type, created_at
                {base_query}
                ORDER BY {order_clause}
                LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        members = cursor.fetchall()

    return render(request, "admin/admin_member.html", {
        "members": members,
        "search": search,
        "current_page": page,
        "offset": offset,
        "page_range": page_range,
        "per_page": per_page,
        "per_page_options": [10, 20, 50, 100],
        "total_records": total_records,
        "sort": sort,
        "direction": direction,
    })




def send_member_credentials_email(email, company, raw_password):
    subject = "Welcome to IG Portal – Member Login Credentials"

    message = (
        f"Dear {company},\n\n"
        f"Your member account has been created successfully on the IG Portal.\n\n"
        f"Login Details:\n"
        f"Email (Username): {email}\n"
        f"Password: {raw_password}\n\n"
        f"Login URL:\n"
        f"{settings.SITE_URL}/login/\n\n"
        f"For security reasons, please change your password after logging in.\n\n"
        f"Regards,\n"
        f"IG Portal Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
from django.core.paginator import Paginator

@admin_required
# def stakeholder_consultation(request):

#     # ================= ADD CONSULTATION =================
#     if request.method == "POST":
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO stakeholder_consultations
#                 (
#                     title,
#                     description,
#                     open_date,
#                     close_date,
#                     organization,
#                     input_focus,
#                     proposals,
#                     contact_email,
#                     category,
#                     requester,
#                     status
#                 )
#                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#             """, [
#                 request.POST.get("title"),
#                 request.POST.get("description"),
#                 request.POST.get("open_date"),
#                 request.POST.get("close_date"),
#                 request.POST.get("organization"),
#                 request.POST.get("input_focus"),
#                 request.POST.get("proposals"),
#                 request.POST.get("contact_email"),
#                 request.POST.get("category"),
#                 request.POST.get("requester"),
#                 "Open"
#             ])

#         return redirect("stakeholder_consultation")

#     # ================= FETCH CONSULTATIONS =================
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT
#                 id,
#                 title,
#                 description,
#                 open_date,
#                 close_date,
#                 organization,
#                 input_focus,
#                 proposals,
#                 contact_email,
#                 category,
#                 requester,
#                 status,
#                 created_at
#             FROM stakeholder_consultations
#             ORDER BY id DESC
#         """)

#         columns = [col[0] for col in cursor.description]
#         data = [dict(zip(columns, row)) for row in cursor.fetchall()]

#     # ================= DAYS LEFT =================
#     for row in data:
#         if row["close_date"]:
#             row["days_left"] = (row["close_date"] - date.today()).days
#         else:
#             row["days_left"] = 0

#     # ================= PAGINATION =================
#     paginator = Paginator(data, 10)
#     page_number = request.GET.get("page")
#     consultations = paginator.get_page(page_number)

#     return render(request, "admin/stakeholder_consultation.html", {
#         "consultations": consultations
#     })



def stakeholder_consultation(request):
    # ================= DELETE CONSULTATION =================
    if request.method == "POST" and request.POST.get("delete_id"):
        delete_id = request.POST.get("delete_id")
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM stakeholder_consultations WHERE id = %s",
                [delete_id]
            )
        messages.success(request, "Consultation deleted successfully.")
        return redirect("stakeholder_consultation")

    # ================= PAGINATION & SEARCH SETUP =================
    import math
    search = request.GET.get("search", "").strip()
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    
    try:
        per_page = int(request.GET.get("per_page", 10))
    except ValueError:
        per_page = 10
        
    offset = (page - 1) * per_page

    base_query = """
        FROM stakeholder_consultations
        WHERE (%s = '' OR title LIKE %s OR organization LIKE %s OR status LIKE %s OR category LIKE %s)
    """
    like = f"%{search}%"
    params = [search, like, like, like, like]

    # ---- Total Count ----
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) {base_query}", params)
        total_records = cursor.fetchone()[0]

    total_pages = math.ceil(total_records / per_page)
    if total_pages > 0 and page > total_pages:
        page = total_pages
        offset = (page - 1) * per_page
        
    page_range = range(1, total_pages + 1)

    # ================= FETCH PAGINATED DATA =================
    sort = request.GET.get("sort", "created_at")
    direction = request.GET.get("direction", "desc")

    allowed_fields = ["id", "title", "organization", "status", "category", "open_date", "close_date", "created_at"]
    if sort not in allowed_fields:
        sort = "created_at"

    if direction not in ["asc", "desc"]:
        direction = "desc"

    order_clause = f"{sort} {direction.upper()}"

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT
                id, title, description, open_date, close_date,
                organization, input_focus, proposals, contact_email,
                category, requester, status, created_at
                {base_query}
                ORDER BY {order_clause}
                LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # ================= DAYS LEFT =================
    for row in data:
        if row["close_date"]:
            row["days_left"] = (row["close_date"] - date.today()).days
        else:
            row["days_left"] = 0

    return render(request, "admin/stakeholder_consultation.html", {
        "consultations": data,
        "search": search,
        "current_page": page,
        "offset": offset,
        "page_range": page_range,
        "per_page": per_page,
        "per_page_options": [10, 20, 50, 100],
        "total_records": total_records,
        "sort": sort,
        "direction": direction,
    })


def _save_stakeholder_consultation_attachment(cursor, consultation_id, uploaded_file):
    allowed_extensions = {"pdf", "doc", "docx"}
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower() if "." in uploaded_file.name else ""
    if ext not in allowed_extensions:
        raise ValueError("Only PDF, DOC, or DOCX files are allowed.")
    if uploaded_file.size > 10 * 1024 * 1024:
        raise ValueError("Attachment size must be under 10 MB.")

    from django.core.files.storage import default_storage

    original_name = (uploaded_file.name or "attachment").strip()
    safe_original_name = os.path.basename(original_name)
    safe_stem = safe_original_name.rsplit(".", 1)[0][:180] or "attachment"
    unique_name = f"{int(timezone.now().timestamp())}_{uuid.uuid4().hex[:8]}_{safe_stem}.{ext}"
    save_path = f"stakeholder_consultations/{unique_name}"
    saved_path = default_storage.save(save_path, uploaded_file)
    stored_name = safe_original_name[:255]
    stored_path = saved_path[:255]
    cursor.execute(
        """
        INSERT INTO stakeholder_documents (consultation_id, document_name, document_path, document_type, uploaded_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [consultation_id, stored_name, stored_path, ext, timezone.now()],
    )


def _stakeholder_document_url(stored_path):
    if not stored_path:
        return ""
    if str(stored_path).startswith(("http://", "https://", "/")):
        return stored_path
    media_url = settings.MEDIA_URL or "/media/"
    return f"{media_url.rstrip('/')}/{str(stored_path).lstrip('/')}"

def stakeholder_consultation_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        open_date = request.POST.get("open_date") or None
        close_date = request.POST.get("close_date") or None
        organization = request.POST.get("organization")
        input_focus = request.POST.get("input_focus")
        proposals = request.POST.get("proposals")
        contact_email = request.POST.get("contact_email")
        category = request.POST.get("category")
        requester = request.POST.get("requester")
        status = request.POST.get("status", "Open")
        attachment = request.FILES.get("attachment")

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO stakeholder_consultations
                (
                    title, description, open_date, close_date,
                    organization, input_focus, proposals,
                    contact_email, category, requester, status
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, [
                title, description, open_date, close_date,
                organization, input_focus, proposals,
                contact_email, category, requester, status
            ])
                consultation_id = cursor.lastrowid

                if attachment:
                    _save_stakeholder_consultation_attachment(cursor, consultation_id, attachment)
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect("stakeholder_consultation_add")
        except Exception:
            messages.error(request, "Failed to save consultation attachment. Please try a shorter filename.")
            return redirect("stakeholder_consultation_add")
        
        messages.success(request, "Consultation added successfully.")
        return redirect("stakeholder_consultation")

    return render(request, "admin/stakeholder_consultation_form.html", {"action": "Add"})


def stakeholder_consultation_edit(request, id):
    # Fetch existing data
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM stakeholder_consultations WHERE id = %s", [id])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()

    if not row:
        messages.error(request, "Consultation not found.")
        return redirect("stakeholder_consultation")

    consultation = dict(zip(columns, row))

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        open_date = request.POST.get("open_date") or None
        close_date = request.POST.get("close_date") or None
        organization = request.POST.get("organization")
        input_focus = request.POST.get("input_focus")
        proposals = request.POST.get("proposals")
        contact_email = request.POST.get("contact_email")
        category = request.POST.get("category")
        requester = request.POST.get("requester")
        status = request.POST.get("status", "Open")
        attachment = request.FILES.get("attachment")

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                UPDATE stakeholder_consultations
                SET title=%s, description=%s, open_date=%s, close_date=%s,
                    organization=%s, input_focus=%s, proposals=%s,
                    contact_email=%s, category=%s, requester=%s, status=%s
                WHERE id=%s
            """, [
                title, description, open_date, close_date,
                organization, input_focus, proposals,
                contact_email, category, requester, status,
                id
            ])

                if attachment:
                    _save_stakeholder_consultation_attachment(cursor, id, attachment)
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect("stakeholder_consultation_edit", id=id)
        except Exception:
            messages.error(request, "Failed to save consultation attachment. Please try a shorter filename.")
            return redirect("stakeholder_consultation_edit", id=id)

        messages.success(request, "Consultation updated successfully.")
        return redirect("stakeholder_consultation")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT document_name, document_path, uploaded_at
            FROM stakeholder_documents
            WHERE consultation_id = %s
            ORDER BY uploaded_at DESC
            """,
            [id],
        )
        documents = [
            {
                "document_name": r[0],
                "document_path": _stakeholder_document_url(r[1]),
                "uploaded_at": r[2],
            }
            for r in cursor.fetchall()
        ]

    return render(request, "admin/stakeholder_consultation_form.html", {
        "action": "Edit",
        "c": consultation,
        "documents": documents,
    })


def stakeholder_consultation_view(request, id):
    with connection.cursor() as cursor:
        # Fetch consultation
        cursor.execute("SELECT * FROM stakeholder_consultations WHERE id = %s", [id])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()

        if not row:
            messages.error(request, "Consultation not found.")
            return redirect("stakeholder_consultation")

        consultation = dict(zip(columns, row))

        # Fetch comments with user details
        cursor.execute("""
            SELECT 
                cc.*,
                ia.email as user_email,
                ia.company_name as user_company
            FROM consultation_comments cc
            LEFT JOIN ig_account ia ON cc.user_id = ia.id
            WHERE cc.consultation_id = %s
            ORDER BY cc.created_at DESC
        """, [id])
        
        columns_comments = [col[0] for col in cursor.description]
        comments = [dict(zip(columns_comments, row)) for row in cursor.fetchall()]

        cursor.execute(
            """
            SELECT id, document_name, document_path, uploaded_at
            FROM stakeholder_documents
            WHERE consultation_id = %s
            ORDER BY uploaded_at DESC
            """,
            [id],
        )
        doc_cols = [col[0] for col in cursor.description]
        documents = [dict(zip(doc_cols, row)) for row in cursor.fetchall()]
        for doc in documents:
            doc["document_path"] = _stakeholder_document_url(doc.get("document_path"))

    return render(request, "admin/stakeholder_consultation_view.html", {
        "c": consultation,
        "comments": comments,
        "documents": documents,
    })


@admin_required
@csrf_protect
def admin_sig_consultations(request):
    from .models import InternalConsultation

    if request.method == "POST" and request.POST.get("delete_id"):
        consultation = InternalConsultation.objects.filter(id=request.POST.get("delete_id")).first()
        if consultation:
            consultation.delete()
            messages.success(request, "SIG consultation deleted successfully.")
        else:
            messages.error(request, "Consultation not found.")
        return redirect("admin_sig_consultations")

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    sig_type = request.GET.get("sig_type", "").strip()

    consultations = InternalConsultation.objects.all().order_by("-created_at")
    if search:
        consultations = consultations.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    if status in {"open", "closed"}:
        consultations = consultations.filter(status=status)
    if sig_type in {"FI", "TPS", "DNN"}:
        consultations = consultations.filter(sig_type=sig_type)

    return render(
        request,
        "admin/sig_consultation.html",
        {
            "consultations": consultations,
            "search": search,
            "status": status,
            "sig_type": sig_type,
            "total_records": consultations.count(),
        },
    )


@admin_required
@csrf_protect
def admin_sig_consultation_add(request):
    from .models import InternalConsultation

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        sig_type = request.POST.get("sig_type", "").strip()
        deadline = request.POST.get("deadline", "").strip()
        status = request.POST.get("status", "open").strip()
        brief_document = request.FILES.get("brief_document")

        if not (title and description and sig_type and deadline):
            messages.error(request, "Title, description, SIG type and deadline are required.")
            return redirect("admin_sig_consultation_add")

        try:
            deadline_dt = datetime.fromisoformat(deadline)
        except ValueError:
            messages.error(request, "Invalid deadline format.")
            return redirect("admin_sig_consultation_add")

        InternalConsultation.objects.create(
            title=title,
            description=description,
            sig_type=sig_type,
            deadline=deadline_dt,
            status=status if status in {"open", "closed"} else "open",
            brief_document=brief_document,
        )
        messages.success(request, "SIG consultation created successfully.")
        return redirect("admin_sig_consultations")

    return render(request, "admin/sig_consultation_form.html", {"action": "Add"})


@admin_required
@csrf_protect
def admin_sig_consultation_edit(request, consultation_id):
    from .models import InternalConsultation

    consultation = get_object_or_404(InternalConsultation, id=consultation_id)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        sig_type = request.POST.get("sig_type", "").strip()
        deadline = request.POST.get("deadline", "").strip()
        status = request.POST.get("status", "open").strip()
        brief_document = request.FILES.get("brief_document")

        if not (title and description and sig_type and deadline):
            messages.error(request, "Title, description, SIG type and deadline are required.")
            return redirect("admin_sig_consultation_edit", consultation_id=consultation.id)

        try:
            deadline_dt = datetime.fromisoformat(deadline)
        except ValueError:
            messages.error(request, "Invalid deadline format.")
            return redirect("admin_sig_consultation_edit", consultation_id=consultation.id)

        consultation.title = title
        consultation.description = description
        consultation.sig_type = sig_type
        consultation.deadline = deadline_dt
        consultation.status = status if status in {"open", "closed"} else "open"
        if brief_document:
            consultation.brief_document = brief_document
        consultation.save()
        messages.success(request, "SIG consultation updated successfully.")
        return redirect("admin_sig_consultations")

    return render(
        request,
        "admin/sig_consultation_form.html",
        {"action": "Edit", "consultation": consultation},
    )


@admin_required
def admin_sig_consultation_view(request, consultation_id):
    from .models import InternalConsultation, InternalConsultationResponse

    consultation = get_object_or_404(InternalConsultation, id=consultation_id)
    responses = InternalConsultationResponse.objects.filter(
        consultation_id=consultation_id
    ).select_related("member")
    return render(
        request,
        "admin/sig_consultation_view.html",
        {"consultation": consultation, "responses": responses},
    )


@admin_required
@csrf_protect
def admin_sig_events(request):
    from .models import SIGEvent

    if request.method == "POST" and request.POST.get("delete_id"):
        ev = SIGEvent.objects.filter(id=request.POST.get("delete_id")).first()
        if ev:
            ev.delete()
            messages.success(request, "SIG event deleted successfully.")
        else:
            messages.error(request, "Event not found.")
        return redirect("admin_sig_events")

    search = request.GET.get("search", "").strip()
    sig_scope = request.GET.get("sig_scope", "").strip()

    events = SIGEvent.objects.all().order_by("-event_datetime")
    if search:
        events = events.filter(Q(title__icontains=search) | Q(desc__icontains=search))
    if sig_scope in {"All", "FI", "TPS", "DNN", "Joint"}:
        events = events.filter(sig_scope=sig_scope)

    return render(
        request,
        "admin/sig_event.html",
        {
            "sig_events": events,
            "search": search,
            "sig_scope": sig_scope,
            "total_records": events.count(),
        },
    )


def _parse_sig_event_datetime(raw: str):
    """Parse datetime-local string to aware datetime."""
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


@admin_required
@csrf_protect
def admin_sig_event_add(request):
    from .models import SIGEvent

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        desc = request.POST.get("desc", "").strip()
        event_type = request.POST.get("type", "").strip()
        event_datetime_raw = request.POST.get("event_datetime", "").strip()
        join = request.POST.get("join", "").strip() or None
        sig_scope = request.POST.get("sig_scope", "All").strip()

        event_dt = _parse_sig_event_datetime(event_datetime_raw)
        if not (title and event_dt and event_type in {"workshop", "meeting", "conference"}):
            messages.error(request, "Title, valid date/time, and event type are required.")
            return redirect("admin_sig_event_add")
        if sig_scope not in {"All", "FI", "TPS", "DNN", "Joint"}:
            sig_scope = "All"

        SIGEvent.objects.create(
            title=title,
            desc=desc,
            event_datetime=event_dt,
            type=event_type,
            join=join,
            sig_scope=sig_scope,
        )
        messages.success(request, "SIG event created successfully.")
        return redirect("admin_sig_events")

    return render(request, "admin/sig_event_form.html", {"action": "Add"})


@admin_required
@csrf_protect
def admin_sig_event_edit(request, event_id):
    from .models import SIGEvent

    sig_event = get_object_or_404(SIGEvent, id=event_id)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        desc = request.POST.get("desc", "").strip()
        event_type = request.POST.get("type", "").strip()
        event_datetime_raw = request.POST.get("event_datetime", "").strip()
        join = request.POST.get("join", "").strip() or None
        sig_scope = request.POST.get("sig_scope", "All").strip()

        event_dt = _parse_sig_event_datetime(event_datetime_raw)
        if not (title and event_dt and event_type in {"workshop", "meeting", "conference"}):
            messages.error(request, "Title, valid date/time, and event type are required.")
            return redirect("admin_sig_event_edit", event_id=sig_event.id)
        if sig_scope not in {"All", "FI", "TPS", "DNN", "Joint"}:
            sig_scope = "All"

        sig_event.title = title
        sig_event.desc = desc
        sig_event.event_datetime = event_dt
        sig_event.type = event_type
        sig_event.join = join
        sig_event.sig_scope = sig_scope
        sig_event.save()
        messages.success(request, "SIG event updated successfully.")
        return redirect("admin_sig_events")

    return render(
        request,
        "admin/sig_event_form.html",
        {"action": "Edit", "sig_event": sig_event},
    )


def moderate_comment(request, id):
    """Update status of a consultation comment (Approve/Reject)"""
    new_status = request.GET.get("status")
    
    if new_status not in ["Approved", "Rejected"]:
        messages.error(request, "Invalid status update.")
        return redirect(request.META.get("HTTP_REFERER", "stakeholder_consultation"))

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE consultation_comments
            SET status = %s
            WHERE id = %s
        """, [new_status, id])
    
    messages.success(request, f"Comment {new_status.lower()} successfully.")
    return redirect(request.META.get("HTTP_REFERER", "stakeholder_consultation"))
import os
from django.conf import settings

def admin_capacity_building(request):

    # ================= DELETE =================
    if request.method == "POST" and request.POST.get("delete_id"):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM capacity_building_profiles WHERE id=%s",
                [request.POST.get("delete_id")]
            )
        return redirect("admin_capacity_building")

    # ================= ADD / EDIT =================
    if request.method == "POST" and request.POST.get("action") in ["add", "edit"]:

        action = request.POST.get("action")

        # ---------- FILES ----------
        photo = request.FILES.get("photo")
        report = request.FILES.get("reportdoc")

        photo_path = request.POST.get("existing_photo")
        report_path = request.POST.get("existing_report")

        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads", "capacity")
        os.makedirs(upload_dir, exist_ok=True)

        # ---------- PHOTO ----------
        if photo:
            photo_path = f"uploads/capacity/{photo.name}"
            with open(os.path.join(settings.MEDIA_ROOT, photo_path), "wb+") as f:
                for chunk in photo.chunks():
                    f.write(chunk)

        # ---------- REPORT ----------
        if report:
            report_path = f"uploads/capacity/{report.name}"
            with open(os.path.join(settings.MEDIA_ROOT, report_path), "wb+") as f:
                for chunk in report.chunks():
                    f.write(chunk)

        with connection.cursor() as cursor:

            # ---------- ADD ----------
            if action == "add":
                cursor.execute("""
                    INSERT INTO capacity_building_profiles
                    (
                        name, linkedin_url, biography, testimonial,
                        fields_of_work, programme, research_topic,
                        about, cohort, photo, report
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, [
                    request.POST.get("name"),
                    request.POST.get("linkedin_url"),
                    request.POST.get("biography"),
                    request.POST.get("testimonial"),
                    request.POST.get("fields_of_work"),
                    request.POST.get("programme"),
                    request.POST.get("research_topic"),
                    request.POST.get("about"),
                    request.POST.get("cohort"),
                    photo_path,
                    report_path
                ])

            # ---------- EDIT ----------
            else:
                cursor.execute("""
                    UPDATE capacity_building_profiles SET
                        name=%s,
                        linkedin_url=%s,
                        biography=%s,
                        testimonial=%s,
                        fields_of_work=%s,
                        programme=%s,
                        research_topic=%s,
                        about=%s,
                        cohort=%s,
                        photo=%s,
                        report=%s
                    WHERE id=%s
                """, [
                    request.POST.get("name"),
                    request.POST.get("linkedin_url"),
                    request.POST.get("biography"),
                    request.POST.get("testimonial"),
                    request.POST.get("fields_of_work"),
                    request.POST.get("programme"),
                    request.POST.get("research_topic"),
                    request.POST.get("about"),
                    request.POST.get("cohort"),
                    photo_path,
                    report_path,
                    request.POST.get("profile_id")
                ])

        return redirect("admin_capacity_building")

    # ================= PAGINATION & SEARCH SETUP =================
    import math
    search = request.GET.get("search", "").strip()
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1
    
    try:
        per_page = int(request.GET.get("per_page", 10))
    except ValueError:
        per_page = 10
        
    offset = (page - 1) * per_page

    base_query = """
        FROM capacity_building_profiles
        WHERE (%s = '' OR name LIKE %s OR programme LIKE %s OR research_topic LIKE %s)
    """
    like = f"%{search}%"
    params = [search, like, like, like]

    # ---- Total Count ----
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) {base_query}", params)
        total_records = cursor.fetchone()[0]

    total_pages = math.ceil(total_records / per_page)
    if total_pages > 0 and page > total_pages:
        page = total_pages
        offset = (page - 1) * per_page
        
    page_range = range(1, total_pages + 1)

    # ================= FETCH PAGINATED DATA =================
    sort = request.GET.get("sort", "id")
    direction = request.GET.get("direction", "desc")

    allowed_fields = ["id", "name", "cohort", "programme", "research_topic"]
    if sort not in allowed_fields:
        sort = "id"

    if direction not in ["asc", "desc"]:
        direction = "desc"

    order_clause = f"{sort} {direction.upper()}"

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT *
            {base_query}
            ORDER BY {order_clause}
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, "admin/capacity_building_admin.html", {
        "profiles": data,
        "search": search,
        "current_page": page,
        "offset": offset,
        "page_range": page_range,
        "per_page": per_page,
        "per_page_options": [10, 20, 50, 100],
        "total_records": total_records,
        "sort": sort,
        "direction": direction,
        "MEDIA_URL": settings.MEDIA_URL
    })



def event_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, title, description, event_date, event_link, photo
            FROM ig_events
            WHERE id = %s
        """, [id])
        row = cursor.fetchone()

    if not row:
        return render(request, "404.html", status=404)

    columns = ["id","title","description","event_date","event_link","photo"]
    event = dict(zip(columns, row))

    return render(request, "core/event_detail.html", {"event": event,"MEDIA_URL": settings.MEDIA_URL
})









# ----------------------------------------S-I-G--------------------------------------------

def generate_uuid():
    return str(uuid.uuid4())

def generate_otp():
    return secrets.randbelow(900000) + 100000  # 6-digit


def sigregister(request):
    if request.method == "POST":
        email = request.POST.get("email", "").lower().strip()
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if not email or not password or not confirm:
            messages.error(request, "Email and password are required.")
            return redirect("sigregister")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("sigregister")

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect("sigregister")

        # Existing account path: allow password setup only if approved member.
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, role, application_status
                FROM ig_account
                WHERE email = %s
                LIMIT 1
                """,
                [email],
            )
            existing = cursor.fetchone()

        if existing:
            account_id, role, application_status = existing
            if (role or "").lower() != "member":
                messages.error(
                    request,
                    "This email is not mapped to a SIG member account.",
                )
                return redirect("apply_sig_member")

            if (application_status or "").lower() != "approved":
                approved_request = SIGMemberRequest.objects.filter(
                    email__iexact=email, status="approved"
                ).order_by("-submitted_at").first()
                if approved_request:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            UPDATE ig_account
                            SET application_status='approved',
                                status=1,
                                updated_at=%s
                            WHERE id=%s
                            """,
                            [timezone.now(), account_id],
                        )
                else:
                    messages.error(
                        request,
                        "Your SIG profile is not approved yet. Please apply first and wait for super admin approval.",
                    )
                    return redirect("apply_sig_member")

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ig_account
                    SET password_hash=%s, status=1, updated_at=%s
                    WHERE id=%s
                    """,
                    [make_password(password), timezone.now(), account_id],
                )
            messages.success(request, "Password set successfully. You can now login.")
            return redirect("siglogin")

        # New account setup path: only for already-approved profile requests.
        approved_request = SIGMemberRequest.objects.filter(
            email__iexact=email, status="approved"
        ).order_by("-submitted_at").first()
        if not approved_request:
            messages.error(
                request,
                "No approved SIG profile found for this email. Please submit application first.",
            )
            return redirect("apply_sig_member")

        try:
            uuid_val = generate_uuid()
            password_hash = make_password(password)

            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO ig_account
                        (
                            uuid, email, password_hash, role, status, mobile,
                            application_type, application_status, company_name, designation,
                            state, sig_selection, reason, linkedin
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        uuid_val,
                        email,
                        password_hash,
                        "member",
                        1,
                        approved_request.mobile[:10] if approved_request.mobile else None,
                        "member",
                        "approved",
                        approved_request.organization,
                        approved_request.designation,
                        approved_request.state,
                        approved_request.target_sigs,
                        approved_request.bio or f"SIG application by {approved_request.first_name} {approved_request.last_name}",
                        approved_request.linkedin or None,
                    ])

        except Exception as e:
            print("SIG REGISTER ERROR:", e)
            messages.error(request, "Account setup failed. Please try again.")
            return redirect("sigregister")

        messages.success(request, "Account setup completed. You can now login.")
        return redirect("siglogin")

    return render(request, "core/SIG/sigregister.html")


def verify_otp(request):
    email = request.session.get("verify_email")
    if not email:
        messages.error(request, "Session expired. Please register again.")
        return redirect("sigregister")

    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()

        if not entered_otp.isdigit():
            messages.error(request, "Invalid OTP format")
            return redirect("verify_otp")

        now_ts = int(time.time())

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, reset_token_expires
                FROM ig_account
                WHERE email = %s
                  AND otp = %s
                  AND status = 0
            """, [email, entered_otp])

            row = cursor.fetchone()

        if not row:
            messages.error(request, "Invalid OTP")
            return redirect("verify_otp")

        user_id, expiry_ts = row

        # ⏱️ UNIX TIMESTAMP CHECK (NO TIMEZONE ISSUES)
        if expiry_ts is None or now_ts > int(expiry_ts):
            messages.error(request, "OTP expired")
            return redirect("verify_otp")

        # ✅ Activate account
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE ig_account
                SET status = 1,
                    otp = NULL,
                    reset_token_expires = NULL
                WHERE id = %s
            """, [user_id])

        # 🧹 Clean session
        request.session.pop("verify_email", None)
        request.session.pop("dev_otp", None)

        messages.success(request, "Account verified successfully. You may login.")
        return redirect("siglogin")

    return render(request, "core/SIG/isgverifyotp.html")



def sig_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'sigprofile'):
            messages.error(request, "Please login as a SIG member to access this page.")
            return redirect("siglogin")

        return view_func(request, *args, **kwargs)

    return _wrapped_view



# @csrf_protect
# def siglogin(request):
#     if request.method == "POST":
#         login_input = request.POST.get("username", "").strip().lower()
#         password_input = request.POST.get("password", "").strip()

#         if not login_input or not password_input:
#             messages.error(request, "Email/Username and password are required.")
#             return render(request, "core/SIG/siglogin.html")

#         # ---------- FETCH SIG MEMBER ----------
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT id, uuid, password_hash, role,
#                        failed_attempts, locked_until
#                 FROM ig_account
#                 WHERE email = %s
#                   AND role = 'member'
#                   AND status = 1
#                 LIMIT 1
#             """, [login_input])
#             row = cursor.fetchone()

#         if not row:
#             messages.error(request, "Invalid login credentials.")
#             return render(request, "core/SIG/siglogin.html")

#         user_id, uuid, password_hash, role, failed_attempts, locked_until = row

#         # ---------- CHECK ACCOUNT LOCK ----------
#         if locked_until:
#             locked_until = timezone.make_aware(locked_until)
#             if locked_until > timezone.now():
#                 messages.error(
#                     request,
#                     f"Account temporarily locked. Try again after "
#                     f"{locked_until.strftime('%d %b %Y %H:%M')}."
#                 )
#                 return render(request, "core/SIG/siglogin.html")

#         # ---------- CHECK PASSWORD ----------
#         if check_password(password_input, password_hash):
#             # Secure login
#             request.session.flush()
#             request.session["member_uuid"] = uuid
#             request.session["member_role"] = role
#             request.session.set_expiry(60 * 60)  # 1 hour

#             # Reset failed attempts
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     UPDATE ig_account
#                     SET failed_attempts = 0,
#                         locked_until = NULL,
#                         last_login = %s
#                     WHERE id = %s
#                 """, [timezone.now(), user_id])

#             messages.success(request, "Login successful.")
#             return redirect(home)

#         # ---------- PASSWORD INCORRECT ----------
#         failed_attempts += 1
#         lock_time = None

#         if failed_attempts >= MAX_ATTEMPTS:
#             lock_time = timezone.now() + timezone.timedelta(minutes=LOCK_TIME_MINUTES)
#             messages.error(
#                 request,
#                 f"Too many failed attempts. Account locked until "
#                 f"{lock_time.strftime('%d %b %Y %H:%M')}."
#             )
#         else:
#             messages.error(request, "Invalid login credentials.")

#         # Update failed attempts
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 UPDATE ig_account
#                 SET failed_attempts = %s,
#                     locked_until = %s
#                 WHERE id = %s
#             """, [failed_attempts, lock_time, user_id])

#     return render(request, "core/SIG/siglogin.html")
    # return render(request, "core/SIG/sig_dashboard.html")


@csrf_protect
def public_login(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        login_input = request.POST.get("username", "").strip().lower()
        password_input = request.POST.get("password", "").strip()

        if not login_input or not password_input:
            messages.error(request, "Email/Username and password are required.")
            return render(request, "core/login.html", {"next": next_url})

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, uuid, password_hash, role,
                       failed_attempts, locked_until
                FROM ig_account
                WHERE email = %s
                  AND role = 'member'
                  AND status = 1
                LIMIT 1
            """, [login_input])
            row = cursor.fetchone()

        if not row:
            messages.error(request, "Invalid login credentials.")
            return render(request, "core/login.html", {"next": next_url})

        user_id, uuid, password_hash, role, failed_attempts, locked_until = row

        if locked_until:
            locked_until = timezone.make_aware(locked_until)
            if locked_until > timezone.now():
                messages.error(
                    request,
                    f"Account temporarily locked. Try again after "
                    f"{locked_until.strftime('%d %b %Y %H:%M')}."
                )
                return render(request, "core/login.html", {"next": next_url})

        if check_password(password_input, password_hash):
            request.session.flush()
            request.session["member_uuid"] = uuid
            request.session["member_role"] = role
            request.session.set_expiry(60 * 60)

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ig_account
                    SET failed_attempts = 0,
                        locked_until = NULL,
                        last_login = %s
                    WHERE id = %s
                """, [timezone.now(), user_id])

            messages.success(request, "Login successful.")

            if next_url:
                return redirect(next_url)

            return redirect(home)

        failed_attempts += 1
        lock_time = None

        if failed_attempts >= MAX_ATTEMPTS:
            lock_time = timezone.now() + timezone.timedelta(minutes=LOCK_TIME_MINUTES)
            messages.error(
                request,
                f"Too many failed attempts. Account locked until "
                f"{lock_time.strftime('%d %b %Y %H:%M')}."
            )
        else:
            messages.error(request, "Invalid login credentials.")

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE ig_account
                SET failed_attempts = %s,
                    locked_until = %s
                WHERE id = %s
            """, [failed_attempts, lock_time, user_id])

    return render(request, "core/login.html", {"next": next_url})


@csrf_protect
def siglogin(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        login_input = request.POST.get("username", "").strip().lower()
        password_input = request.POST.get("password", "").strip()

        if not login_input or not password_input:
            messages.error(request, "Email/Username and password are required.")
            return render(request, "core/SIG/siglogin.html", {"next": next_url})

        # Try mapping email to username appropriately
        user_by_email = User.objects.filter(email__iexact=login_input).first()
        uname = user_by_email.username if user_by_email else login_input
        
        user = authenticate(request, username=uname, password=password_input)

        if user is not None:
            if hasattr(user, 'sigprofile'):
                auth_login(request, user)
                messages.success(request, "Login successful.")
                return redirect(next_url if next_url else 'sig_dashboard')
            else:
                messages.error(request, "This account is not registered as a SIG Member. Please use the normal login.")
                return render(request, "core/SIG/siglogin.html", {"next": next_url})

        # Fallback: authenticate against ig_account (used by OTP-based SIG registration flow).
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash, role, mobile, application_status
                FROM ig_account
                WHERE email = %s
                  AND LOWER(role) = 'member'
                  AND status = 1
                LIMIT 1
                """,
                [login_input],
            )
            row = cursor.fetchone()

        if not row:
            messages.error(request, "Invalid login credentials.")
            return render(request, "core/SIG/siglogin.html", {"next": next_url})

        _, account_email, password_hash, _, mobile, application_status = row
        if not check_password(password_input, password_hash):
            messages.error(request, "Invalid login credentials.")
            return render(request, "core/SIG/siglogin.html", {"next": next_url})

        if (application_status or "").strip().lower() != "approved":
            messages.error(
                request,
                "Your SIG profile is pending super admin approval. You can login after approval.",
            )
            return render(request, "core/SIG/siglogin.html", {"next": next_url})

        # Ensure Django auth user + SIG profile exist so sig_required works.
        base_username = account_email.split("@")[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exclude(email__iexact=account_email).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user, created = User.objects.get_or_create(
            email=account_email,
            defaults={
                "username": username,
                "first_name": "",
                "last_name": "",
                "is_active": True,
            },
        )

        # Keep Django credential in sync for future auth() flow.
        user.set_password(password_input)
        user.save(update_fields=["password"])

        if not hasattr(user, "sigprofile"):
            SIGProfile.objects.create(
                user=user,
                mobile_number=(mobile or "")[:15],
            )

        auth_login(request, user)
        messages.success(request, "Login successful.")
        return redirect(next_url if next_url else "sig_dashboard")

    return render(request, "core/SIG/siglogin.html", {"next": next_url})





@sig_required
def sig_dashboard(request):
    from .models import InternalConsultation, Meeting, MeetingDocument, SIGEvent
    
    if request.method == "POST":
        if request.POST.get("form_type") == "meeting_upload":
            meeting_id = request.POST.get("meeting_id")
            title = request.POST.get("title")
            file_obj = request.FILES.get("document")
            
            if meeting_id and title and file_obj:
                try:
                    meeting = Meeting.objects.get(id=meeting_id)
                    MeetingDocument.objects.create(
                        meeting=meeting,
                        title=title,
                        document=file_obj,
                        uploader=request.user,
                        status="pending"
                    )
                    messages.success(request, "Document uploaded successfully and is pending admin approval.")
                except Exception:
                    messages.error(request, "Failed to upload document.")
            else:
                messages.error(request, "Missing required fields for upload.")
            return redirect("sig_dashboard")

        meeting_id = request.POST.get("meeting_id")
        if meeting_id:
            return redirect("sig_dashboard")
        
    now = timezone.now()
    context = {
        "meetings_fi": Meeting.objects.filter(sig_type="FI").prefetch_related("documents").order_by("-date"),
        "meetings_tps": Meeting.objects.filter(sig_type="TPS").prefetch_related("documents").order_by("-date"),
        "meetings_dnn": Meeting.objects.filter(sig_type="DNN").prefetch_related("documents").order_by("-date"),
        "meetings_joint": Meeting.objects.filter(sig_type="Joint").prefetch_related("documents").order_by("-date"),
        "consultations": InternalConsultation.objects.filter(status="open").order_by("deadline"),
        "events": SIGEvent.objects.filter(event_datetime__gte=now).order_by("event_datetime"),
    }
    return render(request, "core/SIG/sig_dashboard.html", context)


@sig_required
@csrf_protect
def submit_internal_consultation_response(request, consultation_id):
    from .models import InternalConsultation, InternalConsultationResponse

    if request.method != "POST":
        return redirect("sig_dashboard")

    designation = request.POST.get("designation", "").strip()
    organization = request.POST.get("organization", "").strip()
    response_text = request.POST.get("response", "").strip()
    document = request.FILES.get("document")

    if not designation or not organization or not response_text:
        messages.error(request, "Designation, organization, and response are required.")
        return redirect("sig_dashboard")

    consultation = get_object_or_404(InternalConsultation, id=consultation_id, status="open")
    InternalConsultationResponse.objects.create(
        consultation=consultation,
        member=request.user,
        designation=designation,
        organization=organization,
        response=response_text,
        document=document,
    )
    messages.success(request, "Your consultation response has been submitted successfully.")
    return redirect("sig_dashboard")


def sig_logout(request):
    """
    Secure SIG logout:
    - Clears session
    - Prevents back-button access
    - Redirects to SIG login
    """
    request.session.flush()  # clears all session data

    messages.success(request, "You have been logged out successfully.")

    return redirect("home")














@csrf_protect
def public_register(request):
    return render(request,'core/signup.html')


from django.core.files.storage import FileSystemStorage
@csrf_protect
def submit_comment(request, consultation_id):

    # ---------- LOGIN CHECK ----------
    if not request.session.get("member_uuid"):
        messages.error(request, "Please login to submit comments.")
        return redirect("siglogin")

    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        Designation = request.POST.get("designation", "").strip()
        Organization = request.POST.get("Org", "").strip()
        document = request.FILES.get("document")
        member_uuid = request.session.get("member_uuid")

        # ---------- VALIDATION ----------
        if not comment:
            messages.error(request, "Comment cannot be empty.")
            return redirect(request.META.get("HTTP_REFERER"))


        if not Organization:
            messages.error(request, "Organization cannot be empty.")
            return redirect(request.META.get("HTTP_REFERER"))

        if not Designation:
            messages.error(request, "Designation cannot be empty.")
            return redirect(request.META.get("HTTP_REFERER"))

        document_path = None
        if document:
            allowed_types = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ]

            if document.content_type not in allowed_types:
                messages.error(request, "Only PDF or Word documents are allowed.")
                return redirect(request.META.get("HTTP_REFERER"))

            if document.size > 5 * 1024 * 1024:
                messages.error(request, "Document size must be under 5 MB.")
                return redirect(request.META.get("HTTP_REFERER"))

        with connection.cursor() as cursor:

            # ---------- FETCH USER ----------
            cursor.execute("""
                SELECT id, email
                FROM ig_account
                WHERE uuid = %s
                  AND role = 'Member'
                  AND status = 1
                LIMIT 1
            """, [member_uuid])

            user = cursor.fetchone()

            if not user:
                messages.error(request, "Invalid or inactive member session.")
                return redirect("siglogin")

            user_id, email = user

            # ---------- VALIDATE CONSULTATION STATUS ----------
            cursor.execute("""
                SELECT status, close_date
                FROM stakeholder_consultations
                WHERE id = %s
                LIMIT 1
            """, [consultation_id])
            
            cons_row = cursor.fetchone()
            if not cons_row:
                messages.error(request, "Consultation not found.")
                return redirect("consultations")
            
            cons_status, close_date = cons_row
            today = timezone.now().date()
            
            if cons_status != "Open" or (close_date and close_date < today):
                messages.error(request, "This consultation is closed. Submissions are no longer accepted.")
                return redirect(request.META.get("HTTP_REFERER"))

            # ---------- PREVENT DOUBLE SUBMISSION ----------
            cursor.execute("""
                SELECT 1 FROM consultation_comments
                WHERE consultation_id = %s AND user_id = %s
                LIMIT 1
            """, [consultation_id, user_id])
            
            if cursor.fetchone():
                messages.error(request, "You have already submitted a comment for this consultation.")
                return redirect(request.META.get("HTTP_REFERER"))

            # ---------- SAVE DOCUMENT ----------
            if document:
                fs = FileSystemStorage(
                    location=os.path.join(settings.MEDIA_ROOT, "consultation_docs")
                )

                filename = fs.save(document.name, document)
                document_path = fs.url(filename)

            # ---------- INSERT COMMENT ----------
            # Note: status defaults to 'Pending' via DB alteration
            cursor.execute("""
                INSERT INTO consultation_comments
                (consultation_id, user_id, designation, organization, comment, document_path, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                consultation_id,
                user_id,
                Designation,
                Organization,
                comment,
                document_path,
                'Pending',
                timezone.now()
            ])

        # ---------- THANK YOU EMAIL ----------
        send_mail(
            subject="Thank you for your public comment",
            message=(
                "Dear Participant,\n\n"
                "Thank you for submitting your comment on the consultation.\n\n"
                "Your input has been successfully recorded.\n\n"
                "Regards,\n"
                "IG Portal"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True
        )

        messages.success(
            request,
            "Your comment and document have been submitted successfully."
        )

        return redirect(request.META.get("HTTP_REFERER"))





def get_consultation_details(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM stakeholder_consultations WHERE id = %s", [id])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()

    if row:
        data = dict(zip(columns, row))
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Consultation not found"}, status=404)

def apply_sig_member(request):
    from .forms import SIGMemberForm
    if request.method == "POST":
        form = SIGMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your SIG Member application has been submitted and is pending admin approval.")
            return redirect("home")
    else:
        form = SIGMemberForm()
    return render(request, "core/SIG/apply.html", {"form": form, "title": "Apply for SIG Membership"})

def apply_observer(request):
    from .forms import ObserverForm
    if request.method == "POST":
        form = ObserverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Observer application has been submitted and is pending approval.")
            return redirect("home")
    else:
        form = ObserverForm()
    return render(request, "core/SIG/apply.html", {"form": form, "title": "Apply as an Observer"})

@admin_required
def sig_moderation(request):
    from .models import SIGMemberRequest, ObserverRequest, SIGProfile, SIG
    
    if request.method == "POST":
        req_type = request.POST.get("request_type")
        req_id = request.POST.get("request_id")
        action = request.POST.get("action")
        
        if req_type == "member":
            try:
                member_req = SIGMemberRequest.objects.get(id=req_id)
                if action == "approve":
                    base_username = member_req.email.split("@")[0]
                    username = base_username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{counter}"
                        counter += 1
                        
                    password = generate_password()
                    
                    user = User.objects.create_user(
                        username=username,
                        email=member_req.email,
                        password=password,
                        first_name=member_req.first_name,
                        last_name=member_req.last_name,
                        is_active=True,
                    )
                    
                    profile = SIGProfile.objects.create(
                        user=user,
                        mobile_number=member_req.mobile,
                    )
                    
                    if member_req.target_sigs:
                        sigs_list = [s.strip() for s in member_req.target_sigs.split(",") if s.strip()]
                        for code in sigs_list:
                            sig_obj, _ = SIG.objects.get_or_create(code=code, defaults={'name': code})
                            profile.sigs.add(sig_obj)
                            
                    member_req.status = "approved"
                    member_req.save()
                    
                    send_mail(
                        subject="SIG Member Application Approved",
                        message=f"Dear {member_req.first_name},\n\nYour application has been approved.\nLogin details:\nUsername: {username}\nPassword: {password}\nAccess the portal here: https://ig-portal.in/siglogin/\n",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[member_req.email],
                        fail_silently=True
                    )
                    messages.success(request, f"Approved SIG Member: {member_req.first_name}. Credentials have been emailed.")
                
                elif action == "reject":
                    member_req.status = "rejected"
                    member_req.save()
                    send_mail(
                        subject="SIG Member Application Update",
                        message=f"Dear {member_req.first_name},\n\nThank you for applying. We regret to inform you that your SIG application was not approved.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[member_req.email],
                        fail_silently=True
                    )
                    messages.success(request, "Application rejected.")
            except Exception as e:
                messages.error(request, f"Error processing member: {str(e)}")
                
        elif req_type == "observer":
            try:
                obs_req = ObserverRequest.objects.get(id=req_id)
                if action == "approve":
                    obs_req.status = "approved"
                    obs_req.save()
                    if obs_req.email:
                         send_mail(
                            subject="Observer Application Approved",
                            message=f"Dear {obs_req.first_name},\n\nYour application to become an observer for {obs_req.sig} is approved. You will now receive exclusive updates regarding future events.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[obs_req.email],
                            fail_silently=True
                        )
                    messages.success(request, f"Approved Observer: {obs_req.first_name}")
                elif action == "reject":
                    obs_req.status = "rejected"
                    obs_req.save()
                    if obs_req.email:
                        send_mail(
                            subject="Observer Application Update",
                            message=f"Dear {obs_req.first_name},\n\nWe regret to inform you that your Observer application was not approved.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[obs_req.email],
                            fail_silently=True
                        )
                    messages.success(request, "Observer application rejected.")
            except Exception as e:
                messages.error(request, f"Error processing observer: {str(e)}")
                
        return redirect("sig_moderation")
            
    context = {
        "member_requests": SIGMemberRequest.objects.filter(status="pending").order_by("-submitted_at"),
        "observer_requests": ObserverRequest.objects.filter(status="pending").order_by("-submitted_at")
    }
    return render(request, "core/admin/sig_moderation.html", context)

@admin_required
def admin_moderate_documents(request):
    from .models import MeetingDocument
    meeting_id = request.GET.get("meeting_id")

    if request.method == "POST":
        doc_id = request.POST.get("doc_id")
        action = request.POST.get("action")
        try:
            doc = MeetingDocument.objects.get(id=doc_id)
            if action == "approve":
                doc.status = "approved"
                doc.save()
                messages.success(request, "Document approved and published.")
            elif action == "reject":
                doc.delete()
                messages.success(request, "Document rejected and deleted.")
        except Exception as e:
            messages.error(request, "Error toggling document")
        if meeting_id:
            return redirect(f"{reverse('admin_moderate_documents')}?meeting_id={meeting_id}")
        return redirect("admin_moderate_documents")

    pending_docs = MeetingDocument.objects.filter(status="pending").order_by("-uploaded_at")
    all_docs = MeetingDocument.objects.all().order_by("-uploaded_at")
    if meeting_id:
        pending_docs = pending_docs.filter(meeting_id=meeting_id)
        all_docs = all_docs.filter(meeting_id=meeting_id)

    return render(
        request,
        "core/admin/moderate_documents.html",
        {"pending_docs": pending_docs, "all_docs": all_docs, "meeting_id": meeting_id},
    )
