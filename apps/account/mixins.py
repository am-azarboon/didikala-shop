from django.shortcuts import redirect, reverse


# logout required mixin
class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")

        return super(LogoutRequiredMixin, self).dispatch(request, *args, **kwargs)


# Only redirect from valid views will pass (mixin)
class ViewRedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        included_urls = [
            request.build_absolute_uri(reverse("account:register")),
            request.build_absolute_uri(reverse("account:mobile")),
            request.build_absolute_uri(reverse("account:otp_check")),
        ]

        previous_url = request.META.get("HTTP_REFERER")
        if previous_url:
            previous_url = previous_url.split('?')[0]  # Split the url from ? and chose the first part (the url)

        # Raise 404 if url is not in excluded list
        if previous_url not in included_urls and (request.method != "POST" or not request.POST):
            return redirect("account:login")
        
        return super().dispatch(request, *args, **kwargs)
