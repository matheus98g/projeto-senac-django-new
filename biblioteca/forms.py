from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Livro, Autor, Categoria, Emprestimo, Reserva, Usuario

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        })
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Escolha um nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
        
        # Adicionar classes de validação
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'genero', 'quantidade']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['usuario', 'livro']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'livro': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas livros disponíveis
        self.fields['livro'].queryset = Livro.objects.filter(quantidade_disponivel__gt=0)
        # Filtrar apenas usuários ativos
        self.fields['usuario'].queryset = Usuario.objects.filter(is_active=True)
        # Adicionar placeholders
        self.fields['usuario'].empty_label = "Selecione um usuário"
        self.fields['livro'].empty_label = "Selecione um livro"
    
    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        livro = cleaned_data.get('livro')
        
        if usuario and livro:
            # Verificar se o usuário já tem empréstimo ativo do mesmo livro
            emprestimo_ativo = Emprestimo.objects.filter(
                usuario=usuario,
                livro=livro,
                status='ativo'
            ).exists()
            
            if emprestimo_ativo:
                raise forms.ValidationError(
                    'Este usuário já possui um empréstimo ativo deste livro.'
                )
            
            # Verificar se o livro está disponível
            if livro.quantidade_disponivel <= 0:
                raise forms.ValidationError(
                    'Este livro não está disponível para empréstimo.'
                )
            
            # Verificar se o usuário pode fazer mais empréstimos
            emprestimos_ativos = Emprestimo.objects.filter(
                usuario=usuario,
                status='ativo'
            ).count()
            
            if emprestimos_ativos >= 3:
                raise forms.ValidationError(
                    'Este usuário já atingiu o limite máximo de 3 empréstimos ativos.'
                )
        
        return cleaned_data


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['livro']
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
        }


class BuscarLivroForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título, autor...'
        })
    )
    genero = forms.ChoiceField(
        choices=[('', 'Todos os gêneros')] + Livro.TIPO_GENERO,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ProfileForm(forms.ModelForm):
    """Formulário para editar o perfil do usuário"""
    
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'tipo_usuario']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail'
            }),
            'tipo_usuario': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O tipo de usuário só pode ser editado por administradores
        if not kwargs.get('instance') or not kwargs['instance'].is_admin():
            self.fields['tipo_usuario'].widget = forms.HiddenInput()
            self.fields['tipo_usuario'].required = False
