import random
from banco_questoes import questoes_originais


def transforma_base(questoes_originais):
    niveis = {}
    lista_facil = []
    lista_medio = []
    lista_dificil = []
    for questao in questoes_originais:
        if questao["nivel"] == "facil":
            lista_facil.append(questao)
        elif questao["nivel"] == "medio":
            lista_medio.append(questao)
        elif questao["nivel"] == "dificil":
            lista_dificil.append(questao)

    if lista_facil != []:
        niveis["facil"] = lista_facil
    if lista_medio != []:
        niveis["medio"] = lista_medio
    if lista_dificil != []:
        niveis["dificil"] = lista_dificil
        
    return niveis



def valida_questao(questao):
    erros = {}

    chaves_necessarias = ['titulo', 'nivel', 'opcoes', 'correta']

    
    for chave in chaves_necessarias:
        if chave not in questao:
            erros[chave] = 'nao_encontrado'

    
    if len(questao) != 4:
        erros['outro'] = 'numero_chaves_invalido'

    
    if 'titulo' in questao:
        titulo = questao['titulo']
        if titulo.strip() == '':
            erros['titulo'] = 'vazio'

    
    if 'nivel' in questao:
        nivel = questao['nivel']
        if nivel != 'facil' and nivel != 'medio' and nivel != 'dificil':
            erros['nivel'] = 'valor_errado'

    
    if 'opcoes' in questao:
        opcoes = questao['opcoes']

        if len(opcoes) != 4:
            erros['opcoes'] = 'tamanho_invalido'
        else:
            tem_A = False
            tem_B = False
            tem_C = False
            tem_D = False
            extras = False

            for chave in opcoes:
                if chave == 'A':
                    tem_A = True
                elif chave == 'B':
                    tem_B = True
                elif chave == 'C':
                    tem_C = True
                elif chave == 'D':
                    tem_D = True
                else:
                    extras = True

            if not (tem_A and tem_B and tem_C and tem_D) or extras:
                erros['opcoes'] = 'chave_invalida_ou_nao_encontrada'
            else:
                op_vazias = {}
                for letra in ['A', 'B', 'C', 'D']:
                    if opcoes[letra].strip() == '':
                        op_vazias[letra] = 'vazia'
                if len(op_vazias) > 0:
                    erros['opcoes'] = op_vazias

    
    if 'correta' in questao:
        correta = questao['correta']
        if correta != 'A' and correta != 'B' and correta != 'C' and correta != 'D':
            erros['correta'] = 'valor_errado'

    return erros


def valida_questoes(lista_questoes):
    resultado = []

    for questao in lista_questoes:
        erros_da_questao = valida_questao(questao)
        resultado.append(erros_da_questao)

    return resultado


def sorteia_questao(questoes,nivel):
    lista = questoes[nivel]
    sorteada = random.choice(lista)
    return sorteada


def sorteia_questao_inedita(questoes, nivel, questoes_sorteadas):
    while True:
        questao_sugerida = sorteia_questao(questoes, nivel)
        
        if questao_sugerida not in questoes_sorteadas:
            questoes_sorteadas.append(questao_sugerida)
            return questao_sugerida
        

def questao_para_texto(questao, id):
    cabecalho = f"{'-'*40}\nQUESTAO {id}\n\n{questao['titulo']}\n\nRESPOSTAS:\n"

    opcoes_formatadas = []

    for chave, valor in sorted(questao['opcoes'].items()):
        opcoes_formatadas.append(f"{chave}: {valor}")

    #junta as linhas das opções e separa com quebra de linha
    corpo_opcoes = '\n'.join(opcoes_formatadas)

    return cabecalho + corpo_opcoes

def gera_ajuda(questao):
    opcoes_incorretas = []
    chave_correta = questao['correta']

    for chave, valor_texto in questao['opcoes'].items():
        if chave != chave_correta:
            opcoes_incorretas.append(valor_texto)

    quantidade_de_dicas = random.randint(1, 2)
    
    if quantidade_de_dicas > len(opcoes_incorretas):
        quantidade_de_dicas = len(opcoes_incorretas)

    
    #random.sample: sorteia nomes garantindo que um mesmo item não vai repetir
    dicas_selecionadas = random.sample(opcoes_incorretas, k=quantidade_de_dicas)

    #str de saída
    texto_das_dicas = ' | '.join(dicas_selecionadas)
    
    return f"DICA:\nOpções certamente erradas: {texto_das_dicas}"

def inicia_jogo(banco_de_questoes):
    print("Olá! Você está na Fortuna DesSoft e terá a oportunidade de enriquecer!")
    nome_jogador = input("Qual seu nome?")

    print(f"\nOk {nome_jogador.upper()}, você tem direito a pular 3 vezes e 2 ajudas!")
    print('As opções de resposta são "A", "B", "C", "D", "ajuda", "pula" e "parar"!')
    input("\nAperte ENTER para continuar...")

    questoes_ja_sorteadas = []
    pulos = 3
    ajudas = 2
    premio_total = 0
    id_questao_atual = 0

    niveis = ['facil', 'medio', 'dificil']

    for nivel in niveis:
        print(f"\nO jogo já vai começar! Lá vem a primeira questão!")
        print(f"Vamos comecar com questões do nível {nivel.upper()}!")
        input("Aperte ENTER para continuar...")

        while True:
            questao_atual = sorteia_questao_inedita(banco_de_questoes, nivel, questoes_ja_sorteadas)
            
            if questao_atual is None:
                print(f"PARABÉNS, você zerou as questões do nível {nivel.upper()}!")
                break
            
            id_questao_atual += 1
            
            while True:
                print(questao_para_texto(questao_atual, id_questao_atual))
                resposta = input("Qual sua resposta?! ").upper()

                if resposta in ['A', 'B', 'C', 'D']:
                    if resposta == questao_atual['correta']:
                        premio_total += 1000
                        print(f"\nVocê acertou! Seu prêmio atual é de R$ {premio_total:.2f}")
                        input("Aperte ENTER para continuar...")
                        break
                    else:
                        print("\nQue pena! Você errou e vai sair sem nada :(")
                        return
                
                elif resposta == 'AJUDA':
                    if ajudas > 0:
                        ajudas -= 1
                        print(gera_ajuda(questao_atual))
                        print(f"Você ainda tem {ajudas} ajudas e {pulos} pulos.")
                        input("\nAperte ENTER para continuar...")
                    else:
                        print("Você não tem mais ajudas!")

                elif resposta == 'PULA':
                    if pulos > 0:
                        pulos -= 1
                        print(f"Ok, pulando... Você ainda tem {pulos} pulos.")
        
                        questoes_ja_sorteadas.append(questao_atual) 
                        break 
                    else:
                        print("Você não tem mais pulos!")
                
                elif resposta == 'PARAR':
                    print(f"\nOk! Você decidiu parar. Seu prêmio final é de R$ {premio_total:.2f}")
                    return
                
                else:
                    print("\nOpção inválida! As opções são 'A', 'B', 'C', 'D', 'ajuda', 'pula' ou 'parar'.")
                    input("Aperte ENTER para tentar novamente...")
    print(f"\nPARABÉNS {nome_jogador.upper()}! Você zerou o jogo e ganhou R$ {premio_total:.2f}!")

