from django import redirect


# logout required mixin
class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")

        return super(LogoutRequiredMixin, self).dispatch(request, *args, **kwargs)
