from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Prefetch
from django.shortcuts import render
from django.contrib.auth.views import LoginView

from offer.models import Offer, Category, Payout, ACTIVE_STATUS
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


@login_required
def offer_list(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', None)

    offers = Offer.objects.prefetch_related(
        Prefetch('payouts', queryset=Payout.objects.order_by('-payout'))
    ).filter(status=ACTIVE_STATUS)

    if search_query:
        offers = offers.filter(title__icontains=search_query)

    if category_id:
        offers = offers.filter(categories__id=category_id)

    categories = Category.objects.all()

    context = {
        'offers': offers,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'affiliate_ui/offers.html', context)


class AffiliateLoginView(LoginView):
    template_name = 'affiliate_ui/login.html'
    redirect_authenticated_user = True
