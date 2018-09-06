from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.generic.edit import CreateView
from .models import Order, Machine
from .forms import OrderForm
import datetime
from django.db import transaction
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.


def handler404(request):
    return render(request, '404.html', {})


def handler500(request):
    return render(request, '500.html', {})


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
        machines = Machine.objects.filter(is_taken=False)

        ctx = {'machines': machines}

        return render(request, 'orders_tt.html', ctx)

    def post(self, request):
        try:
            with transaction.atomic():
                order = Order.objects.get(pk=int(request.POST['order']), is_taken=False)
                machine = order.machine
                machine.is_taken = True
                machine.save()
                order.is_taken = True
                order.user = request.user
                order.start_date = datetime.datetime.now()
                order.save()
                return HttpResponseRedirect(reverse('index'))

        except ObjectDoesNotExist:
            machines = Machine.filter(is_taken=False)
            ctx = {'machines': machines, 'error': 'Zlecenie zostało już zajęte.'}
            return render(request, 'orders_tt.html', ctx)


class CreateOrderView(CreateView):
    model = Order
    fields = ('order_id', 'machine', 'planned')
    template_name = 'order_form.html'
    success_url = '/'


class CloseOrderView(View):
    def get(self, request, pk):
        form = OrderForm()
        ctx = {'form': form}
        return render(request, 'close_order.html', ctx)

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        form = OrderForm(request.POST)
        if form.is_valid():
            order.realization = float(request.POST['realization'])
            order.waste = float(request.POST['waste'])
            order.is_finished = True
            order.machine.is_taken = False
            order.machine.save()
            order.save()

            return HttpResponseRedirect(reverse('index'))
