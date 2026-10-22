"""
Public and member views for Research Repository + Open Source Projects.
"""
from functools import wraps

from django.contrib import messages
from django.db import connection, transaction
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .models import (
    OpenSourceContribution,
    OpenSourceProject,
    ResearchBroadTopic,
    ResearchPaper,
    ResearchSpecificTopic,
)


ALLOWED_PAPER_EXT = {".pdf", ".doc", ".docx"}
ALLOWED_OSS_EXT = {".pdf", ".doc", ".docx", ".zip", ".txt", ".md"}


def get_member_account(request):
    member_uuid = request.session.get("member_uuid")
    if not member_uuid:
        return None
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, COALESCE(company_name, '')
            FROM ig_account
            WHERE uuid = %s AND LOWER(role) = 'member' AND status = 1
            LIMIT 1
            """,
            [member_uuid],
        )
        row = cursor.fetchone()
    if not row:
        return None
    return {"id": row[0], "email": row[1], "company": row[2] or ""}


def research_login_required(view_func):
    @wraps(view_func)
    def _wrap(request, *args, **kwargs):
        acc = get_member_account(request)
        if not acc:
            messages.error(
                request,
                "Please log in to submit research or open-source materials.",
            )
            return redirect("siglogin")
        return view_func(request, *args, member=acc, **kwargs)

    return _wrap


@csrf_protect
def member_profile(request):
    member_uuid = request.session.get("member_uuid")
    if not member_uuid or (request.session.get("member_role") or "").lower() != "member":
        return redirect("login")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, company_name, mobile, designation, state
            FROM ig_account
            WHERE uuid = %s AND LOWER(role) = 'member' AND status = 1
            LIMIT 1
            """,
            [member_uuid],
        )
        row = cursor.fetchone()
    if not row:
        return redirect("login")

    account = {
        "id": row[0],
        "email": row[1] or "",
        "company_name": row[2] or "",
        "mobile": row[3] or "",
        "designation": row[4] or "",
        "state": row[5] or "",
    }

    if request.method == "POST":
        company_name = (request.POST.get("company_name") or "").strip()
        mobile = (request.POST.get("mobile") or "").strip()
        designation = (request.POST.get("designation") or "").strip()
        state = (request.POST.get("state") or "").strip()
        if mobile and not mobile.isdigit() or (mobile and len(mobile) != 10):
            messages.error(request, "Mobile number must be 10 digits.")
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ig_account
                    SET company_name = %s, mobile = %s, designation = %s, state = %s
                    WHERE id = %s
                    """,
                    (company_name, mobile, designation, state, account["id"]),
                )
            messages.success(request, "Your details were updated.")
            return redirect("member_profile")
        account.update({
            "company_name": company_name,
            "mobile": mobile,
            "designation": designation,
            "state": state,
        })

    from .models import BlogArticle

    papers = ResearchPaper.objects.filter(submitter_email__iexact=account["email"]).order_by("-uploaded_at")
    contributions = OpenSourceContribution.objects.filter(
        contributor_email__iexact=account["email"]
    ).select_related("project").order_by("-uploaded_at")
    blogs = BlogArticle.objects.filter(member_uuid=member_uuid).order_by("-created_at")

    return render(
        request,
        "core/profile.html",
        {
            "account": account,
            "papers": papers,
            "contributions": contributions,
            "blogs": blogs,
        },
    )


def research_hub(request):
    return render(
        request,
        "core/research/hub.html",
        {"page": "research"},
    )


def research_repository_index(request):
    topics = (
        ResearchBroadTopic.objects.filter(is_active=True)
        .prefetch_related("specific_research_topics")
        .order_by("sort_order", "name")
    )
    rows = []
    for bt in topics:
        approved_topics = ResearchSpecificTopic.objects.filter(
            broad_topic=bt,
            status=ResearchSpecificTopic.Status.APPROVED,
        )
        paper_count = ResearchPaper.objects.filter(
            specific_topic__in=approved_topics,
            status=ResearchPaper.Status.APPROVED,
        ).count()
        topic_count = approved_topics.count()
        rows.append(
            {
                "broad": bt,
                "topic_count": topic_count,
                "paper_count": paper_count,
            }
        )
    return render(
        request,
        "core/research/repository_index.html",
        {"page": "research", "rows": rows},
    )


def research_repository_broad(request, broad_slug):
    broad = get_object_or_404(
        ResearchBroadTopic, slug=broad_slug, is_active=True
    )
    topics = ResearchSpecificTopic.objects.filter(
        broad_topic=broad,
        status=ResearchSpecificTopic.Status.APPROVED,
    ).order_by("name")
    topic_list = []
    for t in topics:
        cnt = ResearchPaper.objects.filter(
            specific_topic=t,
            status=ResearchPaper.Status.APPROVED,
        ).count()
        if cnt > 0:
            topic_list.append({"topic": t, "paper_count": cnt})
    return render(
        request,
        "core/research/repository_broad.html",
        {
            "page": "research",
            "broad": broad,
            "topic_list": topic_list,
        },
    )


def research_repository_topic(request, broad_slug, topic_slug):
    broad = get_object_or_404(
        ResearchBroadTopic, slug=broad_slug, is_active=True
    )
    topic = get_object_or_404(
        ResearchSpecificTopic,
        broad_topic=broad,
        slug=topic_slug,
        status=ResearchSpecificTopic.Status.APPROVED,
    )
    papers = ResearchPaper.objects.filter(
        specific_topic=topic,
        status=ResearchPaper.Status.APPROVED,
    ).order_by("-version", "-uploaded_at")
    return render(
        request,
        "core/research/repository_topic.html",
        {
            "page": "research",
            "broad": broad,
            "topic": topic,
            "papers": papers,
        },
    )


def research_paper_download(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk)
    if paper.status != ResearchPaper.Status.APPROVED:
        raise Http404()
    if not paper.document:
        raise Http404()
    try:
        response = FileResponse(
            paper.document.open("rb"),
            as_attachment=True,
            filename=paper.document.name.rsplit("/", 1)[-1],
        )
        return response
    except FileNotFoundError:
        raise Http404()


@csrf_protect
@require_http_methods(["GET", "POST"])
@research_login_required
def research_repository_submit(request, member):
    broad_topics = ResearchBroadTopic.objects.filter(is_active=True).order_by(
        "sort_order", "name"
    )
    if request.method == "POST":
        broad_id = request.POST.get("broad_topic")
        topic_mode = request.POST.get("topic_mode", "existing")
        existing_topic_id = request.POST.get("specific_topic_id")
        new_topic_name = (request.POST.get("new_topic_name") or "").strip()
        title = (request.POST.get("title") or "").strip()
        abstract = (request.POST.get("abstract") or "").strip()
        is_nixi = request.POST.get("is_nixi_intern") == "on"
        batch = (request.POST.get("internship_batch_or_year") or "").strip()
        display_name = (request.POST.get("display_name") or "").strip()
        if not display_name:
            display_name = member["email"].split("@")[0]

        doc = request.FILES.get("document")
        errs = []
        if not broad_id:
            errs.append("Select a broad topic.")
        if not title or not abstract:
            errs.append("Title and abstract are required.")
        if not doc:
            errs.append("Upload a PDF or Word document.")
        else:
            name_lower = doc.name.lower()
            if not any(name_lower.endswith(ext) for ext in ALLOWED_PAPER_EXT):
                errs.append("Document must be PDF, DOC, or DOCX.")
        if is_nixi and not batch:
            errs.append("Internship batch or year is required for NIXI interns.")
        if errs:
            for e in errs:
                messages.error(request, e)
        else:
            try:
                broad = ResearchBroadTopic.objects.get(
                    pk=broad_id, is_active=True
                )
            except ResearchBroadTopic.DoesNotExist:
                messages.error(request, "Invalid broad topic.")
                return redirect("research_repository_submit")

            with transaction.atomic():
                if topic_mode == "existing" and existing_topic_id:
                    try:
                        spec = ResearchSpecificTopic.objects.get(
                            pk=existing_topic_id,
                            broad_topic=broad,
                            status=ResearchSpecificTopic.Status.APPROVED,
                        )
                    except ResearchSpecificTopic.DoesNotExist:
                        messages.error(request, "Select a valid specific topic.")
                        return redirect("research_repository_submit")
                elif topic_mode == "new" and new_topic_name:
                    base = slugify(new_topic_name)[:200] or "topic"
                    slug = base
                    n = 1
                    while ResearchSpecificTopic.objects.filter(
                        broad_topic=broad, slug=slug
                    ).exists():
                        slug = f"{base}-{n}"
                        n += 1
                    spec = ResearchSpecificTopic.objects.create(
                        broad_topic=broad,
                        name=new_topic_name[:255],
                        slug=slug,
                        status=ResearchSpecificTopic.Status.PENDING,
                        proposed_by_email=member["email"],
                        proposed_by_name=display_name[:200],
                    )
                else:
                    messages.error(
                        request,
                        "Choose an existing approved topic or propose a new topic name.",
                    )
                    return redirect("research_repository_submit")

                paper = ResearchPaper(
                    specific_topic=spec,
                    title=title[:500],
                    abstract=abstract,
                    document=doc,
                    is_nixi_intern=is_nixi,
                    internship_batch_or_year=batch[:120],
                    submitter_display_name=display_name[:200],
                    submitter_email=member["email"],
                    submitter_account_id=member["id"],
                    status=ResearchPaper.Status.PENDING,
                )
                paper.save()

            messages.success(
                request,
                "Your paper was submitted for review. It will appear after admin approval.",
            )
            return redirect("research_repository_index")

    existing_by_broad = {}
    for bt in broad_topics:
        existing_by_broad[bt.id] = list(
            ResearchSpecificTopic.objects.filter(
                broad_topic=bt,
                status=ResearchSpecificTopic.Status.APPROVED,
            ).order_by("name")
        )
    existing_topics_map = {
        str(bid): [{"id": t.id, "name": t.name} for t in topics]
        for bid, topics in existing_by_broad.items()
    }
    return render(
        request,
        "core/research/repository_submit.html",
        {
            "page": "research",
            "broad_topics": broad_topics,
            "existing_by_broad": existing_by_broad,
            "existing_topics_map": existing_topics_map,
            "member": member,
        },
    )


def open_source_index(request):
    topics = ResearchBroadTopic.objects.filter(is_active=True).order_by(
        "sort_order", "name"
    )
    rows = []
    for bt in topics:
        projects = OpenSourceProject.objects.filter(
            broad_topic=bt,
            status=OpenSourceProject.Status.APPROVED,
        )
        proj_rows = []
        for p in projects:
            approved_n = OpenSourceContribution.objects.filter(
                project=p,
                status=OpenSourceContribution.Status.APPROVED,
            ).count()
            if approved_n:
                latest = (
                    OpenSourceContribution.objects.filter(
                        project=p,
                        status=OpenSourceContribution.Status.APPROVED,
                    )
                    .order_by("-version")
                    .first()
                )
                proj_rows.append(
                    {
                        "project": p,
                        "contribution_count": approved_n,
                        "latest_version": latest.version if latest else 0,
                    }
                )
        if proj_rows:
            rows.append({"broad": bt, "projects": proj_rows})
    return render(
        request,
        "core/research/oss_index.html",
        {"page": "research", "rows": rows},
    )


def open_source_broad(request, broad_slug):
    broad = get_object_or_404(
        ResearchBroadTopic, slug=broad_slug, is_active=True
    )
    projects = []
    for p in OpenSourceProject.objects.filter(
        broad_topic=broad,
        status=OpenSourceProject.Status.APPROVED,
    ).order_by("name"):
        n = OpenSourceContribution.objects.filter(
            project=p,
            status=OpenSourceContribution.Status.APPROVED,
        ).count()
        if n:
            projects.append({"project": p, "approved_count": n})
    return render(
        request,
        "core/research/oss_broad.html",
        {"page": "research", "broad": broad, "projects": projects},
    )


def open_source_project(request, broad_slug, project_slug):
    broad = get_object_or_404(
        ResearchBroadTopic, slug=broad_slug, is_active=True
    )
    project = get_object_or_404(
        OpenSourceProject,
        broad_topic=broad,
        slug=project_slug,
        status=OpenSourceProject.Status.APPROVED,
    )
    approved = OpenSourceContribution.objects.filter(
        project=project,
        status=OpenSourceContribution.Status.APPROVED,
    ).order_by("-version", "-uploaded_at")
    return render(
        request,
        "core/research/oss_project.html",
        {
            "page": "research",
            "broad": broad,
            "project": project,
            "approved_contributions": approved,
        },
    )


def open_source_contribution_download(request, pk):
    c = get_object_or_404(OpenSourceContribution, pk=pk)
    if c.status != OpenSourceContribution.Status.APPROVED or not c.contribution_file:
        raise Http404()
    try:
        return FileResponse(
            c.contribution_file.open("rb"),
            as_attachment=True,
            filename=c.contribution_file.name.rsplit("/", 1)[-1],
        )
    except FileNotFoundError:
        raise Http404()


@csrf_protect
@require_http_methods(["GET", "POST"])
@research_login_required
def open_source_submit(request, member):
    broad_topics = ResearchBroadTopic.objects.filter(is_active=True).order_by(
        "sort_order", "name"
    )
    mode = (
        request.POST.get("mode", "contribute")
        if request.method == "POST"
        else "contribute"
    )

    approved_projects = list(
        OpenSourceProject.objects.filter(
            status=OpenSourceProject.Status.APPROVED
        ).select_related("broad_topic").order_by("broad_topic__name", "name")
    )

    if request.method == "POST":
        display_name = (request.POST.get("display_name") or "").strip()
        if not display_name:
            display_name = member["email"].split("@")[0]

        if request.POST.get("mode") == "new_project":
            broad_id = request.POST.get("broad_topic")
            pname = (request.POST.get("project_name") or "").strip()
            pdesc = (request.POST.get("project_description") or "").strip()
            title = (request.POST.get("contribution_title") or "").strip()
            summary = (request.POST.get("summary") or "").strip()
            ext_url = (request.POST.get("external_url") or "").strip()
            f = request.FILES.get("contribution_file")
            errs = []
            if not broad_id or not pname or not pdesc:
                errs.append(
                    "Broad topic, project name, and description are required."
                )
            if not title:
                errs.append("Contribution title is required.")
            if not f and not ext_url:
                errs.append("Provide a file or an external URL.")
            if f:
                low = f.name.lower()
                if not any(low.endswith(x) for x in ALLOWED_OSS_EXT):
                    errs.append("File type not allowed for this upload.")
            for e in errs:
                messages.error(request, e)
            if not errs:
                try:
                    broad = ResearchBroadTopic.objects.get(
                        pk=broad_id, is_active=True
                    )
                except ResearchBroadTopic.DoesNotExist:
                    messages.error(request, "Invalid broad topic.")
                    return redirect("open_source_submit")
                base = slugify(pname)[:200] or "project"
                slug = base
                n = 1
                while OpenSourceProject.objects.filter(
                    broad_topic=broad, slug=slug
                ).exists():
                    slug = f"{base}-{n}"
                    n += 1
                with transaction.atomic():
                    proj = OpenSourceProject.objects.create(
                        broad_topic=broad,
                        name=pname[:255],
                        slug=slug,
                        description=pdesc,
                        status=OpenSourceProject.Status.PENDING,
                        proposed_by_email=member["email"],
                        proposed_by_name=display_name[:200],
                    )
                    contrib = OpenSourceContribution(
                        project=proj,
                        title=title[:300],
                        summary=summary,
                        contribution_file=f,
                        external_url=ext_url[:500] if ext_url else "",
                        contributor_display_name=display_name[:200],
                        contributor_email=member["email"],
                        contributor_account_id=member["id"],
                        status=OpenSourceContribution.Status.PENDING,
                    )
                    contrib.save()
                messages.success(
                    request,
                    "Project and first contribution submitted for admin approval.",
                )
                return redirect("open_source_index")
        else:
            project_id = request.POST.get("project_id")
            title = (request.POST.get("contribution_title") or "").strip()
            summary = (request.POST.get("summary") or "").strip()
            ext_url = (request.POST.get("external_url") or "").strip()
            f = request.FILES.get("contribution_file")
            errs = []
            if not project_id:
                errs.append("Select a project.")
            if not title:
                errs.append("Contribution title is required.")
            if not f and not ext_url:
                errs.append("Provide a file or an external URL.")
            if f:
                low = f.name.lower()
                if not any(low.endswith(x) for x in ALLOWED_OSS_EXT):
                    errs.append("File type not allowed for this upload.")
            for e in errs:
                messages.error(request, e)
            if not errs:
                try:
                    proj = OpenSourceProject.objects.get(
                        pk=project_id,
                        status=OpenSourceProject.Status.APPROVED,
                    )
                except OpenSourceProject.DoesNotExist:
                    messages.error(request, "Invalid project.")
                    return redirect("open_source_submit")
                contrib = OpenSourceContribution(
                    project=proj,
                    title=title[:300],
                    summary=summary,
                    contribution_file=f,
                    external_url=ext_url[:500] if ext_url else "",
                    contributor_display_name=display_name[:200],
                    contributor_email=member["email"],
                    contributor_account_id=member["id"],
                    status=OpenSourceContribution.Status.PENDING,
                )
                contrib.save()
                messages.success(
                    request,
                    "Contribution submitted for admin approval.",
                )
                return redirect(
                    "open_source_project",
                    broad_slug=proj.broad_topic.slug,
                    project_slug=proj.slug,
                )

    return render(
        request,
        "core/research/oss_submit.html",
        {
            "page": "research",
            "broad_topics": broad_topics,
            "approved_projects": approved_projects,
            "member": member,
            "mode": mode,
        },
    )
