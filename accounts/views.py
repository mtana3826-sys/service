from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponse

from .forms import PhoneLoginForm

class PhoneLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = PhoneLoginForm

    def get_cache_key(self):
        ip = self.request.META.get("REMOTE_ADDR", "unknown")
        return f"login_attempts_{ip}"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            attempts = cache.get(self.get_cache_key(), 0)

            if attempts >= 5:
                return HttpResponse(
                    "Слишком много попыток. Попробуйте через 15 минут.",
                    status=429
                )

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        key = self.get_cache_key()
        attempts = cache.get(key, 0)
        cache.set(key, attempts + 1, 900)
        return super().form_invalid(form)

    def form_valid(self, form):
        cache.delete(self.get_cache_key())
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect("login")