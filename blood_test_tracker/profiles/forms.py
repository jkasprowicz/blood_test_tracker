from django import forms
from .models import Profile, Place, CustomGroup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['group']
        labels = {
            'group': 'Grupo',
        }


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Place.objects.filter(name=name).exists():
            raise forms.ValidationError("Local Já Existe!")
        return name



class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'duplicate_username': ("Nome de Usuário Já Existe."),
        'password_mismatch': ("Senhas diferentes!")
    }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label="Nome de usuário")
        self.fields['password1'] = forms.CharField(label="Senha", widget=forms.PasswordInput)
        self.fields['password2'] = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)
        self.fields['password1'].help_text = "Sua senha não pode ser muito semelhante às suas outras informações pessoais.<br>Sua senha deve conter pelo menos 8 caracteres.<br>Sua senha não pode ser uma senha comumente usada.<br>Sua senha não pode ser inteiramente numérica."
        self.fields['password2'].help_text = "Digite a mesma senha novamente, para verificação."

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['duplicate_username'], code='duplicate_username')
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class UserPermissionForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': 10}),
        label="Permissões Disponíveis",
        required=False
    )
    selected_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        widget=forms.SelectMultiple(attrs={'size': 10}),
        label="Permissões Selecionadas",
        required=False
    )

    def __init__(self, *args, **kwargs):
        user_permissions = kwargs.pop('user_permissions', [])
        super().__init__(*args, **kwargs)
        self.fields['selected_permissions'].queryset = Permission.objects.filter(id__in=user_permissions)



class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = CustomGroup
        fields = ['name', 'permissions']