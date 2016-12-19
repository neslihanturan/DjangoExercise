from django import forms
from .models import Post, InapproptiateWord, SurveyOffer
from django.forms.fields import DateField
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from settings import *
from .choices import *

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'cols': 55, 'rows': 1}), label="Short Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 54, 'rows': 1}))
    class Meta:
        model = Post
        fields = ('title','description')

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        description = cleaned_data.get("description")
        title = cleaned_data.get("title")

        if description and title and IS_INAPPROPRIATE_CONTENT_FILTERED:
            # Only do something if both fields are valid so far.
            inappropriate_words = InapproptiateWord.objects.all()
            problem = [w for w in inappropriate_words if w.word in description.lower()]
            if problem:
                raise forms.ValidationError(
                    "Please try to be kinder"
                )
class SurveyOfferForm(forms.ModelForm):
    #begin = forms.TimeField(label='begins at',widget=TimeWidget(usel10n=True, bootstrap_version=3))
    #end = forms.TimeField(label='ends at',widget=TimeWidget(usel10n=True, bootstrap_version=3))
    title = forms.CharField(widget=forms.Textarea(attrs={'cols': 55, 'rows': 1}), label="Survey Title")
    questions = forms.CharField(widget=forms.Textarea(attrs={'cols': 57, 'rows': 10}))
    class Meta:
        model = SurveyOffer
        fields = ('title','questions')
        #widgets = {
            #Use localization and bootstrap 3

        #    'datetime': DateTimeWidget(attrs={'id':"date"}, usel10n = True, bootstrap_version=3)
        #}

class UserSelectorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                              empty_label="(Choose a User)")
    #def __init__(self, *args, **kwargs):
    #    extra = kwargs.pop('extra')
    #    super(UserSelectorForm, self).__init__(*args, **kwargs)
    #    self.fields['users'] = forms.ChoiceField(choices=STATUS_CHOICES)

class SurveyForm(forms.Form):
    survey_title = forms.CharField(widget=forms.TextInput(attrs={'title':"Survey Title",'size':'60','maxlength':'70'} ))
    survey_id = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        survey_id = kwargs.pop('survey_id')
        survey_title = kwargs.pop('survey_title')
        super(SurveyForm, self).__init__(*args, **kwargs)

        self.fields['survey_title'] = forms.CharField(initial=survey_title)
        self.fields['survey_title'].widget.attrs['readonly'] = True

        self.fields['survey_id'] = forms.IntegerField(initial=survey_id)
        self.fields['survey_id'].widget.attrs['readonly'] = True
        self.fields['survey_id'].widget = forms.HiddenInput()

        for i, question in enumerate(extra):
            #self.fields['custom_%s' % i] = forms.CharField(label=question)
            self.fields['choices_%s' % i] = forms.ChoiceField(choices = STATUS_CHOICES, required=True,
                                                    widget=forms.RadioSelect, label=question)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))
