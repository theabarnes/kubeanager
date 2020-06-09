from django import forms

class VerifyBucketForm(forms.Form):
    verifybucket = forms.CharField(label='Bucket Name', max_length=100)
