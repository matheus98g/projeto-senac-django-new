from django.core.management.base import BaseCommand
from biblioteca.models import Livro, Emprestimo, Reserva
from django.db.models import Q


class Command(BaseCommand):
    help = 'Corrige a quantidade disponível de todos os livros baseado nos empréstimos e reservas ativas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra o que seria alterado sem fazer as mudanças',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Modo DRY-RUN - Nenhuma alteração será feita'))
        
        livros_corrigidos = 0
        total_livros = Livro.objects.count()
        
        self.stdout.write(f'Analisando {total_livros} livros...')
        
        for livro in Livro.objects.all():
            # Calcular quantidade realmente disponível
            emprestimos_ativos = Emprestimo.objects.filter(
                livro=livro,
                status='ativo'
            ).count()
            
            reservas_ativas = Reserva.objects.filter(
                livro=livro,
                status='ativa'
            ).count()
            
            # Quantidade que deveria estar disponível
            quantidade_esperada = livro.quantidade - emprestimos_ativos - reservas_ativas
            
            # Garantir que não seja negativa
            if quantidade_esperada < 0:
                quantidade_esperada = 0
            
            if livro.quantidade_disponivel != quantidade_esperada:
                self.stdout.write(
                    f'Livro "{livro.titulo}": '
                    f'Quantidade atual: {livro.quantidade_disponivel}, '
                    f'Quantidade esperada: {quantidade_esperada} '
                    f'(Total: {livro.quantidade}, Empréstimos: {emprestimos_ativos}, Reservas: {reservas_ativas})'
                )
                
                if not dry_run:
                    livro.quantidade_disponivel = quantidade_esperada
                    livro.save()
                    livros_corrigidos += 1
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'DRY-RUN: {livros_corrigidos} livros seriam corrigidos'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'{livros_corrigidos} livros foram corrigidos com sucesso!'
                )
            )
