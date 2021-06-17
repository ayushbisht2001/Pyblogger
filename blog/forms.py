from django import forms
from .models import *


class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

    

class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title' ,'image' , 'content' , 'publish_date']
    def clean_title(self,*args,**kwargs):
        instance = self.instance
        title = self.cleaned_data.get("title")
        qs = BlogPost.objects.filter(title__iexact=title) # title__iexact :  it basically ignore the case-sensitivity  ;  title = lower(title)
        if instance is not None:
            qs = qs.exclude(pk = instance.pk)  # same as  (  id = instance.id  )
        if qs.exists():
            raise forms.ValidationError("This title is already been used , pls add another one ")
        return title



class CommentForm(forms.ModelForm):
    body = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment here !',
        'rows':5,
    }))
    class Meta:
        model = Comment
        fields = ['body']



class ReplyForm(forms.ModelForm):
    body = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment here !',
        'rows':4,
        'cols':50,
    }))
    class Meta:
        model = Reply
        fields = ['body']
