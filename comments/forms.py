from django import forms
from django.core.exceptions import ValidationError

from .models import Comment


class CommentForm(forms.ModelForm):
    not_a_you_know_what = forms.CharField(required=False, widget=forms.HiddenInput(), initial='pwned!')

    class Meta:
        model = Comment
        fields = (
            'name',
            'website',
            'comment',
            'not_a_you_know_what',
        )

    def __init__(self, *args, **kwargs):
        self._object = kwargs.pop('obj', None)
        self._request = kwargs.pop('request', None)

        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cd = super(CommentForm, self).clean(*args, **kwargs)

        if cd['not_a_you_know_what']:
            raise ValidationError('Nope!')

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        comment = super(CommentForm, self).save(*args, **kwargs)

        comment.url = self._object.url
        comment.ip = self._request.META['REMOTE_ADDR']

        comment.save()

        # TODO: Send notification email

        return comment
