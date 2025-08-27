from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'biblioteca'

def home_redirect(request):
    if request.user.is_authenticated and request.user.is_admin():
        from .views import HomeView
        return HomeView.as_view()(request)
    return redirect('biblioteca:livro_list')

urlpatterns = [
    path('', home_redirect, name='home'),
    
    # Autenticação
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # URLs para livros e autores
    path('livros/', views.LivroListView.as_view(), name='livro_list'),
    path('livros/<int:pk>/', views.LivroDetailView.as_view(), name='livro_detail'),
    path('livros/buscar/', views.LivroBuscarView.as_view(), name='livro_buscar'),
    
    # URLs para administração de livros e autores
    path('manage/livros/criar/', views.LivroCreateView.as_view(), name='livro_create'),
    path('manage/livros/<int:pk>/editar/', views.LivroUpdateView.as_view(), name='livro_update'),
    path('manage/livros/<int:pk>/deletar/', views.LivroDeleteView.as_view(), name='livro_delete'),

    # URLs para administração de autores
    path('manage/autores/criar/', views.AutorCreateView.as_view(), name='autor_create'),
    path('manage/autores/<int:pk>/editar/', views.AutorUpdateView.as_view(), name='autor_update'),
    path('manage/autores/<int:pk>/deletar/', views.AutorDeleteView.as_view(), name='autor_delete'),

    # URLs para administração de usuários
    path('manage/usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('manage/usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario_detail'),
    path('manage/usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('manage/usuarios/<int:pk>/deletar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),

    # URLs para administração de empréstimos
    path('manage/emprestimos/criar/', views.EmprestimoCreateView.as_view(), name='emprestimo_create'),

    # URLs para administração de categorias
    path('manage/categorias/criar/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('manage/categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('manage/categorias/<int:pk>/deletar/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),

    # URLs para administração de dashboard e relatórios
    path('manage/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),

    # URLs para reservas de livros
    path('reservas/', views.ReservaListView.as_view(), name='reserva_list'),
    path('reservas/minhas/', views.MinhasReservasView.as_view(), name='minhas_reservas'),
    path('livros/<int:livro_id>/reservar/', views.ReservarLivroView.as_view(), name='reservar_livro'),
    path('reservas/<int:pk>/cancelar/', views.CancelarReservaView.as_view(), name='cancelar_reserva'),
    
    # URLs para empréstimos
    path('emprestimos/', views.EmprestimoListView.as_view(), name='emprestimo_list'),
    path('emprestimos/<int:pk>/', views.EmprestimoDetailView.as_view(), name='emprestimo_detail'),
    path('emprestimos/<int:pk>/devolver/', views.devolver_livro, name='devolver_livro'),
    path('emprestimos/<int:pk>/renovar/', views.renovar_emprestimo, name='renovar_emprestimo'),
    
    # URLs para categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    
    # URLs para relatórios e dashboard
    path('relatorios/', views.RelatoriosView.as_view(), name='relatorios'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # AJAX URLs
    path('ajax/livros-disponiveis/', views.livros_disponiveis, name='livros_disponiveis'),
    path('ajax/verificar-disponibilidade/<int:livro_id>/', views.verificar_disponibilidade, name='ajax_verificar_disponibilidade'),
    
    # URLs para administração
    path('api/livros/disponibilidade/<int:livro_id>/', views.VerificarDisponibilidadeView.as_view(), name='verificar_disponibilidade'),
    path('api/reservas/expirar/', views.ExpirarReservasView.as_view(), name='expirar_reservas'),

    # URLs para autores (listagem e detalhes)
    path('autores/', views.AutorListView.as_view(), name='autor_list'),
    path('autores/<int:pk>/', views.AutorDetailView.as_view(), name='autor_detail'),
]