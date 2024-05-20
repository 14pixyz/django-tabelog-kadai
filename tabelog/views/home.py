from django.views import generic

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class WelcomeView(generic.TemplateView):
    template_name = 'welcome.html'

class MemberView(generic.TemplateView):
    template_name = 'member_menu.html'