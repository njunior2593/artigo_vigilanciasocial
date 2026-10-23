"""Priorizacao territorial dos CRAS de Sorocaba/SP: TOPSIS x modelo aditivo (MAVT).

Uso:  python analise.py
Entrada: dados/criterios_cras_nov2025.csv
Saidas:  resultados/*.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

BASE = Path(__file__).parent
CRIT = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
W_BASE = np.array([0.25, 0.12, 0.20, 0.12, 0.15, 0.08, 0.05, 0.03])


def topsis(X, w):
    """TOPSIS (Hwang e Yoon, 1981), todos os criterios do tipo beneficio."""
    V = X / np.sqrt((X ** 2).sum(axis=0)) * w
    d_pos = np.sqrt(((V - V.max(axis=0)) ** 2).sum(axis=1))
    d_neg = np.sqrt(((V - V.min(axis=0)) ** 2).sum(axis=1))
    return d_pos, d_neg, d_neg / (d_pos + d_neg)


def mavt(X, w):
    """Modelo aditivo com funcoes de valor lineares (min-max)."""
    v = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    return v @ w


def sem(w, excluir):
    """Zera os criterios excluidos e redistribui os pesos proporcionalmente."""
    w = w.copy()
    w[[CRIT.index(c) for c in excluir]] = 0
    return w / w.sum()


def posicao(score):
    return pd.Series(score).rank(ascending=False, method="min").astype(int).values


CENARIOS = {
    "A_base": W_BASE,
    "B_pesos_iguais": np.full(8, 1 / 8),
    "C_sem_densidades": sem(W_BASE, ["C3", "C8"]),
    "D_sem_redundancias": sem(W_BASE, ["C2", "C8"]),
}


def main():
    df = pd.read_csv(BASE / "dados" / "criterios_cras_nov2025.csv")
    X = df[CRIT].to_numpy(float)
    out = BASE / "resultados"
    out.mkdir(exist_ok=True)

    # Ranking TOPSIS (cenario base)
    dp, dn, ci = topsis(X, W_BASE)
    rk = pd.DataFrame({"territorio": df.territorio, "D_pos": dp, "D_neg": dn,
                       "Ci": ci, "posicao": posicao(ci)}).sort_values("posicao")
    rk.round(4).to_csv(out / "ranking_topsis_base.csv", index=False)

    # Sensibilidade (posicoes no TOPSIS)
    sens = pd.DataFrame({"territorio": df.territorio})
    for nome, w in CENARIOS.items():
        sens[nome] = posicao(topsis(X, w)[2])
    sens.sort_values("A_base").to_csv(out / "sensibilidade_topsis.csv", index=False)
    pd.DataFrame(CENARIOS, index=CRIT).round(3).to_csv(out / "pesos_cenarios.csv")

    # TOPSIS x MAVT (cenario base)
    v = mavt(X, W_BASE)
    comp = pd.DataFrame({"territorio": df.territorio, "Ci_topsis": ci,
                         "pos_topsis": posicao(ci), "V_mavt": v,
                         "pos_mavt": posicao(v)}).sort_values("pos_topsis")
    comp.round(4).to_csv(out / "topsis_x_mavt.csv", index=False)
    rho, p = spearmanr(ci, v)

    print(rk.round(4).to_string(index=False), "\n")
    print(sens.sort_values("A_base").to_string(index=False), "\n")
    print(comp.round(4).to_string(index=False))
    print(f"\nSpearman TOPSIS x MAVT: rho = {rho:.3f} (p = {p:.3f})")


if __name__ == "__main__":
    main()
