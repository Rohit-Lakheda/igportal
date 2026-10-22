from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    Consultation,
    DesignationMaster,
    Event,
    GlobalForum,
    GlobalForumHighlight,
    GlobalForumPage,
    GlobalForumPosition,
    GroupMaster,
    ObserverRequest,
    OpenSourceContribution,
    OpenSourceProject,
    ResearchBroadTopic,
    ResearchPaper,
    ResearchSpecificTopic,
    SIGObserver,
    SIGProfile,
    SigMember,
    UserProfile,
)

@admin.register(GroupMaster)
class GroupMasterAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

@admin.register(DesignationMaster)
class DesignationMasterAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(SigMember)
class SigMemberAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "mobile",
        "group",
        "designation",
        "user",
        "created_at",
    )
    search_fields = ("first_name", "last_name", "email", "mobile")
    list_filter = ("group", "designation")
    ordering = ("first_name", "last_name")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "event_datetime",
        "type",
        "created_at",
    )
    list_filter = ("type", "event_datetime")
    search_fields = ("title", "desc")
    ordering = ("-event_datetime",)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "closes_on")
    list_filter = ("status",)
    search_fields = ("title", "desc")


@admin.register(ObserverRequest)
class ObserverRequestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "sig", "submitted_at")
    search_fields = ("first_name", "last_name", "sig", "mobile")

@admin.register(SIGObserver)
class SIGObserverAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "mobile", "sig", "created_at")
    list_filter = ("sig", "created_at")
    search_fields = ("first_name", "last_name", "mobile", "linkedin")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    can_delete = False
    extra = 0

class SIGProfileInline(admin.StackedInline):
    model = SIGProfile
    can_delete = False
    extra = 0
    
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, SIGProfileInline)


# ---------------------------------------------------------------------------
# Research module
# ---------------------------------------------------------------------------


def _now():
    return timezone.now()


@admin.action(description="Approve selected (set reviewed time)")
def approve_research_specific_topics(modeladmin, request, queryset):
    queryset.update(status=ResearchSpecificTopic.Status.APPROVED)


@admin.action(description="Reject selected")
def reject_research_specific_topics(modeladmin, request, queryset):
    queryset.update(status=ResearchSpecificTopic.Status.REJECTED)


@admin.action(description="Approve selected (set reviewed time)")
def approve_research_papers(modeladmin, request, queryset):
    queryset.update(
        status=ResearchPaper.Status.APPROVED,
        reviewed_at=_now(),
    )


@admin.action(description="Reject selected")
def reject_research_papers(modeladmin, request, queryset):
    queryset.update(
        status=ResearchPaper.Status.REJECTED,
        reviewed_at=_now(),
    )


@admin.action(description="Approve selected")
def approve_open_source_projects(modeladmin, request, queryset):
    queryset.update(status=OpenSourceProject.Status.APPROVED)


@admin.action(description="Reject selected")
def reject_open_source_projects(modeladmin, request, queryset):
    queryset.update(status=OpenSourceProject.Status.REJECTED)


@admin.action(description="Approve selected (set reviewed time)")
def approve_open_source_contributions(modeladmin, request, queryset):
    queryset.update(
        status=OpenSourceContribution.Status.APPROVED,
        reviewed_at=_now(),
    )


@admin.action(description="Reject selected")
def reject_open_source_contributions(modeladmin, request, queryset):
    queryset.update(
        status=OpenSourceContribution.Status.REJECTED,
        reviewed_at=_now(),
    )


class ResearchPaperInline(admin.TabularInline):
    model = ResearchPaper
    extra = 1
    show_change_link = True
    readonly_fields = (
        "version",
        "uploaded_at",
        "reviewed_at",
        "submitter_email",
        "submitter_account_id",
    )
    fields = (
        "version",
        "title",
        "status",
        "document",
        "is_nixi_intern",
        "uploaded_at",
        "reviewed_at",
        "submitter_email",
    )


@admin.register(ResearchBroadTopic)
class ResearchBroadTopicAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")


@admin.register(ResearchSpecificTopic)
class ResearchSpecificTopicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "broad_topic",
        "status",
        "proposed_by_email",
        "created_at",
    )
    list_filter = ("status", "broad_topic")
    search_fields = ("name", "slug", "proposed_by_email", "proposed_by_name")
    ordering = ("broad_topic", "name")
    actions = (
        approve_research_specific_topics,
        reject_research_specific_topics,
    )
    inlines = (ResearchPaperInline,)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "specific_topic",
        "version",
        "status",
        "submitter_email",
        "uploaded_at",
        "reviewed_at",
    )
    list_filter = ("status", "specific_topic__broad_topic", "is_nixi_intern")
    search_fields = ("title", "abstract", "submitter_email", "submitter_display_name")
    ordering = ("-uploaded_at",)
    readonly_fields = ("version", "uploaded_at")
    actions = (approve_research_papers, reject_research_papers)
    autocomplete_fields = ("specific_topic",)


class OpenSourceContributionInline(admin.TabularInline):
    model = OpenSourceContribution
    extra = 1
    show_change_link = True
    readonly_fields = (
        "version",
        "uploaded_at",
        "reviewed_at",
        "contributor_email",
        "contributor_account_id",
    )
    fields = (
        "version",
        "title",
        "status",
        "contribution_file",
        "external_url",
        "uploaded_at",
        "reviewed_at",
        "contributor_email",
    )


@admin.register(OpenSourceProject)
class OpenSourceProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "broad_topic",
        "status",
        "proposed_by_email",
        "created_at",
    )
    list_filter = ("status", "broad_topic")
    search_fields = ("name", "slug", "description", "proposed_by_email")
    ordering = ("broad_topic", "name")
    actions = (approve_open_source_projects, reject_open_source_projects)
    inlines = (OpenSourceContributionInline,)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("broad_topic",)


@admin.register(OpenSourceContribution)
class OpenSourceContributionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "version",
        "status",
        "contributor_email",
        "uploaded_at",
        "reviewed_at",
    )
    list_filter = ("status", "project__broad_topic")
    search_fields = ("title", "summary", "contributor_email", "external_url")
    ordering = ("-uploaded_at",)
    readonly_fields = ("version", "uploaded_at")
    actions = (
        approve_open_source_contributions,
        reject_open_source_contributions,
    )
    autocomplete_fields = ("project",)


class GlobalForumPositionInline(admin.TabularInline):
    model = GlobalForumPosition
    extra = 1
    fields = ("statement_date", "title", "summary", "source_label", "is_published")
    ordering = ("-statement_date",)


@admin.register(GlobalForumPage)
class GlobalForumPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Banner", {"fields": ("hero_title", "hero_subtitle")}),
        ("Introduction", {"fields": ("intro_heading", "intro_text")}),
        ("Section headings", {"fields": ("positions_heading", "highlights_heading")}),
    )

    def has_add_permission(self, request):
        return not GlobalForumPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GlobalForum)
class GlobalForumAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name", "tagline", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")
    inlines = (GlobalForumPositionInline,)
    fieldsets = (
        (None, {"fields": ("name", "slug", "tagline", "sort_order", "is_published")}),
        ("Logo", {"fields": ("logo", "logo_url", "logo_style")}),
    )


@admin.register(GlobalForumPosition)
class GlobalForumPositionAdmin(admin.ModelAdmin):
    list_display = ("title", "forum", "statement_date", "is_published")
    list_filter = ("is_published", "forum")
    search_fields = ("title", "summary", "source_label")
    ordering = ("-statement_date",)
    autocomplete_fields = ("forum",)


@admin.register(GlobalForumHighlight)
class GlobalForumHighlightAdmin(admin.ModelAdmin):
    list_display = ("caption", "sort_order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("caption", "alt_text")
    ordering = ("sort_order", "id")
    fields = ("image", "image_url", "alt_text", "caption", "sort_order", "is_published")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
