from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('aluno', 'Aluno'),
        ('admin', 'Administrador'),
    )

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO,
        default='aluno',
        verbose_name='Tipo de Usuário'
    )

    email = models.EmailField(
        unique=True,
        verbose_name='E-mail',
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    
    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"


    def is_admin(self):
        return self.tipo_usuario == 'admin'


    def pode_reservar(self):
        reservas_ativas = self.reservas.filter(status='ativa').count()
        return reservas_ativas < 3
    
class Autor(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Autor')
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )   
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nome']

class Livro(models.Model):
    TIPO_GENERO = [
        ('ficcao', 'Ficção'),
        ('nao_ficcao', 'Não Ficção'),
        ('fantasia', 'Fantasia'),
        ('aventura', 'Aventura'),
        ('romance', 'Romance'),
        ('suspense', 'Suspense'),
        ('terror', 'Terror'),
        ('biografia', 'Biografia'),
        ('autoajuda', 'Autoajuda'),
        ('educacional', 'Educacional'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título do Livro')
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='livros',
        verbose_name='Autor'
    )
    genero =  models.CharField(
        max_length=20,
        choices=TIPO_GENERO,
        verbose_name='Gênero'
    )
    
    quantidade = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Quantidade Total'
    )
    
    quantidade_disponivel = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Quantidade Disponível'
    )
    
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        
        if not self.pk:
            self.quantidade_disponivel = self.quantidade
        
        if self.quantidade_disponivel > self.quantidade:
            self.quantidade_disponivel = self.quantidade
        
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.quantidade_disponivel > self.quantidade:
            raise ValidationError(
                "A quantidade disponível não pode ser maior que a quantidade total."
            )
    def is_available(self):
        return self.quantidade_disponivel > 0
    
    def get_author_display(self):
        return  ", ".join([autor.nome for autor in self.autor.all()]) if self.autor else "Nenhum Autor"
    
    def get_total_loans(self):
        return self.emprestimos.count()
    
    def delete(self, *args, **kwargs):
        if self.reservas.filter(status='ativa').exists():
            raise ValidationError("Não é possível excluir um livro com reservas ativas.")
        if self.emprestimos.filter(status='ativo').exists():
            raise ValidationError("Não é possível excluir um livro com empréstimos ativos.")
        super().delete(*args, **kwargs)

class Reserva(models.Model):
    STATUS_RESERVA = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Usuário'
    )
    
    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Livro'
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_RESERVA,
        default='ativa',
        verbose_name='Status da Reserva'
    )    
    data_reserva = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Reserva'
    )
    
    data_expiracao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Expiração'
    )
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-data_reserva']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'livro', 'status'],
                condition=models.Q(status='ativa'),
                name='unique_active_reservation_per_user_and_book'
            )
        ]
    
    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.livro.titulo} ({self.get_status_display()})"

    def clean(self):
        if not self.pk and not self.usuario.pode_reservar():
            raise ValidationError("O usuário não pode fazer mais reservas ativas.")

        if not self.pk and not self.livro.is_available():
            raise ValidationError("O livro não está disponível para reserva.")

        if not self.pk:
            reserva_existente = Reserva.objects.filter(
                usuario=self.usuario,
                livro=self.livro,
                status='ativa'
            ).exists()
            if reserva_existente:
                raise ValidationError("Já existe uma reserva ativa para este livro por este usuário.")

    def save(self, *args, **kwargs):
        is_new = not self.pk
        
        # Set expiration date for new reservations (7 days from now)
        if is_new and not self.data_expiracao:
            self.data_expiracao = timezone.now() + timedelta(days=7)

        if not is_new:
            old_instance = Reserva.objects.get(pk=self.pk)

        super().save(*args, **kwargs)

        if is_new and self.status == 'ativa':
            self.livro.quantidade_disponivel -= 1
            self.livro.save()


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome da Categoria')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    STATUS_EMPRESTIMO = [
        ('ativo', 'Ativo'),
        ('devolvido', 'Devolvido'),
        ('atrasado', 'Atrasado'),
    ]
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='emprestimos',
        verbose_name='Usuário'
    )
    
    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='emprestimos',
        verbose_name='Livro'
    )
    
    data_emprestimo = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do Empréstimo'
    )
    
    data_devolucao_prevista = models.DateTimeField(
        verbose_name='Data de Devolução Prevista'
    )
    
    data_devolucao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Devolução'
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_EMPRESTIMO,
        default='ativo',
        verbose_name='Status'
    )
    
    renovacoes = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Renovações'
    )
    
    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-data_emprestimo']
    
    def __str__(self):
        return f"Empréstimo de {self.livro.titulo} para {self.usuario.username}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # Novo empréstimo - definir data de devolução prevista (15 dias)
            self.data_devolucao_prevista = timezone.now() + timedelta(days=15)
        super().save(*args, **kwargs)
    
    def devolver(self):
        """Marca o empréstimo como devolvido"""
        if not self.data_devolucao:
            self.data_devolucao = timezone.now()
            self.status = 'devolvido'
            # Aumentar quantidade disponível do livro
            self.livro.quantidade_disponivel += 1
            self.livro.save()
            self.save()
    
    def renovar(self):
        """Renova o empréstimo por mais 15 dias"""
        if self.renovacoes < 2 and not self.data_devolucao:
            self.data_devolucao_prevista = timezone.now() + timedelta(days=15)
            self.renovacoes += 1
            self.save()
            return True
        return False
    
    def is_atrasado(self):
        """Verifica se o empréstimo está atrasado"""
        if not self.data_devolucao and timezone.now() > self.data_devolucao_prevista:
            return True
        return False
    
    def dias_atraso(self):
        """Calcula quantos dias de atraso"""
        if self.is_atrasado():
            return (timezone.now() - self.data_devolucao_prevista).days
        return 0