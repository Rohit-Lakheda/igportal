"""Portal admin pages for India at Global Forums."""
from datetime import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_protect

from .models import (
    GlobalForum,
    GlobalForumHighlight,
    GlobalForumPage,
    GlobalForumPosition,
)
from .views import admin_required


def _page():
    page = GlobalForumPage.objects.order_by("id").first()
    if page is None:
        page = GlobalForumPage.objects.create()
    return page


def _unique_slug(name, slug, exclude_pk=None):
    base = (slug or slugify(name) or "forum")[:80]
    final = base
    i = 1
    qs = GlobalForum.objects.all()
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    while qs.filter(slug=final).exists():
        i += 1
        final = f"{base[:70]}-{i}"
    return final


def _day(raw):
    raw = (raw or "").strip()[:10]
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        return None


@admin_required
@csrf_protect
def admin_global_forums(request):
    page = _page()
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "page":
            page.hero_title = (request.POST.get("hero_title") or "").strip() or page.hero_title
            page.hero_subtitle = (request.POST.get("hero_subtitle") or "").strip()
            page.intro_heading = (request.POST.get("intro_heading") or "").strip()
            page.intro_text = (request.POST.get("intro_text") or "").strip()
            page.positions_heading = (request.POST.get("positions_heading") or "").strip()
            page.highlights_heading = (request.POST.get("highlights_heading") or "").strip()
            page.save()
            messages.success(request, "Page text saved.")
        elif action == "delete_forum":
            GlobalForum.objects.filter(pk=request.POST.get("pk")).delete()
            messages.success(request, "Forum removed.")
        elif action == "delete_highlight":
            GlobalForumHighlight.objects.filter(pk=request.POST.get("pk")).delete()
            messages.success(request, "Highlight removed.")
        return redirect("admin_global_forums")

    return render(
        request,
        "admin/global_forums/index.html",
        {
            "page_copy": page,
            "forums": GlobalForum.objects.all().order_by("sort_order", "name"),
            "highlights": GlobalForumHighlight.objects.all().order_by("sort_order", "id"),
        },
    )


@admin_required
@csrf_protect
def admin_global_forum_form(request, pk=None):
    forum = get_object_or_404(GlobalForum, pk=pk) if pk else None
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if not name:
            messages.error(request, "Name is required.")
            return redirect(request.path)
        slug = _unique_slug(name, request.POST.get("slug"), exclude_pk=pk)
        style = request.POST.get("logo_style") or GlobalForum.LogoStyle.STANDARD
        if style not in GlobalForum.LogoStyle.values:
            style = GlobalForum.LogoStyle.STANDARD
        try:
            sort_order = int(request.POST.get("sort_order") or 0)
        except ValueError:
            sort_order = 0
        if forum is None:
            forum = GlobalForum(name=name, slug=slug)
        forum.name = name
        forum.slug = slug
        forum.tagline = (request.POST.get("tagline") or "").strip()
        forum.logo_url = (request.POST.get("logo_url") or "").strip()
        forum.logo_style = style
        forum.sort_order = sort_order
        forum.is_published = request.POST.get("is_published") == "on"
        logo = request.FILES.get("logo")
        if logo:
            forum.logo = logo
        forum.save()
        messages.success(request, "Forum saved.")
        return redirect("admin_global_forums")

    return render(
        request,
        "admin/global_forums/forum_form.html",
        {"forum": forum, "styles": GlobalForum.LogoStyle.choices},
    )


@admin_required
@csrf_protect
def admin_global_forum_positions(request, pk):
    forum = get_object_or_404(GlobalForum, pk=pk)
    if request.method == "POST" and request.POST.get("action") == "delete":
        forum.positions.filter(pk=request.POST.get("position_id")).delete()
        messages.success(request, "Position removed.")
        return redirect("admin_global_forum_positions", pk=forum.pk)
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        summary = (request.POST.get("summary") or "").strip()
        statement_date = _day(request.POST.get("statement_date"))
        if not (title and summary and statement_date):
            messages.error(request, "Date, title, and summary are required.")
            return redirect("admin_global_forum_positions", pk=forum.pk)
        GlobalForumPosition.objects.create(
            forum=forum,
            statement_date=statement_date,
            title=title,
            summary=summary,
            source_label=(request.POST.get("source_label") or "").strip(),
            is_published=request.POST.get("is_published") == "on",
        )
        messages.success(request, "Position added.")
        return redirect("admin_global_forum_positions", pk=forum.pk)

    return render(
        request,
        "admin/global_forums/positions.html",
        {
            "forum": forum,
            "positions": forum.positions.all().order_by("-statement_date", "title"),
        },
    )


@admin_required
@csrf_protect
def admin_global_forum_position_edit(request, pk):
    position = get_object_or_404(GlobalForumPosition, pk=pk)
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        summary = (request.POST.get("summary") or "").strip()
        statement_date = _day(request.POST.get("statement_date"))
        if not (title and summary and statement_date):
            messages.error(request, "Date, title, and summary are required.")
            return redirect("admin_global_forum_position_edit", pk=position.pk)
        position.statement_date = statement_date
        position.title = title
        position.summary = summary
        position.source_label = (request.POST.get("source_label") or "").strip()
        position.is_published = request.POST.get("is_published") == "on"
        position.save()
        messages.success(request, "Position saved.")
        return redirect("admin_global_forum_positions", pk=position.forum_id)

    return render(
        request,
        "admin/global_forums/position_form.html",
        {"position": position},
    )


@admin_required
@csrf_protect
def admin_global_highlight_form(request, pk=None):
    highlight = get_object_or_404(GlobalForumHighlight, pk=pk) if pk else None
    if request.method == "POST":
        try:
            sort_order = int(request.POST.get("sort_order") or 0)
        except ValueError:
            sort_order = 0
        if highlight is None:
            highlight = GlobalForumHighlight()
        highlight.image_url = (request.POST.get("image_url") or "").strip()
        highlight.alt_text = (request.POST.get("alt_text") or "").strip()
        highlight.caption = (request.POST.get("caption") or "").strip()
        highlight.sort_order = sort_order
        highlight.is_published = request.POST.get("is_published") == "on"
        image = request.FILES.get("image")
        if image:
            highlight.image = image
        if not highlight.image and not highlight.image_url:
            messages.error(request, "Upload a photo or paste an image link.")
            return redirect(request.path)
        highlight.save()
        messages.success(request, "Highlight saved.")
        return redirect("admin_global_forums")

    return render(
        request,
        "admin/global_forums/highlight_form.html",
        {"highlight": highlight},
    )
