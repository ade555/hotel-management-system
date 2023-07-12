from django import forms

class BookingForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'})
    )
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control'})
    )

    """
    
    TO DO:
    Work on form widget to allow cross browser compatibility in date time field

    """
