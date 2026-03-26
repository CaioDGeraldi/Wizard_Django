import os
import subprocess
import re
import customtkinter as ctk
from tkinter import messagebox

# Configurações de interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class DjangoWizard(ctk.CTk): 
    def __init__(self):
        super().__init__()
        
        self.title("Django Setup Wizard - CaioDGeraldi")
        self.geometry("500x480")

        # Elementos da Interface
        self.label_titulo = ctk.CTkLabel(self, text="Assistente Django", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=20)

        self.label_instrucao = ctk.CTkLabel(self, text="Digite o nome do seu projeto:")
        self.label_instrucao.pack(pady=5)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Ex: meu_projeto", width=300)
        self.entry_nome.pack(pady=10)

        self.btn_instalar = ctk.CTkButton(self, text="Gerar Projeto", command=self.iniciar_setup)
        self.btn_instalar.pack(pady=20)

        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.set(0)
        self.progress.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Pronto para começar", font=("Roboto", 12))
        self.status_label.pack(pady=5)

    def executar_comando(self, comando, mensagem):
        self.status_label.configure(text=mensagem)
        self.update()
        processo = subprocess.run(comando, shell=True, capture_output=True, text=True)
        return processo.returncode == 0

    def configurar_arquivos(self):
        caminho_settings = os.path.join(os.getcwd(), "setup", "settings.py")
        caminho_env = os.path.join(os.getcwd(), ".env")
        caminho_gitignore = os.path.join(os.getcwd(), ".gitignore")
        
        if not os.path.exists(caminho_settings):
            return False

        linhas_modificadas = []
        secret_key_valor = ""
        
        try:
            # 1. Processando o settings.py
            with open(caminho_settings, 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            for linha in linhas:
                # Captura a Secret Key original via Regex (seguro contra caracteres especiais)
                match = re.search(r"SECRET_KEY\s*=\s*['\"]([^'\"]+)['\"]", linha)
                if match:
                    secret_key_valor = match.group(1)
                    linhas_modificadas.append("SECRET_KEY = str(os.getenv('SECRET_KEY'))\n")
                elif linha.strip().startswith("LANGUAGE_CODE ="):
                    linhas_modificadas.append("LANGUAGE_CODE = 'pt-br'\n")
                elif linha.strip().startswith("TIME_ZONE ="):
                    linhas_modificadas.append("TIME_ZONE = 'America/Sao_Paulo'\n")
                else:
                    linhas_modificadas.append(linha)

            # Adiciona imports necessários no topo
            imports = [
                "import os\n",
                "from dotenv import load_dotenv\n",
                "load_dotenv()\n",
                "\n"
            ]

            with open(caminho_settings, 'w', encoding='utf-8') as f:
                f.writelines(imports + linhas_modificadas)

            # 2. Criando o arquivo .env
            if secret_key_valor:
                with open(caminho_env, 'w', encoding='utf-8') as env_f:
                    env_f.write(f"SECRET_KEY={secret_key_valor}\n")
            
            # 3. Criando o .gitignore
            gitignore_content = (
                "*.log\n*.pot\n*.pyc\n__pycache__/\n"
                "db.sqlite3\nmedia/\nlocal_settings.py\n"
                ".env\n.venv\nvenv/\nENV/\n"
                "*.sublime-project\n*.sublime-workspace\n"
                ".vscode/\n.idea/\n"
            )
            with open(caminho_gitignore, 'w', encoding='utf-8') as git_f:
                git_f.write(gitignore_content)
            
            return True
        except Exception as e:
            print(f"Erro na configuração: {e}")
            return False

    def iniciar_setup(self):
        nome_projeto = self.entry_nome.get().strip()
        
        if not nome_projeto:
            messagebox.showwarning("Atenção", "Por favor, digite um nome para o projeto.")
            return

        self.btn_instalar.configure(state="disabled")
        
        try:
            # Etapa 1: Estrutura de Pastas
            os.makedirs(nome_projeto, exist_ok=True)
            os.chdir(nome_projeto)
            self.progress.set(0.1)

            # Etapa 2: Ambiente Virtual
            if self.executar_comando("python -m venv venv", "Criando Ambiente Virtual (VENV)..."):
                self.progress.set(0.3)
            
            # Etapa 3: Instalação do Django
            cmd_django = r"venv\Scripts\activate && pip install django"
            if self.executar_comando(cmd_django, "Instalando Django..."):
                self.progress.set(0.5)

            # Etapa 4: DotEnv e Requirements
            cmd_extras = r"venv\Scripts\activate && pip install python-dotenv && pip freeze > requirements.txt"
            if self.executar_comando(cmd_extras, "Instalando DotEnv e gerando requirements.txt..."):
                self.progress.set(0.7)

            # Etapa 5: Iniciar Projeto Django
            cmd_init = r"venv\Scripts\activate && django-admin startproject setup ."
            if self.executar_comando(cmd_init, "Gerando arquivos do Django..."):
                self.progress.set(0.85)

                # Etapa 6: Configurações de Código (.env, .gitignore, tradução)
                self.status_label.configure(text="Finalizando configurações internas...")
                self.update()
                
                if self.configurar_arquivos():
                    self.progress.set(1.0)
                    messagebox.showinfo("Sucesso!", f"Projeto '{nome_projeto}' configurado com sucesso!")
                    os.startfile(".") 
                    self.destroy()
                else:
                    messagebox.showerror("Erro", "O projeto foi criado, mas houve erro ao editar os arquivos.")

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Ocorreu um problema: {str(e)}")
            self.btn_instalar.configure(state="normal")

if __name__ == "__main__":
    app = DjangoWizard()
    app.mainloop()