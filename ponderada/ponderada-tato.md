**Nome completo:** Rebeca Sbroglio | **D1 = 6** | **D2 = 4** | **N = 7**

# Ponderada CC08: do pipeline ao deadlock (pulseira Tato)

## Parâmetros individuais

| Item | Conta | Valor |
|---|---|---|
| Letras do primeiro nome | R-e-b-e-c-a | 6 |
| Letras do nome completo | Rebeca (6) + Sbroglio (8) | 14 |
| **D1** | 6 (menor que 10) | **6** |
| **D2** | último dígito de 14 | **4** |
| **IC** (instruções por amostra) | 100.000 + 20.000 × 4 | **180.000** |
| **m** (taxa de falta na L1 do SoC) | 3% + 0,5% × 6 | **6% = 0,06** |
| **N** (tamanho do buffer) | 3 + (4 mod 5) = 3 + 4 | **7** |

Requisito: cada amostra processada em **≤ 5 ms** (amostras chegam a cada 10 ms).

---

# Parte A: o problema técnico
