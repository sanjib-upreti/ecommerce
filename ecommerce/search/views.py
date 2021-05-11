from django.shortcuts import render
from django.db.models import Q
""" Q used for look ups """

# Create your views here.
from products.models import TestProduct, SubCategory,Brand



def search(request):

    query = request.GET.get('search')
    category = SubCategory.objects.all()
    if query is not None:
        lookups = (Q(description__icontains=query)|
                   Q(brand__brandname__icontains=query) |
                   Q(title__icontains=query) |
                   Q(tag__title__icontains=query)
                   )
        """ Look ups with foreign key association   VERY IMPORTANT CONCEPT """
        products = TestProduct.objects.filter(lookups,active = True).distinct
        context = {'products':products,
                   'category':category,
                   }


    else:
        products = TestProduct.objects.none()
        context = {'products': products,
                   'category': category,
                   }


    return render(request, 'product/product_list.html', context)