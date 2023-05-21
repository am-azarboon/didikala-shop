from django.views.generic import CreateView, DeleteView
from django.shortcuts import get_object_or_404
from apps.address.models import Address, City
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .mixins import NewLoginRequiredMixin
from django.urls import reverse_lazy
from .forms import AddressForm


# Render AddAddressView:
class AddAddressView(NewLoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('order:shopping')

    def form_valid(self, form):
        data = form.cleaned_data

        # Add additional arguments
        data['user_id'] = self.request.user.id
        data['active'] = True
        self.object = Address.objects.create(**data)  # Create the new object
        self.object.save()

        return redirect('order:shopping')  # Redirect to the success URL

    def render_to_response(self, context, **response_kwargs):
        return redirect(self.get_success_url())


# Render DeleteAddressView
class DeleteAddressView(DeleteView):
    model = Address
    success_url = reverse_lazy('order:shopping')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Change the active address if this the active address
        if self.object.active is True:
            sec_address = Address.objects.exclude(address=self.object).first()
            sec_address.active = True
            sec_address.save()

        self.object.delete()  # Delete obj

        return redirect(self.get_success_url())


# Render ChangeActiveAddressView
def active_address_view(request, pk):
    if request.method == 'POST':
        return HttpResponseNotFound()

    address = get_object_or_404(Address, id=pk)
    address.active = True  # Active this address
    address.save()

    return redirect('order:shopping')


# Render GetCities
def get_cities(request):
    province_id = request.GET.get('province')  # Get province from ajax request
    cities = City.objects.filter(province_id=province_id).all()  # Get all cities with this province_id

    return render(request, 'address/cities_html_select.html', context={'cities': cities})  # Render select box html form
