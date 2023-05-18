from django.shortcuts import redirect, reverse


# logout required mixin
class NewLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('account:login')+'?next='+request.get_full_path())

        return super(NewLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
