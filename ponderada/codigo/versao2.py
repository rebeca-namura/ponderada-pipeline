"""
versao2.py - A4, Versão 2: produtor/consumidor COM semáforos.

Ponderada CC08 (pulseira Tato) - Rebeca Sbroglio.

Mesmo cenário da versão 1, mas a coordenação é feita por três semáforos:
    vazio -> começa em N: conta as posições livres do buffer;
    cheio -> começa em 0: conta as posições ocupadas;
    mutex -> começa em 1: exclusão mútua no acesso ao buffer e aos índices.

Ordem correta: cada thread espera primeiro pelo semáforo de contagem
(vazio/cheio) e só depois pelo mutex. As esperas do consumidor usam timeout
de TIMEOUT_TRAVAMENTO segundos para detectar travamento.

Uso: python versao2.py
"""

import threading

from comum import N, TOTAL_AMOSTRAS, TIMEOUT_TRAVAMENTO, rodar_experimento


def executar_uma_vez():
    """
    Roda uma execução completa da versão com semáforos (ordem correta).

    Parâmetros:
        nenhum (usa N, TOTAL_AMOSTRAS e TIMEOUT_TRAVAMENTO de comum.py).

    Retorno:
        tuple(list, bool): amostras lidas pelo consumidor, na ordem, e True
        se o consumidor ficou TIMEOUT_TRAVAMENTO segundos sem conseguir ler.

    Funcionamento:
        Cria o buffer, os três semáforos e as duas threads; espera o
        consumidor ler TOTAL_AMOSTRAS amostras ou detectar travamento.
    """
    buffer = [None] * N
    vazio = threading.Semaphore(N)
    cheio = threading.Semaphore(0)
    mutex = threading.Semaphore(1)
    consumidas = []
    travou = [False]

    def produtor():
        """
        Thread do sensor: produz TOTAL_AMOSTRAS amostras.

        Parâmetros: nenhum. Retorno: nenhum.

        Funcionamento: wait(vazio) garante que há posição livre;
        wait(mutex) garante acesso exclusivo ao buffer; escreve a amostra;
        signal(mutex) libera o buffer; signal(cheio) avisa o consumidor.
        """
        entrada = 0
        for amostra in range(TOTAL_AMOSTRAS):
            vazio.acquire()          # wait(vazio)
            mutex.acquire()          # wait(mutex)
            buffer[entrada] = amostra
            entrada = (entrada + 1) % N
            mutex.release()          # signal(mutex)
            cheio.release()          # signal(cheio)

    def consumidor():
        """
        Thread do motor: consome TOTAL_AMOSTRAS amostras.

        Parâmetros: nenhum. Retorno: nenhum (preenche `consumidas`/`travou`).

        Funcionamento: wait(cheio) com timeout garante que há amostra;
        wait(mutex) com timeout garante exclusão mútua; lê a amostra;
        signal(mutex); signal(vazio) devolve a posição ao produtor.
        Se algum wait estourar o timeout, registra travamento.
        """
        saida = 0
        for _ in range(TOTAL_AMOSTRAS):
            if not cheio.acquire(timeout=TIMEOUT_TRAVAMENTO):   # wait(cheio)
                travou[0] = True
                return
            if not mutex.acquire(timeout=TIMEOUT_TRAVAMENTO):   # wait(mutex)
                travou[0] = True
                return
            consumidas.append(buffer[saida])
            saida = (saida + 1) % N
            mutex.release()          # signal(mutex)
            vazio.release()          # signal(vazio)

    t_prod = threading.Thread(target=produtor, daemon=True)
    t_cons = threading.Thread(target=consumidor)
    t_prod.start()
    t_cons.start()
    t_cons.join()
    return consumidas, travou[0]


if __name__ == "__main__":
    rodar_experimento("Versão 2 - com semáforos", executar_uma_vez)
