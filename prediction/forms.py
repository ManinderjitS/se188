from django import forms

class ImportantClassifiersForm(forms.Form):
    name = forms.CharField(label="Name of your company", max_length=200)
    goal = forms.CharField(label="Kickstarter financial goal", max_length=200)
    pledge = forms.CharField(label="Current Pledged Money", max_length=200)
    backers = forms.CharField(label="Current Total Backers", max_length=200)
