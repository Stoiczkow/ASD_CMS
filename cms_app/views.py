# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.generic.edit import CreateView
from .models import (Order, Machine, Realization, Interruption,
                     ETYKIECIARKA_CAUSES, KARTONIARKA_CAUSES, DBName,
                     ETYKIECIARKA_POSITIONS, KARTONIARKA_POSITIONS, Employee,
                     EmployeeRealization)
from .forms import RealizationForm, InterruptionForm, OrderForm
import datetime
from django.db import transaction
from django.http import JsonResponse


# Create your views here.


def handler404(request):
    return render(request, '404.html', {})


def handler500(request):
    return render(request, '500.html', {})


class MainPageView(View):
    def get(self, request):
        if not request.user.is_anonymous:
            db_name = DBName.objects.get(pk=1).name
            realizations = Realization.objects.using(db_name).filter(
                user=request.user,
                stop_date=None)
            ctx = {'realizations': realizations}

            return render(request, 'index.html', ctx)
        else:
            return render(request, 'index.html', {})


class OrdersToTakeView(View):
    def get(self, request):
        db_name = DBName.objects.get(pk=1).name
        machines = Machine.objects.using(db_name).filter(is_taken=False)
        orders = Order.objects.using(db_name)
        ctx = {'machines': machines, 'orders': orders}

        return render(request, 'orders_tt.html', ctx)

    def post(self, request):
        try:
            with transaction.atomic():
                db_name = DBName.objects.get(pk=1).name
                order = Order.objects.using(db_name).get(
                    pk=int(request.POST['order']))
                machine = order.machine
                machine.is_taken = True
                machine.save(using=db_name)

                if not order.start_date:
                    order.start_date = datetime.datetime.now()
                    order.save(using=db_name)
                new_realization = Realization.objects.using(db_name).create(
                    order=order,
                    user=request.user,
                    start_date=datetime.datetime.now())
                return HttpResponseRedirect(reverse('edit_realization',
                                                    kwargs={
                                                        'pk': new_realization.pk}))

        except ObjectDoesNotExist:
            ctx = {'error': 'Zlecenie zostalo juz zajete.'}
            return render(request, 'orders_tt.html', ctx)


class EditOrderView(View):
    def get(self, request, pk):
        db_name = DBName.objects.get(pk=1).name
        realization = Realization.objects.using(db_name).get(pk=pk)
        machine = realization.order.machine.name
        employees = Employee.objects.using(db_name).filter(is_busy=False)
        avalible_realizations = EmployeeRealization.objects.using(
            db_name).filter(realization=realization)
        if machine == 'Kartoniarka':
            positions = KARTONIARKA_POSITIONS
        elif machine == 'Etykieciarka':
            positions = ETYKIECIARKA_POSITIONS

        ctx = {'realization': realization, 'positions': positions,
               'employees': employees,
               'avalible_realizations': avalible_realizations}
        return render(request, 'order_edit.html', ctx)

    def post(self, request, pk):
        db_name = DBName.objects.get(pk=1).name
        positions = request.POST
        start_date = request.POST['start']
        stop_date = request.POST['stop']
        exclude = ['start', 'stop', 'csrfmiddlewaretoken']
        for key in positions:
            if (key not in exclude) and int(positions[key]) != -1:
                employee = Employee.objects.using(db_name).get(
                    pk=int(positions[key]))
                EmployeeRealization.objects.using(db_name).create(
                    employee=employee,
                    realization=Realization.objects.using(db_name).get(pk=pk),
                    start_date=start_date,
                    stop_date=stop_date,
                    position=key)

        return HttpResponseRedirect(reverse('index'))


class ClosePositions(View):
    def get(self, request, pk):
        db_name = DBName.objects.get(pk=1).name
        realization = Realization.objects.using(db_name).get(pk=pk)
        realization.is_cast = True
        realization.save()
        return HttpResponseRedirect(reverse('list_positions'))


class ListRealizationsPositions(View):
    def get(self, request):
        db_name = DBName.objects.get(pk=1).name
        realizations = Realization.objects.using(db_name).filter(
            user=request.user, is_cast=False)
        ctx = {'realizations': realizations}
        return render(request, 'list_positions.html', ctx)


class CreateOrderView(View):
    def get(self, request):
        ctx = {'machines': Machine.objects.using(
            DBName.objects.get(pk=1).name).all()}
        return render(request, 'order_form.html', ctx)

    def post(self, request):
        form = OrderForm(request.POST)
        db_name = DBName.objects.get(pk=1).name
        Order.objects.using(db_name).create(
            order_id=int(request.POST['order_id']),
            planned=int(request.POST['planned']),
            machine=Machine.objects.using(db_name).get(
                name=request.POST['machine']))
        return HttpResponseRedirect(reverse('index'))


class CloseRealizationView(View):
    def get(self, request, pk):
        form = RealizationForm()
        ctx = {'form': form}
        return render(request, 'close_order.html', ctx)

    def post(self, request, pk):
        db_name = DBName.objects.get(pk=1).name
        realization = Realization.objects.using(db_name).get(pk=pk)
        form = RealizationForm(request.POST)
        if form.is_valid():
            realization.realization = float(request.POST['realization'])
            realization.waste = float(request.POST['waste'])
            realization.stop_date = datetime.datetime.now()
            realization.is_active = False
            realization.order.machine.is_taken = False
            realization.order.machine.save(using=db_name)
            realization.order.save(using=db_name)
            realization.save(using=db_name)

            return HttpResponseRedirect(reverse('index'))


class CloseOrderListView(View):
    def get(self, request):
        orders = Order.objects.using(DBName.objects.get(pk=1).name).filter(
            is_finished=False)
        ctx = {'orders': orders}
        return render(request, 'orders_to_close.html', ctx)


class CloseOrderDetailsView(View):
    def get(self, request, pk):
        order = Order.objects.using(DBName.objects.get(pk=1).name).get(pk=pk)
        ctx = {'order': order}
        return render(request, 'order_to_close.html', ctx)

    def post(self, request, pk):
        order = Order.objects.using(DBName.objects.get(pk=1).name).get(
            pk=int(request.POST['order']))
        order.is_finished = True
        order.save(using=DBName.objects.get(pk=1).name)

        return HttpResponseRedirect(reverse('close_order'))


class CurrentInteruptionsView(View):
    def get(self, request):
        interruptions = Interruption.objects.using(
            DBName.objects.get(pk=1).name).filter(
            realization__user=request.user,
            is_closed=False,
            was_alerted=False)
        ctx = {}
        alert = False
        for interruption in interruptions:
            if interruption.interruption_time >= datetime.timedelta(
                    minutes=10):
                alert = True
                interruption.was_alerted = True
                interruption.save(using=DBName.objects.get(pk=1).name)

        ctx['alert'] = alert

        return JsonResponse(ctx)


class InterruptionsListView(View):
    def get(self, request):
        interruptions = Interruption.objects.using(
            DBName.objects.get(pk=1).name).filter(
            realization__user=request.user,
            is_closed=False)
        ctx = {'interruptions': interruptions}
        return render(request, 'interruptions_list.html', ctx)


class CloseInterruptionView(View):
    def get(self, request, pk):
        interruption = Interruption.objects.using(
            DBName.objects.get(pk=1).name).get(pk=pk)
        if interruption.machine.name == 'Etykieciarka':
            causes = ETYKIECIARKA_CAUSES
        elif interruption.machine.name == 'Kartoniarka':
            causes = KARTONIARKA_CAUSES

        ctx = {'interruption': interruption,
               'causes': causes}

        return render(request, 'interruption_form.html', ctx)

    def post(self, request, pk):
        form = InterruptionForm(request.POST)
        interruption = Interruption.objects.using(
            DBName.objects.get(pk=1).name).get(pk=pk)
        if form.is_valid():
            interruption.cause_1 = request.POST.get('cause_1')
            interruption.cause_2 = request.POST.get('cause_2')
            interruption.cause_3 = request.POST.get('cause_3')
            interruption.is_closed = True
            interruption.save(using=DBName.objects.get(pk=1).name)
        return HttpResponseRedirect(reverse('interruptions'))


class ChangeSaveView(View):
    def get(self, request):
        return render(request, 'change_form.html', {})

    def post(self, request):
        try:
            db_name = DBName.objects.get(pk=1)
            db_name.name = request.POST['change']
            db_name.save()
            db_name_2 = DBName.objects.using('excel').get(pk=1)
            db_name_2.name = request.POST['change']
            db_name_2.save(using='excel')
        except ObjectDoesNotExist:
            DBName.objects.create(name=request.POST['change'])
            DBName.objects.using('excel').create(name=request.POST['change'])
        return HttpResponseRedirect(reverse('index'))
