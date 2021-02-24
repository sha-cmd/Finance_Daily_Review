#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 17:13:58 2020
Ce programme analyse et crée un rapport financier
@author: romain Boyrie
"""

#import sys
from data import listes
#from data.listes import YAHOO, BOURSORAMA, DBASE, MAJ, INV
from objects.titre import Action, Fonds, Indice, Bitcoin
from objects.singleton import SingletonType
class Selecteur(metaclass=SingletonType):
    
    def __init__(self, liste_de_titres, liste_de_dates_debut, liste_de_dates_arrivee, commande='DBASE'):
        print('Selector')
        self._commande = commande
        self._liste_de_titres = list()
        self._groupe_de_titres = dict()
        self._pea = listes.liste_action_pea()
        self._pme = listes.liste_action_pme()
        self._fonds = listes.liste_fonds()
        self._indices = listes.liste_indices()
        self._bitcoins = listes.liste_bitcoins()
        self._actions_pea = dict()
        self._actions_pme = dict()
        self._titres_fonds = dict()
        self._titres_indices = dict()
        self._titres_bitcoins = dict()
        #Objet Action,… Instancié
        self._groupe_pea = dict()
        self._groupe_pme = dict()
        self._groupe_fonds = dict()
        self._groupe_indices = dict()
        self._groupe_bitcoins = dict()
        #Nom et mnemo en liste
        self._liste_pea = list()
        self._liste_pme = list()
        self._liste_fonds = list()
        self._liste_indices = list()
        self._liste_bitcoins = list()
        self._liste_date_arrivee = list()

        # Lancement automatique pour tous les titres PEA et PEA-PME inscrits dans le dictionnaire (data/listes.py)
        if '0' in liste_de_titres:
            print('Action Selection')
            keys = []
            for key in self._pea.keys():
                keys.append(key) 
            for key in self._pme.keys():
                keys.append(key) 
            for key in self._indices.keys():
                keys.append(key) 
            if len(liste_de_dates_debut)==1:
                liste_de_dates_debut = [ele for ele in liste_de_dates_debut for i in range(len(keys))] 
            self._dates_achat = {keys[i]:liste_de_dates_debut[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_debut))}
            if len(liste_de_dates_arrivee)==1:
                liste_de_dates_arrivee = [ele for ele in liste_de_dates_arrivee for i in range(len(keys))] 
            self._dates_vente = {keys[i]:liste_de_dates_arrivee[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_arrivee))}
            self.collecteur_de_portefeuille(keys)

        # Lancement automatique pour tous les titres PEA grands groupes inscrits dans le dictionnaire (data/listes.py)
        elif '1' in liste_de_titres:
            print('All PEA')
            keys = []
            for key in self._pea.keys():
                keys.append(key) 
            for key in self._indices.keys():
                keys.append(key) 
            if len(liste_de_dates_debut)==1:
                liste_de_dates_debut = [ele for ele in liste_de_dates_debut for i in range(len(keys))] 
            self._dates_achat = {keys[i]:liste_de_dates_debut[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_debut))}
            if len(liste_de_dates_arrivee)==1:
                liste_de_dates_arrivee = [ele for ele in liste_de_dates_arrivee for i in range(len(keys))] 
            self._dates_vente = {keys[i]:liste_de_dates_arrivee[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_arrivee))}
            self.collecteur_de_portefeuille(keys)

        # Lancement automatique pour tous les titres PEA-PME inscrits dans le dictionnaire (data/listes.py)
        elif '2' in liste_de_titres:
            print('All PME')
            keys = []
            for key in self._pme.keys():
                keys.append(key) 
            for key in self._indices.keys():
                keys.append(key) 
            if len(liste_de_dates_debut)==1:
                liste_de_dates_debut = [ele for ele in liste_de_dates_debut for i in range(len(keys))] 
            self._dates_achat = {keys[i]:liste_de_dates_debut[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_debut))}
            if len(liste_de_dates_arrivee)==1:
                liste_de_dates_arrivee = [ele for ele in liste_de_dates_arrivee for i in range(len(keys))] 
            self._dates_vente = {keys[i]:liste_de_dates_arrivee[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_arrivee))}
            self.collecteur_de_portefeuille(keys)

        # Lancement automatique pour tous les titres Fonds en Assurance Vie inscrits dans le dictionnaire (data/listes.py)
        elif '3' in liste_de_titres:
            print('All FUNDS')
            keys = []
            for key in self._fonds.keys():
                keys.append(key) 
            for key in self._indices.keys():
                keys.append(key) 
            if len(liste_de_dates_debut)==1:
                liste_de_dates_debut = [ele for ele in liste_de_dates_debut for i in range(len(keys))] 
            self._dates_achat = {keys[i]:liste_de_dates_debut[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_debut))}
            if len(liste_de_dates_arrivee)==1:
                liste_de_dates_arrivee = [ele for ele in liste_de_dates_arrivee for i in range(len(keys))] 
            self._dates_vente = {keys[i]:liste_de_dates_arrivee[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_arrivee))}
            self.collecteur_de_portefeuille(keys)

        # Lancement automatique pour tous les titres de crypto-monnaies inscrits dans le dictionnaire (data/listes.py)
        elif '4' in liste_de_titres:
            print('All BITCOINS')
            keys = []
            for key in self._bitcoins.keys():
                keys.append(key) 
            for key in self._indices.keys():
                keys.append(key) 
            if len(liste_de_dates_debut)==1:
                liste_de_dates_debut = [ele for ele in liste_de_dates_debut for i in range(len(keys))] 
            self._dates_achat = {keys[i]:liste_de_dates_debut[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_debut))}
            if len(liste_de_dates_arrivee)==1:
                liste_de_dates_arrivee = [ele for ele in liste_de_dates_arrivee for i in range(len(keys))] 
            self._dates_vente = {keys[i]:liste_de_dates_arrivee[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_arrivee))}
            self.collecteur_de_portefeuille(keys)

        # Lancement automatique pour tous les titres inscrits dans le dictionnaire (data/listes.py)
        elif '5' in liste_de_titres:
            print('Total Selection')
            keys = []
            for key in self._pea.keys():
                keys.append(key) 
            for key in self._pme.keys():
                keys.append(key) 
            for key in self._fonds.keys():
                keys.append(key)
            for key in self._bitcoins.keys():
                keys.append(key)
            for key in self._indices.keys():
                keys.append(key)

            if len(liste_de_dates_debut)==1:
                liste_de_dates_debut = [ele for ele in liste_de_dates_debut for i in range(len(keys))]

            self._dates_achat = {keys[i]:liste_de_dates_debut[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_debut))}

            if len(liste_de_dates_arrivee)==1:
                liste_de_dates_arrivee = [ele for ele in liste_de_dates_arrivee for i in range(len(keys))]

            self._dates_vente = {keys[i]:liste_de_dates_arrivee[i] for i in range(0, len(keys)) if (len(keys) == len(liste_de_dates_arrivee))}
            self.collecteur_de_portefeuille(keys)

        else:

            if len(liste_de_dates_debut)==1:
                liste_de_dates_debut = [ele for ele in liste_de_dates_debut for i in range(len(liste_de_titres))]

            self._dates_achat = {liste_de_titres[i].upper():liste_de_dates_debut[i] for i in range(0, len(liste_de_titres)) if (len(liste_de_titres) == len(liste_de_dates_debut))}

            if len(liste_de_dates_arrivee)==1:
                liste_de_dates_arrivee = [ele for ele in liste_de_dates_arrivee for i in range(len(liste_de_titres))]

            self._dates_vente = {liste_de_titres[i].upper():liste_de_dates_arrivee[i] for i in range(0, len(liste_de_titres)) if (len(liste_de_titres) == len(liste_de_dates_arrivee))}

            # Si l’utilisateur demande de recharger les données historique du portefeuille
            if commande == 'RELOAD':
                pass
            #
            else:
                for key in self._indices.keys():
                    liste_de_titres.append(key)
            #
            self.collecteur_de_portefeuille(liste_de_titres)

    def collecteur_de_portefeuille(self, liste_de_titres):
        """
        Dictionnaire construit à partir de la liste_de_titres, cette liste
        peut contenir soit le noms soit le mnémonic, mais les clés seront
        toutes des noms et les valeurs des mnémonics en sortie.

        Returns
        -------
        Dict
            Ce dictionnaire permettra de récupérer les couples noms et Isin
            (mnémonics)

        """
        dictionnaire = dict()
        for titre_case in liste_de_titres:
            titre = titre_case.upper()
            if self._pea.get(titre) != None:
                #            print(self.pea.get(titre))
                dictionnaire.update({titre: self._pea.get(titre)})
                self._actions_pea.update({titre: self._pea.get(titre)})
            if self._pme.get(titre) != None:
                #             print(self.pme.get(titre))
                dictionnaire.update({titre: self._pme.get(titre)})
                self._actions_pme.update({titre: self._pme.get(titre)})
            if self._fonds.get(titre) != None:
                #              print(self.fonds.get(titre))
                dictionnaire.update({titre: self._fonds.get(titre)})
                self._titres_fonds.update({titre: self._fonds.get(titre)})
            if self._indices.get(titre) != None:
                dictionnaire.update({titre: self._indices.get(titre)})
                self._titres_indices.update({titre: self._indices.get(titre)})
            if self._bitcoins.get(titre) != None:
                dictionnaire.update({titre: self._bitcoins.get(titre)})
                self._titres_bitcoins.update({titre: self._bitcoins.get(titre)})
        pea_mnemo = dict()
        pme_mnemo = dict()
        fonds_mnemo = dict()
        indices_mnemo = dict()
        bitcoins_mnemo = dict()
        for nom, mnemo in self._pea.items():
            pea_mnemo.update({mnemo: nom})
        for nom, mnemo in self._pme.items():
            pme_mnemo.update({mnemo: nom})
        for nom, mnemo in self._fonds.items():
            fonds_mnemo.update({mnemo: nom})
        for nom, mnemo in self._indices.items():
            indices_mnemo.update({mnemo: nom})
        for nom, mnemo in self._bitcoins.items():
            bitcoins_mnemo.update({mnemo: nom})
        for mnemo in liste_de_titres:
            if pea_mnemo.get(mnemo) != None:
                dictionnaire.update({pea_mnemo.get(mnemo): mnemo})
                self._actions_pea.update({pea_mnemo.get(mnemo): mnemo})
            if pme_mnemo.get(mnemo) != None:
                dictionnaire.update({pme_mnemo.get(mnemo): mnemo})
                self._actions_pme.update({pme_mnemo.get(mnemo): mnemo})
            if fonds_mnemo.get(mnemo) != None:
                dictionnaire.update({fonds_mnemo.get(mnemo): mnemo})
                self._titres_fonds.update({fonds_mnemo.get(mnemo): mnemo})
            if indices_mnemo.get(mnemo) != None:
                dictionnaire.update({indices_mnemo.get(mnemo): mnemo})
                self._titres_indices.update({indices_mnemo.get(mnemo): mnemo})
            if bitcoins_mnemo.get(mnemo) != None:
                dictionnaire.update({bitcoins_mnemo.get(mnemo): mnemo})
                self._titres_bitcoins.update({bitcoins_mnemo.get(mnemo): mnemo})
        for titre_case in liste_de_titres:
            titre = titre_case.upper()
            if (titre not in self._pea) & (titre not in self._pme) \
                    & (titre not in self._fonds) & (titre not in self._indices) \
                    & (titre not in self._bitcoins) \
                    & (titre not in pea_mnemo) & (titre not in fonds_mnemo) \
                    & (titre not in pme_mnemo) & (titre not in indices_mnemo) \
                    & (titre not in bitcoins_mnemo):
                raise NameError('erreur d\'écriture de ', titre)
        self._portefeuille = dictionnaire
        del pea_mnemo, pme_mnemo, fonds_mnemo, indices_mnemo, dictionnaire

    def creer_portefeuille(self):
        """Crée un dictionnaire d'objet Titre avec les noms en clés

        """
        # print(self._actions_pea)
        for nom, mnemo in self._actions_pea.items():
            self._groupe_pea.update({nom: Action({nom: self._actions_pea[nom]}, self.commande)})
            self._groupe_de_titres.update(self._groupe_pea)
            self._liste_pea.append([nom, mnemo])
            self._liste_de_titres.append([nom, mnemo])

        for nom, mnemo in self._actions_pme.items():
            self._groupe_pme.update({nom: Action({nom: self._actions_pme[nom]}, self.commande)})
            self._groupe_de_titres.update(self._groupe_pme)
            self._liste_pme.append([nom, mnemo])
            self._liste_de_titres.append([nom, mnemo])

        for nom, mnemo in self._titres_fonds.items():
            self._groupe_fonds.update({nom: Fonds({nom: self._titres_fonds
            [nom]}, self.commande)})
            self._groupe_de_titres.update(self._groupe_fonds)
            self._liste_fonds.append([nom, mnemo])
            self._liste_de_titres.append([nom, mnemo])

        for nom, mnemo in self._titres_indices.items():
            self._groupe_indices.update({nom: Indice({nom: self._titres_indices[nom]}, self.commande)})
            self._groupe_de_titres.update(self._groupe_indices)
            self._liste_indices.append([nom, mnemo])
            self._liste_de_titres.append([nom, mnemo])

        for nom, mnemo in self._titres_bitcoins.items():
            self._groupe_bitcoins.update({nom: Bitcoin({nom: self._titres_bitcoins[nom]}, self.commande)})
            self._groupe_de_titres.update(self._groupe_bitcoins)
            self._liste_bitcoins.append([nom, mnemo])
            self._liste_de_titres.append([nom, mnemo])

    def __repr__(self):
        return f'{self._portefeuille}'

    def __doc__(self):
        return "Permet de catégoriser une liste de titres à partir de noms ou " \
               "de mnémonics dans le but d'analyse par catégorie"

    # liste des attributs de l’objet en mode private quand précédé de _ pour modification seulement par accesseurs.
    @property
    def commande(self):
        return self._commande
    
    @property
    def pea(self, key):
        return self._pea.__getitem__(key)
    
    @property
    def pme(self, key):
        return self._pme.__getitem__(key)

    @property
    def fonds(self, key):
        return self._fonds.__getitem__(key)
        
    @property
    def indices(self, key):
        return self._indices.__getitem__(key)      

    @property
    def bitcoins(self, key):
        return self._bitcoins.__getitem__(key) 

    @property
    def liste_pea(self):
        return self._liste_pea
    
    @property
    def liste_pme(self):
        return self._liste_pme
    
    @property
    def liste_fonds(self):
        return self._liste_fonds

    
    @property
    def liste_indices(self):
        return self._liste_indices
    
    @property
    def liste_bitcoins(self):
        return self._liste_bitcoins
    
    @property
    def liste_de_titres(self):
        return self._liste_de_titres
    
    @property
    def liste_de_dates_arrivee(self):
        return self._liste_de_dates_arrivee
    
    @property
    def dates_achat(self, key):
        return self._dates_achat.__getitem__(key)

    @property
    def dates_vente(self, key):
        return self._dates_vente.__getitem__(key)

    @property
    def actions_pea(self, key):
        return self._actions_pea.__getitem__(key)
    
    @property
    def actions_pme(self, key):
        return self._actions_pme.__getitem__(key)

    @property
    def titres_fonds(self, key):
        return self._titres_fonds.__getitem__(key)

    @property
    def titres_indices(self, key):
        return self._titres_indices.__getitem__(key)
    
    @property
    def titres_bitcoins(self, key):
        return self._titres_bitcoins.__getitem__(key)
    
    @property
    def portefeuille(self, key):
        return self._portefeuille.__getitem__(key)
    
    @commande.setter
    def commande(self, value):
        self._commande = value
        
    # Liste des noms des Titre 0: nom, 1: mnemo
    @liste_pea.setter
    def liste_pea(self, value):
        self._liste_pea = value
    
    @liste_pme.setter
    def liste_pme(self, value):
        self._liste_pme = value
        
    @liste_fonds.setter
    def liste_fonds(self, value):
        self._liste_fonds = value
        
    @liste_indices.setter
    def liste_indices(self, value):
        self._liste_indices = value
        
    @liste_bitcoins.setter
    def liste_bitcoins(self, value):
        self._liste_bitcoins = value
    
    @liste_de_titres.setter
    def liste_de_titres(self, value):
        self._liste_de_titres = value
        
    @liste_de_dates_arrivee.setter
    def liste_de_dates_arrivee(self, value):
        self._liste_de_dates_arrivee = value
    # Dictionnaires des noms des Titres clés: nom, value: mnemo
    @actions_pea.setter
    def actions_pea(self, key, value):
        self._actions_pea.__setitem__({key:value})
    
    @actions_pme.setter
    def actions_pme(self, key, value):
        self._actions_pme.__setitem__(key, value)
        
    @titres_fonds.setter
    def titres_fonds(self, key, value):
        self._titres_fonds.__setitem__(key, value)

    @titres_indices.setter
    def titres_indices(self, key, value):
        self._titres_indices.__setitem__(key, value) 
        
    @titres_bitcoins.setter
    def titres_bitcoins(self, key, value):
        self._titres_bitcoins.__setitem__(key, value) 
    
    @dates_achat.setter
    def dates_achat(self, key, value):
        self._dates_achat.__setitem__(key, value) 
    
    @dates_vente.setter
    def dates_vente(self, key, value):
        self._dates_vente.__setitem__(key, value) 
      
    @portefeuille.setter
    def portefeuille(self, key, value):
        self._portefeuille.__setitem__(key, value)
    # Dictionnaire d'objet instantié
    @property
    def groupe_pea(self, key):
        return self._pea.__getitem__(key)

    @groupe_pea.setter
    def groupe_pea(self, key, value):
        self._groupe_pea.__setitem__(key, value)
    
    @property
    def groupe_pme(self, key):
        return self._groupe_pme.__getitem__(key)

    @groupe_pme.setter
    def groupe_pme(self, key, value):
        self._groupe_pme.__setitem__(key, value)
  
    @property
    def groupe_fonds(self, key):
        return self._groupe_fonds.__getitem__(key)
    
    @groupe_fonds.setter
    def groupe_fonds(self, key, value):
        self._groupe_fonds.__setitem__(key, value)

    @property
    def groupe_indices(self, key):
        return self._groupe_indices.__getitem__(key)

    @groupe_indices.setter
    def groupe_indices(self, key, value):
        self._groupe_indices.__setitem__(key, value)
        
    @property
    def groupe_bitcoins(self, key):
        return self._groupe_bitcoins.__getitem__(key)

    @groupe_bitcoins.setter
    def groupe_bitcoins(self, key, value):
        self._groupe_bitcoins.__setitem__(key, value)
    
    @property
    def groupe_de_titres(self, key):
        return self._groupe_de_titres.__getitem__(key)

    @groupe_de_titres.setter
    def groupe_de_titres(self, key, value):
        self.groupe_de_titres.__setitem__(key, value)
    
  
    



