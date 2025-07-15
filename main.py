

from funçoes_PL import (
    transforma_base,
    valida_questoes,
    sorteia_questao_inedita,
    questao_para_texto,
    gera_ajuda,
    inicia_jogo
)

from banco_questoes import questoes_originais

if __name__ == '__main__':

    banco_de_questoes = transforma_base(questoes_originais)
    
    inicia_jogo(banco_de_questoes)
