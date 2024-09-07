from django import forms


class CART_ADD_PRODUCT_FORM(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=50, help_text='PRODUCT SHOULN NOT EXCEED 50 QUANTITIES')
    override = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=False)
    
    
class CART_OVERRIDE_PRODUCT(forms.Form):
    quantity = forms.IntegerField(max_value=50, min_value=1,)
    override = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=False)