#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:31:21 2020

@author: romain Boyrie
"""
from objects.singleton import SingletonType

class PortefeuilleIterator:  

    def __init__(self, liste_valeurs):
        # the list of players and coaches
        self.liste_valeurs = liste_valeurs
        self.index = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index < len(self.liste_valeurs):
            val = self.liste_valeurs[self.index]
            self.index += 1 
            return val
        else:
            return StopIteration()

class PeaIterator:  

    def __init__(self, liste_valeurs):
        # the list of players and coaches
        self.liste_valeurs = liste_valeurs
        self.index = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index < len(self.liste_valeurs):
            val = self.liste_valeurs[self.index]
            self.index += 1 
            return val
        else:
            return StopIteration()
        
class PmeIterator:  

    def __init__(self, liste_valeurs):
        # the list of players and coaches
        self.liste_valeurs = liste_valeurs
        self.index = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index < len(self.liste_valeurs):
            val = self.liste_valeurs[self.index]
            self.index += 1 
            return val
        else:
            return StopIteration()
        
        
class FondsCicIterator:  

    def __init__(self, liste_valeurs):
        # the list of players and coaches
        self.liste_valeurs = liste_valeurs
        self.index = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index < len(self.liste_valeurs):
            val = self.liste_valeurs[self.index]
            self.index += 1 
            return val
        else:
            return StopIteration()
        
class IndicesIterator:  

    def __init__(self, liste_valeurs):
        # the list of players and coaches
        self.liste_valeurs = liste_valeurs
        self.index = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index < len(self.liste_valeurs):
            val = self.liste_valeurs[self.index]
            self.index += 1 
            return val
        else:
            return StopIteration()
        
class BitcoinsIterator:  

    def __init__(self, liste_valeurs):
        # the list of players and coaches
        self.liste_valeurs = liste_valeurs
        self.index = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index < len(self.liste_valeurs):
            val = self.liste_valeurs[self.index]
            self.index += 1 
            return val
        else:
            return StopIteration()

class Portefeuille(metaclass=SingletonType):
    
    def __init__(self, selecteur):
        print('************************************\nPortefeuille')
        self._selecteur = selecteur
        self._actions_pea = selecteur._groupe_pea
        self._actions_pme = selecteur._groupe_pme
        self._titres_fonds = selecteur._groupe_fonds 
        self._titres_indices = selecteur._groupe_indices 
        self._titres_bitcoins = selecteur._groupe_bitcoins

        # Stockage des titres en dictionnaire
        self._valeurs = {}
        if self._actions_pea:
            self._valeurs.update(self._actions_pea)
        if self._actions_pme:
            self._valeurs.update(self._actions_pme)
        if self._titres_fonds:
            self._valeurs.update(self._titres_fonds)
        if self._titres_indices:
            self._valeurs.update(self._titres_indices)
        if self._titres_bitcoins:
            self._valeurs.update(self._titres_bitcoins)
        # Stockage des titres en listes par référence
        self._liste_valeurs = []
        for key, value in self._valeurs.items():
            self._liste_valeurs.append(value)   
        self._liste_pea = []
        for key, value in self._actions_pea.items():
            self._liste_pea.append(value)  
        self._liste_pme = []
        for key, value in self._actions_pme.items():
            self._liste_pme.append(value)  
        self._liste_fonds = []
        for key, value in self._titres_fonds.items():
            self._liste_fonds.append(value)  
        self._liste_indices = []
        for key, value in self._titres_indices.items():
            self._liste_indices.append(value)  
        self._liste_bitcoins = []
        for key, value in self._titres_bitcoins.items():
            self._liste_bitcoins.append(value) 
    
    @property
    def selecteur(self):
        return self._selecteur
    
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
    def valeurs(self, key):
        return self._valeurs.__getitem__(key)
    
    @property
    def liste_valeurs(self):
        return self._liste_valeurs
    
    @selecteur.setter
    def selecteur(self, value):
        self._selecteur = value
        
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
        
    @valeurs.setter
    def valeurs(self, key, value):
        self._valeurs.__setitem__(key, value)
    
    @liste_valeurs.setter
    def liste_valeurs(self, value):
        self._liste_valeurs = value
        
    # Titres triés par catégorie et en liste
    @property
    def liste_pea(self):
        return self._liste_pea

    @liste_pea.setter
    def liste_pea(self, value):
        self._liste_pea = value

    @property
    def liste_pme(self):
        return self._liste_pme

    @liste_pme.setter
    def liste_pme(self, value):
        self._liste_pme = value
    
    @property
    def liste_fonds(self):
        return self._liste_fonds

    @liste_fonds.setter
    def liste_fonds(self, value):
        self._liste_fonds = value
    
    @property
    def liste_indices(self):
        return self._liste_indices

    @liste_indices.setter
    def liste_indices(self, value):
        self._liste_indices = value
        
    @property
    def liste_bitcoins(self):
        return self._liste_bitcoins

    @liste_bitcoins.setter
    def liste_bitcoins(self, value):
        self._liste_bitcoins = value
        
    def pea_iter(self):
        return PeaIterator(self._liste_pea)
    
    def pme_iter(self):
        return PmeIterator(self._liste_pme)
    
    def fonds_iter(self):
        return FondsCicIterator(self._liste_fonds)
    
    def indices_iter(self):
        return IndicesIterator(self._liste_indices)
    
    def bitcoins_iter(self):
        return bitcoinsIterator(self._liste_bitcoins)

    def __len__(self):
        return len(self._liste_valeurs)

    def __iter__(self):
        return PortefeuilleIterator(self._liste_valeurs)
    
    def __repr__(self):
        return f'Portefeuille d\'actions pea: {self._actions_pea.keys()}' + \
    f'\nd\'actions pme: {self._actions_pme.keys()}' + \
    f'\nde fonds cic: {self._titres_fonds.keys()}' + \
    f'\nd\'indices: {self._titres_indices.keys()}'    