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


## Instruction de doctest ##
# def initialize():
#     """ lance les tests pour l'allumage
#     >>> os.path.exists(Path('./data'))
#     True
#     >>> portefeuille, date, dates_fin = ['ATOS','AIRBUS','0P00000LT0.F','COX.PA','PHARMAGESTINTERACT','CM-CIC OBLI ISR'], [], []
#     >>> selecteur = Selecteur(portefeuille, date, dates_fin)
#     Selector
#     >>> selecteur
#     {'ATOS': 'ATO.PA', 'AIRBUS': 'AIR.PA', 'PHARMAGESTINTERACT': 'PHA.PA', 'CM-CIC OBLI ISR': '0P0000Q1L3.F', 'CAC 40': '^FCHI', 'DAX': '^GDAXI', 'NASDAQ': '^IXIC', 'CM-CIC GLOBAL EMERGING MARKETS (RC)': '0P00000LT0.F', 'NICOX': 'COX.PA'}
#     """

def main(): 

    # 0 pour PEA et PME, 5 pour All, 1 pour PEA, 2 pour PME', 3 pour FONDS, 4 pour Bitcoin
    titres = ['0'] # Liste de titre, voir data/listes.py ou entrer un nombre entre 0 et 4

    # Date de début d’observation par défaut 10 ans
    dates_debut = [] # La date de début de l’achat du portefeuille (titres groupés, action non-individuelle)

    # Date de fin d’observation, par défaut aujourd’hui, à partir de la fin de séance, sauf si selecteur contient ACTU
    dates_fin = [] # La date de fine
    
# Boucle d’alarme pour laisser le programme en attente de fin de séance en automatique
   # while pd.to_datetime(datetime.now().strftime('%Y-%m-%d ')+ '18:05:01') > datetime.now():
    #    time.sleep(1)
    #
    selecteur = Selecteur(titres, dates_debut, dates_fin, 'MAJ') # Valeur à 15 minutes si le dernier paramètre est ACTU

    selecteur.portefeuille() # Crée un objet structuré pour automatisation des requêtes en base de données

    portefeuille = Portefeuille(selecteur)
    analyse = Analyse(portefeuille)
    analyse.math_finance()
    analyse.to_txt()
    analyse.to_xlsx()
    
    
     
    report = Report(analyse)    
    report.plot()
    report.create()
    report.compiler()
    
    
    #facteur = Facteur()
    #destinataires = ['toto@titi.fr']
    #for dest in destinataires:
    #    facteur.send(dest)
    del selecteur, portefeuille, analyse, report
    # Boucle pour lancer une mise à jour à la bonne heure
    print('out')
    

if __name__ == "__main__":
    main()
    
