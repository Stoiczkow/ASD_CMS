from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.generic.edit import CreateView
from .models import Order, Machine, Realization, Interruption, ETYKIECIARKA_CAUSES, KARTONIARKA_CAUSES
from .forms import RealizationForm, InterruptionForm
import datetime
from django.db import transaction
# Create your views here.


def handler404(request):
    return render(request, '404.html', {})


def handler500(request):
    return render(request, '500.html', {})


class MainPageView(View):
    def get(self, request):
        if not request.user.is_anonymous:
            realizations = Realization.objects.filter(user=request.user, stop_date=None)
            ctx = {'realizations': realizations}

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
                order = Order.objects.get(pk=int(request.POST['order']))
                machine = order.machine
                machine.is_taken = True
                machine.save()
                if not order.start_date:
                    order.start_date = datetime.datetime.now()
                    order.save()
                Realization.objects.create(order=order, user=request.user, start_date=datetime.datetime.now())
                return HttpResponseRedirect(reverse('index'))

        except ObjectDoesNotExist:
            ctx = {'error': 'Zlecenie zostało już zajęte.'}
            return render(request, 'orders_tt.html', ctx)


class CreateOrderView(CreateView):
    model = Order
    fields = ('order_id', 'machine', 'planned')
    template_name = 'order_form.html'
    success_url = '/'


class CloseRealizationView(View):
    def get(self, request, pk):
        form = RealizationForm()
        ctx = {'form': form}
        return render(request, 'close_order.html', ctx)

    def post(self, request, pk):
        realization = Realization.objects.get(pk=pk)
        form = RealizationForm(request.POST)
        if form.is_valid():
            realization.realization = float(request.POST['realization'])
            realization.waste = float(request.POST['waste'])
            realization.stop_date = datetime.datetime.now()
            realization.is_active = False
            realization.order.machine.is_taken = False
            realization.order.machine.save()
            realization.order.save()
            realization.save()

            return HttpResponseRedirect(reverse('index'))


class CloseOrderListView(View):
    def get(self, request):
        orders = Order.objects.filter(is_finished=False)
        ctx = {'orders': orders}
        return render(request, 'orders_to_close.html', ctx)


class CloseOrderDetailsView(View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        ctx = {'order': order}
        return render(request, 'order_to_close.html', ctx)

    def post(self, request, pk):
        order = Order.objects.get(pk=int(request.POST['order']))
        order.is_finished = True
        order.save()

        return HttpResponseRedirect(reverse('close_order'))


class CurrentInteruptionsView(View):
    def get(self, request):
        pass


class InterruptionsListView(View):
    def get(self, request):
        interruptions = Interruption.objects.filter(realization__user=request.user,
                                                    is_closed=False)
        ctx = {'interruptions': interruptions}
        return render(request, 'interruptions_list.html', ctx)


class CloseInterruptionView(View):
    def get(self, request, pk):
        interruption = Interruption.objects.get(pk=pk)
        if interruption.machine.name == 'Etykieciarka':
            causes = ETYKIECIARKA_CAUSES
        elif interruption.machine.name == 'Kartoniarka':
            causes = KARTONIARKA_CAUSES

        ctx = {'interruption': interruption,
               'causes': causes}

        return render(request, 'interruption_form.html', ctx)

    def post(self, request, pk):
        form = InterruptionForm(request.POST)
        if form.is_valid():
            print(request.POST['cause_1'])
        ctx = {}
        return render(request, 'interruption_form.html', ctx)