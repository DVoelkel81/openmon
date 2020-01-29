from django.views.generic import TemplateView


class LeftSidebarView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(LeftSidebarView, self).get_context_data(**kwargs)
        context['mode_detached'] = self.request.GET.get('mode_detached', False)
        return context


class TopbarView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(TopbarView, self).get_context_data(**kwargs)
        context['mode_dark'] = self.request.GET.get('mode_dark', False)
        return context


class HorizontalNavView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HorizontalNavView, self).get_context_data(**kwargs)
        return context


left_sidebar_view = LeftSidebarView.as_view(template_name="partials/left-sidebar.html")
topbar_view = TopbarView.as_view(template_name="partials/topbar.html")
horizontal_nav_view = HorizontalNavView.as_view(template_name="partials/horizontal-nav.html")
