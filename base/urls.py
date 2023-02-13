from django.urls import path

from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # api
    path('api/posts/', views.all_entries, name="all_entries"),
    path('api/posts/<post_id>', views.entry_detail, name="entry_detail"),
    path('contact_me/', views.contact_me, name="contact_me"),
]

urlpatterns = format_suffix_patterns(urlpatterns)