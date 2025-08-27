from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from biblioteca.models import Autor, Livro, Categoria

User = get_user_model()


class Command(BaseCommand):
    help = 'Configura dados iniciais para o sistema de biblioteca'

    def handle(self, *args, **options):
        self.stdout.write('Configurando dados iniciais...')
        
        # Criar administrador padrão se não existir
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@biblioteca.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                tipo_usuario='admin',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Usuário administrador criado: {admin_user.username}')
            )
        
        # Criar algumas categorias básicas
        categorias = [
            'Literatura Brasileira',
            'Literatura Estrangeira',
            'Ficção Científica',
            'Romance',
            'Suspense',
            'Educacional',
            'Técnico',
            'Biografias'
        ]
        
        for nome_categoria in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nome=nome_categoria,
                defaults={'descricao': f'Categoria de {nome_categoria}'}
            )
            if created:
                self.stdout.write(f'Categoria criada: {categoria.nome}')
        
        # Criar alguns autores de exemplo
        autores_exemplo = [
            'Machado de Assis',
            'Clarice Lispector',
            'José Saramago',
            'Gabriel García Márquez',
            'J.K. Rowling',
            'Agatha Christie',
            'Stephen King',
            'Isaac Asimov'
        ]
        
        for nome_autor in autores_exemplo:
            autor, created = Autor.objects.get_or_create(nome=nome_autor)
            if created:
                self.stdout.write(f'Autor criado: {autor.nome}')
        
        # Criar alguns livros de exemplo
        livros_exemplo = [
            {
                'titulo': 'Dom Casmurro',
                'autor': 'Machado de Assis',
                'genero': 'romance',
                'quantidade': 3
            },
            {
                'titulo': 'A Hora da Estrela',
                'autor': 'Clarice Lispector',
                'genero': 'romance',
                'quantidade': 2
            },
            {
                'titulo': 'O Nome da Rosa',
                'autor': 'José Saramago',
                'genero': 'ficcao',
                'quantidade': 2
            },
            {
                'titulo': 'Cem Anos de Solidão',
                'autor': 'Gabriel García Márquez',
                'genero': 'ficcao',
                'quantidade': 4
            },
            {
                'titulo': 'Harry Potter e a Pedra Filosofal',
                'autor': 'J.K. Rowling',
                'genero': 'fantasia',
                'quantidade': 5
            }
        ]
        
        for livro_data in livros_exemplo:
            try:
                autor = Autor.objects.get(nome=livro_data['autor'])
                livro, created = Livro.objects.get_or_create(
                    titulo=livro_data['titulo'],
                    autor=autor,
                    defaults={
                        'genero': livro_data['genero'],
                        'quantidade': livro_data['quantidade'],
                        'quantidade_disponivel': livro_data['quantidade']
                    }
                )
                if created:
                    self.stdout.write(f'Livro criado: {livro.titulo}')
            except Autor.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Autor não encontrado: {livro_data["autor"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Configuração inicial concluída!')
        )
        self.stdout.write('Usuário admin criado com senha: admin123')
        self.stdout.write('Você pode fazer login em: /admin/ ou /login/')
