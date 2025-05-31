import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import json
import logging
import os # Para obter o diretorio do script

class AplicacaoTriagem:
    """
    Classe principal para a aplicacao de triagem de sintomas.
    Gerencia a interface grafica, a logica da arvore de decisao e os dados do usuario.
    """
    def __init__(self, janela_tk):
        self.janela_principal = janela_tk
        self.janela_principal.title("Triagem de Sintomas")
        self.janela_principal.geometry("700x650")
        self.janela_principal.configure(bg="#f0f0f0")

        self._configurar_logging()
        self.logger.info("Aplicacao iniciada.")

        self.df_resultados = None
        self.arvore_decisao = None
        self._carregar_dados_configuracao() # Carrega resultados.json e arvore_decisao.json

        self.dados_usuario = {}
        self.caminho_percorrido = [] # Para logar o caminho de nos
        self.no_atual_id = None

        # --- Widgets Principais da UI ---
        self.rotulo_titulo_app = tk.Label(self.janela_principal, text="Sistema de Triagem Inicial de Sintomas", font=("Arial", 16, "bold"), bg="#f0f0f0", pady=15)
        self.rotulo_titulo_app.pack()

        self.rotulo_pergunta_atual = tk.Label(self.janela_principal, text="Bem-vindo!", font=("Arial", 14), wraplength=650, justify="center", bg="#f0f0f0", pady=20)
        self.rotulo_pergunta_atual.pack()

        self.frame_conteudo = tk.Frame(self.janela_principal, bg="#f0f0f0")
        self.frame_conteudo.pack(pady=20, fill="both", expand=True)
        
        self.rotulo_aviso_rodape = tk.Label(self.janela_principal,
                                        text="IMPORTANTE: Este sistema NAO fornece diagnostico medico.\nProcure um profissional de saude para diagnosticos e tratamentos.",
                                        font=("Arial", 9), fg="red", bg="#f0f0f0", pady=10)
        self.rotulo_aviso_rodape.pack(side=tk.BOTTOM, fill=tk.X)

        # Referencias aos widgets dinamicos
        self.botao_sim = None
        self.botao_nao = None
        self.entrada_numerica_widget = None
        self.botao_enviar_entrada = None
        self.area_texto_resultado_widget = None
        self.botao_reiniciar_widget = None
        self.botao_iniciar_widget = None

        if self.df_resultados is not None and self.arvore_decisao is not None:
            self.mostrar_tela_inicial()
        else:
            self.logger.critical("Falha critica ao carregar dados de configuracao. Aplicacao sera encerrada.")
            messagebox.showerror("Erro Critico", "Falha ao carregar arquivos de configuracao (resultados.json ou arvore_decisao.json).\nVerifique os arquivos e o arquivo 'triagem_log.txt' para detalhes.")
            self.janela_principal.destroy() # Fecha a janela se nao puder carregar


    def _configurar_logging(self):
        """Configura o sistema de logging para registrar eventos em um arquivo."""
        self.logger = logging.getLogger("TriagemApp")
        self.logger.setLevel(logging.INFO) # Mude para logging.DEBUG para mais detalhes
        
        if not self.logger.handlers:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            log_file_path = os.path.join(script_dir, "triagem_log.txt")

            try:
                file_handler = logging.FileHandler(log_file_path, encoding='utf-8', mode='a') # Modo 'a' para append
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"Erro ao configurar o logging para arquivo: {e}") 
            
            # console_handler = logging.StreamHandler() # Descomente para ver logs no console
            # console_handler.setFormatter(formatter)
            # self.logger.addHandler(console_handler)


    def _carregar_dados_configuracao(self):
        """Carrega os dados de resultados e a arvore de decisao de arquivos JSON."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        path_resultados = os.path.join(script_dir, "resultados.json")
        try:
            with open(path_resultados, 'r', encoding='utf-8') as f:
                dados_resultados_raw = json.load(f)
            self.df_resultados = pd.DataFrame(dados_resultados_raw)
            self.logger.info(f"Arquivo {path_resultados} carregado com sucesso.")
        except FileNotFoundError:
            self.logger.error(f"Arquivo {path_resultados} nao encontrado.")
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao decodificar {path_resultados}: {e}")
        except Exception as e:
            self.logger.error(f"Erro inesperado ao carregar {path_resultados}: {e}")

        path_arvore = os.path.join(script_dir, "arvore_decisao.json")
        try:
            with open(path_arvore, 'r', encoding='utf-8') as f:
                self.arvore_decisao = json.load(f)
            self.logger.info(f"Arquivo {path_arvore} carregado com sucesso.")
        except FileNotFoundError:
            self.logger.error(f"Arquivo {path_arvore} nao encontrado.")
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao decodificar {path_arvore}: {e}")
        except Exception as e:
            self.logger.error(f"Erro inesperado ao carregar {path_arvore}: {e}")

    def registrar_resposta_booleana(self, chave, valor_booleano):
        """Registra uma resposta booleana do usuario nos dados da sessao."""
        self.dados_usuario[chave] = valor_booleano
        self.logger.info(f"Resposta registrada: {chave} = {valor_booleano}")

    def mostrar_tela_inicial(self):
        """Configura e exibe a tela inicial da aplicacao."""
        self.limpar_frame_conteudo()
        self.dados_usuario = {}
        self.caminho_percorrido = ["inicio_triagem"]
        self.logger.info("Triagem iniciada/reiniciada.")
        self.rotulo_pergunta_atual.config(text="Bem-vindo! Clique em 'Iniciar Triagem' para comecar.")
        self.botao_iniciar_widget = tk.Button(self.frame_conteudo, text="Iniciar Triagem",
                                            command=lambda: self.processar_no_atual('inicio'),
                                            width=20, bg="#007bff", fg="white", font=("Arial", 12, "bold"))
        self.botao_iniciar_widget.pack(pady=30)

    def limpar_frame_conteudo(self):
        """Remove todos os widgets do frame de conteudo dinamico."""
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        self.botao_sim = self.botao_nao = self.entrada_numerica_widget = None
        self.botao_enviar_entrada = self.area_texto_resultado_widget = None
        self.botao_reiniciar_widget = self.botao_iniciar_widget = None
        
    def processar_no_atual(self, id_no_ou_info_resultado):
        """
        Processa o no atual da arvore de decisao, exibindo a pergunta/entrada apropriada
        ou o resultado final.
        """
        self.limpar_frame_conteudo()
        
        if isinstance(id_no_ou_info_resultado, dict):
            self.caminho_percorrido.append(f"resultado_direto_id_{id_no_ou_info_resultado.get('id_resultado')}")
        else:
            self.caminho_percorrido.append(str(id_no_ou_info_resultado))

        if isinstance(id_no_ou_info_resultado, dict) and id_no_ou_info_resultado.get('tipo_resultado') == 'direto':
            id_res = id_no_ou_info_resultado['id_resultado']
            self.logger.info(f"No de resultado direto: ID {id_res}. Caminho: {' -> '.join(self.caminho_percorrido)}")
            self.exibir_resultado_final_gui(id_res)
            return

        id_no = id_no_ou_info_resultado
        no_info = self.arvore_decisao.get(id_no)

        if not no_info:
            self.logger.error(f"Erro de Navegacao: No da arvore nao encontrado: {id_no}. Caminho: {' -> '.join(self.caminho_percorrido)}")
            messagebox.showerror("Erro de Navegacao", f"No da arvore nao encontrado: {id_no}")
            self.mostrar_tela_inicial()
            return

        self.no_atual_id = id_no
        self.rotulo_pergunta_atual.config(text=no_info.get('texto', "Processando..."))
        self.logger.info(f"Processando no: {id_no} - '{no_info.get('texto', '')}'")

        tipo_no = no_info['tipo']

        if tipo_no == 'pergunta':
            self._montar_pergunta_sim_nao(no_info)
        elif tipo_no == 'entrada_numerica':
            self._montar_entrada_numerica(no_info)
        elif tipo_no == 'logica':
            nome_metodo_logica = no_info.get('nome_metodo_logica')
            if nome_metodo_logica and hasattr(self, nome_metodo_logica):
                metodo_logica = getattr(self, nome_metodo_logica)
                resultado_logica = metodo_logica() 
                self.processar_no_atual(resultado_logica)
            else:
                self.logger.error(f"Metodo de logica '{nome_metodo_logica}' nao encontrado no no '{id_no}'. Caminho: {' -> '.join(self.caminho_percorrido)}")
                messagebox.showerror("Erro de Configuracao da Arvore", f"Metodo de logica nao definido para o no {id_no}.")
                self.mostrar_tela_inicial()
        else:
            self.logger.error(f"Tipo de no desconhecido: {tipo_no} no no '{id_no}'. Caminho: {' -> '.join(self.caminho_percorrido)}")
            messagebox.showerror("Erro de No", f"Tipo de no desconhecido: {tipo_no}")
            self.mostrar_tela_inicial()

    def _executar_acao_registro(self, acao_registro_info, valor_resposta_booleana):
        """Executa a acao de registrar a resposta do usuario se especificada no no."""
        if acao_registro_info:
            chave = acao_registro_info.get('chave')
            if chave: 
                self.registrar_resposta_booleana(chave, valor_resposta_booleana)

    def _montar_pergunta_sim_nao(self, no_info):
        """Monta os botoes Sim/Nao para um no do tipo 'pergunta'."""
        acao_registro_info = no_info.get('acao_registro') 
        
        proximo_no_sim = no_info['proximo_no_sim']
        proximo_no_nao = no_info['proximo_no_nao']

        self.botao_sim = tk.Button(self.frame_conteudo, text="Sim", 
                                    command=lambda: (self._executar_acao_registro(acao_registro_info, True), 
                                                    self.processar_no_atual(proximo_no_sim)),
                                    width=10, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.botao_sim.pack(side=tk.LEFT, padx=20, pady=20)

        self.botao_nao = tk.Button(self.frame_conteudo, text="Nao",
                                    command=lambda: (self._executar_acao_registro(acao_registro_info, False),
                                                    self.processar_no_atual(proximo_no_nao)),
                                    width=10, bg="#f44336", fg="white", font=("Arial", 12))
        self.botao_nao.pack(side=tk.RIGHT, padx=20, pady=20)

    def _montar_entrada_numerica(self, no_info):
        """Monta la caixa de entrada para um no do tipo 'entrada_numerica'."""
        self.entrada_numerica_widget = tk.Entry(self.frame_conteudo, width=10, font=("Arial", 12))
        self.entrada_numerica_widget.pack(pady=10)
        self.entrada_numerica_widget.focus()

        current_entry_widget = self.entrada_numerica_widget 

        def acao_enviar(event=None): 
            valor_str = current_entry_widget.get()
            try:
                valor = float(valor_str)
                self.dados_usuario[no_info['chave_dado']] = valor
                self.logger.info(f"Entrada numerica registrada: {no_info['chave_dado']} = {valor}")
                if self.janela_principal.winfo_exists():
                    self.janela_principal.unbind('<Return>')
                self.processar_no_atual(no_info['proximo_no'])
            except ValueError:
                self.logger.warning(f"Entrada numerica invalida: '{valor_str}'")
                messagebox.showerror("Erro de Entrada", "Por favor, insira um valor numerico valido.")
                if current_entry_widget and current_entry_widget.winfo_exists():
                    current_entry_widget.delete(0, tk.END)
                    current_entry_widget.focus()
            
        self.botao_enviar_entrada = tk.Button(self.frame_conteudo, text="Enviar", command=acao_enviar,
                                            bg="#2196F3", fg="white", font=("Arial", 12))
        self.botao_enviar_entrada.pack(pady=10)
        self.janela_principal.bind('<Return>', acao_enviar)


    def exibir_resultado_final_gui(self, id_resultado_selecionado):
        """Exibe o resultado final da triagem na interface grafica, incluindo orientacoes de cuidados."""
        self.limpar_frame_conteudo()
        self.rotulo_pergunta_atual.config(text="--- Triagem Inicial Concluida ---")
        self.logger.info(f"Resultado final exibido: ID {id_resultado_selecionado}. Dados do usuario: {self.dados_usuario}. Caminho final: {' -> '.join(self.caminho_percorrido)}")

        resultado_df_filtrado = self.df_resultados[self.df_resultados['ID_Resultado'] == id_resultado_selecionado]
        if resultado_df_filtrado.empty:
            self.logger.error(f"Resultado com ID {id_resultado_selecionado} nao encontrado no DataFrame.")
            messagebox.showerror("Erro", f"Resultado com ID {id_resultado_selecionado} nao encontrado.")
            self.mostrar_tela_inicial()
            return

        resultado = resultado_df_filtrado.iloc[0]
        
        self.area_texto_resultado_widget = scrolledtext.ScrolledText(self.frame_conteudo, wrap=tk.WORD, width=60, height=20, font=("Arial", 10)) # Aumentei altura
        self.area_texto_resultado_widget.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.area_texto_resultado_widget.insert(tk.INSERT, f"Com base nas suas respostas, a indicacao principal e: {resultado['Resultado_Principal']}\n\n")
        self.area_texto_resultado_widget.insert(tk.INSERT, "Probabilidades Estimadas (hipoteticas):\n")
        for col in ['Prob_Gripe', 'Prob_Resfriado', 'Prob_Alergia', 'Prob_Viral_Leve', 'Prob_COVID']:
            if col in resultado and pd.notna(resultado[col]):
                    nome_condicao = col.replace('Prob_', '').replace('_', ' ')
                    if nome_condicao == "COVID": nome_condicao = "COVID-19 (Estimativa)"
                    self.area_texto_resultado_widget.insert(tk.INSERT, f"   - {nome_condicao.capitalize()}: {resultado[col]*100:.0f}%\n")
        self.area_texto_resultado_widget.insert(tk.INSERT, "\n")

        if ("ALERTA" in str(resultado['Resultado_Principal']).upper()) or \
            (pd.notna(resultado['Prob_Aval_Medica']) and resultado['Prob_Aval_Medica'] > 0.20) :
            prob_aval_medica_str = f"{resultado['Prob_Aval_Medica']*100:.0f}%" if pd.notna(resultado['Prob_Aval_Medica']) else "significativa"
            self.area_texto_resultado_widget.insert(tk.INSERT, f"ATENCAO: Ha uma probabilidade consideravel ({prob_aval_medica_str}) ou um indicativo de que voce deve procurar AVALIACAO MEDICA PROFISSIONAL.\n\n", "alerta")
        elif pd.notna(resultado['Prob_Outro']) and resultado['Prob_Outro'] > 0.50:
                self.area_texto_resultado_widget.insert(tk.INSERT, f"   - Outra condicao / Sintomas inespecificos: {resultado['Prob_Outro']*100:.0f}%\n")
                self.area_texto_resultado_widget.insert(tk.INSERT, "Seus sintomas sao um pouco inespecificos ou nao se encaixam claramente nos padroes mais comuns.\n")
                self.area_texto_resultado_widget.insert(tk.INSERT, "Recomendamos observar a evolucao dos sintomas. Se persistirem ou piorarem, procure orientacao medica.\n\n")

        self.area_texto_resultado_widget.insert(tk.INSERT, "--- Orientacoes Gerais de Cuidados ---\n", "subtitulo_cuidados")
        if pd.notna(resultado.get('Orientacoes_Cuidados')) and str(resultado['Orientacoes_Cuidados']).strip():
            self.area_texto_resultado_widget.insert(tk.INSERT, f"{resultado['Orientacoes_Cuidados']}\n\n")
        else:
            self.area_texto_resultado_widget.insert(tk.INSERT, "Monitore seus sintomas atentamente. Beba liquidos, descanse e alimente-se de forma saudavel. Em caso de piora, persistencia dos sintomas ou qualquer duvida, procure orientacao medica profissional.\n\n")
        
        self.area_texto_resultado_widget.insert(tk.INSERT, "Lembre-se: Este e um sistema de triagem inicial e NAO SUBSTITUI UM DIAGNOSTICO MEDICO.\n")
        self.area_texto_resultado_widget.insert(tk.INSERT, "Se os sintomas persistirem, piorarem, ou se voce tiver qualquer preocupacao, procure um profissional de saude.")
        
        self.area_texto_resultado_widget.tag_config("alerta", foreground="red", font=("Arial", 10, "bold"))
        self.area_texto_resultado_widget.tag_config("subtitulo_cuidados", font=("Arial", 10, "bold"), foreground="#0056b3")
        
        self.area_texto_resultado_widget.config(state=tk.DISABLED)

        self.botao_reiniciar_widget = tk.Button(self.frame_conteudo, text="Iniciar Nova Triagem", command=self.mostrar_tela_inicial,
                                                bg="#FF9800", fg="white", font=("Arial", 12))
        self.botao_reiniciar_widget.pack(pady=20)
        if self.janela_principal.winfo_exists():
            self.janela_principal.unbind('<Return>')

    # --- Metodos de Logica da Arvore ---
    def avaliar_com_febre_e_dor_corpo(self):
        """
        Avalia o resultado se o usuario tem febre (sem dificuldade respiratoria inicial) E dor no corpo.
        Pode levar ao ID 1 (Gripe Forte) ou a um no para checar perda de olfato antes do ID 3.
        """
        self.logger.debug(f"Avaliando 'avaliar_com_febre_e_dor_corpo'. Temperatura: {self.dados_usuario.get('temperatura')}")
        temp = self.dados_usuario.get('temperatura', 0)
        if temp >= 38.5:
            # Febre alta com dor no corpo intensa (sem dif. resp. inicial) -> Gripe Forte (ID 1)
            # Considerar se aqui tambem deveria checar olfato para um ID COVID especifico.
            # Por ora, mantem simples, direcionando para Gripe Forte se febre alta + dor corpo.
            return {'tipo_resultado': 'direto', 'id_resultado': 1} 
        else:
            # Febre baixa/moderada com dor no corpo intensa. Antes de concluir ID 3, checar olfato.
            return 'checar_olfato_para_ID3_contexto_febre_dorcorpo'

    def avaliar_com_febre_sem_dor_corpo_ou_proxima_pergunta(self):
        """
        Avalia se deve ir para proxima pergunta ou resultado, se febre sem dor no corpo (e sem dif. resp. inicial).
        Pode levar a 'no_tosse_produtiva...' (para ID 2) ou a um no para checar perda de olfato antes de ID 3 ou 8.
        """
        self.logger.debug(f"Avaliando 'avaliar_com_febre_sem_dor_corpo_ou_proxima_pergunta'. Temperatura: {self.dados_usuario.get('temperatura')}")
        temp = self.dados_usuario.get('temperatura', 0)
        if temp >= 38.5: 
            # Febre alta sem dor no corpo. Leva a pergunta sobre tosse produtiva (ID 2).
            # Similar ao caso acima, poderia haver uma checagem de olfato antes de direcionar para ID 2,
            # se quisessemos um ID especifico para "Febre Alta + Tosse Produtiva + Perda Olfato".
            return 'no_tosse_produtiva_com_febre_sem_dor'
        else: 
            # Febre baixa/moderada sem dor no corpo.
            # O no 'no_dor_garganta_febre_baixa_sem_dor_corpo_checar_olfato' ja foi inserido
            # no JSON para lidar com a checagem de olfato neste fluxo.
            return 'no_dor_garganta_febre_baixa_sem_dor_corpo_checar_olfato'

# --- Execucao do Programa ---
if __name__ == "__main__":
    janela_raiz_tk = tk.Tk()
    app = AplicacaoTriagem(janela_raiz_tk)
    
    if app.df_resultados is not None and app.arvore_decisao is not None:
        janela_raiz_tk.mainloop()
    else:
        print("Encerrando a aplicacao devido a erro no carregamento da configuracao.")
        if janela_raiz_tk.winfo_exists():
            janela_raiz_tk.destroy()