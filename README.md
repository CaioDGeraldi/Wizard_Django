# Django Setup Wizard ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)<br>
O Django Setup Wizard é uma ferramenta de automação de ambiente desenvolvida em Python. O objetivo deste software é simplificar a       inicialização de projetos Django, automatizando tarefas repetitivas de terminal através de uma interface gráfica intuitiva.

O assistente gerencia a criação de diretórios, configuração de ambientes isolados (Virtual Environments) e a instalação de dependências estruturais.

## Funcionalidades Principais
* Interface Grafica (GUI): Desenvolvida com a biblioteca CustomTkinter, oferecendo suporte a temas claros e escuros do sistema operacional.

* Isolamento de Ambiente: Criação automática de Virtual Env (venv) para evitar conflitos de bibliotecas no sistema global.

* Gerenciamento de Processos: Execução independente de comandos de terminal com monitoramento de status em tempo real.

* Barra de Progresso: Feedback visual constante sobre o estágio da instalação (Venv, Pip, Django Admin).

* Tratamento de Exceções: Sistema de captura de erros que interrompe a execução e informa o usuário em caso de falhas de rede ou permissão.

## Requisitos de Sistema
Para o correto funcionamento do assistente e dos comandos que ele executa, os seguintes itens devem estar instalados na máquina hospedeira:

* Python 3.x: O interpretador deve estar configurado no PATH do sistema.

* Pip: Gerenciador de pacotes para instalação do Django e CustomTkinter (normalemente já vem instalado com o Python).

* Acesso a Internet: Necessário para o download dos pacotes via pip.

## Estrutura do Projeto
O assistente segue o seguinte fluxo de operações:

* Entrada: Coleta o nome do projeto via interface.

* Diretório: Cria a pasta raiz utilizando o módulo OS.

* Ambiente: Executa python -m venv venv.

* seia de natal

* Dependências: Ativa o ambiente e executa pip install django.

* Bootstrap: Executa django-admin startproject para gerar a estrutura inicial do projeto.
---
# Feito por [CaioDGeraldi](https://caiodgeraldi.github.io/)
