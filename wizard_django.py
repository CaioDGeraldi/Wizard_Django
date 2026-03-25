import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox

#Definição de tema do sistema.
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class DjangoWizard(ctk.CTk): 
    def __init__(self):
        super().__init__()
        
        #Definindo 'Titulo' e 'Tamanho' da janela.
        self.title("Django Setup Wizard - CaioDGeraldi")
        self.geometry("500x400")

        #Header da janela.
        self.label_titulo = ctk.CTkLabel(self, text="Assistente de Instalação Django", font=("Roboto", 24))
        self.label_titulo.pack(pady=20)

        #Label para o nome do projeto.
        self.label_instrucao = ctk.CTkLabel(self, text="Digite o nome do seu projeto:")
        self.label_instrucao.pack(pady=5)

        #Entrada para o nome do projeto.
        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Ex: Master", width=300)
        self.entry_nome.pack(pady=10)

        #Botão iniciar configuração.
        self.btn_instalar = ctk.CTkButton(self, text="Iniciar Configuração", command=self.iniciar_setup)
        self.btn_instalar.pack(pady=20)

        #Barra de progresso.
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.set(0)
        self.progress.pack(pady=10)

        #Warning enquanto não começa o sistema.
        self.status_label = ctk.CTkLabel(self, text="Aguardando início...", font=("Roboto", 12))
        self.status_label.pack(pady=5)

    #Subprocesso para rodar os comandos fora do campo de visão do usuário.
    def executar_comando(self, comando, mensagem):
        self.status_label.configure(text=mensagem)
        self.update()
        processo = subprocess.run(comando, shell=True, capture_output=True, text=True)
        return processo.returncode == 0

    #Configurando o arquivo 'settings.py'.
    def configurar_settings(self):
        caminho_settings = os.path.join("setup", "settings.py")
        
        if not os.path.exists(caminho_settings):
            return False

        linhas_modificadas = []
        with open(caminho_settings, 'r', encoding='utf-8') as f:
            for linha in f:
                # Altera o LANGUAGE_CODE para Português do Brasil
                if linha.strip().startswith("LANGUAGE_CODE ="):
                    linhas_modificadas.append("LANGUAGE_CODE = 'pt-br'\n")
                # Altera o TIME_ZONE para o de Brasília
                elif linha.strip().startswith("TIME_ZONE ="):
                    linhas_modificadas.append("TIME_ZONE = 'America/Sao_Paulo'\n")
                else:
                    linhas_modificadas.append(linha)

        with open(caminho_settings, 'w', encoding='utf-8') as f:
            f.writelines(linhas_modificadas)
        return True

    #Inicio da configuração do projeto em si.
    def iniciar_setup(self):
        nome_projeto = self.entry_nome.get()
        
        if not nome_projeto: #Warning caso não exista um nome de projeto definido.
            messagebox.showwarning("Atenção", "Por favor, digite um nome para o projeto.")
            return

        self.btn_instalar.configure(state="disabled") #Desativando o botão de iniciar configuração para evitar cliques duplos.
        
        try: #Fluxo de comandos para criação da pasta 'Master' do projeto, criação de uma VirtualEnv, e instalação de Django.
            os.makedirs(nome_projeto, exist_ok=True)
            os.chdir(nome_projeto)
            self.progress.set(0.20)

            if self.executar_comando("python -m venv venv", "Criando Ambiente Virtual..."):
                self.progress.set(0.40)
            
            cmd_django = r"venv\Scripts\activate && pip install django"
            if self.executar_comando(cmd_django, "Instalando Django (isso pode demorar)..."):
                self.progress.set(0.60)

            cmd_init = r"venv\Scripts\activate && django-admin startproject setup ."
            if self.executar_comando(cmd_init, "Finalizando estrutura..."):
                self.progress.set(0.80)
                messagebox.showinfo("Sucesso!", f"Projeto '{nome_projeto}' configurado com sucesso!")

            self.status_label.configure(text="Traduzindo configurações para (pt-br)")
            self.update()

            self.status_label.configure(text="Traduzindo configurações (pt-br)...")
            self.update()
            if self.configurar_settings():
                self.progress.set(1.0)
                messagebox.showinfo("Sucesso!", f"Projeto '{nome_projeto}' configurado e traduzido!")
                os.startfile(".") #Abre o navegador de arquivos na pasta 'Master' do projeto.
                self.destroy() #Fecha o Wizard.

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um problema: {str(e)}") #Caso algum erro ocorra durante a instalação e configuração.
            self.btn_instalar.configure(state="normal") #Volta o botão para o estado normal (clicavel).

if __name__ == "__main__": #Loop para rodar o projeto até que o mesmo seja terminado.
    app = DjangoWizard()
    app.mainloop()