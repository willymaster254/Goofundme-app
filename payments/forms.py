from django import forms

class DonationForm(forms.Form):
    amount = forms.DecimalField(
        label="Donation Amount (USD)",
        min_value=1,
        decimal_places=2,
        max_digits=8,
        widget=forms.NumberInput(attrs={
            "placeholder": "Enter amount",
            "class": "form-control"
        })
    )
