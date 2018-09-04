from django.shortcuts import render
from django.views import View
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
        orders = Order.objects.all()

        ctx = {'machines': machines,
               'orders': orders}

        return render(request, 'orders_tt.html', ctx)