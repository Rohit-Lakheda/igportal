"""
Custom IG admin portal — research repository & open-source approvals.
"""
from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
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
from .views import admin_required


def _review_now():
    return timezone.now()


@admin_required
def admin_research_hub(request):
    ctx = {
        "pending_topics": ResearchSpecificTopic.objects.filter(
            status=ResearchSpecificTopic.Status.PENDING
        ).count(),
        "pending_papers": ResearchPaper.objects.filter(
            status=ResearchPaper.Status.PENDING
        ).count(),
        "pending_oss_projects": OpenSourceProject.objects.filter(
            status=OpenSourceProject.Status.PENDING
        ).count(),
        "pending_oss_contributions": OpenSourceContribution.objects.filter(
            status=OpenSourceContribution.Status.PENDING
        ).count(),
        "broad_topics": ResearchBroadTopic.objects.filter(is_active=True).order_by(
            "sort_order", "name"
        ),
    }
    ctx["pending_total"] = (
        ctx["pending_topics"]
        + ctx["pending_papers"]
        + ctx["pending_oss_projects"]
        + ctx["pending_oss_contributions"]
    )
    return render(request, "admin/research/hub.html", ctx)


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_broad_topics(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            name = (request.POST.get("name") or "").strip()
            slug = (request.POST.get("slug") or "").strip()
            description = (request.POST.get("description") or "").strip()
            sort_order = int(request.POST.get("sort_order") or 0)
            if not name:
                messages.error(request, "Name is required.")
            else:
                base_slug = (slug or slugify(name))[:220]
                final_slug = base_slug
                i = 1
                while ResearchBroadTopic.objects.filter(slug=final_slug).exists():
                    i += 1
                    final_slug = f"{base_slug[:210]}-{i}"
                ResearchBroadTopic.objects.create(
                    name=name,
                    slug=final_slug,
                    description=description,
                    sort_order=sort_order,
                    is_active=True,
                )
                messages.success(request, f"Broad topic “{name}” added.")
        elif action == "toggle":
            pk = request.POST.get("pk")
            topic = get_object_or_404(ResearchBroadTopic, pk=pk)
            topic.is_active = not topic.is_active
            topic.save(update_fields=["is_active"])
            messages.success(
                request,
                f"Broad topic “{topic.name}” {'enabled' if topic.is_active else 'disabled'}.",
            )
        return redirect("admin_research_broad_topics")

    topics = ResearchBroadTopic.objects.all().order_by("sort_order", "name")
    return render(request, "admin/research/broad_topics.html", {"topics": topics})


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_broad_topic_edit(request, pk):
    topic = get_object_or_404(ResearchBroadTopic, pk=pk)
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        slug = (request.POST.get("slug") or "").strip()
        description = (request.POST.get("description") or "").strip()
        sort_order = int(request.POST.get("sort_order") or 0)
        is_active = request.POST.get("is_active") == "on"
        if not name:
            messages.error(request, "Name is required.")
            return redirect("admin_research_broad_topic_edit", pk=pk)

        desired_slug = (slug or slugify(name))[:220]
        clash = ResearchBroadTopic.objects.filter(slug=desired_slug).exclude(pk=topic.pk)
        if clash.exists():
            messages.error(request, "Slug already exists. Choose another slug.")
            return redirect("admin_research_broad_topic_edit", pk=pk)

        topic.name = name
        topic.slug = desired_slug
        topic.description = description
        topic.sort_order = sort_order
        topic.is_active = is_active
        topic.save()
        messages.success(request, f"Broad topic “{topic.name}” updated.")
        return redirect("admin_research_broad_topics")
    return render(request, "admin/research/broad_topic_form.html", {"topic": topic})


@admin_required
def admin_research_broad_topic_submissions(request, pk):
    topic = get_object_or_404(ResearchBroadTopic, pk=pk)
    specific_topics = ResearchSpecificTopic.objects.filter(broad_topic=topic).order_by("-created_at")
    papers = ResearchPaper.objects.filter(
        specific_topic__broad_topic=topic
    ).select_related("specific_topic").order_by("-uploaded_at", "-version")
    projects = OpenSourceProject.objects.filter(broad_topic=topic).order_by("-created_at")
    contributions = OpenSourceContribution.objects.filter(
        project__broad_topic=topic
    ).select_related("project").order_by("-uploaded_at", "-version")
    return render(
        request,
        "admin/research/broad_topic_submissions.html",
        {
            "topic": topic,
            "specific_topics": specific_topics,
            "papers": papers,
            "projects": projects,
            "contributions": contributions,
        },
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_topics(request):
    if request.method == "POST":
        pk = request.POST.get("pk")
        action = request.POST.get("action")
        if pk and action in ("approve", "reject"):
            topic = get_object_or_404(ResearchSpecificTopic, pk=pk)
            if action == "approve":
                topic.status = ResearchSpecificTopic.Status.APPROVED
                msg = f"Topic “{topic.name}” approved."
            else:
                topic.status = ResearchSpecificTopic.Status.REJECTED
                msg = f"Topic “{topic.name}” rejected."
            topic.save(update_fields=["status"])
            messages.success(request, msg)
        rs = request.POST.get("return_status") or "pending"
        return redirect(f"{reverse('admin_research_topics')}?status={rs}")

    status = (request.GET.get("status") or "pending").lower()
    qs = ResearchSpecificTopic.objects.select_related("broad_topic").order_by(
        "-created_at"
    )
    if status in (
        ResearchSpecificTopic.Status.PENDING,
        ResearchSpecificTopic.Status.APPROVED,
        ResearchSpecificTopic.Status.REJECTED,
    ):
        qs = qs.filter(status=status)
    else:
        status = "all"

    return render(
        request,
        "admin/research/topics.html",
        {"topics": qs, "filter_status": status},
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_papers(request):
    if request.method == "POST":
        pk = request.POST.get("pk")
        action = request.POST.get("action")
        if pk and action in ("approve", "reject"):
            paper = get_object_or_404(ResearchPaper, pk=pk)
            now = _review_now()
            if action == "approve":
                paper.status = ResearchPaper.Status.APPROVED
                paper.reviewed_at = now
                msg = f"Paper “{paper.title[:60]}” approved."
            else:
                paper.status = ResearchPaper.Status.REJECTED
                paper.reviewed_at = now
                msg = f"Paper “{paper.title[:60]}” rejected."
            paper.save(update_fields=["status", "reviewed_at"])
            messages.success(request, msg)
        rs = request.POST.get("return_status") or "pending"
        return redirect(f"{reverse('admin_research_papers')}?status={rs}")

    status = (request.GET.get("status") or "pending").lower()
    qs = ResearchPaper.objects.select_related(
        "specific_topic", "specific_topic__broad_topic"
    ).order_by("-uploaded_at")
    if status in (
        ResearchPaper.Status.PENDING,
        ResearchPaper.Status.APPROVED,
        ResearchPaper.Status.REJECTED,
    ):
        qs = qs.filter(status=status)
    else:
        status = "all"

    return render(
        request,
        "admin/research/papers.html",
        {"papers": qs, "filter_status": status},
    )


@admin_required
def admin_research_paper_file(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk)
    if not paper.document:
        raise Http404()
    try:
        return FileResponse(
            paper.document.open("rb"),
            as_attachment=False,
            filename=paper.document.name.rsplit("/", 1)[-1],
        )
    except FileNotFoundError:
        raise Http404()


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_oss_projects(request):
    if request.method == "POST":
        pk = request.POST.get("pk")
        action = request.POST.get("action")
        if pk and action in ("approve", "reject"):
            proj = get_object_or_404(OpenSourceProject, pk=pk)
            if action == "approve":
                proj.status = OpenSourceProject.Status.APPROVED
                msg = f"Project “{proj.name}” approved."
            else:
                proj.status = OpenSourceProject.Status.REJECTED
                msg = f"Project “{proj.name}” rejected."
            proj.save(update_fields=["status"])
            messages.success(request, msg)
        rs = request.POST.get("return_status") or "pending"
        return redirect(f"{reverse('admin_research_oss_projects')}?status={rs}")

    status = (request.GET.get("status") or "pending").lower()
    qs = OpenSourceProject.objects.select_related("broad_topic").order_by("-created_at")
    if status in (
        OpenSourceProject.Status.PENDING,
        OpenSourceProject.Status.APPROVED,
        OpenSourceProject.Status.REJECTED,
    ):
        qs = qs.filter(status=status)
    else:
        status = "all"

    return render(
        request,
        "admin/research/oss_projects.html",
        {"projects": qs, "filter_status": status},
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_oss_contributions(request):
    if request.method == "POST":
        pk = request.POST.get("pk")
        action = request.POST.get("action")
        if pk and action in ("approve", "reject"):
            c = get_object_or_404(OpenSourceContribution, pk=pk)
            now = _review_now()
            if action == "approve":
                c.status = OpenSourceContribution.Status.APPROVED
                c.reviewed_at = now
                msg = f"Contribution “{c.title[:50]}” approved."
            else:
                c.status = OpenSourceContribution.Status.REJECTED
                c.reviewed_at = now
                msg = f"Contribution “{c.title[:50]}” rejected."
            c.save(update_fields=["status", "reviewed_at"])
            messages.success(request, msg)
        rs = request.POST.get("return_status") or "pending"
        return redirect(f"{reverse('admin_research_oss_contributions')}?status={rs}")

    status = (request.GET.get("status") or "pending").lower()
    qs = OpenSourceContribution.objects.select_related(
        "project", "project__broad_topic"
    ).order_by("-uploaded_at")
    if status in (
        OpenSourceContribution.Status.PENDING,
        OpenSourceContribution.Status.APPROVED,
        OpenSourceContribution.Status.REJECTED,
    ):
        qs = qs.filter(status=status)
    else:
        status = "all"

    return render(
        request,
        "admin/research/oss_contributions.html",
        {"contributions": qs, "filter_status": status},
    )


@admin_required
def admin_research_oss_contribution_file(request, pk):
    c = get_object_or_404(OpenSourceContribution, pk=pk)
    if not c.contribution_file:
        raise Http404()
    try:
        return FileResponse(
            c.contribution_file.open("rb"),
            as_attachment=False,
            filename=c.contribution_file.name.rsplit("/", 1)[-1],
        )
    except FileNotFoundError:
        raise Http404()


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_specific_topic_edit(request, pk):
    topic = get_object_or_404(ResearchSpecificTopic, pk=pk)
    broad_topics = ResearchBroadTopic.objects.order_by("sort_order", "name")
    if request.method == "POST":
        topic.name = (request.POST.get("name") or "").strip()
        topic.slug = (request.POST.get("slug") or slugify(topic.name))[:255]
        topic.status = request.POST.get("status") or topic.status
        topic.broad_topic_id = request.POST.get("broad_topic") or topic.broad_topic_id
        if not topic.name:
            messages.error(request, "Topic name is required.")
            return redirect("admin_research_specific_topic_edit", pk=pk)
        topic.save()
        messages.success(request, "Specific topic updated.")
        return redirect("admin_research_broad_topic_submissions", pk=topic.broad_topic_id)
    return render(
        request,
        "admin/research/edit_specific_topic.html",
        {"topic": topic, "broad_topics": broad_topics},
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_paper_edit(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk)
    specific_topics = ResearchSpecificTopic.objects.select_related("broad_topic").order_by(
        "broad_topic__sort_order", "broad_topic__name", "name"
    )
    if request.method == "POST":
        paper.title = (request.POST.get("title") or "").strip()
        paper.abstract = (request.POST.get("abstract") or "").strip()
        paper.status = request.POST.get("status") or paper.status
        paper.submitter_display_name = (request.POST.get("submitter_display_name") or "").strip()
        paper.submitter_email = (request.POST.get("submitter_email") or "").strip()
        paper.specific_topic_id = request.POST.get("specific_topic") or paper.specific_topic_id
        if request.FILES.get("document"):
            paper.document = request.FILES["document"]
        if not paper.title:
            messages.error(request, "Paper title is required.")
            return redirect("admin_research_paper_edit", pk=pk)
        paper.save()
        messages.success(request, "Paper version updated.")
        return redirect(
            "admin_research_broad_topic_submissions",
            pk=paper.specific_topic.broad_topic_id,
        )
    return render(
        request,
        "admin/research/edit_paper.html",
        {"paper": paper, "specific_topics": specific_topics},
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_oss_project_edit(request, pk):
    project = get_object_or_404(OpenSourceProject, pk=pk)
    broad_topics = ResearchBroadTopic.objects.order_by("sort_order", "name")
    if request.method == "POST":
        project.name = (request.POST.get("name") or "").strip()
        project.slug = (request.POST.get("slug") or slugify(project.name))[:255]
        project.description = (request.POST.get("description") or "").strip()
        project.status = request.POST.get("status") or project.status
        project.broad_topic_id = request.POST.get("broad_topic") or project.broad_topic_id
        if not project.name:
            messages.error(request, "Project name is required.")
            return redirect("admin_research_oss_project_edit", pk=pk)
        project.save()
        messages.success(request, "OSS project updated.")
        return redirect("admin_research_broad_topic_submissions", pk=project.broad_topic_id)
    return render(
        request,
        "admin/research/edit_oss_project.html",
        {"project": project, "broad_topics": broad_topics},
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
@admin_required
def admin_research_oss_contribution_edit(request, pk):
    contribution = get_object_or_404(OpenSourceContribution, pk=pk)
    projects = OpenSourceProject.objects.select_related("broad_topic").order_by(
        "broad_topic__sort_order", "broad_topic__name", "name"
    )
    if request.method == "POST":
        contribution.title = (request.POST.get("title") or "").strip()
        contribution.summary = (request.POST.get("summary") or "").strip()
        contribution.status = request.POST.get("status") or contribution.status
        contribution.external_url = (request.POST.get("external_url") or "").strip()
        contribution.contributor_display_name = (
            request.POST.get("contributor_display_name") or ""
        ).strip()
        contribution.contributor_email = (request.POST.get("contributor_email") or "").strip()
        contribution.project_id = request.POST.get("project") or contribution.project_id
        if request.FILES.get("contribution_file"):
            contribution.contribution_file = request.FILES["contribution_file"]
        if not contribution.title:
            messages.error(request, "Contribution title is required.")
            return redirect("admin_research_oss_contribution_edit", pk=pk)
        contribution.save()
        messages.success(request, "Contribution version updated.")
        return redirect(
            "admin_research_broad_topic_submissions",
            pk=contribution.project.broad_topic_id,
        )
    return render(
        request,
        "admin/research/edit_oss_contribution.html",
        {"contribution": contribution, "projects": projects},
    )
