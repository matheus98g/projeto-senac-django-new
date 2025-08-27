from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from .forms import LoginForm, RegisterForm, LivroForm, AutorForm, CategoriaForm, EmprestimoForm, ReservaForm
from .models import Livro, Autor, Categoria, Emprestimo, Reserva, Usuario
import datetime
from django.db import models

# Mixin for admin-only access
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

# Basic views
class HomeView(AdminRequiredMixin, TemplateView):
    template_name = 'biblioteca/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_livros'] = Livro.objects.count()
        context['total_usuarios'] = Usuario.objects.count()
        context['emprestimos_ativos'] = Emprestimo.objects.filter(status='ativa').count()
        context['reservas_ativas'] = Reserva.objects.filter(status='ativa').count()
        return context

class LoginView(AuthLoginView):
    template_name = 'biblioteca/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        if self.request.user.is_admin():
            return reverse_lazy('biblioteca:admin_dashboard')
        return reverse_lazy('biblioteca:home')

class LogoutView(AuthLogoutView):
    next_page = 'biblioteca:home'

class RegisterView(TemplateView):
    template_name = 'biblioteca/register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm()
        return context
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('biblioteca:home')
        return render(request, self.template_name, {'form': form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'biblioteca/profile.html'

# Livro views
class LivroListView(ListView):
    model = Livro
    template_name = 'biblioteca/livro_list.html'
    context_object_name = 'livros'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Livro.objects.select_related('autor').all()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(autor__nome__icontains=query)
            )
        
        # Filter by genre
        genero = self.request.GET.get('genero')
        if genero:
            queryset = queryset.filter(genero=genero)
            
        return queryset.order_by('titulo')

class LivroDetailView(DetailView):
    model = Livro
    template_name = 'biblioteca/livro_detail.html'
    context_object_name = 'livro'

class LivroBuscarView(TemplateView):
    template_name = 'biblioteca/livro_buscar.html'

class LivroCreateView(AdminRequiredMixin, CreateView):
    model = Livro
    form_class = LivroForm
    template_name = 'biblioteca/livro_form.html'
    success_url = reverse_lazy('biblioteca:livro_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Livro criado com sucesso!')
        return super().form_valid(form)

class LivroUpdateView(AdminRequiredMixin, UpdateView):
    model = Livro
    form_class = LivroForm
    template_name = 'biblioteca/livro_form.html'
    success_url = reverse_lazy('biblioteca:livro_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Livro atualizado com sucesso!')
        return super().form_valid(form)

class LivroDeleteView(AdminRequiredMixin, DeleteView):
    model = Livro
    template_name = 'biblioteca/livro_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:livro_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Livro excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# Autor views
class AutorListView(ListView):
    model = Autor
    template_name = 'biblioteca/autor_list.html'
    context_object_name = 'autores'

class AutorDetailView(DetailView):
    model = Autor
    template_name = 'biblioteca/autor_detail.html'
    context_object_name = 'autor'

class AutorCreateView(AdminRequiredMixin, CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'biblioteca/autor_form.html'
    success_url = reverse_lazy('biblioteca:autor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Autor criado com sucesso!')
        return super().form_valid(form)

class AutorUpdateView(AdminRequiredMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'biblioteca/autor_form.html'
    success_url = reverse_lazy('biblioteca:autor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Autor atualizado com sucesso!')
        return super().form_valid(form)

class AutorDeleteView(AdminRequiredMixin, DeleteView):
    model = Autor
    template_name = 'biblioteca/autor_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:autor_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Autor excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# Reserva views
class ReservaListView(AdminRequiredMixin, ListView):
    model = Reserva
    template_name = 'biblioteca/reserva_list.html'
    context_object_name = 'reservas'

class MinhasReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'biblioteca/minhas_reservas.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        # This is not used by the template, so we override get_context_data
        return Reserva.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_reservas = Reserva.objects.filter(usuario=self.request.user)
        context['reservas_ativas'] = user_reservas.filter(status='ativa')
        context['reservas_historico'] = user_reservas.exclude(status='ativa')
        context['reservas_expiradas'] = user_reservas.filter(status='expirada')
        context['reservas_canceladas'] = user_reservas.filter(status='cancelada')
        context['total_reservas'] = user_reservas.count()
        return context

class ReservarLivroView(LoginRequiredMixin, CreateView):
    model = Reserva
    template_name = 'biblioteca/reservar_livro.html'
    fields = []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livro'] = get_object_or_404(Livro, pk=self.kwargs['livro_id'])
        return context
    
    def post(self, request, *args, **kwargs):
        livro = get_object_or_404(Livro, pk=self.kwargs['livro_id'])
        
        # Create the reservation instance manually
        reserva = Reserva(
            usuario=request.user,
            livro=livro,
            status='ativa'
        )
        
        try:
            # Validate the instance
            reserva.clean()
            reserva.save()
            messages.success(request, 'Reserva realizada com sucesso!')
            return redirect('biblioteca:minhas_reservas')
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {
                'livro': livro,
                'form': self.get_form()
            })
    
    def get_success_url(self):
        return reverse_lazy('biblioteca:minhas_reservas')

class CancelarReservaView(LoginRequiredMixin, UpdateView):
    model = Reserva
    fields = []
    
    def post(self, request, *args, **kwargs):
        reserva = self.get_object()
        if reserva.usuario != request.user and not request.user.is_admin():
            messages.error(request, 'Você não tem permissão para cancelar esta reserva.')
            return redirect('biblioteca:minhas_reservas')
        
        reserva.status = 'cancelada'
        reserva.save()
        
        # Aumentar quantidade disponível
        reserva.livro.quantidade_disponivel += 1
        reserva.livro.save()
        
        messages.success(request, 'Reserva cancelada com sucesso!')
        return redirect('biblioteca:minhas_reservas')

class ReservaDetailView(DetailView):
    model = Reserva
    template_name = 'biblioteca/reserva_detail.html'
    context_object_name = 'reserva'

# Admin views
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'biblioteca/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_livros'] = Livro.objects.count()
        context['total_usuarios'] = Usuario.objects.count()
        context['emprestimos_ativos'] = Emprestimo.objects.filter(status='ativa').count()
        context['reservas_ativas'] = Reserva.objects.filter(status='ativa').count()
        # Optionally add more context for alerts and recent activities
        context['emprestimos_vencidos'] = Emprestimo.objects.filter(status='vencido')
        context['reservas_expirando'] = Reserva.objects.filter(status='expirada')
        context['livros_sem_estoque'] = Livro.objects.filter(quantidade_disponivel=0)
        context['atividades_recentes'] = []  # Add your logic for recent activities here
        return context

class UsuarioListView(AdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'biblioteca/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 12

    def get_queryset(self):
        queryset = Usuario.objects.all()
        search = self.request.GET.get('search')
        tipo_usuario = self.request.GET.get('tipo_usuario')
        status = self.request.GET.get('status')
        ordenar = self.request.GET.get('ordenar')

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        if tipo_usuario:
            queryset = queryset.filter(tipo_usuario=tipo_usuario)
        if status:
            if status == 'ativo':
                queryset = queryset.filter(is_active=True)
            elif status == 'inativo':
                queryset = queryset.filter(is_active=False)
        if ordenar:
            if ordenar == 'nome':
                queryset = queryset.order_by('first_name', 'last_name')
            elif ordenar == 'data_cadastro':
                queryset = queryset.order_by('-date_joined')
            elif ordenar == 'ultimo_acesso':
                queryset = queryset.order_by('-last_login')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = context['usuarios']

        # Estatísticas
        now = datetime.datetime.now()
        context['total_usuarios'] = Usuario.objects.count()
        context['usuarios_ativos'] = Usuario.objects.filter(is_active=True).count()
        context['usuarios_admin'] = Usuario.objects.filter(tipo_usuario='admin').count()
        context['novos_usuarios_mes'] = Usuario.objects.filter(
            date_joined__month=now.month,
            date_joined__year=now.year
        ).count()

        # Estatísticas individuais
        for usuario in usuarios:
            usuario.emprestimos_count = Emprestimo.objects.filter(usuario=usuario).count()
            usuario.reservas_count = Reserva.objects.filter(usuario=usuario).count()
            usuario.pendencias_count = Emprestimo.objects.filter(usuario=usuario, status='vencido').count()

        return context

class UsuarioDetailView(AdminRequiredMixin, DetailView):
    model = Usuario
    template_name = 'biblioteca/usuario_detail.html'
    context_object_name = 'usuario'

class UsuarioUpdateView(AdminRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'biblioteca/usuario_form.html'
    fields = ['first_name', 'last_name', 'email', 'tipo_usuario', 'is_active']
    success_url = reverse_lazy('biblioteca:usuario_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return super().form_valid(form)

class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'biblioteca/usuario_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:usuario_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuário excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# Emprestimo views
class EmprestimoListView(AdminRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'biblioteca/emprestimo_list.html'
    context_object_name = 'emprestimos'

class EmprestimoDetailView(DetailView):
    model = Emprestimo
    template_name = 'biblioteca/emprestimo_detail.html'
    context_object_name = 'emprestimo'

class EmprestimoCreateView(AdminRequiredMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'biblioteca/emprestimo_form.html'
    success_url = reverse_lazy('biblioteca:emprestimo_list')
    
    def form_valid(self, form):
        # Diminuir quantidade disponível do livro
        livro = form.instance.livro
        if livro.quantidade_disponivel > 0:
            livro.quantidade_disponivel -= 1
            livro.save()
            messages.success(self.request, 'Empréstimo criado com sucesso!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Livro não disponível para empréstimo.')
            return self.form_invalid(form)

# Categoria views
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'biblioteca/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'biblioteca/categoria_detail.html'
    context_object_name = 'categoria'

class CategoriaCreateView(AdminRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'biblioteca/categoria_form.html'
    success_url = reverse_lazy('biblioteca:categoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoria criada com sucesso!')
        return super().form_valid(form)

class CategoriaUpdateView(AdminRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'biblioteca/categoria_form.html'
    success_url = reverse_lazy('biblioteca:categoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada com sucesso!')
        return super().form_valid(form)

class CategoriaDeleteView(AdminRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'biblioteca/categoria_confirm_delete.html'
    success_url = reverse_lazy('biblioteca:categoria_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoria excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Dashboard views
class RelatoriosView(AdminRequiredMixin, TemplateView):
    template_name = 'biblioteca/relatorios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        tipo_relatorio = self.request.GET.get('tipo_relatorio')

        emprestimos = Emprestimo.objects.all()
        if data_inicio:
            emprestimos = emprestimos.filter(data_emprestimo__gte=data_inicio)
        if data_fim:
            emprestimos = emprestimos.filter(data_emprestimo__lte=data_fim)

        total_emprestimos = emprestimos.count()

        # Livros mais emprestados (correto)
        livros_populares = (
            Livro.objects
            .filter(id__in=emprestimos.values_list('livro', flat=True))
            .annotate(total_emprestimos=models.Count('emprestimos'))
            .order_by('-total_emprestimos')[:10]
        )

        usuarios_ativos = Usuario.objects.filter(
            id__in=emprestimos.filter(status='ativa').values_list('usuario', flat=True)
        ).count()

        devolvidos_no_prazo = emprestimos.filter(
            status='devolvido',
            data_devolucao__lte=models.F('data_devolucao_prevista')
        ).count()
        total_devolvidos = emprestimos.filter(status='devolvido').count()
        taxa_devolucao = (
            (devolvidos_no_prazo / total_devolvidos) * 100 if total_devolvidos > 0 else 0
        )

        context['stats'] = {
            'total_emprestimos': total_emprestimos,
            'livros_populares': livros_populares.count(),
            'usuarios_ativos': usuarios_ativos,
            'taxa_devolucao': round(taxa_devolucao, 2),
        }
        context['emprestimos'] = emprestimos
        context['livros_populares'] = livros_populares
        context['today'] = datetime.date.today()
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'biblioteca/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Estatísticas principais
        context['stats'] = {
            'total_livros': Livro.objects.count(),
            'total_usuarios': Usuario.objects.filter(is_active=True).count(),
            'emprestimos_ativos': Emprestimo.objects.filter(status='ativa').count(),
            'emprestimos_atrasados': Emprestimo.objects.filter(status='vencido').count(),
        }
        # Livros mais emprestados
        context['livros_populares'] = (
            Livro.objects
            .annotate(total_emprestimos=models.Count('emprestimos'))
            .order_by('-total_emprestimos')[:10]
        )
        return context

class VerificarDisponibilidadeView(TemplateView):
    template_name = 'biblioteca/verificar_disponibilidade.html'

class ExpirarReservasView(AdminRequiredMixin, TemplateView):
    template_name = 'biblioteca/expirar_reservas.html'

# Function-based views
def devolver_livro(request, pk):
    if request.method == 'POST':
        emprestimo = get_object_or_404(Emprestimo, pk=pk)
        emprestimo.devolver()
        messages.success(request, 'Livro devolvido com sucesso!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def renovar_emprestimo(request, pk):
    if request.method == 'POST':
        emprestimo = get_object_or_404(Emprestimo, pk=pk)
        if emprestimo.renovar():
            messages.success(request, 'Empréstimo renovado com sucesso!')
            return JsonResponse({'status': 'success'})
        else:
            messages.error(request, 'Não foi possível renovar o empréstimo.')
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

def livros_disponiveis(request):
    livros = Livro.objects.filter(quantidade_disponivel__gt=0)
    data = [{'id': l.id, 'titulo': l.titulo, 'autor': l.autor.nome} for l in livros]
    return JsonResponse({'livros': data})

def verificar_disponibilidade(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    return JsonResponse({
        'disponivel': livro.is_available(),
        'quantidade_disponivel': livro.quantidade_disponivel,
        'quantidade_total': livro.quantidade
    })