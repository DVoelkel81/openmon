from django.urls import path

from .views import (left_sidebar_view, topbar_view, horizontal_nav_view, )

app_name = "layout"
urlpatterns = [
    path("left-sidebar.html", view=left_sidebar_view, name="left-side-bar"),
    path("topbar.html", view=topbar_view, name="topbar"),
    path("horizontal-nav.html", view=horizontal_nav_view, name="horizontal"),
]
