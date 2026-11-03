"""
comum.py - Utilitários compartilhados pelas três versões da questão A4.

Ponderada CC08 (pulseira Tato) - Rebeca Sbroglio.

Define os parâmetros da simulação (N, total de amostras, timeout de
travamento), a função que calcula as métricas de uma execução
(consumidas, perdidas, duplicadas) e a função que executa uma versão
várias vezes e imprime a tabela de resultados.
"""

import sys
import time

# Garante acentos corretos no terminal do Windows
sys.stdout.reconfigure(encoding="utf-8")

# D2 = 4  ->  N = 3 + (D2 mod 5) = 3 + 4 = 7
N = 7
TOTAL_AMOSTRAS = 20_000
TIMEOUT_TRAVAMENTO = 1.0  # segundos sem receber nada = travamento
EXECUCOES = 3


def calcular_metricas(consumidas, total=TOTAL_AMOSTRAS):
    """
    Calcula as métricas de uma execução a partir do que o consumidor recebeu.

    Parâmetros:
        consumidas (list[int]): amostras na ordem em que o consumidor as leu.
        total (int): quantidade de amostras que o produtor deveria gerar.

    Retorno:
        dict com as chaves:
            'consumidas' -> número total de leituras feitas pelo consumidor;
            'perdidas'   -> amostras 0..total-1 que nunca foram lidas;
            'duplicadas' -> leituras repetidas de uma amostra já lida.

    Funcionamento:
        Uma amostra é perdida se o seu número não aparece em `consumidas`.
        Cada leitura além da primeira de um mesmo número conta como duplicada.
        Leituras de posições nunca escritas (valor None) também contam como
        duplicadas, pois são lixo entregue ao motor.
    """
    vistas = set()
    duplicadas = 0
    for amostra in consumidas:
        if amostra is None or amostra in vistas:
            duplicadas += 1
        else:
            vistas.add(amostra)
    perdidas = sum(1 for i in range(total) if i not in vistas)
    return {
        "consumidas": len(consumidas),
        "perdidas": perdidas,
        "duplicadas": duplicadas,
    }


def rodar_experimento(nome_versao, executar_uma_vez, execucoes=EXECUCOES):
    """
    Executa uma versão do produtor/consumidor várias vezes e imprime a tabela.

    Parâmetros:
        nome_versao (str): título exibido no cabeçalho da saída.
        executar_uma_vez (callable): função sem argumentos que roda uma
            execução completa e retorna (lista_consumidas, travou: bool).
        execucoes (int): quantas vezes repetir o experimento.

    Retorno:
        list[dict]: métricas de cada execução, já com a chave 'travou'.

    Funcionamento:
        Para cada execução mede o tempo, calcula as métricas com
        calcular_metricas() e imprime uma linha da tabela.
    """
    print(f"=== {nome_versao} | N = {N} | {TOTAL_AMOSTRAS} amostras ===")
    print(f"{'Exec':<6}{'Consumidas':>12}{'Perdidas':>10}{'Duplicadas':>12}"
          f"{'Travou':>8}{'Tempo (s)':>11}")
    resultados = []
    for i in range(1, execucoes + 1):
        inicio = time.perf_counter()
        consumidas, travou = executar_uma_vez()
        duracao = time.perf_counter() - inicio
        m = calcular_metricas(consumidas)
        m["travou"] = travou
        resultados.append(m)
        print(f"{i:<6}{m['consumidas']:>12}{m['perdidas']:>10}"
              f"{m['duplicadas']:>12}{'sim' if travou else 'não':>8}"
              f"{duracao:>11.2f}")
    return resultados
