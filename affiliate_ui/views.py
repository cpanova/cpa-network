from django.contrib.auth.views import LoginView
from django.shortcuts import render

def dashboard(request):
    return render(request, 'affiliate_ui/dashboard.html')

class AffiliateLoginView(LoginView):
    template_name = 'affiliate_ui/login.html'
    redirect_authenticated_user = True
