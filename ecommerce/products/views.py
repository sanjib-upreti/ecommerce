from django.shortcuts import render, redirect
#import models from models
from .models import TestProduct,Category,SubCategory,Review
from django.http  import HttpResponse,JsonResponse
from .forms import ReviewForm
from django.core.paginator import Paginator
from cart.models import Cart

# Create your views here.
def product_page(request):
    #testproducts = TestProduct.objects.all()
    if request.method =="POST" and request.is_ajax():
        price = request.POST.get("price")
        #print(JsonResponse(TestProduct.objects.filter(price__lte = price).values(),safe=False))

        #return JsonResponse(TestProduct.objects.filter(price__lte = price).values(),safe=False)
        testproducts = TestProduct.objects.filter(price__lte=price)
        global data
        data='<div class="row">'


        for testproduct in testproducts:
            data = data + '<div class="col-md-3 col-6 col-sm-6"><div class="card" style="width: 100%;margin:5px 0 5px 0" >'+\
                       '<div class="view overlay zoom">'+\
                        '<img src="'+testproduct.image.url+ '"class="card-img-top" alt="'+testproduct.title+'" title="'+testproduct.title+'" >\
                         </div><div class="card-body">'+\
                        '<h6 class="card-title">'+testproduct.title+' <span class="text-success">'+testproduct.brand.brandname+'</span></h6>'+\
                        '<p class="card-text"> &#8377; '+str(testproduct.price)+'</p>\
                        <a href="../productdetails/'+str(testproduct.id) +'" target="_blank"><button class="btn btn-warning">View Details</button></a>\
                        </div></div></div>'
        data = data +'</div>'
        return HttpResponse(data)

    else:
        testproducts = TestProduct.objects.all()
    category = SubCategory.objects.all()

    context ={ "title":"Product List",
               "products":testproducts,
               'category':category,

               }
    return render(request,'product/product_list.html',context)

def productcategory_page(request,id):
    testproducts = TestProduct.objects.filter(subcategory=id)
    category = SubCategory.objects.all()
    context ={ "title":"Product List",
               "products":testproducts,
               'category':category,


               }
    return render(request,'product/product_list.html',context)



def product_details(request,id):
    if 'username' not in  request.session:
        form = ReviewForm(request.POST or None)
    else:
        form = ReviewForm(request.POST or None,initial={'reviewby': request.session['username'], "productid": id})




    if request.method =="POST":
        if form.is_valid():
            #print(form.cleaned_data)

            reviewby = form.cleaned_data.get("reviewby")
            description = form.cleaned_data.get("description")

            review = Review(reviewby=reviewby,description=description,productid=id)

            try:
                review.save()
            except:
                #pass
                return redirect("/unsuccessful")




    try:
        testproducts = TestProduct.objects.get(id=id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        reviews_list = Review.objects.filter(productid=id)
        paginator = Paginator(reviews_list, 1)  # Show 25 contacts per page

        page = request.GET.get('page')
        reviews = paginator.get_page(page)

        context = {"title": "Product Details",
                       "product": testproducts,
                       "form":form,
                       "reviews":reviews,
                       "cart":cart_obj,


                       }
        return render(request, 'product/products_details.html', context)
    except:
        return HttpResponse("<p> No product found")


def user_previous_orders(request):
    pass

