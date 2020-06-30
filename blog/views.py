from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import(LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy, reverse
from . import models
from accounts.models import Profile, Follow
# from braces.views import SelectRelatedMixin
# from django.http import Http404
from django.contrib.auth import get_user_model
from .forms import NewCommentForm, ImageForm


User = get_user_model()


class CreateTwitt(LoginRequiredMixin, generic.CreateView):
    fields = ("text",)
    model = models.Twitt
    template_name = 'blog/twitt_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:for_user", kwargs={"username": self.request.user.username})

######################################################################################

class SingleTwitt(generic.DetailView):
    model = models.Twitt
    template_name = 'blog/twitt_detail.html'
    context_object_name = 'twitt'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = models.Comment.objects.filter(twitt_connected=self.get_object()).order_by('-publish_date')         # get all comments that are connected to the given Twitt
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)                           # set form from forms.py
        return data

    def post(self, request, *args, **kwargs):
        new_comment = models.Comment(text=request.POST.get('text'), author=self.request.user, twitt_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

######################################################################################

class UserTwitt(generic.ListView):
    model = models.Twitt
    template_name = 'blog/user_twitt_list.html'
    image_form = ImageForm

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):                                                                   #returns objects (twitts) sorted by date of the user whose profile we are on
        twitt_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return models.Twitt.objects.filter(author=twitt_user).order_by('-publish_date')

    def get_context_data(self, **kwargs):

        if self.request.user.username == '' or self.request.user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=self.request.user,
                                                follow_user=self.visible_user()).count() == 0)    # set can_follow as the Follow object of the logged in user with follow_user for the user whose profile is visiting == 0

        data = super().get_context_data(**kwargs)
        data['user_profile'] = self.visible_user()
        data['can_follow'] = can_follow
        return data

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())        # set follows_between as the Follow object of the logged in user with follow_user for the user whose profile is visiting

            if 'follow' in request.POST:                                                            # if 'follow' set new_relation as the Follow object of the logged in user with follow_user for the user whose profile is visiting
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())       # then if follows_between == 0, make that new_relation and save it
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:                                                        # if 'unfollow' that mean follows_between is > 0 and we delete that particularly follows_between --> switching
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)

######################################################################################

class DeleteTwitt(LoginRequiredMixin, generic.DeleteView):
    model = models.Twitt

    def get_success_url(self):
        return reverse_lazy("blog:for_user", kwargs = {'username':self.request.user.username})


    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")          # after delete show message
        return super().delete(*args, **kwargs)

######################################################################################

class UpdateTwitt(LoginRequiredMixin, generic.UpdateView):
    model = models.Twitt
    fields = ['text']
    template_name = 'blog/twitt_update.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:singletwitt", kwargs={"username": self.request.user.username, "pk": self.object.pk})

######################################################################################

def edit_photo(request):
    if request.method == "POST":
        profile_form = ImageForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('/home/')

    else:
        profile_form = ImageForm(instance=request.user.profile)

    context = {'profile_form':profile_form}
    return render(request, 'blog/profile.html', context)
