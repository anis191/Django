from django import forms 
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserCreationForm
import re
from task.forms import StyleFormMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from user.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

'''
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None
'''
class CustomRegisterForm(StyleFormMixin, forms.ModelForm):
    CreatePassword = forms.CharField(widget=forms.PasswordInput)
    ConfirmPassword = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','CreatePassword','ConfirmPassword']

    # 1.Field Error:
    def clean_CreatePassword(self):
        password1 = self.cleaned_data.get('CreatePassword')
        errors = []
        if len(password1) < 8:
            errors.append("Password must be 8 characters needed")
        if not re.search(r"[A-Z]", password1):
            errors.append("Password must contain at least one uppercase letter.")
    
        if not re.search(r"[a-z]", password1):
            errors.append("Password must contain at least one lowercase letter.")

        if not re.search(r"\d", password1):
            errors.append("Password must contain at least one digit.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            errors.append("Password must contain at least one special character.") 
        
        if errors:
            raise forms.ValidationError(errors)
        return password1
    
    # dulicate email check:
    def clean_email(self):
        email = self.cleaned_data.get('email')
        check = User.objects.filter(email = email)
        if check:
            raise forms.ValidationError("Duplicate Email Not Allow")
        return email
    
    # 2.Non-Field Error:
    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('CreatePassword')
        password2 = self.cleaned_data.get('ConfirmPassword')

        if password1 != password2:
            raise forms.ValidationError("Password Not Match")
        
        return cleaned_data

class LoginForm(StyleFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

class AssignRoleForm(StyleFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label="Select a role"
    )

class CreateGroupForm(StyleFormMixin, forms.ModelForm):
    #for create a group we need "permissions" field
    permissions = forms.ModelMultipleChoiceField(
        queryset = Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required=False,     #For this we can create a "group" without any permission
        label= 'Assign Permissions'
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]

class CustomPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyleFormMixin, SetPasswordForm):
    pass

'''
class EditProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']
    
    bio = forms.CharField(required=False, widget=forms.Textarea, label='bio')
    profile_image = forms.ImageField(required=False, label='profile image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)
        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image
    
    def save(self, commit=True):
        user = super().save(commit=False)

        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')

            if commit:
                self.userprofile.save()
        if commit:
            user.save()
        return user
'''

class EditProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','bio','profile_image']