import stripe

from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import moncashify
from .forms import OrderDetailsForm
import random

def process_order(request):
    """Convert a user's basket (and basket items) into an order (with order
    items). This requires that payment is succesfully processed and stripe_id
    passed through"""

    if hasattr(request, 'basket'):
        basket = request.basket
    else:
        basket = None

    # user must have items in their basket before proceeding
    if not basket or basket.count() == 0:
        return redirect(reverse('basket'))

    if request.method == 'POST':
        shipping_form = OrderDetailsForm(request.POST)

        if shipping_form.is_valid():
            # check that stripe token exists
            moncash = moncashify.API(settings.MONCASH_CLIENT_ID, settings.MONCASH_SECRET_KEY, debug=False)
            order_id = create_ref_code()
            
            if not request.user.is_authenticated:
                order_data = {
                    'user': None,
                    # billing data is populated from user profile
                    'billing_name': shipping_form.cleaned_data.get('shipping_name'),
                    'billing_address': shipping_form.cleaned_data.get('shipping_address'),
                    'billing_city': shipping_form.cleaned_data.get('shipping_city'),
                    'billing_country': shipping_form.cleaned_data.get('shipping_country'),
                    'billing_post_code': shipping_form.cleaned_data.get('shipping_post_code'),
                    # user can add shipping inshipping_formation if different from billing
                    'shipping_name': shipping_form.cleaned_data.get('shipping_name'),
                    'shipping_address': shipping_form.cleaned_data.get('shipping_address'),
                    'shipping_city': shipping_form.cleaned_data.get('shipping_city'),
                    'shipping_country': shipping_form.cleaned_data.get('shipping_country'),
                    'shipping_post_code': shipping_form.cleaned_data.get('shipping_post_code'),
                    # store payment id
                    'ref_code': order_id
                }
            else:
                order_data = {
                    'user': request.user,
                    # billing data is populated from user profile
                    'billing_name': user.first_name + ' ' + user.last_name,
                    'billing_address': user.address,
                    'billing_city': user.city,
                    'billing_country': user.country,
                    'billing_post_code': user.post_code,
                    # user can add shipping inshipping_formation if different from billing
                    'shipping_name': shipping_form.cleaned_data.get('shipping_name'),
                    'shipping_address': shipping_form.cleaned_data.get('shipping_address'),
                    'shipping_city': shipping_form.cleaned_data.get('shipping_city'),
                    'shipping_country': shipping_form.cleaned_data.get('shipping_country'),
                    'shipping_post_code': shipping_form.cleaned_data.get('shipping_post_code'),
                    # store payment id
                    'ref_code': order_id
                }
            order = Order.objects.create(**order_data)
            total = basket.total()
            prix = int(total)
            payment = moncash.payment(order_id, prix)
            return redirect(payment.redirect_url)
        else:
            return render(request, 'checkout/order_processing.html', {
                'shipping_form': shipping_form,
            })
    else:
        # setup shipping details form
        initial = {}
        if request.user.is_authenticated:
            user = request.user
        # pre-populate details with user information
        # form field prefixes
        prefix = ('billing_',)
        for _prefix in prefix:
            if request.user.is_authenticated:
                initial[_prefix + 'name'] = user.first_name + ' ' + user.last_name
                initial[_prefix + 'address'] = user.address
                initial[_prefix + 'post_code'] = user.post_code
                initial[_prefix + 'city'] = user.city
                initial[_prefix + 'country'] = user.country
            else:
                initial[_prefix + 'name'] = 'Anonyme'
                initial[_prefix + 'address'] = 'Anonyme'
                initial[_prefix + 'post_code'] = 'Anonyme'
                initial[_prefix + 'city'] = 'Anonyme'
                initial[_prefix + 'country'] = 'Anonyme'

        shipping_form = OrderDetailsForm(initial=initial)
        return render(request, 'checkout/order_processing.html', {
            'shipping_form': shipping_form,
        })


def create_ref_code():
    prefix = 'AGOGO-'
    # return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return prefix + ''.join(random.choices(string.digits, k=5))

def moncash_p_done(request):
    if request.method == 'GET':
        request.session['basket_id'] = None
        request.basket = None
        transaction_id_moncash = request.GET['transactionId']
        moncash = moncashify.API(settings.MONCASH_CLIENT_ID, settings.MONCASH_SECRET_KEY, debug=False)
        if request.user:
            order = Order.objects.get(user=request.user, ordered=False)
            transaction = moncash.transaction_details_by_order_id(order.ref_code)
            if transaction:
                mail_admins("produits ventes!!!", "vous venez de vendre quelques articles")
                messages.success(request, "transaction reussi, un mail vous a ete envoyer")
            else:
                messages.error(request, "Erreur de transaction!!")
        else:
            return redirect('home')
    return redirect('home')

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect("request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("request-refund")
