from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, TemplateView, CreateView, DetailView, DeleteView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.http import HttpResponse

from .models import Post, Response
from .forms import PostForm, RespondForm, ResponsesFilterForm


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
            context['respond'] = "Откликнулся"
        elif self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
            context['respond'] = "Мое_объявление"
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('board.add_post'):
        # if not self.request.user.has_perm('blog.add_post'):
            return HttpResponseRedirect(reverse('account_profile'))
        return super().dispatch(request, *args, **kwargs)

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


# def responses(request):
#     form = ResponsesFilterForm()
#     context = {'form': form}
#     # form = list(Post.objects.filter(author_id=request.user).order_by('-dateCreation'))
#     return render(request, 'responses.html', context)

title = str("")


class Responses(ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super(Responses, self).get_context_data(**kwargs)
        global title
        context['form'] = ResponsesFilterForm(self.request.user, initial={'title': title})
        context['title'] = title
        if title:
            post_id = Post.objects.get(title=title)
            context['filter_responses'] = list(Response.objects.filter(post_id=post_id).order_by('-dateCreation'))
            context['response_post_id'] = post_id.id
        else:
            context['filter_responses'] = list(Response.objects.filter(post_id__author_id=self.request.user).order_by('-dateCreation'))
        context['myresponses'] = list(Response.objects.filter(author_id=self.request.user).order_by('-dateCreation'))
        return context

    def post(self, request, *args, **kwargs):
        global title
        title = self.request.POST.get('title')
        return self.get(request, *args, **kwargs)


def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.status = True
        response.save()
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


def response_delete(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.delete()
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')






















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











# Пользователи нашего ресурса должны иметь возможность зарегистрироваться в нём по e-mail, получив
# письмо с кодом подтверждения регистрации. После регистрации им становится доступно создание и редактирование
# объявлений. Объявления состоят из заголовка и текста, внутри которого могут быть картинки, встроенные видео и
# другой контент. При отправке отклика пользователь должен получить e-mail с оповещением о нём. Также пользователю должна
# быть доступна приватная страница с откликами на его объявления, внутри которой он может фильтровать отклики по
# объявлениям, удалять их и принимать (при принятии отклика пользователю, оставившему отклик, также должно прийти
# уведомление).
#
# Также мы бы хотели иметь возможность отправлять пользователям новостные рассылки.
