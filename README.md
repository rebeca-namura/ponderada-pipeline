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

O código usa só a biblioteca padrão do Python, então não é preciso instalar nenhum pacote.

### 1. Verifique se o Python 3 está instalado

Abra um terminal (no Windows: PowerShell ou Prompt de Comando; no Linux/macOS: Terminal) e digite:

```bash
python --version
```

A resposta deve ser `Python 3.8` ou mais nova. No Linux/macOS, se o comando não existir ou mostrar Python 2, use `python3 --version`. Nesse caso, troque `python` por `python3` em todos os comandos abaixo. Se o Python não estiver instalado, baixe em <https://www.python.org/downloads/>. No Windows, marque a opção **"Add Python to PATH"** durante a instalação.

### 2. Baixe o repositório e entre na pasta

```bash
git clone <URL-deste-repositório>
cd <nome-da-pasta-clonada>
```

Se você já tem a pasta no computador, basta navegar até ela com `cd`.

### 3. Rode cada versão com um único comando

Os comandos podem ser executados **na raiz do repositório**:

| Versão | Comando | O que esperar |
|---|---|---|
| 1 - sem sincronização | `python ponderada/codigo/versao1.py` | amostras perdidas e duplicadas (os números mudam a cada execução) |
| 2 - com semáforos | `python ponderada/codigo/versao2.py` | 20.000 consumidas, 0 perdidas, 0 duplicadas |
| 3 - ordem trocada | `python ponderada/codigo/versao3.py` | 0 consumidas e `Travou = sim` (deadlock detectado após 1 s) |

Também dá para entrar antes na pasta do código e rodar pelo nome do arquivo:

```bash
cd ponderada/codigo
python versao1.py
python versao2.py
python versao3.py
```

> No Prompt de Comando do Windows (cmd), as barras do caminho podem ser invertidas: `python ponderada\codigo\versao1.py`. No PowerShell, as duas formas funcionam.

### 4. Como ler a saída

Cada comando roda **3 execuções** de 20.000 amostras com buffer de N = 7 posições e imprime uma tabela como esta (exemplo da versão 2):

```
=== Versão 2 - com semáforos | N = 7 | 20000 amostras ===
Exec    Consumidas  Perdidas  Duplicadas  Travou  Tempo (s)
1            20000         0           0     não       0.09
2            20000         0           0     não       0.09
3            20000         0           0     não       0.09
```

| Coluna | Significado |
|---|---|
| `Exec` | número da execução (1 a 3) |
| `Consumidas` | quantas leituras o consumidor (motor) fez |
| `Perdidas` | amostras de 0 a 19.999 que nunca foram lidas |
| `Duplicadas` | leituras repetidas de uma amostra que já tinha sido lida |
| `Travou` | `sim` se o consumidor ficou 1 s sem receber nada |
| `Tempo (s)` | duração da execução |

A versão 1 termina em menos de 1 s, a versão 2 também, e a versão 3 leva cerca de 1 s por execução, que é o tempo até o travamento ser detectado. O programa encerra sozinho nos três casos, sem precisar de Ctrl+C.

### Problemas comuns

- **`ModuleNotFoundError: No module named 'comum'`**: o arquivo foi copiado sozinho para outra pasta. Os scripts `versaoX.py` precisam do `comum.py` na mesma pasta.
- **`python` não é reconhecido** (Windows): o Python não está no PATH. Reinstale marcando "Add Python to PATH", ou use o launcher `py`, como em `py ponderada/codigo/versao1.py`.
- **Acentos aparecendo como `�`**: o terminal não está em UTF-8. O código já força UTF-8 na saída; se ainda acontecer, rode `chcp 65001` no cmd antes do comando.
