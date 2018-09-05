from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.generic.edit import CreateView
from .models import Order, Machine
# Create your views here.

class MainPageView(View):
    def get(self, request):
        if not request.user.is_anonymous:
            orders = Order.objects.filter(user=request.user,
                                          is_taken=True,
                                          is_finished=False)
            ctx = {'orders': orders}

            return render(request, 'index.html', ctx)
        else:
            return render(request, 'index.html', {})


class OrdersToTakeView(View):
    def get(self, request):
        machines = Machine.objects.all()

        ctx = {'machines': machines,}

        return render(request, 'orders_tt.html', ctx)

    def post(self, request):
        try:
            order = Order.objects.get(pk=int(request.POST['order']), is_taken=False)
            order.is_taken = True
            order.user = request.user
            order.save()
            return HttpResponseRedirect(reverse('index'))
        except ObjectDoesNotExist:
            machines = Machine.objects.all()
            ctx = {'machines': machines, 'error': 'Zlecenie zostało już zajęte.'}
            return render(request, 'orders_tt.html', ctx)



class CreateOrderView(CreateView):
    model = Order
    fields = ('order_id', 'machine', 'planned')
    template_name = 'order_form.html'
    success_url = '/'