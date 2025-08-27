from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Autor, Livro, Categoria, Emprestimo, Reserva


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_active')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('tipo_usuario', 'data_cadastro')
        }),
    )
    
    readonly_fields = ('data_cadastro',)


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_cadastro')
    search_fields = ('nome',)
    readonly_fields = ('data_cadastro',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_cadastro')
    search_fields = ('nome',)
    readonly_fields = ('data_cadastro',)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'genero', 'quantidade', 'quantidade_disponivel', 'data_cadastro')
    list_filter = ('genero', 'data_cadastro')
    search_fields = ('titulo', 'autor__nome')
    readonly_fields = ('data_cadastro',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Novo objeto
            obj.quantidade_disponivel = obj.quantidade
        super().save_model(request, obj, form, change)


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livro', 'data_emprestimo', 'data_devolucao_prevista', 'data_devolucao', 'status')
    list_filter = ('status', 'data_emprestimo', 'data_devolucao')
    search_fields = ('usuario__username', 'livro__titulo')
    readonly_fields = ('data_emprestimo',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livro', 'status', 'data_reserva', 'data_expiracao')
    list_filter = ('status', 'data_reserva')
    search_fields = ('usuario__username', 'livro__titulo')
    readonly_fields = ('data_reserva',)
