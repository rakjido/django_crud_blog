from django import forms

from .models import Post, Comment, Attachment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('upfiles',)


# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadFile
#         fields = ('title', 'files',)
