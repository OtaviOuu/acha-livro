from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Termo
from users.models import User
from django.shortcuts import redirect


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
        livros = request.user.livros
        return render(
            request,
            "tracker/dashboard.html",
            {
                "termos": termos,
                "livros": livros,
            },
        )

    def post(self, request, livro_name):
        request.user.livros = [
            livro for livro in request.user.livros if livro["name"] != livro_name
        ]
        request.user.save()
        return redirect("dashboard")

class DeleteTermView(LoginRequiredMixin, View):
    def post(self, request, term_id):
        Termo.objects.filter(id=term_id, user=request.user).delete()
        return redirect("dashboard")


class HomeView(View):
    """
    Landing page de boas-vindas ao site.
    """
    def get(self, request):
        return render(request, "tracker/home.html")
