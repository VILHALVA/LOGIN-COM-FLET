import flet as ft
import sqlite3
import os
import hashlib

def obter_caminho_db():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "DATABASE.db")

def criar_banco_de_dados():
    caminho_db = obter_caminho_db()
    if not os.path.exists(caminho_db):
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT NOT NULL,
                            senha TEXT NOT NULL
                          )''')
        conn.commit()
        conn.close()

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def processar_usuario(usuario, senha_usuario, acao, exibir_mensagem):
    caminho_db = obter_caminho_db()
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    senha_criptografada = criptografar_senha(senha_usuario)

    if acao == "cadastrar":
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if not cursor.fetchone():
            cursor.execute('''CREATE TABLE usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL,
                                senha TEXT NOT NULL
                              )''')
            conn.commit()

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            exibir_mensagem("Este usuário já está cadastrado!")
            conn.close()
            return
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_criptografada))
        conn.commit()
        exibir_mensagem("Cadastro realizado com sucesso!")
    
    elif acao == "login":
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_criptografada))
        if cursor.fetchone():
            exibir_mensagem(f"Bem-vindo, {usuario}!")
        else:
            exibir_mensagem("Usuário ou senha incorretos.")
    
    conn.close()

def main(page: ft.Page):
    page.title = "LOGIN COM FLET"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    criar_banco_de_dados()

    def exibir_mensagem(msg):
        page.dialog = ft.AlertDialog(title=ft.Text(msg))
        page.dialog.open = True
        page.update()

    usuario = ft.TextField(label="USUÁRIO", width=300)
    senha = ft.TextField(label="SENHA", width=300, password=True, can_reveal_password=True)

    def cadastrar(e):
        usuario_input = usuario.value
        senha_input = senha.value
        if not usuario_input or not senha_input:
            exibir_mensagem("Por favor, preencha ambos os campos!")
        else:
            processar_usuario(usuario_input, senha_input, "cadastrar", exibir_mensagem)

    def login(e):
        usuario_input = usuario.value
        senha_input = senha.value
        if not usuario_input or not senha_input:
            exibir_mensagem("Por favor, preencha ambos os campos!")
        else:
            processar_usuario(usuario_input, senha_input, "login", exibir_mensagem)

    titulo = ft.Text("CADASTRO E LOGIN", size=24, weight="bold")
    botao_cadastrar = ft.ElevatedButton("CADASTRAR", on_click=cadastrar, width=200)
    botao_login = ft.ElevatedButton("LOGIN", on_click=login, width=200)

    page.add(
        ft.Column(
            [
                titulo,
                usuario,
                senha,
                ft.Row([botao_cadastrar, botao_login], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
