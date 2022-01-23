from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404

from .models import Post
from .forms import EditProfile


class Index(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'





# art = Post.objects.first()
# art.upload.url # Полная ссылка до файла
# art.upload.path
# art.upload.name # Имя файла














class AccountProfile(LoginRequiredMixin, TemplateView):
    template_name = 'allauth/account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfile
    success_url = '/accounts/profile'
    template_name = 'allauth/account/update_profile.html'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
          queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
