
'''
Este Jogo foi feito com ajuda
de inteligência artificial (ChatGTP e Gemini), para ver 
as propriedades dos botões e imagens consultei o site
da W3Schools.

O jogo foi idealizado para ser um jogo educativo,
utilizado nas escolas para ensinar os alunos a
gerir o seu dinheiro. (Literacia Financeira)

Seria introduzido na disciplina de Cidadania
e Desenvolvimento, para os alunos secundário.

'''


import os
import tkinter as tk
from PIL import Image, ImageTk
from random import random, choice
import json


# Game Settings
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 640
GAME_TITLE = "FinanceGame"


# Cores
BG_COLOR = "#0067CD"
BUTTON_COLOR = "snow"
SELECTED_COLOR = "white"
UNSELECTED_COLOR = "#014B94"


# Game Constants
CASA = 0
APARTAMENTO = 1
MANSAO = 2
CARRO = 3
AUTOCARRO = 4
BICICLETA = 5
ALIMENTACAO = 100
TRABALHOS = [6, 7, 8]
PRECO_CASA = [300, 500, 900]
PRECO_TRANSPORTES = [300, 40, 0]
START_CHANCE = 0.2

NOMES = [["Casa", "Apartamento", "Mansão"],
         ["Carro", "Autocarro", "Bicicleta"],
         ["Construtor Civil", "Professor", "Advogado"]]

# Initial Values
INITIAL_BALANCE_SUSTAINABLE = 500
INITIAL_BALANCE_DIFFICULT = 0
INITIAL_BALANCE_DEFAULT = 100

#==============================Helper Functions==============================
def avancar():
    global active_frame, escolhas
    if None in selecionados:  # Se não foram selecionados todos os botões,
        return
    escolhas = [selecionados[i] for i in range(3) if selecionados[i] is not None]
    desenhar_comentario_inicial()

def selecionar_botao(index, linha):
    global botoes, selecionados

    if selecionados[linha] is not None:
        botoes[selecionados[linha]].config(bg=UNSELECTED_COLOR)
    botoes[index].config(bg=SELECTED_COLOR)
    selecionados[linha] = index

def destroy_button(button):
    if button:  # Verifica se o botão ainda existe
        button.after(1, button.destroy)  # Agendar a destruição do botão

def destroy_buttons(buttons):
    for button in buttons:
        destroy_button(button)

def clear_frame():
    global frame
    # Iterate through every widget inside the frame
    for widget in frame.winfo_children():
        widget.destroy()  # deleting widget

def escrever_json():
    global mes, escolhas, saldo, dinheiro_gasto, dinheiro_ganho, vezes_jantar_fora, vezes_hobbie, vezes_cinema, vezes_roupa_nova, comprou_telemovel, aumento_salarial
    data = {
        "meses_jogados": mes,
        "habitacao": NOMES[0][escolhas[0]],
        "transporte": NOMES[1][escolhas[1]-3],
        "profissao": NOMES[2][escolhas[2]-6],
        "saldo_final": saldo,
        "dinheiro_gasto": dinheiro_gasto,
        "dinheiro_ganho": dinheiro_ganho,
        "jantar_fora": vezes_jantar_fora,
        "hobbie": vezes_hobbie,
        "lazer": vezes_cinema,
        "compras_de_roupa": vezes_roupa_nova,
        "comprou_telemovel": comprou_telemovel,
        "aumento_salarial": aumento_salarial
    }
    with open("dados_jogo.json", "w", encoding='UTF-8') as file:
        json.dump(data, file)

#==============================Starting Screen===============================
def desenhar_ecra_inicial():
    global frame, imagens

    clear_frame()

    img_name = "coin.png"
    imagem_tk = ImageTk.PhotoImage(imagens[img_name].resize((250, 250)) if img_name in imagens else None)

    label_imagem = tk.Label(frame, image=imagem_tk, bg=BG_COLOR)
    label_imagem.image = imagem_tk
    label_imagem.place(relx=0.5, rely=0.3, anchor="center")

    titulo = tk.Label(frame, text="FinanceGame", font=("Helvetica", 32, "bold"), bg=BG_COLOR, fg="white")
    titulo.place(relx=0.5, rely=0.50, anchor="center")

    botao_iniciar = tk.Button(frame, text="         Jogar         ", font=("Helvetica", 22, "bold"), bg="#014B94", \
                              fg="white", bd=0, activebackground="white", activeforeground="black", command=desenhar_ecra_escolhas)
    botao_iniciar.place(relx=0.5, rely=0.80, anchor="center")

#===============================Choices Screen===============================
def desenhar_ecra_escolhas():
    global frame, imagens, saldo, mes, ordenado, despesas, escolhas, selecionados, botoes, botao_popup, chance_acontecimento, dinheiro_gasto, dinheiro_ganho, \
        vezes_jantar_fora, vezes_hobbie, vezes_roupa_nova, vezes_cinema, comprou_telemovel, aumento_salarial, acontecimentos, acoes
    
    acoes = {"jantar_fora_vezes": [], "novo_hobbie_vezes": [], "roupa_nova_vezes": [], "cinema_vezes": []}
    saldo = 0  # Saldo inicial do jogador
    mes = 1  # Mês atual
    ordenado = 870  # Ordenado do jogador
    despesas = [f"Alimentação: -{ALIMENTACAO}€"]  # Dicionário para armazenar as despesas do jogador
    escolhas = []  # Lista para armazenar as escolhas do jogador
    selecionados = [None, None, None]  # Guarda o índice do botão selecionado por linha
    botoes = []
    botao_popup = None
    chance_acontecimento = START_CHANCE
    dinheiro_gasto = 0
    dinheiro_ganho = 0
    vezes_jantar_fora = 0
    vezes_hobbie = 0
    vezes_roupa_nova = 0
    vezes_cinema = 0
    comprou_telemovel = False
    aumento_salarial = False
    
    #Abrir o json com os acontecimentos
    with open('acontecimentos.json', encoding="UTF-8") as file:
        acontecimentos = json.load(file)

    clear_frame()

    titulo_jogo = tk.Label(frame, text="Começar por escolher a\ntua Habitação, o Transporte\ne a tua Profissão.", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg="white")
    titulo_jogo.place(relx=0.5, y=60, anchor="center")
    titulo_jogo = tk.Label(frame, text="Habitação", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg="#062F57")
    titulo_jogo.place(x=118, y=60, anchor="center")
    titulo_jogo = tk.Label(frame, text="Transporte", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg="#062F57")
    titulo_jogo.place(x=280, y=60, anchor="center")
    titulo_jogo = tk.Label(frame, text="Profissão", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg="#062F57")
    titulo_jogo.place(x=215, y=90, anchor="center")

    botoes.clear()
    espacamento_x = 10
    espacamento_y = 10
    largura_botao = 100
    altura_botao = 100

    inicio_x = (WINDOW_WIDTH - (3 * largura_botao + 2 * espacamento_x)) // 2
    inicio_y = 150

    for linha in range(3):
        for coluna in range(3):
            index = linha * 3 + coluna
            x = inicio_x + coluna * (largura_botao + espacamento_x)
            y = inicio_y + linha * (altura_botao + espacamento_y)
            name = f"imagem{index+1}.png"
            image_tk = ImageTk.PhotoImage(imagens[name].resize((100, 100)) if name in imagens else None)
            botao = tk.Button(frame, image=image_tk, bg=UNSELECTED_COLOR, width=100, height=100, bd=0, \
                              command=lambda i=index, l=linha: selecionar_botao(i, l))
            botao.image = image_tk
            botao.place(x=x, y=y)
            botoes.append(botao)

    botao_avancar = tk.Button(frame, text="     Avançar     ", font=("Helvetica", 22, "bold"), bg="#014B94", fg="white", bd=0,\
                             activebackground="white", activeforeground="black", command=avancar)
    botao_avancar.place(relx=0.5, y=550, anchor="center")

def desenhar_comentario_inicial():
    global frame, saldo, dinheiro_ganho
    
    clear_frame()

    # Verifica a combinação escolhida
    if (CASA in escolhas or APARTAMENTO in escolhas) and BICICLETA in escolhas:
        saldo = INITIAL_BALANCE_SUSTAINABLE
        mensagem = "Boa, escolheste \num caminho mais\n sustentável,\n começas com:"
        texto = tk.Label(frame, text=mensagem, font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=100, anchor="center")

        palavra = tk.Label(frame, text="sustentável", font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="#40D81A")
        palavra.place(x=175, y=115, anchor="center")

        palavra2 = tk.Label(frame, text="Boa", font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="#40D81A")
        palavra2.place(x=90, y=50, anchor="center")

    elif MANSAO in escolhas and CARRO in escolhas:
        saldo = INITIAL_BALANCE_DIFFICULT
        mensagem = "Cuidado escolheste\num caminho difícil\n de sustentar,\n começas com:"
        texto = tk.Label(frame, text=mensagem, font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=100, anchor="center")

        palavra = tk.Label(frame, text="Cuidado", font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="orange")
        palavra.place(x=100, y=50, anchor="center")
    else:
        saldo = INITIAL_BALANCE_DEFAULT
        mensagem = "Escolha interessante,\ncomeças com:"
        texto = tk.Label(frame, text=mensagem, font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=100, anchor="center")

        palavra = tk.Label(frame, text="interessante", font=("Helvetica", 22, "bold"), bg=BG_COLOR, fg="#062F57")
        palavra.place(x=235, y=85, anchor="center")

    dinheiro_ganho += saldo

    valor_texto = tk.Label(frame, text=f"{saldo}€", font=("Helvetica", 70, "bold"), bg=BG_COLOR, fg="white")
    valor_texto.place(relx=0.5, y=300, anchor="center")

    botao_comecar = tk.Button(frame, text="     Começar     ", font=("Helvetica", 22, "bold"), bg="#014B94", fg="white" \
                              , bd=0, activebackground="white", activeforeground="black", command=desenhar_ecra_jogo)
    botao_comecar.place(relx=0.5, y=540, anchor="center")
    
#================================Game Screen=================================
def desenhar_ecra_jogo():
    global frame, mes, saldo
    
    clear_frame()

    #meses
    img_name = "button.png"
    button_imagem_tk = ImageTk.PhotoImage(imagens[img_name].resize((WINDOW_WIDTH, 20)) if img_name in imagens else None)
    meses = tk.Label(frame, image=button_imagem_tk, text=f"Mês: {mes}"+ " "*55, font=("Helvetica", 14, "bold"), bd=0, \
                    bg="DodgerBlue2", fg="white", compound=tk.CENTER)
    meses.place(relx=0.5, y=12, anchor="center")

    #colocar imagem da habitação
    img_name = f"imagem{escolhas[0]+1}.png"
    imagem_habitacao_tk = ImageTk.PhotoImage(imagens[img_name].resize((85, 85)) if img_name in imagens else None) 
    imagem_habitacao = tk.Label(frame, image=imagem_habitacao_tk, bg=BG_COLOR)
    imagem_habitacao.image = imagem_habitacao_tk
    imagem_habitacao.place(relx=0.17, rely=0.21, anchor="center")

    #label habitacao
    habitacao_label = tk.Label(frame, text=f"-{PRECO_CASA[escolhas[0]]}€", font=("Helvetica", 14, "bold"), \
                    bg=BG_COLOR, fg="red")    
    habitacao_label.place(relx=0.15, y=190, anchor="center")

    #colocar imagem da profissao
    img_name = f"imagem{escolhas[2]+1}.png"
    imagem_profissao_tk = ImageTk.PhotoImage(imagens[img_name].resize((120, 120)) if img_name in imagens else None)
    imagem_profissao = tk.Label(frame, image=imagem_profissao_tk, bg=BG_COLOR)
    imagem_profissao.image = imagem_profissao_tk
    imagem_profissao.place(relx=0.5, rely=0.18, anchor="center")
   
    #label profissao
    emprego = tk.Label(frame, text=f"+{ordenado}€", font=("Helvetica", 14, "bold"), \
                    bg=BG_COLOR, fg="#40D81A")
    emprego.place(relx=0.5, y=190, anchor="center")

    #colocar imagem do transporte
    img_name = f"imagem{escolhas[1]+1}.png"
    imagem_transporte_tk = ImageTk.PhotoImage(imagens[img_name].resize((85, 85)) if img_name in imagens else None)
    imagem_transporte = tk.Label(frame, image=imagem_transporte_tk, bg=BG_COLOR)
    imagem_transporte.image = imagem_transporte_tk
    imagem_transporte.place(relx=0.83, rely=0.22, anchor="center")

    #label transporte
    transporte_label = tk.Label(frame, text=f"-{PRECO_TRANSPORTES[escolhas[1]-3]}€", font=("Helvetica", 14, "bold"), \
                    bg=BG_COLOR, fg="red")
    transporte_label.place(relx=0.85, y=190, anchor="center")

    #saldo
    saldo_label = tk.Label(frame, text=f"{saldo}€", font=("Helvetica", 38, "bold"), bg=BG_COLOR, fg="white")
    saldo_label.place(relx=0.5, y=240, anchor="center")

    #despesas
    img_name = "button.png"
    button_imagem_tk = ImageTk.PhotoImage(imagens[img_name].resize((WINDOW_WIDTH, 20)) if img_name in imagens else None)
    descricao = tk.Label(frame, image=button_imagem_tk, text="Despesas deste mês:"+" "*30, font=("Helvetica", 14, "bold"), bd=0, \
                         bg="DodgerBlue2", fg="white", compound=tk.CENTER)
    descricao.place(relx=0.5, y=295, anchor="center")

    #Mostrar despesas
    for i, despesa in enumerate(despesas):
        label_despesa = tk.Label(frame, text=despesa, font=("Helvetica", 10, "bold"), bg=BG_COLOR, fg="white")  
        if i < 4:
            label_despesa.place(relx=0.25, y=325 + i * 20, anchor="center")
        elif i < 8:
            label_despesa.place(relx=0.75, y=325 + (i-4) * 20, anchor="center")
        else:
            break

    #retangulo
    retangulo = tk.Label(frame,image=button_imagem_tk, bg="DodgerBlue2", fg="white", bd=0)
    retangulo.place(relx=0.5, y=415, anchor="center")

    #BOTÃO CASAS
    img_name = "button.png"
    button_imagem_tk = ImageTk.PhotoImage(imagens[img_name].resize((120, 100)) if img_name in imagens else None)
    botao_casas = tk.Button(frame, image=button_imagem_tk, text="Habitação", font=("Helvetica", 14, "bold"), bd=0, \
                            bg="DodgerBlue4", fg="white", activebackground="DodgerBlue4", compound=tk.CENTER, command=desenhar_trocar_casas)
    botao_casas.image = button_imagem_tk
    botao_casas.place(x=60, y=475, anchor="center")
    
    #BOTÃO MESES
    botao_continuar = tk.Button(frame, image=button_imagem_tk, text="+", font=("Helvetica", 39, "bold"), \
                                bg="#0E355B", fg="white", bd=0, compound=tk.CENTER, command=atualizar_meses_ordenado)
    botao_continuar.place(relx=0.5, y=475, anchor="center")

    #BOTÃO TRANSPORTES
    botao_transportes = tk.Button(frame, image=button_imagem_tk, text="Transporte", font=("Helvetica", 14, "bold"),\
                                   bg="DodgerBlue4", fg="white", activebackground="DodgerBlue4", bd=0, compound=tk.CENTER, command=desenhar_trocar_transportes)
    botao_transportes.image = button_imagem_tk
    botao_transportes.place(x=300, y=475 , anchor="center")
        
    #botões despesas
    img_name = "button.png"
    button_imagem_tk = ImageTk.PhotoImage(imagens[img_name].resize((180, 70)) if img_name in imagens else None)
    botao_continuar = tk.Button(frame, image=button_imagem_tk ,text="Jantar Fora \n -30€", font=("Helvetica", 12, "bold"), \
                                bg="#2479CD", fg="white", bd=0, compound=tk.CENTER, command=lambda : aplicar_despesa("Jantar Fora", 30))
    botao_continuar.image = button_imagem_tk
    botao_continuar.place(relx=0.25, y=560, anchor="center")

    botao_continuar = tk.Button(frame, image=button_imagem_tk ,text="Novo Hobbie \n -27€", font=("Helvetica", 12, "bold"), \
                                bg="#2479CD", fg="white", bd=0, compound=tk.CENTER, command=lambda : aplicar_despesa("Novo Hobbie", 27))
    botao_continuar.image = button_imagem_tk
    botao_continuar.place(relx=0.75, y=560, anchor="center")

    botao_continuar = tk.Button(frame, image=button_imagem_tk ,text="Roupa Nova \n -90€", font=("Helvetica", 12, "bold"), \
                                bg="#2479CD", fg="white", bd=0, compound=tk.CENTER, command=lambda : aplicar_despesa("Roupa Nova", 90))
    botao_continuar.image = button_imagem_tk
    botao_continuar.place(relx=0.25, y=620, anchor="center")

    botao_continuar = tk.Button(frame, image=button_imagem_tk ,text="Ir ao cinema \n -10€", font=("Helvetica", 12, "bold"), \
                                bg="#2479CD", fg="white", bd=0, compound=tk.CENTER, command=lambda : aplicar_despesa("Ir ao cinema", 10))
    botao_continuar.image = button_imagem_tk
    botao_continuar.place(relx=0.75, y=620, anchor="center")

    escrever_json()

def atualizar_meses_ordenado():
    global frame, botao_popup, chance_acontecimento, saldo, mes, despesas, button_imagem_tk, button_imagem_tk2, button_imagem_tk3, label_imagem_tk3, button_imagem_tk4, \
        acoes, ordenado, dinheiro_gasto, dinheiro_ganho, aumento_salarial
    
    despesas = []
    popup = False
    popup2 = False
    popup3 = False

    if mes == 6:
        desenhar_frame_final()
        return
    
    mes += 1
   
    saldo += ordenado
    saldo -= PRECO_CASA[escolhas[0]]
    saldo -= PRECO_TRANSPORTES[escolhas[1]-3]
    saldo -= ALIMENTACAO
    
    despesas.append(f"Alimentação: -{ALIMENTACAO}€")
    
    dinheiro_ganho += ordenado
    dinheiro_gasto += PRECO_CASA[escolhas[0]] + ALIMENTACAO + PRECO_TRANSPORTES[escolhas[1]-3]

    if random() <= chance_acontecimento: #SORTEAR ACONTECIMENTO ALEATÓRIO
        
        keys = list(acontecimentos.keys()) #chaves do dicionário
        
        categorias = [9] # Acontecimento geral
        categorias.extend(escolhas) # Adicionar categorias escolhidas
        while True:
            categoria = choice(categorias) #sortear categoria
            nome_categoria = keys[categoria] #escolher nome da categoria
            if acontecimentos[nome_categoria]:
                break

        acontecimentos_categoria = acontecimentos[nome_categoria] #escolher categoria
        
        random_chave = choice(list(acontecimentos_categoria))
        acontecimento = acontecimentos_categoria[random_chave] #sortear acontecimento
        
        #aplicar acontecimento
        saldo += acontecimento["valor"] if "valor" in acontecimento else 0
        despesas.append(f"{acontecimento['despesa']}" if "despesa" in acontecimento else "") # caso não tenha "despesa" não adicionar
        mensagem = acontecimento["mensagem"] if "mensagem" in acontecimento else "" # caso não tenha "mensagem" não adicionar
        if acontecimento["valor"] < 0:
            dinheiro_gasto += acontecimento["valor"]
        elif acontecimento["valor"] > 0:
            dinheiro_ganho += acontecimento["valor"]
            
        acontecimentos[nome_categoria].pop(random_chave) #remover acontecimento da lista para que não volte a "calhar"
        
        popup = True
        chance_acontecimento = START_CHANCE #probalidade de acontecimento DEFAULT
    else:
        chance_acontecimento += 0.1 #aumentar a probabilidade de acontecimento
    
    
    if saldo < 0:
        desenhar_frame_final()
        return
    

    if len(acoes["jantar_fora_vezes"]) == 3:
        ordenado = 1000
        popup2 = True
        mensagem2 = "Fechar\n\nJantar fora tem\n te feito bem,\n andas mais descontraido/a\n e trabalhas melhor!\nParabéns, \nconseguiste um aumento\n de ordenado, +130€"
        acoes["jantar_fora_vezes"].clear() #limpar lista para não voltar a dar o bónus
        aumento_salarial = True
        
    elif len(acoes["roupa_nova_vezes"]) == 2:
        ordenado = 1000
        popup2 = True   
        mensagem2 = "Fechar\n\nEssas roupas novas deram-te\n mais confiança,\n andas mais descontraido/a\n e trabalhas melhor!\nParabéns, \nconseguiste um aumento\n +130€"
        acoes["roupa_nova_vezes"].clear() #limpar lista para não voltar a dar o bónus
        aumento_salarial = True

    elif len(acoes["novo_hobbie_vezes"]) == 2:
        ordenado = 1000
        popup2 = True
        mensagem2 = "Fechar\n\nPraticar um Hobbie, relaxa-te!\nParabéns, \nconseguiste um aumento\n +130€"
        acoes["novo_hobbie_vezes"].clear() #limpar lista para não voltar a dar o bónus
        aumento_salarial = True

    elif len(acoes["cinema_vezes"]) == 5:
        ordenado = 1000
        popup2 = True
        mensagem2 = "Fechar\n\nO cinema deixa-te\n animado/a e\n bem disposto!Parabéns,conseguiste\n um aumento\n  +130€"
        acoes["cinema_vezes"].clear() #limpar lista para não voltar a dar o bónus
        aumento_salarial = True

    if escolhas[1] == BICICLETA and mes == 2:
        saldo += 100
        despesas.append("Bónus de Transporte +100€")
        mensagem3 = "Fechar\n\nBoa, escolheste a bicicleta,\n um transporte sustentável!\n \n Passas a receber um\n apoio do Estado, todos\n os meses no valor de\n 100€\n "
        popup3 = True 
        dinheiro_ganho += 100

    desenhar_ecra_jogo()
    

    # fazer o "popup"
    if popup:
        img_name = "button.png"
        button_imagem_tk = ImageTk.PhotoImage(imagens[img_name].resize((180, 90)) if img_name in imagens else None)
        botao_popup = tk.Button(frame, image=button_imagem_tk, text=mensagem, \
                                font=("Helvetica", 16, "bold"), bg="white", fg="gray8", bd=0, compound=tk.CENTER)
        botao_popup.image = button_imagem_tk  # Keep a reference to prevent garbage collection
        botao_popup.place(relx=0.5, y=250, anchor="center")
        botao_popup.config(command=lambda : destroy_button(botao_popup))

    # fazer o "popup2"
    if popup2:
        img_name = "button.png"
        button_imagem_tk2 = ImageTk.PhotoImage(imagens[img_name].resize((180, 90)) if img_name in imagens else None)
        botao_popup2 = tk.Button(frame, image=button_imagem_tk2, text=mensagem2, \
                                font=("Helvetica", 16, "bold"), bg="white", fg="gray8", bd=0, compound=tk.CENTER)
        botao_popup2.image = button_imagem_tk2  # Keep a reference to prevent garbage collection
        botao_popup2.place(relx=0.5, y=250, anchor="center")
        botao_popup2.config(command=lambda : destroy_button(botao_popup2))

    # fazer o "popup3"
    if popup3:
        img_name = "button.png"
        button_imagem_tk3 = ImageTk.PhotoImage(imagens[img_name].resize((180, 90)) if img_name in imagens else None)
        botao_popup3 = tk.Button(frame, image=button_imagem_tk3, text=mensagem3, \
                                font=("Helvetica", 16, "bold"), bg="white", fg="gray8", bd=0, compound=tk.CENTER)
        botao_popup3.image = button_imagem_tk3  # Keep a reference to prevent garbage collection
        botao_popup3.place(relx=0.5, y=250, anchor="center")
        botao_popup3.config(command=lambda : destroy_button(botao_popup3))

    
    if mes == 5:
        mensagem3 = "\nSaiu o novo Iphone 20!\n Por apenas 1300€\n\n Queres comprar?\n\n"
    
        # fazer o "popup3"
        img_name = "button.png"
        label_imagem_tk3 = ImageTk.PhotoImage(imagens[img_name].resize((200, 90)) if img_name in imagens else None)
        label_popup3 = tk.Label(frame, image=label_imagem_tk3, text=mensagem3, \
                                font=("Helvetica", 16, "bold"), bg="white", fg="gray8", bd=0, compound=tk.CENTER)
        label_popup3.image = label_imagem_tk3  # Keep a reference to prevent garbage collection
        label_popup3.place(relx=0.5, y=250, anchor="center")

        #botao sim
        img_name = "button.png"
        button_imagem_tk4 = ImageTk.PhotoImage(imagens[img_name].resize((30, 20)) if img_name in imagens else None)
        popup_sim = tk.Button(frame, image=button_imagem_tk4, text="Sim", \
                                font=("Helvetica", 16, "bold"), bg="white", fg="#40D81A", bd=0, compound=tk.CENTER)
        popup_sim.image = button_imagem_tk4  # Keep a reference to prevent garbage collection
        popup_sim.place(relx=0.35, y=315, anchor="center")


        # botao nao
        popup_nao = tk.Button(frame, image=button_imagem_tk4, text="Não", \
                                font=("Helvetica", 16, "bold"), bg="white", fg="red", bd=0, compound=tk.CENTER)
        popup_nao.image = button_imagem_tk4  # Keep a reference to prevent garbage collection
        popup_nao.place(relx=0.65, y=315, anchor="center")
        
        popup_sim.config(command=lambda : botao_sim([label_popup3, popup_sim, popup_nao]))
        popup_nao.config(command=lambda : destroy_buttons([label_popup3, popup_sim, popup_nao]))

def botao_sim(buttons):
    global frame, saldo, despesas, button_imagem_tk4, botao_popup4, dinheiro_gasto, comprou_telemovel
    destroy_buttons(buttons)

    # Verifica se o jogador tem saldo suficiente para comprar o telefone
    img_name = "button.png"
    button_imagem_tk4 = ImageTk.PhotoImage(imagens[img_name].resize((180, 90)) if img_name in imagens else None)
    botao_popup4 = tk.Button(frame, image=button_imagem_tk4, \
                            font=("Helvetica", 16, "bold"), bg="white", fg="gray8", bd=0, compound=tk.CENTER)
    botao_popup4.image = button_imagem_tk4  # Keep a reference to prevent garbage collection
    botao_popup4.place(relx=0.5, y=250, anchor="center")

    if saldo >= 1300:
        saldo -= 1300
        dinheiro_gasto +=1300
        despesas.append("Novo Iphone 20: -1300€")
        mensagem = "Fechar\n\nParabéns!\nCompraste o novo Iphone 20!\n\n\n\n"
        emoji = ImageTk.PhotoImage(imagens["emoji.png"].resize((80, 80)) if "emoji.png" in imagens else None) 
        label_emoji = tk.Button(frame, image=emoji, bg="white", bd=0, compound=tk.CENTER)
        label_emoji.image = emoji  # Keep a reference to prevent garbage collection
        label_emoji.place(relx=0.5, y=295, anchor="center")
        label_emoji.config(command=lambda : destroy_buttons([botao_popup4, label_emoji]))
        botao_popup4.config(command=lambda : destroy_buttons([botao_popup4, label_emoji]))
        comprou_telemovel = True
    else:
        mensagem = "Fechar\n\nNão tens dinheiro suficiente\npara comprar o novo Iphone 20!\n\n"
        botao_popup4.config(command=lambda : destroy_button(botao_popup4))

    botao_popup4.config(text=mensagem)   
 
def aplicar_despesa(nome_despesa, valor):
    global saldo, despesas, dinheiro_gasto, vezes_cinema, vezes_hobbie, vezes_roupa_nova, vezes_jantar_fora
    
    if saldo < valor:
        return
    saldo -= valor
    dinheiro_gasto += valor
    despesas.append(f"{nome_despesa}: -{valor}€")

    # Verifica se a pessoa fez alguma vez uma despesa 
    if nome_despesa == "Jantar Fora":
        vezes_jantar_fora += 1
        if mes not in acoes["jantar_fora_vezes"]:
            acoes["jantar_fora_vezes"].append(mes)
                
    elif nome_despesa == "Roupa Nova":
        vezes_roupa_nova += 1
        if mes not in acoes["roupa_nova_vezes"]:
            acoes["roupa_nova_vezes"].append(mes)
    elif nome_despesa == "Novo Hobbie":
        vezes_hobbie += 1
        if mes not in acoes["novo_hobbie_vezes"]:
            acoes["novo_hobbie_vezes"].append(mes)
    elif nome_despesa == "Ir ao cinema":
        vezes_cinema += 1
        if mes not in acoes["cinema_vezes"]:
            acoes["cinema_vezes"].append(mes)
    
    desenhar_ecra_jogo()

def selecionar_transporte(index):
    global escolhas
    
    escolhas[1] = index
    desenhar_ecra_jogo()

def desenhar_trocar_transportes():
    global frame

    clear_frame()

    espacamento_x = 10
    espacamento_y = 10
    largura_botao = 100
    altura_botao = 100

    inicio_x = (WINDOW_WIDTH - (3 * largura_botao + 2 * espacamento_x)) // 2
    inicio_y = 150

    for index in range(3):
        x = inicio_x + index * (largura_botao + espacamento_x)
        y = inicio_y + (altura_botao + espacamento_y)
        name = f"imagem{index+1+3}.png"
        image_tk = ImageTk.PhotoImage(imagens[name].resize((100, 100)) if name in imagens else None)
        botao = tk.Button(frame, image=image_tk, bg=UNSELECTED_COLOR, width=100, height=100, bd=0, \
                          command=lambda i=index+3: selecionar_transporte(i))
        botao.image = image_tk
        botao.place(x=x, y=y)
        botoes.append(botao)
    
    texto = tk.Label(frame, text="Seleciona o Transporte\n para qual queres trocar.", \
                         font=("Helvetica", 24), bg=BG_COLOR, fg="white")
    texto.place(relx=0.5, y=150, anchor="center")
    texto = tk.Label(frame, text="Transporte", \
                         font=("Helvetica", 24), bg=BG_COLOR, fg="#062F57")
    texto.place(x=265, y=132, anchor="center")

def selecionar_casa(index):
    global escolhas
    
    escolhas[0] = index
    desenhar_ecra_jogo()    

def desenhar_trocar_casas():
    global frame

    clear_frame()

    espacamento_x = 10
    espacamento_y = 10
    largura_botao = 100
    altura_botao = 100

    inicio_x = (WINDOW_WIDTH - (3 * largura_botao + 2 * espacamento_x)) // 2
    inicio_y = 150

    for index in range(3):
        x = inicio_x + index * (largura_botao + espacamento_x)
        y = inicio_y + (altura_botao + espacamento_y)
        name = f"imagem{index+1}.png"
        image_tk = ImageTk.PhotoImage(imagens[name].resize((100, 100)) if name in imagens else None)
        botao = tk.Button(frame, image=image_tk, bg=UNSELECTED_COLOR, width=100, height=100, bd=0, \
                          command=lambda i=index: selecionar_casa(i))
        botao.image = image_tk
        botao.place(x=x, y=y)
        botoes.append(botao)

    texto = tk.Label(frame, text="Seleciona a Habitação\n para qual queres trocar.", \
                         font=("Helvetica", 24), bg=BG_COLOR, fg="white")
    texto.place(relx=0.5, y=150, anchor="center")
    texto = tk.Label(frame, text="Habitação", \
                         font=("Helvetica", 24), bg=BG_COLOR, fg="#062F57")
    texto.place(x=265, y=132, anchor="center")

#=================================End Screen=================================
def desenhar_frame_final():
    global frame, saldo, comprou_telemovel

    clear_frame()

    if saldo < 0:
        textop = tk.Label(frame, text="Perdeste o Jogo!", font=("Helvetica", 31, "bold"), bg=BG_COLOR, fg="white")
        textop.place(relx=0.5, y=100, anchor="center")

        texto = tk.Label(frame, text="As tuas escolhas \nlevaram-te à falência!\n O teu saldo foi de:", \
                         font=("Helvetica", 18), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=200, anchor="center")
        textosaldo = tk.Label(frame, text=f"{saldo}€", font=("Helvetica", 56, "bold"), bg=BG_COLOR, fg="red")
        textosaldo.place(relx=0.5, y=350, anchor="center")
    else:
        textop = tk.Label(frame, text="Ganhaste o Jogo!", font=("Helvetica", 31, "bold"), bg=BG_COLOR, fg="white")
        textop.place(relx=0.5, y=100, anchor="center")
        textosaldo = tk.Label(frame, text=f"{saldo}€", font=("Helvetica", 56, "bold"), bg=BG_COLOR, fg="#40D81A")
        textosaldo.place(relx=0.5, y=350, anchor="center")
    
    if saldo <1000:
        texto = tk.Label(frame, text="Não conseguiste guardar\n muito dinheiro, cuidado\n com as tuas escolhas!", \
                         font=("Helvetica", 18), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=200, anchor="center")
    elif saldo >= 2000:
        texto = tk.Label(frame, text="Conseguiste guardar\n uma quantia favorável de\n dinheiro, continua com\n as tuas boas estratégias!", \
                         font=("Helvetica", 18), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=200, anchor="center")
    elif saldo >= 1000 and saldo < 2000:
        texto = tk.Label(frame, text="Conseguiste guardar\n algum dinheiro, estás\n num bom caminho!", \
                         font=("Helvetica", 18), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=200, anchor="center")
    
    if comprou_telemovel == True:
        texto = tk.Label(frame, text="Cuidado com as\n compras impulsivas!", font=("Helvetica", 18), bg=BG_COLOR, fg="white")
        texto.place(relx=0.5, y=450, anchor="center")
        texto = tk.Label(frame, text="Cuidado", font=("Helvetica", 18), bg=BG_COLOR, fg="orange")
        texto.place(x=140, y=435, anchor="center")


    botao_voltar_a_jogar = tk.Button(frame, text= "     Voltar a Jogar     ", font=("Helvetica", 22, "bold"), bg="#014B94", fg="white"\
                                     , bd=0, activebackground="white", activeforeground="black", command=desenhar_ecra_escolhas)
    botao_voltar_a_jogar.place(relx=0.5, y=540, anchor="center")

    escrever_json()

if __name__ == "__main__":
    # Criar a janela principal com dimensões de ecrã Android (360x640)
    root = tk.Tk()
    root.title(GAME_TITLE)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)  # Bloquear redimensionamento

    frame = tk.Frame(root, bg=BG_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_propagate(False)

    images_path = "imagens"

    imagens = {}  # Dicionário para armazenar as imagens carregadas

    # Carregar as imagens do jogo
    for img in os.listdir(images_path):
        img_path = os.path.join(images_path, img)
        try:
            imagens[img] = Image.open(img_path)
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")

    # Iniciar o ecrã principal
    desenhar_ecra_inicial()

    # Iniciar a interface
    root.mainloop()
