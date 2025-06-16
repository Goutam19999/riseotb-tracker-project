from django.urls import path

from scmtracker import views

urlpatterns = [
    path("",views.HomePageView.as_view(),name='home'),
    path("stream-list",views.StreamListView.as_view(),name='stream-list'),
    path("moderation-form/<int:stream_id>/",views.ModerationFormView.as_view(),name="moderation-form"),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('tracker-table/',views.tracker_table,name='tracker-table'),
    path('search-post/',views.PostSearchView.as_view(), name='search-post'),
]