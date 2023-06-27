from django import forms

class BookingForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
