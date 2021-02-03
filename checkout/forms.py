from django import forms

from .models import Order

from crispy_forms.bootstrap import Field, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Fieldset, Layout


class OrderDetailsForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('user', 'status', 'last_updated', 'order_date', 'ref_code')

    def __init__(self, *args, **kwargs):
        super(OrderDetailsForm, self).__init__(*args, **kwargs)
        # create form structure using crispy forms
        self.helper = FormHelper()
        self.helper.form_id = 'shipping-details-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Billing Details',
                     Div(
                         Field('billing_name',
                               wrapper_class='col-12 col-md-6',
                               readonly='readonly'),

                         Field('billing_address',
                               wrapper_class='col-12 col-md-8',
                               readonly='readonly'),

                         Field('billing_post_code',
                               wrapper_class='col-12 col-md-4',
                               readonly='readonly'),

                         Field('billing_city',
                               wrapper_class='col-12 col-md-6',
                               readonly='readonly'),

                         Field('billing_country',
                               wrapper_class='col-12 col-md-6',
                               readonly='readonly'),

                         css_class='row')
                     ),
            Fieldset('Shipping Details',
                     Div(
                         Field('shipping_name',
                               wrapper_class='col-12 col-md-6'),

                         Field('shipping_address',
                               wrapper_class='col-12 col-md-8'),

                         Field('shipping_post_code',
                               wrapper_class='col-12 col-md-4'),

                         Field('shipping_city',
                               wrapper_class='col-12 col-md-6'),

                         Field('shipping_country',
                               wrapper_class='col-12 col-md-6'),

                         css_class='row')
                     )
        )