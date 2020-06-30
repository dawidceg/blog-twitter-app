from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from blog.models import Twitt
from django.db.models import Q

class TestPage(TemplateView):
    template_name = 'home.html'


def list_of_twitt(request):
    queryset = Twitt.objects.all().order_by('-publish_date')
    context = {"page_obj": queryset}
    return render(request, "home.html", context)


def listing(request):
    queryset_list = Twitt.objects.all().order_by('-publish_date')
    paginator = Paginator(queryset_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)


def search(request):
    query = request.GET.get('q')
    alltwitts = Twitt.objects.filter(Q(comment__text__icontains=query) | Q(text__icontains=query)).distinct()
    params = {'alltwitts':alltwitts}
    return render(request, 'search.html', params)
