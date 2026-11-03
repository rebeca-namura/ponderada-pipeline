# Ponderada CC08: do pipeline ao deadlock

**Aluna:** Rebeca Sbroglio

Análise de arquitetura, pipeline, processos/threads, semáforos e deadlock aplicada à pulseira sensorial Tato, com a decisão de CTO.

## Estrutura

```
.
├── README.md
├── .gitignore
└── ponderada/
    ├── ponderada-tato.md   # Parte A (A1–A5) e Parte B (memorando do CTO)
    ├── codigo/             # questão A4 (produtor/consumidor, N = 7)
    │   ├── comum.py        # parâmetros, métricas e tabela de resultados
    │   ├── versao1.py      # sem sincronização (contador + espera ocupada)
    │   ├── versao2.py      # semáforos vazio / cheio / mutex
    │   └── versao3.py      # semáforos com a ordem trocada (deadlock)
    └── img/                # prints usados no ponderada-tato.md
```

## Como rodar a A4

Requisito: Python 3.8+ (só biblioteca padrão). Os comandos são executados a partir da pasta `ponderada/codigo`:

```bash
cd ponderada/codigo
```

| Versão | Comando | O que esperar |
|---|---|---|
| 1 - sem sincronização | `python versao1.py` | 3 execuções com amostras perdidas e duplicadas |
| 2 - com semáforos | `python versao2.py` | 3 execuções com 20.000 consumidas, 0 perdidas, 0 duplicadas |
| 3 - ordem trocada | `python versao3.py` | 3 execuções que travam (deadlock detectado após 1 s) |

Cada comando executa a versão 3 vezes com 20.000 amostras e imprime uma tabela com amostras consumidas, perdidas, duplicadas e se travou. No Linux/macOS, use `python3` no lugar de `python`.
