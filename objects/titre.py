#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 16:34:02 2020

@author: romain Boyrie
"""

from data.listes import YAHOO, BOURSORAMA, MAJ, DATE_MAJ, DBASE, DATE_DU_JOUR, DATE_DE_DERNIERE_SEANCE, DB_PATH, XLSX_PATH, INV
from objects.panneau import RessourceEnPanneau_Xlsx, RessourceEnPanneau_Dbase,\
    RessourceEnPanneau_Txt, RessourceEnPanneau_Actu
import pandas as pd
import pandas_datareader as dr
from sqlite3 import connect
import os.path
from datetime import datetime
import sys
import time

class Titre:
    
    def __init__(self, nom_et_mnemo, commande):
        for key, value in nom_et_mnemo.items():
            self._nom = key
            self._mnemo = value
            self._table_nom = self._nom.lower().replace(' ','_').replace('-','_').replace('.','').replace('(','').replace(')','')
        print('\n************************************\nTitre : ', self._nom, self._mnemo)
        if commande == 'XLSX':
            self.xlsx()
        elif commande == 'TXT':
            self.txt()
        elif commande == 'XLSX->DBASE':
            self.xlsx_dbase()
        elif commande == 'DBASE->XLSX':
            self.dbase_xlsx()
        elif commande == 'DBASE':
            self.dbase()
        elif commande == 'MAJ':
            self.maj()
        elif commande == 'RELOAD':
            self.reload()
        elif commande == 'ACTU':
            self.actu()
        else:
            print('pas de commande pour le chargement du titre {}'.format(self._nom))
        
        
        
    def xlsx(self):
        self._donnees = RessourceEnPanneau_Xlsx()
        self._donnees.atteindre( self._mnemo, self._table_nom)
        print('données à partir du fichier xlsx')
        
    def txt(self):
        self._donnees = RessourceEnPanneau_Txt()
        self._donnees.atteindre(self._nom)
        print('données à partir du fichier txt')
        
    def xlsx_dbase(self):
        print('données à partir d\'xlsx puis inscrite en base de données si plus récente')
        self._donnees = RessourceEnPanneau_Xlsx()
        self._donnees.atteindre( self._mnemo)
        #construction de la base si pas trouvé en base, à partir des Xlsx
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + self._table_nom + "';")
        #if the count is 1, then table exists
        if c.fetchone()[0]==1 : 
            donnees = RessourceEnPanneau_Dbase()
            donnees.atteindre(self._table_nom)
            if pd.to_datetime(self._donnees._last_day) > pd.to_datetime(donnees._last_day):
                self._donnees.drop_a_table(self._table_nom)
                self._donnees.base_panel_insert(self._donnees._panel, self._table_nom)
        else:
            conn.close() 
            self._donnees.base_panel_insert(self._donnees._panel, self._table_nom)
        conn.close()     
    def dbase_xlsx(self):
        print('données à partir de la base et écrite en xlsx si plus récente')
        self._donnees = RessourceEnPanneau_Xlsx()
        self._donnees.atteindre(self._mnemo)
        # construction de la base si pas trouvé en base, à partir des Xlsx
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + self._table_nom + "';")
        # if the count is 1, then table exists
        if c.fetchone()[0]==1 : 
            donnees = RessourceEnPanneau_Dbase()
            donnees.atteindre(self._table_nom)
            if pd.to_datetime(self._donnees._last_day) < pd.to_datetime(donnees._last_day):
                donnees.xlsx_panel_write_on_disk(donnees._panel, self._mnemo)
                conn.close() 
                return True
        else:
            conn.close() 
            self._donnees.base_panel_insert(self._donnees._panel, self._table_nom)
            return False
        conn.close() 
        return True
    
    def dbase(self):
        self._donnees = RessourceEnPanneau_Dbase()
        self._donnees.atteindre(self._table_nom)
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + self._table_nom + "';")
        print('données à partir de la base locale')
        
    def maj(self):
        self._donnees = RessourceEnPanneau_Dbase()
        dataframe_yahoo  = pd.DataFrame()
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + self._table_nom + "';")
        # if the count is 1, then table exists
        if c.fetchone()[0]==1: 
            self._donnees.atteindre(self._table_nom)
            print('vérification des données de ', self._nom)
            if self.donnees._doit_etre_maj:
                print('Téléchargement de la données depuis yahoo')
                print(self._mnemo,' valable jusqu\'au ', self._donnees._next_day)
                try:
                    dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=self._donnees._next_day, end= DATE_MAJ)
                except:
                    try:
                        print('Attente de 16 minutes à ', datetime.now())
                        dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=self._donnees._next_day, end= DATE_MAJ)
                        time.sleep(960)
                    except:
                        try:
                            print('Attente de 16 minutes à ', datetime.now())
                            dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=self._donnees._next_day, end= DATE_MAJ)
                            time.sleep(960)  
                        except:
                            try:
                                print('Attente de 16 minutes à ', datetime.now())
                                dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=self._donnees._next_day, end= DATE_MAJ)
                                time.sleep(960)
                            except:
                                try:
                                    print('Attente de 16 minutes à ', datetime.now())
                                    dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=self._donnees._next_day, end= DATE_MAJ)
                                    time.sleep(960)
                                except:
                                    print('mise à jour échouée')
            else:
                pass

            if not dataframe_yahoo.empty:
                self._donnees._panel = self._donnees._panel.append(dataframe_yahoo)
                self._donnees.xlsx_panel_write_on_disk(self._donnees._panel, self._mnemo)
                self._donnees = RessourceEnPanneau_Xlsx()
                self._donnees.atteindre(self._mnemo)
                print('dernier jour du panneau de donnée ', self._donnees._last_day)
                # Sauver le nouveau panneau en base à la place de la table en place
                self._donnees.drop_a_table(self._table_nom)
                self._donnees.base_panel_insert(self._donnees._panel, self._table_nom)    
        else:
            print('Table du titre n\'existe pas en base')
            return   
        message = f'données {self._nom} à mettre à jour' if self._donnees._doit_etre_maj else f'données {self._nom} à jour'
        print(message) 
        
    def reload(self):
        print('Téléchargement de tout l’historique et inscription en base et xlsx, très long')
        self._donnees = RessourceEnPanneau_Dbase()
        dataframe_yahoo  = pd.DataFrame()
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + self._table_nom + "';")
        if c.fetchone()[0]==1: 
            self._donnees.drop_a_table(self._table_nom)
            print('vérification des données ', self._nom)

        print('Téléchargement de la données depuis yahoo')
        try:
            dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start='1990-01-01', end= DATE_MAJ)
        except:
            try:
                print('Attente de 16 minutes à ', datetime.now())
                time.sleep(960)
                dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start='1990-01-01', end= DATE_MAJ)
            except:
                try:
                    print('Attente de 16 minutes à ', datetime.now())
                    time.sleep(960)  
                    dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start='1990-01-01', end= DATE_MAJ)
                except:
                    try:
                        print('Attente de 16 minutes à ', datetime.now())
                        time.sleep(960)
                        dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start='1990-01-01', end= DATE_MAJ)
                    except:
                        try:
                            print('Attente de 16 minutes à ', datetime.now())
                            time.sleep(960)
                            dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start='1990-01-01', end= DATE_MAJ)
                        except:
                            print('mise à jour échouée')
        if not dataframe_yahoo.empty:
            self._donnees.xlsx_panel_write_on_disk(dataframe_yahoo, self._mnemo)
            self._donnees = RessourceEnPanneau_Xlsx()
            self._donnees.atteindre(self._mnemo)
            print('dernier jour du panneau de donnée ', self._donnees._last_day)
            # Sauver le nouveau panneau en base à la place de la table en place
            self._donnees.base_panel_insert(dataframe_yahoo, self._table_nom)    
            conn = connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + self._table_nom + "';")
            conn.close()
            return True
        else:
            return False
    
    def actu(self):
        donnees_base = RessourceEnPanneau_Dbase()
        dataframe_yahoo  = pd.DataFrame()
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + self._table_nom + "';")
        #if the count is 1, then table exists
        if c.fetchone()[0]==1: 
            donnees_base.atteindre(self._table_nom)
            print('vérification des données de ', self._nom)
            if True:
                print('Téléchargement de la données depuis yahoo')
                print(self._mnemo,' valable jusqu\'au ', donnees_base._next_day)
                try:
                    dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=donnees_base._next_day, end= DATE_DU_JOUR)
                except:
                    try:
                        print('Attente de 16 minutes à ', datetime.now())
                        dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=donnees_base._next_day, end= DATE_DU_JOUR)
                        time.sleep(960)
                    except:
                        try:
                            print('Attente de 16 minutes à ', datetime.now())
                            dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=donnees_base._next_day, end= DATE_DU_JOUR)
                            time.sleep(960)  
                        except:
                            try:
                                print('Attente de 16 minutes à ', datetime.now())
                                dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=donnees_base._next_day, end= DATE_DU_JOUR)
                                time.sleep(960)
                            except:
                                try:
                                    print('Attente de 16 minutes à ', datetime.now())
                                    dataframe_yahoo = dr.data.get_data_yahoo(self._mnemo, start=donnees_base._next_day, end= DATE_DU_JOUR)
                                    time.sleep(960)
                                except:
                                    print('mise à jour échouée')
            else:
                pass

            if not dataframe_yahoo.empty:
                donnees = donnees_base._panel.append(dataframe_yahoo)
                
                self._donnees = RessourceEnPanneau_Actu()
                self._donnees.atteindre(donnees)
                    
        else:
            print('Table du titre n\'existe pas en base')
            return
        
    @property
    def donnees(self):
        return self._donnees
    
    @donnees.setter
    def donnees(self, value):
        self._donnees = value
    
    @property
    def nom(self):
        return self._donnees
    
    @nom.setter
    def nom(self, value):
        self._nom = value
        
    @property
    def mnemo(self):
        return self._donnees
    
    @mnemo.setter
    def mnemo(self, value):
        self._mnemo = value
        
class Action(Titre):

    
    def __init__(self, nom_et_mnemo, commande):
        Titre.__init__(self, nom_et_mnemo, commande) 

class Fonds(Titre):
    
         
    def __init__(self, nom_et_mnemo, commande):
        Titre.__init__(self, nom_et_mnemo, commande) 

class Indice(Titre):
    
         
    def __init__(self, nom_et_mnemo, commande):
        Titre.__init__(self, nom_et_mnemo, commande) 

class Bitcoin(Titre):
    
         
    def __init__(self, nom_et_mnemo, commande):
        Titre.__init__(self, nom_et_mnemo, commande) 
        
