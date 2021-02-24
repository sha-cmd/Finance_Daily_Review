# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 06:22:16 2020
Ce programme analyse et crée un rapport financier
@author: romain Boyrie
"""

from objects.analyse import Analyse
from objects.portefeuille import Portefeuille
from objects.selecteur import Selecteur
from tex.reports import Report

# Instruction de doctest ##
"""
def initialize():
    lance les tests pour l'allumage
    >>> os.path.exists(Path('./data'))
    True
    >>> portefeuille, date, dates_fin = ['ATOS','AIRBUS','0P00000LT0.F','COX.PA','PHARMAGESTINTERACT','CM-CIC OBLI ISR'], [], []
    >>> selecteur = Selecteur(portefeuille, date, dates_fin)
    Selector
    >>> selecteur
    {'ATOS': 'ATO.PA', 'AIRBUS': 'AIR.PA', 'PHARMAGESTINTERACT': 'PHA.PA', 'CM-CIC OBLI ISR': '0P0000Q1L3.F', 'CAC 40': '^FCHI', 'DAX': '^GDAXI', 'NASDAQ': '^IXIC', 'CM-CIC GLOBAL EMERGING MARKETS (RC)': '0P00000LT0.F', 'NICOX': 'COX.PA'
"""


def main():
    # 0 pour PEA et PME, 5 pour All, 1 pour PEA, 2 pour PME', 3 pour FONDS, 4 pour Bitcoin
    titres = ['0']  # Liste de titre, voir data/listes.py ou entrer un nombre entre 0 et 4

    # Date de début d’observation par défaut 10 ans
    dates_debut = []  # La date de début de l’achat du portefeuille (titres groupés, action non-individuelle)

    # Date de fin d’observation, par défaut aujourd’hui, à partir de la fin de séance, sauf si selecteur contient ACTU
    dates_fin = []  # La date de fine

    # Boucle d’alarme pour laisser le programme en attente de fin de séance en automatique
    """
   while pd.to_datetime(datetime.now().strftime('%Y-%m-%d ')+ '18:05:01') > datetime.now():
       time.sleep(1)
    """

    # Launch of the command to fetch necessary data and store it locally if needed
    selector = Selecteur(titres, dates_debut, dates_fin, 'MAJ')

    # Sort names of portfolio values in memory to accomplish loops of requesting
    selector.creer_portefeuille()

    # Create a unique dictionary for all values
    portefeuille = Portefeuille(selector)

    # Load historical data, then make operations (beta, ror…, risk, monte carlo simulation)
    analyse = Analyse(portefeuille) # Huge amount of memory consumability
    analyse.math_finance() # Mathematics operation
    analyse.to_txt() # For plain text presentation
    analyse.to_xlsx() # Excel presentation

    # Build of a pdf report by the use of Latex Compiler
    # Can be comment if you do not have that compiler on your system
    report = Report(analyse) # Use some extra files in xlsx to complete the information
    report.plot() # Creation of all graphics
    report.create() # Creation of the tex file
    report.compiler() # Compilation (2 compilations are required to update the summary)

    # Send excel file to a list of contact
    """
    facteur = Facteur()
    destinataires = ['toto@titi.fr']
    for dest in destinataires:
       facteur.send(dest)
    """

    # Freed memory, not always necessary in Python
    del selector, portefeuille, analyse, report

    # The final message
    print('Thank you for using this program')


if __name__ == "__main__":
    main()
