# views.py (Template View)
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from .api_views import ProductViewSet  # reusing the ViewSet logic

def product_list_template(request):
    # Create a DRF-style request (so filters/search work)
    factory = APIRequestFactory()
    drf_request = factory.get('/api/products/', request.GET)
    drf_request.user = request.user  # carry over user

    # Instantiate the viewset
    viewset = ProductViewSet(request=drf_request)
    queryset = viewset.filter_queryset(viewset.get_queryset())

    # Paginate using DRF’s paginator
    paginator = PageNumberPagination()
    paginator.page_size = 9
    page = paginator.paginate_queryset(queryset, drf_request)

    # We’ll use the paginated `page` for the template
    return render(request, 'product_list.html', {
        'products': page,
        'paginator': paginator,
        'page_obj': paginator.page,  # for Bootstrap pagination controls
        'query': request.GET.get('search', ''),
    })
