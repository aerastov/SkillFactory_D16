from django import forms
from django.contrib.auth.models import User

from .models import Post, Response
from ckeditor.widgets import CKEditorWidget

class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'title': forms.TextInput(attrs={'size': '100'})}
        fields = ('category', 'title', 'text',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Категория:"
        self.fields['title'].label = "Заголовок"
        self.fields['text'].label = "Текст объявления:"


class RespondForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(RespondForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Текст отклика:"


# class ResponsesFilterForm(forms.Form):
#
#     title = forms.ModelChoiceField(
#         label='Объявление',
#         queryset=Post.objects.filter(author_id=2).order_by('-dateCreation').values_list('title', flat=True),
#         empty_label="Все",
#         required=False
#     )

class ResponsesFilterForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ResponsesFilterForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.ModelChoiceField(
            label='Объявление',
            queryset=Post.objects.filter(author_id=user.id).order_by('-dateCreation').values_list('title', flat=True),
            empty_label="Все",
            required=False
        )
