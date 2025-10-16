from django.shortcuts import render, redirect
from phones.models import Phone

def index(request):
    return redirect('catalog')



def show_catalog(request):
    sor = request.GET.get('sort')
    if sor == 'name':
        phone_objects = Phone.objects.order_by('name')
        template = 'catalog.html'
        context = {'phones': phone_objects}
        return render(request, template, context)
    elif sor == 'min_price':
        phone_objects = Phone.objects.order_by('price')
        template = 'catalog.html'
        context = {'phones': phone_objects}
        return render(request, template, context)
    elif sor == 'max_price':
        phone_objects = Phone.objects.order_by('-price')
        template = 'catalog.html'
        context = {'phones': phone_objects}
        return render(request, template, context)
    else:
        phone_objects = Phone.objects.all()
        template = 'catalog.html'
        context = {'phones': phone_objects}
        return render(request, template, context)



def show_product(request, slug):
    phone_slug = slug
    phone = Phone.objects.get(slug=phone_slug)
    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)
