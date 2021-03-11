# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 16:44:11 2020
Objet pour obtenir les panneaux de ressource de données financières
@author: romain Boyrie
"""
import abc
import os.path
import numpy as np
import pandas as pd
import sys
import copy
from datetime import datetime
from sqlite3 import connect
from data.listes import  DATE_DE_DERNIERE_SEANCE, \
    ANS_A_ANALYSER, FILTRE, DB_PATH, XLSX_PATH, TXT_PATH, DATE_DU_JOUR, DATE_MAJ


class RessourceEnPanneau:
    
    """
    Définie l'interface pour atteindre les données 
    """
    def __init__(self):
        self._panel: pd.DataFrame()
        self._panel_filtre: pd.DataFrame()
        self._path: str()
        self._last_day: str()
        self._doit_etre_maj = bool()
        

    @property
    def panel(self):
        return self._panel

    @property
    def path(self):
        return self._path

    @property
    def last_day(self):
        return self._last_day

    @property
    def first_day(self):
        return self._first_day
    
    @property
    def doit_etre_maj(self):
        return self._doit_etre_maj
    
    @panel.setter
    def panel(self, panel):
        self._panel = panel
    
    @path.setter
    def path(self, path):
        self._path = path

    @last_day.setter
    def last_day(self, last_day):
        self._last_day = last_day
    
    @first_day.setter
    def first_day(self, first_day):
        self._first_day = first_day
    
    @doit_etre_maj.setter
    def doit_etre_maj(self, value):
        self._doit_etre_maj = value
    
    def acces_location_panel(self, date):
        try:
            return self._panel.loc[date]
        except KeyError:
            return None
        
    def base_panel_insert(self, data_frame, table_nom):
        conn = connect(DB_PATH)
        data_frame.to_sql(table_nom, conn)
        conn.close()
        print('written')
        
    def xlsx_panel_write_on_disk(self, data_frame, mnemo):
        if os.path.exists(XLSX_PATH):
            self._path = os.path.join(XLSX_PATH, mnemo + '.xlsx')
            data_frame.to_excel(self._path)
            return True
        else:
            return False

    @abc.abstractmethod
    def atteindre(path):
        pass
    
    def drop_a_table(self, table_nom):
       conn = connect(DB_PATH)
       c = conn.cursor()
       c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_nom + "';")
       #if the count is 1, then table exists
       if c.fetchone()[0]==1 :     
           #get the count of tables with the name
           c.execute("DROP TABLE '" + table_nom + "';")
           conn.close()
           return True
       else:
           return False
    
    def filtre_panel(self):
        self._panel_filtre = self._panel.loc[pd.to_datetime(self._panel.index) > FILTRE]
        if self._panel_filtre.empty:
            return False
        else:
            return True

class RessourceEnPanneau_Dbase(RessourceEnPanneau):    
    
    """Implemente l'interface et définie sa méthode concrète pour la structure de
     données de type SQLite3.
    
    """
    
    def __init__(self):
        RessourceEnPanneau.__init__(self)
        
    def atteindre(self, table_nom):
        # path is the filepath to a text file
        conn = connect(DB_PATH)
        c = conn.cursor()
    # get the count of tables with the name
        # print('test de l\'existence de la table')
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_nom + "';")
    # if the count is 1, then table exists
        if c.fetchone()[0]==1 : 
            self._panel = pd.read_sql('SELECT * FROM ' + table_nom, conn)#, index_col='Date')
            self._panel['Date'] = pd.to_datetime(self._panel['Date'])
            # self._panel.reset_index()
            self._panel.index = self._panel['Date']
            self._panel.drop('Date', axis=1, inplace=True)
            # print(table_nom)
            if not self._panel.empty:
                # print(type(self._panel.iloc[-1:].index[0]))
                self._last_day = self._panel.iloc[-1:].index[0].strftime("%Y-%m-%d")
                # print(self._last_day)
                self._first_day = self._panel.iloc[0:].index[0].strftime("%Y-%m-%d")
                print(self._first_day)
                # print('elle existe')
                self._next_day = np.busday_offset(np.datetime64(self._last_day), offsets=1, roll='forward')
                a_jour = pd.to_datetime(str(self._last_day)) == pd.to_datetime(DATE_DU_JOUR)
                le_jour_avant = pd.to_datetime(str(self._next_day))  <  pd.to_datetime(DATE_DU_JOUR)
                avant_l_heure_de_fin_seance_du_jour = pd.to_datetime(DATE_DU_JOUR  + datetime.now().time().strftime(' %H:%M:%S')) <  pd.to_datetime(DATE_DU_JOUR + ' 17:00:00')
                self._doit_etre_maj = ( le_jour_avant )| (( not le_jour_avant) & (not avant_l_heure_de_fin_seance_du_jour) & (not a_jour))
                # print('Demande de condition')
                print('Indication pour MAJ, vide entre le : ',self._last_day, ' et ',DATE_MAJ)
                return True
                
            else:
                return False
        conn.close()

class RessourceEnPanneau_Actu(RessourceEnPanneau):    
    
    """Implemente l'interface et définie sa méthode concrète pour la structure de
     données de type SQLite3.
    
    """
    
    def __init__(self):
        RessourceEnPanneau.__init__(self)
        
    def atteindre(self, panneau_live):
        self._panel = panneau_live
        self._last_day = self._panel.iloc[-1:].index[0].strftime("%Y-%m-%d")
        self._first_day = self._panel.iloc[0:].index[0].strftime("%Y-%m-%d")
        self._next_day = np.busday_offset(np.datetime64(self._last_day), offsets=1, roll='forward')
        a_jour = pd.to_datetime(str(self._last_day)) == pd.to_datetime(DATE_DU_JOUR)
        le_jour_avant = pd.to_datetime(str(self._next_day))  <  pd.to_datetime(DATE_DU_JOUR)
        avant_l_heure_de_fin_seance_du_jour = pd.to_datetime(DATE_DU_JOUR  + datetime.now().time().strftime(' %H:%M:%S')) <  pd.to_datetime(DATE_DU_JOUR + ' 17:00:00')
        self._doit_etre_maj = ( le_jour_avant )| (( not le_jour_avant) & (not avant_l_heure_de_fin_seance_du_jour) & (not a_jour))
        
        
class RessourceEnPanneau_Xlsx(RessourceEnPanneau):
    
    """
    Implemente l'interface et définie sa méthode concrète pour la structure de
     données de type Yahoo Finance.
    
    """
    
    def __init__(self):
        RessourceEnPanneau.__init__(self)
        
    def atteindre(self, isin):
        # path is the filepath to a text file
        if os.path.exists(XLSX_PATH):
            self._path = os.path.join(XLSX_PATH, isin + '.xlsx')
            self._panel = pd.read_excel(self._path, index_col='Date', 
                                    usecols=['High','Low','Open','Close',
                                             'Volume','Adj Close','Date'])
            if not self._panel.empty:
                try:
                    self._last_day = self._panel.iloc[-1:].index[0].split(' ')[0]
                    self._first_day = self._panel.iloc[0:].index[0].split(' ')[0]
                    self._next_day = np.busday_offset(np.datetime64(self._last_day), offsets=1, roll='forward')
                    a_jour = pd.to_datetime(str(self._last_day)) == pd.to_datetime(DATE_DU_JOUR)
                    le_jour_avant = pd.to_datetime(str(self._next_day))  <  pd.to_datetime(DATE_DU_JOUR)
                    avant_l_heure_de_fin_seance_du_jour = pd.to_datetime(DATE_DU_JOUR  + datetime.now().time().strftime(' %H:%M:%S')) <  pd.to_datetime(DATE_DU_JOUR + ' 17:00:00')
                    self._doit_etre_maj = ( le_jour_avant )| (( not le_jour_avant) & (not avant_l_heure_de_fin_seance_du_jour) & (not a_jour))
                
                except:
                    self._last_day = self._panel.iloc[-1:].index[0].date().strftime('%Y-%m-%d')
                    self._first_day = self._panel.iloc[0:].index[0]
                    self._next_day = np.busday_offset(np.datetime64(self._last_day), offsets=1, roll='forward')
                    a_jour = pd.to_datetime(str(self._last_day)) == pd.to_datetime(DATE_DU_JOUR)
                    le_jour_avant = pd.to_datetime(str(self._next_day))  <  pd.to_datetime(DATE_DU_JOUR)
                    avant_l_heure_de_fin_seance_du_jour = pd.to_datetime(DATE_DU_JOUR  + datetime.now().time().strftime(' %H:%M:%S')) <  pd.to_datetime(DATE_DU_JOUR + ' 17:00:00')
                    self._doit_etre_maj = ( le_jour_avant )| (( not le_jour_avant) & (not avant_l_heure_de_fin_seance_du_jour) & (not a_jour))
                
            print('prochaine MAJ', self._next_day)
        else:
            raise FileNotFoundError('Le fichier ', isin, 'est introuvable')

    
    
class RessourceEnPanneau_Txt(RessourceEnPanneau):
     
    """
    Implemente l'interface et définie sa méthode concrète de la base 
    boursorama fournissant des fichiers texte nommé par le nom de l'entreprise
    
    """
    def __init__(self):
        RessourceEnPanneau.__init__(self)
        self._panel: pd.DataFrame()

        
    def atteindre(self, nom):
        # path is the filepath to a text file
        print('atteindre')
        if os.path.exists(TXT_PATH):
            files = os.listdir(TXT_PATH)
            fail_to_found_file = True
            for file in files:
                print(nom ,file.split('_')[0],'.txt' in file[-4:])
                if (nom in file.split('_')[0]) & ('.txt' in file[-4:]):
                    fail_to_found_file = False
                    self._path = os.path.join(TXT_PATH, file)
                    self._panel = pd.read_csv(self._path, sep="\t", index_col=False)
                    self._panel.columns = ["date","ouv","haut","bas",
                                           "clot","vol","devise","trash"]
                    self._panel.drop("trash", axis=1, inplace=True)
                    self._panel['date'] = pd.to_datetime(self._panel['date'], format='%d/%m/%Y %H:%M')
                    self._panel['devise'] = pd.Series(self._panel['devise'],dtype="string")
                    self._panel.index.name = 'index'
                    print('panel')
                    self.date_en_index()
                    if not self._panel.empty:
                        try:
                            self._last_day = self._panel.iloc[-1:].index[0].split(' ')[0]
                            self._first_day = self._panel.iloc[0:].index[0].split(' ')[0]
                            self._next_day = np.busday_offset(np.datetime64(self._last_day), offsets=1, roll='forward')
                            a_jour = pd.to_datetime(str(self._last_day)) == pd.to_datetime(DATE_DU_JOUR)
                            le_jour_avant = pd.to_datetime(str(self._next_day))  <  pd.to_datetime(DATE_DU_JOUR)
                            avant_l_heure_de_fin_seance_du_jour = pd.to_datetime(DATE_DU_JOUR  + datetime.now().time().strftime(' %H:%M:%S')) <  pd.to_datetime(DATE_DU_JOUR + ' 17:00:00')
                            self._doit_etre_maj = ( le_jour_avant )| (( not le_jour_avant) & (not avant_l_heure_de_fin_seance_du_jour) & (not a_jour))
                
                        except:
                            self._last_day = self._panel.iloc[-1:].index[0].date().strftime('%Y-%m-%d')
                            self._first_day = self._panel.iloc[0:].index[0].date().strftime('%Y-%m-%d')
                            self._next_day = np.busday_offset(np.datetime64(self._last_day), offsets=1, roll='forward')
                            a_jour = pd.to_datetime(str(self._last_day)) == pd.to_datetime(DATE_DU_JOUR)
                            le_jour_avant = pd.to_datetime(str(self._next_day))  <  pd.to_datetime(DATE_DU_JOUR)
                            avant_l_heure_de_fin_seance_du_jour = pd.to_datetime(DATE_DU_JOUR  + datetime.now().time().strftime(' %H:%M:%S')) <  pd.to_datetime(DATE_DU_JOUR + ' 17:00:00')
                            self._doit_etre_maj = ( le_jour_avant )| (( not le_jour_avant) & (not avant_l_heure_de_fin_seance_du_jour) & (not a_jour))
                
                    print('prochaine MAJ', self._next_day)
                    return True
            if fail_to_found_file:
                print('fichier texte boursorama absent pour ', nom)
                sys.exit()
            
    
    def date_en_index(self):
        if self._panel.index.name != 'Date':
            self._panel.rename(columns={'date':'Date', 'ouv':'Open', 'haut':'High', 'bas':'Low', 'clot':'Close', 'vol':'Volume', 'devise':'Currency'}, inplace=True)
            self._panel.index = self._panel['Date']
            self._panel.drop('Date', axis=1, inplace=True)
            return True
        else:
            raise NameError("L'index est déjà la date pour le fichier : ", self._path)
            return False