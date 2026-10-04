import numpy as np

def calculate_tax(revenue, tax_individual=True, quotient_familial=1):
    # Abattement de 10% sur le revenu imposable
    if revenue * 0.1 > 14555 :
        abbatement = 14555
    elif revenue * 0.1 < 509 :
        abbatement = 509
    else:
        abbatement = revenue * 0.1

    revenue -= abbatement 
    # print(f"Abbatement: {abbatement}")
    # print(f"Revenue imposable après abbatement: {revenue}")

    if quotient_familial != 1:
        revenue = revenue / quotient_familial

    if revenue <= 11600:
        tax = 0
    elif revenue <= 29579:
        tax = (revenue - 11600) * 0.11
    elif revenue <= 84577:
        tax = ((29579 - 11600) * 0.11) + (revenue - 29579) * 0.3
    elif revenue <= 181917:
        tax = ((29579 - 11600) * 0.11) + ((84577 - 29579) * 0.3) + ((revenue - 84577) * 0.41)
    else:
        tax = ((29579 - 11600) * 0.11) + ((84577 - 29579) * 0.3) + ((181917 - 84577) * 0.41) + ((revenue - 181917) * 0.45)

    if quotient_familial != 1:
            tax = tax * quotient_familial

    if tax_individual:
        decote_forfait = 897
    else :
        decote_forfait = 1483

    decote = max(decote_forfait - tax * 0.4525, 0)
    # print(f"Decote forfait: {decote_forfait}")
    # print(f"Taxe avant decote: {tax}")
    # print(f"Decote: {decote}")
    # print(f"Taxe après decote: {tax}")

    # Possible décote soit supérieure à la taxe donc on applique 0 si c'est le cas, pour éviter taxe négative
    if tax < decote:
        tax = 0
    else:
        tax = tax - decote

    # print(f"Taxe après decote: {tax}")

    return tax
    
def calculate_tax_vectorized(revenue_array, tax_individual=True, quotient_familial=1):
    tax = np.zeros_like(revenue_array)

    # Abattement de 10 % borné entre 509 et 14 555, sans dépasser le revenu
    abattement = np.clip(revenue_array * 0.10, 509, 14555)
    abattement = np.minimum(abattement, revenue_array)
    revenue_array = revenue_array - abattement

    # Prise en compte du quotient familial
    if quotient_familial != 1:
        revenue_array = revenue_array / quotient_familial

    # Définition des tranches d'imposition
    tranche_1 = (revenue_array > 11600) & (revenue_array <= 29579)
    tranche_2 = (revenue_array > 29579) & (revenue_array <= 84577)
    tranche_3 = (revenue_array > 84577) & (revenue_array <= 181917)
    tranche_4 = (revenue_array > 181917)

    # Calcul du montant de l'impôt pour chaque tranche
    tax[tranche_1] = (revenue_array[tranche_1] - 11600) * 0.11
    tax[tranche_2] = ((29579 - 11600) * 0.11) + (revenue_array[tranche_2] - 29579) * 0.3
    tax[tranche_3] = ((29579 - 11600) * 0.11) + ((84577 - 29579) * 0.3) + ((revenue_array[tranche_3] - 84577) * 0.41)
    tax[tranche_4] = ((29579 - 11600)  * 0.11) + ((84577 - 29579) * 0.3) + ((181917 - 84577) * 0.41) + ((revenue_array[tranche_4] - 181917) * 0.45)

    # Prise en compte du quotient familial pour le calcul final de l'impôt
    if quotient_familial != 1:
        tax = tax * quotient_familial

    # Application de la décote
    if tax_individual:
        decote_forfait = 897
    else :
        decote_forfait = 1483

    decote = np.maximum(decote_forfait - tax * 0.4525, 0)

    # Possible décote soit supérieure à la taxe donc on applique 0 si c'est le cas, pour éviter taxe négative
    tax = np.maximum(tax - decote, 0)

    return tax