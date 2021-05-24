from django import forms

CITIES = (
    ('K', 'Karachi'),
    ('L', 'Lahore')
)

class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ammar Abbasi'
    }))

    email = forms.EmailField(max_length=100)

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 Main St'
    }))

    # apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Apartment or suite'
    # }))

    city = forms.ChoiceField(
        widget=forms.RadioSelect, choices=CITIES)


    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
