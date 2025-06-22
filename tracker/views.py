from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Termo


class RegisterTermView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "tracker/index.html")

    def post(self, request):
        termo = request.POST.get("term")
        user_associated = request.user

        if Termo.objects.filter(name=termo, user=user_associated).exists():
            return render(
                request,
                "tracker/index.html",
                {"message": f'Termo "{termo}" já registrado!'},
            )

        new_termo = Termo(name=termo, user=user_associated)
        new_termo.save()

        return render(
            request,
            "tracker/index.html",
            {"message": f'Termo "{termo}" registrado com sucesso!'},
        )


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        termos = Termo.objects.filter(user=request.user)
        return render(request, "tracker/dashboard.html", {"termos": termos})

    def delete(self):
        pass
