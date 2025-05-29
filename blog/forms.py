from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Post, Comment, UserProfile, Category, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'tags', 'featured_image_url', 'status', 'is_featured', 'is_breaking', 'read_time']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'featured_image_url': forms.URLInput(attrs={'placeholder': 'https://example.com/image.jpg'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-8 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('read_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'featured_image_url',
            'excerpt',
            'content',
            'tags',
            Row(
                Column('is_featured', css_class='form-group col-md-6 mb-0'),
                Column('is_breaking', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Post', css_class='btn btn-primary')
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Write your comment here...',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'content',
            Submit('submit', 'Post Comment', css_class='btn btn-primary')
        )

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar_url', 'website', 'twitter', 'github', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'avatar_url': forms.URLInput(attrs={'placeholder': 'https://example.com/avatar.jpg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            'bio',
            'avatar_url',
            Row(
                Column('website', css_class='form-group col-md-6 mb-0'),
                Column('twitter', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('github', css_class='form-group col-md-6 mb-0'),
                Column('linkedin', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile.save()
        return profile
