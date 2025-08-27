from django.views.generic import TemplateView

class TestView(TemplateView):
    template_name = 'biblioteca/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Test'
        return context
