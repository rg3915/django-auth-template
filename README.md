# django-auth-template

Template do [Copier](https://copier.readthedocs.io/) para projetos Django 6 com login por e-mail.

Vídeo: [Copier + Django: login por e-mail em um comando](https://youtu.be/-TBGoqLYYxA)

Passo a passo: [Dicas de Django](https://www.dicas-de-django.com.br/123-copier-django/)

## O que vem pronto

* App `accounts`: usuário sem username, que entra com e-mail (sem diferenciar maiúsculas), com a migração inicial já pronta.
* Cadastro, perfil, login, logout, troca e reset de senha, com templates em português.
* App `core`: `TimeStampedModel`, `UUIDModel`, `ActiveModel`, `base.html` com menu e mensagens, rota `/health/` e e-mail legível no terminal.
* Settings com python-decouple e dj-database-url, `pt-br` e fuso de São Paulo.
* SQLite ou Postgres, à sua escolha.
* 15 testes.

## Como usar

```
uv tool install copier
copier copy --trust gh:rg3915/django-auth-template loja
cd loja
uv run python manage.py createsuperuser
uv run python manage.py test
uv run python manage.py runserver
```

Sem perguntas, com Postgres:

```
copier copy --trust --defaults -d project_name=Blog -d database=postgres gh:rg3915/django-auth-template blog
```

Quando o template ganhar uma versão nova, no projeto gerado (com o git limpo):

```
copier update --trust
```

O `--trust` é necessário porque o template roda tasks depois de gerar o projeto: `git init`, `uv sync`, o script que cria o `.env` e o `migrate` (só com SQLite).
