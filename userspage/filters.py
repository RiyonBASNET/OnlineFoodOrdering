import django_filters
from django_filters import CharFilter
from admin_app.models import FoodItems


class ItemFilter(django_filters.FilterSet):
    item_name_contains = CharFilter(field_name='item_name',
                                    lookup_expr='icontains')

    class Meta:
        model = FoodItems
        fields = ''
        exclude = [
            'item_price', 'item_description', 'item_image', 'category', 'created_at', 'stock'
        ]
