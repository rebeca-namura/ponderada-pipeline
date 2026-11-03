"""
versao1.py - A4, Versão 1: produtor/consumidor SEM sincronização.

Ponderada CC08 (pulseira Tato) - Rebeca Sbroglio.

A thread do sensor (produtora) gera amostras 0, 1, 2, ... e a thread do
motor (consumidora) as retira de um buffer circular de N posições. A única
coordenação é um contador compartilhado de posições ocupadas, verificado com
espera ocupada. Entre ler e escrever o contador há um time.sleep(0), que
força a troca de thread no pior momento e faz a condição de corrida aparecer.

Se o consumidor ficar TIMEOUT_TRAVAMENTO segundos sem receber nada enquanto
o produtor ainda não terminou, a execução é encerrada como travamento.

Uso: python versao1.py
"""

import threading
import time

from comum import N, TOTAL_AMOSTRAS, TIMEOUT_TRAVAMENTO, rodar_experimento


def executar_uma_vez():
    """
    Roda uma execução completa da versão sem sincronização.

    Parâmetros:
        nenhum (usa N, TOTAL_AMOSTRAS e TIMEOUT_TRAVAMENTO de comum.py).

    Retorno:
        tuple(list, bool): lista das amostras lidas pelo consumidor, na
        ordem de leitura, e True se a execução terminou por travamento.

    Funcionamento:
        Cria o buffer, o contador e as duas threads, inicia ambas e espera
        o consumidor terminar. O produtor é daemon para não segurar o
        programa caso fique preso na espera ocupada.
    """
    buffer = [None] * N
    estado = {"contador": 0, "produtor_terminou": False, "parar": False}
    consumidas = []
    travou = [False]

    def produtor():
        """
        Thread do sensor: escreve TOTAL_AMOSTRAS amostras no buffer.

        Parâmetros: nenhum (usa as variáveis da função externa).
        Retorno: nenhum.

        Funcionamento: espera ocupada enquanto o contador indica buffer
        cheio; depois escreve a amostra na posição `entrada` e incrementa o
        contador em duas etapas (ler, ceder a CPU, escrever) - essa é a
        região crítica desprotegida.
        """
        entrada = 0
        for amostra in range(TOTAL_AMOSTRAS):
            while estado["contador"] >= N:          # espera ocupada
                if estado["parar"]:
                    return
                time.sleep(0)
            buffer[entrada] = amostra
            entrada = (entrada + 1) % N
            lido = estado["contador"]               # lê o contador
            time.sleep(0)                           # interrompida aqui
            estado["contador"] = lido + 1           # escreve o contador
        estado["produtor_terminou"] = True

    def consumidor():
        """
        Thread do motor: retira amostras do buffer até o produtor acabar.

        Parâmetros: nenhum (usa as variáveis da função externa).
        Retorno: nenhum (preenche `consumidas` e `travou`).

        Funcionamento: espera ocupada enquanto o contador indica buffer
        vazio. Se esperar mais de TIMEOUT_TRAVAMENTO segundos com o produtor
        ainda ativo, marca travamento. Lê a posição `saida` e decrementa o
        contador em duas etapas, com sleep(0) no meio.
        """
        saida = 0
        while True:
            inicio_espera = time.perf_counter()
            while estado["contador"] <= 0:          # espera ocupada
                if estado["produtor_terminou"]:
                    return
                if time.perf_counter() - inicio_espera > TIMEOUT_TRAVAMENTO:
                    travou[0] = True
                    estado["parar"] = True
                    return
                time.sleep(0)
            consumidas.append(buffer[saida])
            saida = (saida + 1) % N
            lido = estado["contador"]               # lê o contador
            time.sleep(0)                           # interrompida aqui
            estado["contador"] = lido - 1           # escreve o contador

    t_prod = threading.Thread(target=produtor, daemon=True)
    t_cons = threading.Thread(target=consumidor)
    t_prod.start()
    t_cons.start()
    t_cons.join()
    estado["parar"] = True
    return consumidas, travou[0]


if __name__ == "__main__":
    rodar_experimento("Versão 1 - sem sincronização", executar_uma_vez)
