import numpy as np

ABATTEMENT_MIN, ABATTEMENT_MAX = 509, 14555

def revenu_net(revenu):
    revenu = np.asarray(revenu, dtype=float)
    abattement = np.minimum(np.clip(revenu * 0.10, ABATTEMENT_MIN, ABATTEMENT_MAX), revenu)
    return revenu - abattement

def impot(net, parts, decote_forfait):
    q = net / parts
    tax = parts * (
        (np.maximum(q - 11600, 0) - np.maximum(q - 29579, 0)) * 0.11
        + (np.maximum(q - 29579, 0) - np.maximum(q - 84577, 0)) * 0.30
        + (np.maximum(q - 84577, 0) - np.maximum(q - 181917, 0)) * 0.41
        + np.maximum(q - 181917, 0) * 0.45
    )
    decote = np.maximum(decote_forfait - tax * 0.4525, 0)
    return np.maximum(tax - decote, 0)

def calculate_tax_vectorized(revenu):
    return impot(revenu_net(revenu), parts=1, decote_forfait=897)

def calculate_tax_couple_vectorized(revenu_1, revenu_2):
    net = revenu_net(revenu_1) + revenu_net(revenu_2)
    return impot(net, parts=2, decote_forfait=1483)

def calculate_tax(revenu):
    return float(calculate_tax_vectorized(revenu))

def calculate_tax_couple(revenu_1, revenu_2):
    return float(calculate_tax_couple_vectorized(revenu_1, revenu_2))