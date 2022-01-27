from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, TemplateView, CreateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.http import HttpResponse

from .models import Post, Response
from .forms import EditProfile, PostForm, RespondForm


class Index(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

class PostItem(DetailView):
    model = Post
    template_name = 'post_item.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Response.objects.filter(author_id=self.request.user.id).filter(post_id=self.kwargs.get('pk')):
            context['respond'] = "True"
        else:
            context['respond'] = "False"
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return redirect(f'/post/{post.id}')


class EditPost(LoginRequiredMixin, UpdateView):
    template_name = 'edit_post.html'
    form_class = PostForm
    success_url = '/create/'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Редактировать объявление может только автор")
            # raise Http404

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/post/' + str(self.kwargs.get('pk')))


class DeletePost(LoginRequiredMixin, DeleteView):
    template_name = 'delete_post.html'
    queryset = Post.objects.all()
    success_url = '/index'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Удалить объявление может только автор")
            # raise Http404


class Responses(ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'


class Respond(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'respond.html'
    form_class = RespondForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        respond = form.save(commit=False)
        respond.author = User.objects.get(id=self.request.user.id)
        # return HttpResponse(self.kwargs.get('pk'))
        respond.post = Post.objects.get(id=self.kwargs.get('pk'))
        respond.save()
        return redirect(f'/post/{self.kwargs.get("pk")}')


"""
art = Post.objects.first()
art.upload.url # Полная ссылка до файла
art.upload.path
art.upload.name # Имя файла
"""













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
