from django.urls import path
from linktree import views
from linktree.views import DeleteSocial, DeleteURL

urlpatterns = [
    path('<username>/add_url/', views.add_url, name = 'add_url'),
    path('<username>/add_social', views.add_social, name = 'add_social'),
    path('<username>/<pk>/delete_social', DeleteSocial.as_view(template_name="linktree/delete-social.html"), name = 'delete_social'),
    path('<username>/<pk>/delete_url', DeleteURL.as_view(template_name="linktree/delete-url.html"), name = 'delete_url'),
    path('<username>/url_list', views.social_and_url_list, name = 'url_list'),
    ]

