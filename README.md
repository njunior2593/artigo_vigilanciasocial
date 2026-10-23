# Priorização territorial dos CRAS de Sorocaba/SP — TOPSIS × MAVT

Código e dados do artigo de TCC (Serviço Social) sobre o uso de métodos multicritério
na Vigilância Socioassistencial.

## Fonte dos dados
SOROCABA. Secretaria da Cidadania. Vigilância Socioassistencial. *Painel Cadastro Único – Novembro de 2025*.
Disponível em: https://vigilanciasocial.com.br/. Acesso em: [DATA].

Dados **públicos, agregados por território de CRAS e não identificáveis**.
O território Sul Leste corresponde ao antigo CRAS João Romão.
A área (km²) foi estimada por: PcD total ÷ PcD por km².

## Estrutura
| Caminho | Conteúdo |
|---|---|
| `dados/criterios_cras_nov2025.csv` | Valores dos critérios C1–C8 por território |
| `dados/painel_original/` | Cópia arquivada do painel (adicionar PDF/XLSX com data de acesso) |
| `analise.py` | TOPSIS, modelo aditivo (MAVT), cenários de sensibilidade e Spearman |
| `resultados/` | Tabelas geradas pelo script |

## Critérios
C1 extrema pobreza · C2 pobreza · C3 crianças 0–6/km² · C4 % idosos 65+ · C5 % PcD ·
C6 precariedade habitacional · C7 não ocupação · C8 famílias vulneráveis/km²
(todos do tipo benefício; pesos base 0,25 · 0,12 · 0,20 · 0,12 · 0,15 · 0,08 · 0,05 · 0,03).

## Como reproduzir
```bash
pip install -r requirements.txt
python analise.py
```
