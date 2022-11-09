from warehouse.models import Category, Product


def index(request):
    categories = Category.objects.filter(active=True, parent_id=None)
    return {'categories': categories}