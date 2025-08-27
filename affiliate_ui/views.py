from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render
from django.contrib.auth.views import LoginView

from tracker.models import Click, Conversion, APPROVED_STATUS


@login_required
def dashboard(request):
    clicks_count = Click.objects.filter(affiliate=request.user).count()

    conversions = Conversion.objects.filter(affiliate=request.user)
    conversions_count = conversions.count()

    total_earnings = conversions.filter(
        status=APPROVED_STATUS).aggregate(total=Sum('payout'))['total'] or 0

    context = {
        'clicks_count': clicks_count,
        'conversions_count': conversions_count,
        'total_earnings': f'{total_earnings:.2f}',
    }
    return render(request, 'affiliate_ui/dashboard.html', context)


class AffiliateLoginView(LoginView):
    template_name = 'affiliate_ui/login.html'
    redirect_authenticated_user = True
