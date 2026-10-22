
from django.urls import path
from . import admin_global_forum_views
from . import admin_research_views
from . import research_views
from . import views

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("", views.home, name="home"),
    path("base/", views.base, name="base"),
    path("capacity/", views.capacity, name="capacity"),
    path("global-forums/", views.global_forums, name="global"),

    path("events/", views.events, name="events"),
    # path("events1/", views.events1, name="events1"),
    path("consultations/", views.consultations, name="consultations"),
    path("blogs/", views.blogs, name="blogs"),
    path('blogs/article/<int:id>/',views.blog_detail,name='blog_detail'),
    path('blog_page/',views.blog_page,name='blog_page'),
    path('blog_page/submit_blog',views.submit_blog,name='submit_blog'),
    path("save-read-time/",views.save_read_time,name="save_read_time"),

    path("research/", research_views.research_hub, name="research_hub"),
    path(
        "research/repository/",
        research_views.research_repository_index,
        name="research_repository_index",
    ),
    path(
        "research/repository/submit/",
        research_views.research_repository_submit,
        name="research_repository_submit",
    ),
    path(
        "research/repository/<slug:broad_slug>/",
        research_views.research_repository_broad,
        name="research_repository_broad",
    ),
    path(
        "research/repository/<slug:broad_slug>/<slug:topic_slug>/",
        research_views.research_repository_topic,
        name="research_repository_topic",
    ),
    path(
        "research/papers/<int:pk>/download/",
        research_views.research_paper_download,
        name="research_paper_download",
    ),
    path(
        "research/open-source/",
        research_views.open_source_index,
        name="open_source_index",
    ),
    path(
        "research/open-source/submit/",
        research_views.open_source_submit,
        name="open_source_submit",
    ),
    path(
        "research/open-source/<slug:broad_slug>/",
        research_views.open_source_broad,
        name="open_source_broad",
    ),
    path(
        "research/open-source/<slug:broad_slug>/<slug:project_slug>/",
        research_views.open_source_project,
        name="open_source_project",
    ),
    path(
        "research/open-source/contributions/<int:pk>/download/",
        research_views.open_source_contribution_download,
        name="open_source_contribution_download",
    ),

    path("sig/", views.sig, name="sig"),

    path("admin-login/", views.login_view, name="admin_login"),
    path("login/", views.public_login, name="login"),
    path("profile/", research_views.member_profile, name="member_profile"),
    path("logout/", views.logout_view, name="logout"),

    path("apply/sig-member/", views.apply_sig_member, name="apply_sig_member"),
    path("apply/observer/", views.apply_observer, name="apply_observer"),
    path("dashboard/documents/moderation/", views.admin_moderate_documents, name="admin_moderate_documents"),
    path("dashboard/events/add/", views.add_event, name="add_event"),
    path("dashboard/create-sig-user/", views.create_sig_user, name="create_sig_user"),
    path("dashboard/sig-moderation/", views.sig_moderation, name="sig_moderation"),
    path(
        "dashboard/sig-members/add/",
        views.admin_create_sig_member,
        name="admin_create_sig_member",
    ),
    path("add_meeting", views.add_meeting, name="add_meeting"),
    path("member", views.member, name="member"),
    path("consultation", views.consultation, name="consultation"),

    # __________________________________________________________________

    # abhishek work
    
    path("chortdtl/<int:id>/", views.chortdtl, name="chortdtl"),
    path("fellows/cohort/<int:cohort>/", views.cohort_fellows, name="cohort_fellows"),

    path("about/", views.about, name="about"),
    
    path("proceedings/<int:id>/", views.Proceedingsdtl, name="Proceedingsdtl"),
    path('Adminn/',views.sigadmin,name='sigadmin'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin_events/',views.admin_events,name='admin_events'),
    path('admin_events/add/', views.admin_event_add, name='admin_event_add'),
    path('admin_events/<int:event_id>/edit/', views.admin_event_edit, name='admin_event_edit'),
    path('admin_events/<int:event_id>/delete/', views.admin_event_delete, name='admin_event_delete'),
    path('meetings/',views.admin_meetings,name='admin_meetings'),
    path('members/',views.admin_member,name='admin_member'),
    path("stakeholder-consultations/",views.stakeholder_consultation,name="stakeholder_consultation"),
    path("stakeholder-consultations/add/", views.stakeholder_consultation_add, name="stakeholder_consultation_add"),
    path("stakeholder-consultations/edit/<int:id>/", views.stakeholder_consultation_edit, name="stakeholder_consultation_edit"),
    path("stakeholder-consultations/view/<int:id>/", views.stakeholder_consultation_view, name="stakeholder_consultation_view"),
    path("sig-consultations/", views.admin_sig_consultations, name="admin_sig_consultations"),
    path("sig-consultations/add/", views.admin_sig_consultation_add, name="admin_sig_consultation_add"),
    path("sig-consultations/<int:consultation_id>/edit/", views.admin_sig_consultation_edit, name="admin_sig_consultation_edit"),
    path("sig-consultations/<int:consultation_id>/view/", views.admin_sig_consultation_view, name="admin_sig_consultation_view"),
    path("sig-events/", views.admin_sig_events, name="admin_sig_events"),
    path("sig-events/add/", views.admin_sig_event_add, name="admin_sig_event_add"),
    path("sig-events/<int:event_id>/edit/", views.admin_sig_event_edit, name="admin_sig_event_edit"),
    path("admin_capacity_building/",views.admin_capacity_building,name="admin_capacity_building"),

    path(
        "admin-research/",
        admin_research_views.admin_research_hub,
        name="admin_research_hub",
    ),
    path(
        "admin-research/topics/",
        admin_research_views.admin_research_topics,
        name="admin_research_topics",
    ),
    path(
        "admin-research/broad-topics/",
        admin_research_views.admin_research_broad_topics,
        name="admin_research_broad_topics",
    ),
    path(
        "admin-research/broad-topics/<int:pk>/edit/",
        admin_research_views.admin_research_broad_topic_edit,
        name="admin_research_broad_topic_edit",
    ),
    path(
        "admin-research/broad-topics/<int:pk>/submissions/",
        admin_research_views.admin_research_broad_topic_submissions,
        name="admin_research_broad_topic_submissions",
    ),
    path(
        "admin-research/papers/",
        admin_research_views.admin_research_papers,
        name="admin_research_papers",
    ),
    path(
        "admin-research/papers/<int:pk>/file/",
        admin_research_views.admin_research_paper_file,
        name="admin_research_paper_file",
    ),
    path(
        "admin-research/open-source/projects/",
        admin_research_views.admin_research_oss_projects,
        name="admin_research_oss_projects",
    ),
    path(
        "admin-research/open-source/contributions/",
        admin_research_views.admin_research_oss_contributions,
        name="admin_research_oss_contributions",
    ),
    path(
        "admin-research/open-source/contributions/<int:pk>/file/",
        admin_research_views.admin_research_oss_contribution_file,
        name="admin_research_oss_contribution_file",
    ),
    path(
        "admin-research/topics/<int:pk>/edit/",
        admin_research_views.admin_research_specific_topic_edit,
        name="admin_research_specific_topic_edit",
    ),
    path(
        "admin-research/papers/<int:pk>/edit/",
        admin_research_views.admin_research_paper_edit,
        name="admin_research_paper_edit",
    ),
    path(
        "admin-research/open-source/projects/<int:pk>/edit/",
        admin_research_views.admin_research_oss_project_edit,
        name="admin_research_oss_project_edit",
    ),
    path(
        "admin-research/open-source/contributions/<int:pk>/edit/",
        admin_research_views.admin_research_oss_contribution_edit,
        name="admin_research_oss_contribution_edit",
    ),

    
    path('admin-blogs',views.admin_blogs,name='admin_blogs'),
    path("admin-global-forums/", admin_global_forum_views.admin_global_forums, name="admin_global_forums"),
    path("admin-global-forums/forums/add/", admin_global_forum_views.admin_global_forum_form, name="admin_global_forum_add"),
    path("admin-global-forums/forums/<int:pk>/edit/", admin_global_forum_views.admin_global_forum_form, name="admin_global_forum_edit"),
    path("admin-global-forums/forums/<int:pk>/positions/", admin_global_forum_views.admin_global_forum_positions, name="admin_global_forum_positions"),
    path("admin-global-forums/positions/<int:pk>/edit/", admin_global_forum_views.admin_global_forum_position_edit, name="admin_global_forum_position_edit"),
    path("admin-global-forums/highlights/add/", admin_global_forum_views.admin_global_highlight_form, name="admin_global_highlight_add"),
    path("admin-global-forums/highlights/<int:pk>/edit/", admin_global_forum_views.admin_global_highlight_form, name="admin_global_highlight_edit"),

    path("events/<int:id>/", views.event_detail, name="event_detail"),
    path('siglogin/',views.siglogin,name='siglogin'),
    path('sigregister/',views.sigregister,name='sigregister'),
    path('sig_logout/',views.sig_logout,name='sig_logout'),
    path('sig_dashboard/',views.sig_dashboard,name='sig_dashboard'),
    path(
        "sig-dashboard/consultations/<int:consultation_id>/respond/",
        views.submit_internal_consultation_response,
        name="submit_internal_consultation_response",
    ),





    path("register/", views.public_register, name="public_register"),
    path("submit-comment/<int:consultation_id>/", views.submit_comment, name="submit_comment"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("admin-profile/", views.admin_profile, name="admin_profile"),
    path("admin-request/", views.admin_membership_requests, name="admin_membership_requests"),
    path("admin-request/sig-members/", views.admin_sig_member_requests, name="admin_sig_member_requests"),

    

    path("moderate-comment/<int:id>/", views.moderate_comment, name="moderate_comment"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)