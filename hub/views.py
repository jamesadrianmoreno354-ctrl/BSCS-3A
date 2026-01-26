from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Portfolio


def index(request):
    # Basic server-side filtering for SEO-friendly pages
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'All')

    qs = Portfolio.objects.all()
    if category and category != 'All':
        qs = qs.filter(category=category)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(tech__icontains=q))

    # Provide data for template rendering; pages are SEO-friendly
    context = {
        'portfolios': qs,
        'categories': ['All'] + [c[0] for c in Portfolio.CATEGORY_CHOICES],
        'active_category': category,
        'query': q,
    }
    return render(request, 'hub/index.html', context)


def portfolios_json(request):
    items = list(Portfolio.objects.values('id', 'name', 'description', 'category', 'tech', 'url'))
    return JsonResponse(items, safe=False)


def detail(request, pk):
    from django.shortcuts import get_object_or_404

    p = get_object_or_404(Portfolio, pk=pk)
    context = {
        'p': p,
    }
    return render(request, 'hub/portfolio_detail.html', context)
