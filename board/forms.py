from django import forms
from django.contrib.auth.models import User

from .models import Post, Response
from ckeditor.widgets import CKEditorWidget

class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class PostForm(forms.ModelForm):
    # text = forms.CharField(widget=CKEditorWidget(config_name='default'))
    # text = forms.CharField(widget=CKEditorWidget, label='')
    class Meta:
        model = Post
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
