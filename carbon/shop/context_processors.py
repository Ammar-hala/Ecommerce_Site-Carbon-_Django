from .models import Category

#to enable links for category
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links) # links will contain all categories can be used in any html file inside shop
