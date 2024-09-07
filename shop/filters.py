from django_filters.filterset import FilterSet
from .models import Product


class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = ['price',  'name']