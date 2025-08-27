# Sistema de Biblioteca SENAC

Sistema de gerenciamento de biblioteca desenvolvido em Django para o SENAC.

## Funcionalidades

- 📚 Cadastro e gerenciamento de livros
- 👥 Cadastro e gerenciamento de usuários
- 📋 Sistema de reservas de livros
- 🔍 Busca avançada de livros
- 📊 Dashboard administrativo
- 🔐 Sistema de autenticação
- 👨‍💼 Diferentes níveis de usuário (Admin/Aluno)

## Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Automática (Windows)

1. Execute o arquivo `setup.bat` como administrador
2. Aguarde a instalação e configuração automática
3. O sistema criará um usuário administrador padrão

### Instalação Manual

1. Clone ou baixe o projeto
2. Navegue até o diretório do projeto:

   ```bash
   cd bibliotecasenac
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute as migrações:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Configure dados iniciais:

   ```bash
   python manage.py setup_initial_data
   ```

6. Colete arquivos estáticos:
   ```bash
   python manage.py collectstatic
   ```

## Executando o Sistema

1. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

2. Acesse o sistema no navegador:
   - **URL:** http://127.0.0.1:8000/
   - **Admin Django:** http://127.0.0.1:8000/admin/

## Credenciais Padrão

- **Usuário:** admin
- **Senha:** admin123

## Estrutura do Projeto

```
bibliotecasenac/
├── biblioteca/                 # App principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views/Controllers
│   ├── urls.py                # Roteamento de URLs
│   ├── forms.py               # Formulários
│   ├── admin.py               # Interface administrativa
│   ├── templates/             # Templates HTML
│   └── management/            # Comandos personalizados
├── bibliotecasenac/           # Configurações do projeto
│   ├── settings.py            # Configurações Django
│   └── urls.py                # URLs principais
├── static/                    # Arquivos estáticos (CSS, JS)
├── requirements.txt           # Dependências
└── manage.py                  # Script de gerenciamento Django
```

## Modelos de Dados

### Usuario

- Extensão do modelo User do Django
- Tipos: Aluno, Administrador
- Campos: username, email, nome, tipo

### Livro

- Título, autor, gênero
- Quantidade total e disponível
- Sistema de disponibilidade

### Autor

- Nome e data de cadastro
- Relacionamento com livros

### Reserva

- Usuário, livro, status
- Controle de expiração
- Validações de negócio

### Empréstimo

- Sistema de empréstimo com datas
- Controle de devoluções
- Sistema de renovações

## Funcionalidades por Tipo de Usuário

### Administrador

- Gerenciar todos os livros, autores e usuários
- Visualizar relatórios e estatísticas
- Controlar reservas e empréstimos
- Acesso ao painel administrativo

### Aluno

- Visualizar catálogo de livros
- Fazer reservas (máximo 3 simultâneas)
- Gerenciar suas próprias reservas
- Visualizar histórico

## APIs Disponíveis

- `GET /api/livros/disponibilidade/<id>/` - Verifica disponibilidade
- `POST /api/reservas/expirar/` - Expira reservas antigas

## Desenvolvimento

### Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar testes
python manage.py test

# Shell do Django
python manage.py shell
```

### Estrutura de Templates

- `base.html` - Template base (não implementado ainda)
- `home.html` - Página inicial
- `livro_*.html` - Templates para livros
- `usuario_*.html` - Templates para usuários
- `reserva_*.html` - Templates para reservas

## Problemas Comuns

### Erro de Migração

```bash
python manage.py migrate --fake-initial
```

### Erro de Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Banco de Dados Corrompido

```bash
# Deletar db.sqlite3 e executar
python manage.py migrate
python manage.py setup_initial_data
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é desenvolvido para fins educacionais no SENAC.

## Suporte

Para suporte e dúvidas, entre em contato com a equipe de desenvolvimento.

---

**Sistema de Biblioteca SENAC** - Versão 1.0
