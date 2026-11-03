"""
versao3.py - A4, Versão 3: semáforos com a ORDEM TROCADA no produtor.

Ponderada CC08 (pulseira Tato) - Rebeca Sbroglio.

Igual à versão 2, exceto que o produtor faz wait(mutex) ANTES de
wait(vazio). Quando o buffer enche, o produtor dorme em `vazio` segurando o
mutex; o consumidor, que precisaria do mutex para liberar uma posição, fica
bloqueado para sempre: deadlock. O consumidor detecta o travamento pelo
timeout de TIMEOUT_TRAVAMENTO segundos.

Uso: python versao3.py
"""

import threading

from comum import N, TOTAL_AMOSTRAS, TIMEOUT_TRAVAMENTO, rodar_experimento


def executar_uma_vez():
    """
    Roda uma execução completa da versão com a ordem dos waits trocada.

    Parâmetros:
        nenhum (usa N, TOTAL_AMOSTRAS e TIMEOUT_TRAVAMENTO de comum.py).

    Retorno:
        tuple(list, bool): amostras lidas pelo consumidor, na ordem, e True
        se o consumidor ficou TIMEOUT_TRAVAMENTO segundos sem conseguir ler.

    Funcionamento:
        Igual à versão 2. O produtor é daemon porque, no deadlock, ele
        fica bloqueado para sempre e não pode impedir o programa de sair.
    """
    buffer = [None] * N
    vazio = threading.Semaphore(N)
    cheio = threading.Semaphore(0)
    mutex = threading.Semaphore(1)
    consumidas = []
    travou = [False]

    def produtor():
        """
        Thread do sensor com a ordem errada: wait(mutex) antes de wait(vazio).

        Parâmetros: nenhum. Retorno: nenhum.

        Funcionamento: pega o mutex e só então verifica se há espaço. Com o
        buffer cheio, dorme em `vazio` sem soltar o mutex.
        """
        entrada = 0
        for amostra in range(TOTAL_AMOSTRAS):
            mutex.acquire()          # wait(mutex)  <- ordem trocada
            vazio.acquire()          # wait(vazio)
            buffer[entrada] = amostra
            entrada = (entrada + 1) % N
            mutex.release()          # signal(mutex)
            cheio.release()          # signal(cheio)

    def consumidor():
        """
        Thread do motor: idêntica à da versão 2.

        Parâmetros: nenhum. Retorno: nenhum (preenche `consumidas`/`travou`).

        Funcionamento: wait(cheio) e wait(mutex) com timeout; se algum
        estourar, registra travamento e encerra.
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
    rodar_experimento("Versão 3 - ordem trocada (mutex antes de vazio)",
                      executar_uma_vez)
