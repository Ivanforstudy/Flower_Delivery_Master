from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'delivery_time']
        widgets = {
            'delivery_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
