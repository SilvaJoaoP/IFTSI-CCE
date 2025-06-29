import tkinter as tk
from tkinter import ttk, messagebox
from sistema import CentroDeControle
from modelos.solicitacao import Solicitacao
import math

# --- Paleta de Cores e Fontes para o Tema Espacial ---
COLOR_BACKGROUND = "#1e2a3a"
COLOR_FRAME = "#2a3b4c"
COLOR_TEXT = "#e0e0e0"
COLOR_HIGHLIGHT = "#00ffff"  # Cyan para destaque
COLOR_SUCCESS = "#76ff03"   # Verde limão para sucesso
COLOR_ERROR = "#ff5252"     # Vermelho para erros
FONT_PRIMARY = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_MONO = ("Consolas", 10)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Centro de Controle Espacial")
        self.geometry("1100x700") # Aumentei o tamanho para a nova interface
        self.configure(bg=COLOR_BACKGROUND)

        # Instancia o cérebro do sistema
        self.centro_de_controle = CentroDeControle()
        
        # --- Variáveis de estado para a triagem ---
        self.lista_completa_triagem = []
        self.chamado_selecionado = None
        self.pagina_atual_triagem = 1
        self.itens_por_pagina = 10

        # Configura o estilo global da aplicação
        self.configure_styles()

        # Cria a estrutura de abas
        self.notebook = ttk.Notebook(self, style="TNotebook")
        self.notebook.pack(pady=15, padx=15, fill="both", expand=True)

        # Cria as diferentes abas/painéis
        self.criar_aba_solicitacao()
        self.criar_aba_triagem()
        self.criar_aba_especialista()
        self.criar_aba_estatisticas()
        self.criar_aba_historico()

    def configure_styles(self):
        """Centraliza toda a configuração de estilo da aplicação."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", background=COLOR_BACKGROUND, foreground=COLOR_TEXT, font=FONT_PRIMARY)
        style.map(".", background=[("active", COLOR_FRAME)])

        style.configure("TNotebook", background=COLOR_BACKGROUND, borderwidth=0)
        style.configure("TNotebook.Tab", background=COLOR_FRAME, foreground=COLOR_TEXT, padding=[10, 5], font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", COLOR_HIGHLIGHT), ("active", COLOR_FRAME)], foreground=[("selected", "#000000"), ("active", COLOR_HIGHLIGHT)])

        style.configure("TFrame", background=COLOR_FRAME)
        style.configure("TLabelframe", background=COLOR_FRAME, bordercolor=COLOR_HIGHLIGHT, relief="solid")
        style.configure("TLabelframe.Label", foreground=COLOR_HIGHLIGHT, background=COLOR_FRAME, font=("Segoe UI", 12, "bold"))
        
        style.configure("TButton", foreground="#000000", background=COLOR_HIGHLIGHT, font=("Segoe UI", 10, "bold"), padding=5, borderwidth=0)
        style.map("TButton", background=[("active", COLOR_TEXT), ("!disabled", COLOR_HIGHLIGHT)])
        
        style.configure("TLabel", background=COLOR_FRAME, foreground=COLOR_TEXT, font=FONT_PRIMARY)
        style.configure("TEntry", fieldbackground="#1e2a3a", foreground=COLOR_TEXT, bordercolor=COLOR_HIGHLIGHT, insertcolor=COLOR_TEXT)
        style.configure("TCombobox", fieldbackground="#1e2a3a", foreground=COLOR_TEXT, bordercolor=COLOR_HIGHLIGHT, arrowcolor=COLOR_HIGHLIGHT)
        self.option_add("*TCombobox*Listbox*Background", "#1e2a3a")
        self.option_add("*TCombobox*Listbox*Foreground", COLOR_TEXT)
        
        # Estilo para o Treeview (tabela de chamados)
        style.configure("Treeview", background=COLOR_BACKGROUND, fieldbackground=COLOR_BACKGROUND, foreground=COLOR_TEXT, relief="solid")
        style.configure("Treeview.Heading", background=COLOR_FRAME, foreground=COLOR_HIGHLIGHT, font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview.Heading", background=[("active", COLOR_HIGHLIGHT)])


    def criar_aba(self, nome_aba):
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text=nome_aba, sticky="nsew")
        return frame

    # --- ABA 1: REGISTRAR NOVA SOLICITAÇÃO ---
    def criar_aba_solicitacao(self):
        frame = self.criar_aba("Nova Solicitação")
        
        ttk.Label(frame, text="Registrar Nova Solicitação", font=FONT_TITLE, foreground=COLOR_HIGHLIGHT).pack(pady=(0, 20))
        
        inner_frame = ttk.Frame(frame)
        inner_frame.pack(pady=10, padx=10)

        ttk.Label(inner_frame, text="Prioridade:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.prioridade_var = tk.StringVar(value="NORMAL")
        prioridade_combo = ttk.Combobox(inner_frame, textvariable=self.prioridade_var, values=["EMERGENCIA", "ALTA", "NORMAL"], width=30)
        prioridade_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(inner_frame, text="Descrição Inicial do Problema:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.desc_inicial_text = tk.Text(inner_frame, height=8, width=50, bg=COLOR_BACKGROUND, fg=COLOR_TEXT, font=FONT_PRIMARY, relief="solid", borderwidth=1, insertbackground=COLOR_TEXT)
        self.desc_inicial_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Registrar Solicitação", command=self.registrar_solicitacao, width=30).pack(pady=20)
    
    def registrar_solicitacao(self):
        prioridade = self.prioridade_var.get()
        descricao = self.desc_inicial_text.get("1.0", tk.END).strip()

        if not descricao:
            messagebox.showerror("Erro de Validação", "A descrição não pode estar em branco.")
            return

        try:
            nova_solicitacao = Solicitacao(prioridade, descricao)
            self.centro_de_controle.adicionar_solicitacao(nova_solicitacao)
            messagebox.showinfo("Sucesso", f"Solicitação com prioridade '{prioridade}' registrada com sucesso!")
            self.desc_inicial_text.delete("1.0", tk.END)
            # Atualiza a lista de triagem se ela estiver visível
            if self.notebook.tab(self.notebook.select(), "text") == "Painel de Triagem":
                self.atualizar_lista_triagem()
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    # --- ABA 2: PAINEL DE TRIAGEM (COMPLETAMENTE REDESENHADO) ---
    def criar_aba_triagem(self):
        frame_triagem = self.criar_aba("Painel de Triagem")
        frame_triagem.columnconfigure(0, weight=3) # Coluna da lista
        frame_triagem.columnconfigure(1, weight=2) # Coluna dos detalhes
        frame_triagem.rowconfigure(0, weight=1)

        # --- Frame da Lista de Chamados (Esquerda) ---
        frame_lista = ttk.Frame(frame_triagem)
        frame_lista.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        frame_lista.rowconfigure(1, weight=1)
        frame_lista.columnconfigure(0, weight=1)
        
        # Controles (Atualizar e Paginação)
        controles_frame = ttk.Frame(frame_lista)
        controles_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Button(controles_frame, text="Atualizar", command=self.atualizar_lista_triagem).pack(side="left")
        self.btn_triagem_seguinte = ttk.Button(controles_frame, text="Seguinte >", command=self.ir_pagina_seguinte)
        self.btn_triagem_seguinte.pack(side="right")
        self.lbl_pagina_triagem = ttk.Label(controles_frame, text="Página 1 / 1")
        self.lbl_pagina_triagem.pack(side="right", padx=10)
        self.btn_triagem_anterior = ttk.Button(controles_frame, text="< Anterior", command=self.ir_pagina_anterior)
        self.btn_triagem_anterior.pack(side="right")

        # Tabela (Treeview)
        cols = ("ID", "Prioridade", "Descrição")
        self.tree_triagem = ttk.Treeview(frame_lista, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.tree_triagem.heading(col, text=col)
        self.tree_triagem.column("ID", width=120, anchor="center")
        self.tree_triagem.column("Prioridade", width=100, anchor="center")
        self.tree_triagem.column("Descrição", width=300)
        self.tree_triagem.grid(row=1, column=0, sticky="nsew")
        self.tree_triagem.bind("<<TreeviewSelect>>", self.on_chamado_selecionado)

        # --- Frame de Detalhes do Chamado (Direita) ---
        self.triagem_details_frame = ttk.LabelFrame(frame_triagem, text="Processar Chamado Selecionado")
        self.triagem_details_frame.grid(row=0, column=1, sticky="nsew")

        self.id_chamado_label = ttk.Label(self.triagem_details_frame, text="Nenhum chamado selecionado.", font=("Segoe UI", 10, "italic"))
        self.id_chamado_label.grid(row=0, column=0, columnspan=2, pady=15, padx=10)

        # Campos de entrada
        ttk.Label(self.triagem_details_frame, text="Nome da Nave:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.nome_nave_entry = ttk.Entry(self.triagem_details_frame, width=40)
        self.nome_nave_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        # ... (outros campos)
        ttk.Label(self.triagem_details_frame, text="Código da Missão:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.codigo_missao_entry = ttk.Entry(self.triagem_details_frame, width=40)
        self.codigo_missao_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        ttk.Label(self.triagem_details_frame, text="Setor Orbital:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.setor_orbital_entry = ttk.Entry(self.triagem_details_frame, width=40)
        self.setor_orbital_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        ttk.Label(self.triagem_details_frame, text="Descrição Detalhada:").grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        self.desc_completa_text = tk.Text(self.triagem_details_frame, height=5, width=40, bg=COLOR_BACKGROUND, fg=COLOR_TEXT, relief="solid", borderwidth=1, insertbackground=COLOR_TEXT)
        self.desc_completa_text.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        self.tripulacao_var = tk.BooleanVar()
        ttk.Checkbutton(self.triagem_details_frame, text="Há tripulação humana envolvida", variable=self.tripulacao_var).grid(row=5, column=1, sticky="w", padx=10, pady=10)
        ttk.Label(self.triagem_details_frame, text="Encaminhar para:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.especialista_triagem_var = tk.StringVar()
        self.especialista_combo = ttk.Combobox(self.triagem_details_frame, textvariable=self.especialista_triagem_var, values=list(self.centro_de_controle.filas_especialistas.keys()))
        self.especialista_combo.grid(row=6, column=1, sticky="ew", padx=10, pady=5)
        
        ttk.Button(self.triagem_details_frame, text="Processar e Enviar para Especialista", command=self.processar_chamado_selecionado).grid(row=7, column=1, sticky="e", pady=20, padx=10)
        
        frame_triagem.bind("<Visibility>", lambda e: self.atualizar_lista_triagem())
        self.limpar_painel_processamento() # Garante o estado inicial correto

    def atualizar_lista_triagem(self):
        """Busca os dados mais recentes e atualiza a lista e a paginação."""
        self.lista_completa_triagem = self.centro_de_controle.get_todas_solicitacoes_para_triagem()
        self.pagina_atual_triagem = 1
        self.limpar_painel_processamento()
        self.exibir_pagina_triagem()

    def exibir_pagina_triagem(self):
        """Limpa a tabela e exibe apenas os itens da página atual."""
        for i in self.tree_triagem.get_children():
            self.tree_triagem.delete(i)
        
        total_paginas = math.ceil(len(self.lista_completa_triagem) / self.itens_por_pagina)
        total_paginas = max(1, total_paginas) # Garante pelo menos 1 página
        self.lbl_pagina_triagem.config(text=f"Página {self.pagina_atual_triagem} / {total_paginas}")

        inicio = (self.pagina_atual_triagem - 1) * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        
        for chamado in self.lista_completa_triagem[inicio:fim]:
            self.tree_triagem.insert("", "end", iid=chamado.id, values=(
                str(chamado.id)[:8], 
                chamado.prioridade, 
                chamado.descricao_ocorrido[:40] + '...'
            ))

        self.btn_triagem_anterior.config(state="normal" if self.pagina_atual_triagem > 1 else "disabled")
        self.btn_triagem_seguinte.config(state="normal" if self.pagina_atual_triagem < total_paginas else "disabled")

    def ir_pagina_anterior(self):
        if self.pagina_atual_triagem > 1:
            self.pagina_atual_triagem -= 1
            self.exibir_pagina_triagem()

    def ir_pagina_seguinte(self):
        total_paginas = math.ceil(len(self.lista_completa_triagem) / self.itens_por_pagina)
        if self.pagina_atual_triagem < total_paginas:
            self.pagina_atual_triagem += 1
            self.exibir_pagina_triagem()

    def on_chamado_selecionado(self, event):
        """Ativado quando um item da tabela é selecionado."""
        selecao = self.tree_triagem.focus()
        if not selecao: return
        
        # Encontra o objeto solicitação correspondente ao ID selecionado
        self.chamado_selecionado = next((c for c in self.lista_completa_triagem if str(c.id) == selecao), None)
        
        if self.chamado_selecionado:
            for child in self.triagem_details_frame.winfo_children():
                if isinstance(child, (ttk.Entry, tk.Text, ttk.Combobox, ttk.Checkbutton, ttk.Button)):
                    child.config(state="normal")
            
            self.id_chamado_label.config(text=f"ID: {str(self.chamado_selecionado.id)[:8]} | Prioridade: {self.chamado_selecionado.prioridade}")
            self.desc_completa_text.delete("1.0", tk.END)
            self.desc_completa_text.insert("1.0", self.chamado_selecionado.descricao_ocorrido)
    
    def limpar_painel_processamento(self):
        """Desativa e limpa o painel de detalhes."""
        self.chamado_selecionado = None
        self.tree_triagem.selection_remove(self.tree_triagem.selection())
        
        self.id_chamado_label.config(text="Nenhum chamado selecionado.")
        self.nome_nave_entry.delete(0, tk.END)
        self.codigo_missao_entry.delete(0, tk.END)
        self.setor_orbital_entry.delete(0, tk.END)
        self.desc_completa_text.delete("1.0", tk.END)
        self.especialista_triagem_var.set("")
        self.tripulacao_var.set(False)

        for child in self.triagem_details_frame.winfo_children():
            if isinstance(child, (ttk.Entry, tk.Text, ttk.Combobox, ttk.Checkbutton, ttk.Button)):
                child.config(state="disabled")

    def processar_chamado_selecionado(self):
        if not self.chamado_selecionado:
            messagebox.showerror("Erro", "Nenhum chamado foi selecionado para processar.")
            return

        nome_nave = self.nome_nave_entry.get().strip()
        codigo_missao = self.codigo_missao_entry.get().strip()
        setor_orbital = self.setor_orbital_entry.get().strip()
        desc_completa = self.desc_completa_text.get("1.0", tk.END).strip()
        tripulacao = self.tripulacao_var.get()
        especialidade = self.especialista_triagem_var.get()
        operador = "Operador-GUI"

        if not all([nome_nave, codigo_missao, setor_orbital, desc_completa, especialidade]):
            messagebox.showerror("Erro de Validação", "Todos os campos devem ser preenchidos.")
            return
        
        # 1. Registrar os dados de triagem no objeto
        self.chamado_selecionado.registrar_triagem(nome_nave, codigo_missao, setor_orbital, desc_completa, tripulacao, operador)
        
        # 2. Remover o chamado das filas de triagem originais
        removido = self.centro_de_controle.remover_solicitacao_da_triagem(self.chamado_selecionado)
        if not removido:
            messagebox.showerror("Erro Crítico", "Não foi possível encontrar e remover o chamado da fila original. A operação foi cancelada.")
            return

        # 3. Enviar para a fila do especialista e contabilizar
        self.centro_de_controle.enviar_para_especialista(self.chamado_selecionado, especialidade)
        self.centro_de_controle.contabilizar_triagem(operador)

        messagebox.showinfo("Sucesso", f"Chamado para a nave '{nome_nave}' processado e enviado para {especialidade}.")
        self.atualizar_lista_triagem()

    # --- ABA 3: PAINEL DO ESPECIALISTA ---
    def criar_aba_especialista(self):
        frame = self.criar_aba("Painel do Especialista")
        
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(top_frame, text="Especialidade:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 10))
        self.especialidade_atendimento_var = tk.StringVar()
        especialista_atendimento_combo = ttk.Combobox(top_frame, textvariable=self.especialidade_atendimento_var, values=list(self.centro_de_controle.filas_especialistas.keys()), width=30)
        especialista_atendimento_combo.pack(side="left", fill="x", expand=True)
        especialista_atendimento_combo.bind("<<ComboboxSelected>>", self.atualizar_fila_especialista)

        self.fila_especialista_frame = ttk.LabelFrame(frame, text="Fila de Atendimento")
        self.fila_especialista_frame.pack(fill="both", expand=True, pady=10)

        self.fila_especialista_text = tk.Text(self.fila_especialista_frame, height=15, width=80, state="disabled", bg=COLOR_BACKGROUND, fg=COLOR_TEXT, relief="solid", borderwidth=1, font=FONT_PRIMARY)
        self.fila_especialista_text.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Atender Próximo Chamado da Fila", command=self.atender_chamado_especialista).pack(pady=10)

    def atualizar_fila_especialista(self, event=None):
        especialidade = self.especialidade_atendimento_var.get()
        if not especialidade: return

        self.fila_especialista_frame.config(text=f"Fila de Atendimento - {especialidade}")
        self.fila_especialista_text.config(state="normal")
        self.fila_especialista_text.delete("1.0", tk.END)

        fila = self.centro_de_controle.filas_especialistas[especialidade]
        if fila.is_empty():
            self.fila_especialista_text.insert(tk.END, "Fila de atendimento vazia.")
        else:
            for chamado in fila:
                 self.fila_especialista_text.insert(tk.END, f"Nave: {chamado.nome_nave} | Prioridade: {chamado.prioridade}\n", "bold")
                 self.fila_especialista_text.insert(tk.END, f"  ID Missão: {chamado.codigo_missao} | Setor: {chamado.setor_orbital}\n")
                 self.fila_especialista_text.insert(tk.END, f"  Descrição: {chamado.descricao_ocorrido}\n{'-'*60}\n")

        self.fila_especialista_text.config(state="disabled")

    def atender_chamado_especialista(self):
        especialidade = self.especialidade_atendimento_var.get()
        if not especialidade:
            messagebox.showerror("Ação Inválida", "Selecione uma especialidade primeiro.")
            return

        fila_especialista = self.centro_de_controle.filas_especialistas[especialidade]
        if fila_especialista.is_empty():
            messagebox.showinfo("Fila Vazia", f"Não há chamados na fila de {especialidade}.")
            return
            
        chamado_atendido = fila_especialista.remove_first()
        chamado_atendido.status = "FINALIZADA"
        self.centro_de_controle.arquivar_solicitacao_na_nave(chamado_atendido)
        
        messagebox.showinfo("Sucesso", f"Chamado da nave '{chamado_atendido.nome_nave}' foi finalizado!")
        self.atualizar_fila_especialista()

    # --- ABA 4: ESTATÍSTICAS ---
    def criar_aba_estatisticas(self):
        self.frame_stats = self.criar_aba("Estatísticas e Relatórios")
        
        ttk.Button(self.frame_stats, text="Atualizar Relatórios", command=self.atualizar_estatisticas).pack(pady=(0,15))

        self.stats_text = tk.Text(self.frame_stats, height=20, width=80, font=FONT_MONO, state="disabled", bg=COLOR_BACKGROUND, fg=COLOR_TEXT, relief="solid", borderwidth=1)
        self.stats_text.pack(fill="both", expand=True)
        
        self.frame_stats.bind("<Visibility>", lambda event: self.atualizar_estatisticas())

    def atualizar_estatisticas(self):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)

        cc = self.centro_de_controle
        report = []
        report.append("--- RELATÓRIO DE SESSÃO DO CENTRO DE CONTROLE ---")
        report.append("="*55)
        report.append(f"Total de Solicitações Criadas......: {cc.stats_solicitacoes_criadas}")
        report.append("-"*55)
        
        report.append("\n[ATENDIMENTOS FINALIZADOS POR PRIORIDADE]")
        for p, t in cc.stats_atendimentos_por_prioridade.items():
            report.append(f"  - {p.title():<12}: {t}")
        report.append("-"*55)

        report.append("\n[ATENDIMENTOS FINALIZADOS POR ESPECIALISTA]")
        for e, t in cc.stats_atendimentos_por_especialista.items():
            report.append(f"  - {e:<15}: {t}")
        report.append("-"*55)

        report.append("\n[TRIAGENS PROCESSADAS POR OPERADOR]")
        for o, t in cc.stats_triagens_por_operador.items():
            report.append(f"  - {o:<15}: {t}")
        report.append("-"*55)

        nave, num = cc.get_nave_com_mais_chamados()
        report.append("\n[NAVE COM MAIOR NÚMERO DE CHAMADOS]")
        report.append(f"  - Nave: {nave}")
        report.append(f"  - Total de Chamados: {num}")
        report.append("="*55)
        
        self.stats_text.insert("1.0", "\n".join(report))
        self.stats_text.config(state="disabled")
        
    # --- ABA 5: HISTÓRICO DE NAVE ---
    def criar_aba_historico(self):
        frame = self.criar_aba("Histórico de Nave")
        
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(top_frame, text="Nome da Nave:").pack(side="left", padx=(0,10))
        self.nave_hist_entry = ttk.Entry(top_frame, width=40)
        self.nave_hist_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(top_frame, text="Consultar Histórico", command=self.consultar_historico).pack(side="left", padx=(10,0))
        
        self.hist_text = tk.Text(frame, height=15, width=80, state="disabled", bg=COLOR_BACKGROUND, fg=COLOR_TEXT, relief="solid", borderwidth=1, font=FONT_PRIMARY)
        self.hist_text.pack(pady=10, fill="both", expand=True)

    def consultar_historico(self):
        nome_nave = self.nave_hist_entry.get().strip()
        if not nome_nave:
            messagebox.showerror("Erro de Validação", "Digite o nome de uma nave.")
            return
            
        self.hist_text.config(state="normal")
        self.hist_text.delete("1.0", tk.END)

        nave = self.centro_de_controle.consultar_historico_nave(nome_nave)
        if nave and not nave.historico_solicitacoes.is_empty():
            self.hist_text.insert(tk.END, f"--- Histórico para a Nave: {nave.nome} ---\n\n")
            for chamado in nave.historico_solicitacoes:
                self.hist_text.insert(tk.END, f"ID: {str(chamado.id)[:8]} | Data: {chamado.timestamp_criacao.strftime('%d/%m/%Y %H:%M')}\n", "bold")
                self.hist_text.insert(tk.END, f"  Especialista: {chamado.especialista_responsavel} | Prioridade: {chamado.prioridade}\n")
                self.hist_text.insert(tk.END, f"  Descrição: {chamado.descricao_ocorrido}\n{'-'*70}\n")
        else:
            self.hist_text.insert(tk.END, f"Nenhum histórico encontrado para a nave '{nome_nave}'.")
            
        self.hist_text.config(state="disabled")

