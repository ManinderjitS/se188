from django import forms

class ImportantClassifiersForm(forms.Form):
    first_classifier = forms.CharField(label="1st Classifier", max_length=200)
