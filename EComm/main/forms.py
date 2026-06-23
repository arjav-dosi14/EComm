from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile, Product, Order, Category

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'w-full padding-3 border border-outline-variant rounded-lg'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'w-full padding-3 border border-outline-variant rounded-lg'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return profile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'price', 'old_price', 'image_url', 'image', 'description', 'stock', 'specifications', 'is_featured', 'is_trending']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            from django.utils.text import slugify
            slug = slugify(self.cleaned_data.get('name'))
        return slug

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country', 'delivery_method', 'payment_method']
