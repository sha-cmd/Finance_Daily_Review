# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 09:07:39 2020
Ce programme analyse et crée un rapport financier
@author: romain Boyrie
"""

import xlsxwriter
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
import copy
from decimal import Decimal
from data.listes import FILTRE, NOMBRE
from data.listes import  FILTRE, DATE_DE_DERNIERE_SEANCE, DB_PATH,\
    DATE_DU_JOUR, DATE_MAJ
from objects.titre import Fonds, Indice
import mplfinance as mpf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDRegressor
from sklearn import linear_model


class Analyse:


    def __init__(self, portefeuille):
        print('************************************\nAnalyse')
        texte = 'de performances à dates variables ' if (len(portefeuille._selecteur._dates_achat) != 0) else ('globale à partir du ' + np.datetime_as_string(FILTRE))
        texte = (texte + ' jusqu\'à ' + portefeuille._selecteur._dates_vente[portefeuille._selecteur._liste_de_titres[0][0]] ) if (len(portefeuille._selecteur._dates_vente) != 0) else (texte + ' jusqu\'à aujourd\'hui')
        print(texte)    
        self.analyse_a_date_variable = True if (len(portefeuille._selecteur._dates_achat) != 0) else False
        self.analyse_a_date_fin_variable = True if (len(portefeuille._selecteur._dates_vente) != 0) else False
        print('len date fin variable : ', self.analyse_a_date_fin_variable)
        print('len date début variable : ', self.analyse_a_date_variable)
        self._portefeuille = portefeuille
        # Copie profonde dans math_finance du panel selecteur groupe donnees
        self.avg_d_log = {str():Decimal()}
        self.avg_a_log = {str():Decimal()}
        self.avg_d_dis = {str():Decimal()}
        self.avg_a_dis = {str():Decimal()}
        self.avg = {str():Decimal()}
        self.avg_cac40 = {str():Decimal()}
        self.avg1 = {str():Decimal()}
        self.avg3 = {str():Decimal()}
        self.avg5 = {str():Decimal()}
        self.avg10 = {str():Decimal()}
        self.avg25j = {str():Decimal()}
        self.avg5j = {str():Decimal()}
        self.perf_instantane = {str():Decimal()}
        self.price = {str():Decimal()}
    #self.avg_a = {str():Decimal()}
        self.panel = dict()
        self.panel_predict = dict()
        self.panel_filtre = dict()
        self.indice_filtre = dict()
        self.cac40 = dict()
        self.predicted = {}
        self.beta = {}
        self.risk  = {}
        # Données économique et financière sur les entreprises
        self.df = pd.read_excel('tex/Strategie_PME.xlsx')
        #self.avg_a_log_ac = 0
        col = ['Nom','Prix','Achat','Vente','Perf','Cac 40','5 ans','3 ans','1er janv','Moy/ans','Mois','Semaine','Séance','Avis','Rôle','Secteur','Activité']
        #for nb in NOMBRE:
         #   col.append(str(nb) + ' jours')
        self.synoptique = pd.DataFrame(columns=col)
        
        
    @property
    def portefeuille(self):
        self._portefeuille
        
    @portefeuille.setter
    def portefeuille(self, value):
        self._portefeuille = value
        
    def math_finance(self):
        print('Mathématique Financière')
        self.date_du_jour_de_fin_de_l_analyse = str(self._portefeuille._selecteur._groupe_de_titres[self._portefeuille._selecteur._liste_de_titres[0][0]]._donnees._last_day)
        self.j_moins_2_avant_fin = pd.to_datetime(self.date_du_jour_de_fin_de_l_analyse, format='%Y-%m-%d') - pd.tseries.offsets.Day(2)
        
        for nom, objet in self._portefeuille._selecteur._groupe_de_titres.items():
            self.date_d_analyse_debut = pd.to_datetime(self._portefeuille._selecteur._dates_achat[nom]) if self.analyse_a_date_variable else pd.to_datetime(FILTRE)
            self.date_d_analyse_fin = pd.to_datetime(self._portefeuille._selecteur._dates_vente[nom]) if self.analyse_a_date_fin_variable else pd.to_datetime(objet._donnees._last_day)#pd.to_datetime(datetime.now().date())
            self.date_d_analyse_debut = self.date_d_analyse_debut if \
                         (self.date_d_analyse_debut.date() > \
                             pd.to_datetime(objet._donnees._first_day)) \
                                 else pd.to_datetime(objet._donnees._first_day)

            if self.analyse_a_date_variable | self.analyse_a_date_fin_variable:
                self.panel_filtre.update({nom:copy.deepcopy(objet._donnees._panel.
                                                            loc[(pd.to_datetime(objet._donnees._panel.index) >= pd.to_datetime(self.date_d_analyse_debut)) &
                                                                (pd.to_datetime(objet._donnees._panel.index) <= pd.to_datetime(self.date_d_analyse_fin))])})
            else:
                self.panel_filtre.update({nom:copy.deepcopy(objet._donnees._panel.loc[(pd.to_datetime(objet._donnees._panel.index) > FILTRE) & 
                                                                             (pd.to_datetime(objet._donnees._panel.index) <= pd.to_datetime(DATE_MAJ)) ])})#datetime.now().date() à la place de DATE_MAJ
            panel = self.panel_filtre.get(nom)[~self.panel_filtre.get(nom).index.duplicated()]
            self.panel_filtre.update({nom:panel})
            for nom_indice, objet_indice in self._portefeuille._selecteur._groupe_indices.items():
                self.indice_filtre.update({nom_indice:copy.deepcopy(objet_indice._donnees._panel.
                                                                loc[(pd.to_datetime(objet_indice._donnees._panel.index) >= pd.to_datetime(self.date_d_analyse_debut)) &
                                                                    (pd.to_datetime(objet_indice._donnees._panel.index) < pd.to_datetime(self.date_d_analyse_fin))])})
            self.beta.update(self.beta_calc(nom))
            self.log_ror(nom)
            self.dis_ror(nom)
            self.ror(nom, objet)
            self.perf_du_dernier_jour(nom)
            self.get_price(nom)
           # Indice ror à placé après là fonction beta_calc
            self.indice_ror(nom, objet)
            self.risk_stock(nom,objet)

        self.transform()
        
    def beta_calc(self, nom):
        dictionnaire_beta = {}
        trans = {}
        for nom_indice, objet in self.indice_filtre.items():
            try :
                data_ac = pd.DataFrame({'stock':self.panel_filtre.get(nom).get('Adj Close'),nom_indice: self.indice_filtre.get(nom_indice).get('Adj Close')})
            except:
                data_ac = pd.DataFrame({'stock':self.panel_filtre.get(nom).get('Close'),nom_indice: self.indice_filtre.get(nom_indice).get('Close')})
            
            sec_returns_ac = np.log( data_ac / data_ac.shift(1))
            cov_ac = sec_returns_ac.cov() * 250
           
            cov_with_market_ac = cov_ac.loc['stock',nom_indice]
          
            market_var_ac = sec_returns_ac[nom_indice].var() * 250
          
            beta_temp_ac = cov_with_market_ac / market_var_ac
            trans.update({nom_indice:beta_temp_ac})
        dictionnaire_beta.update({nom:trans})
        return dictionnaire_beta
        #FORMULE PAR SCIPY
            #stock_returns = data_ac['stock']
            #mkt_returns = data_ac['indice']
            #print(stock_returns)
            #self.beta, self.alpha, self.r_value, self.p_value, self.std_err = stats.linregress(stock_returns, mkt_returns)
            #self.beta_indices_ac.append(self.beta)
            
        
    def perf_du_dernier_jour(self, nom):
        if not self.panel_filtre.get(nom).get('Adj Close').empty:
            self.perf_instantane.update({nom:round(((self.panel_filtre.get(nom).get('Adj Close')[-1] / \
                                        self.panel_filtre.get(nom).get('Adj Close')[-2])-1) * 100, 2)})
        else:
            self.perf_instantane.update({nom:None})
    def get_price(self, nom):
        #print(self.panel_filtre.get(nom))
        try:
            return self.price.update({nom:copy.deepcopy(round(self.panel_filtre.get(nom).iloc[-1]['Adj Close'],2))})
        except:
            return self.price.update({nom:copy.deepcopy(round(self.panel_filtre.get(nom).iloc[-1]['Close'],2))})                                
    def to_txt(self):
        fichier = open("performance_du_jour.txt", "w")
        for nom, objet in self._portefeuille._selecteur._groupe_de_titres.items():
            if (not isinstance(objet, Indice)):    
                fichier.write(f'****************************\nPour {nom:>36}  aujourd\'hui: {self.perf_instantane[nom]:>+5}% -> {self.price[nom]:5}€\n')
                fichier.write(f'sur période du  {self.date_d_analyse_debut.date()} au {objet._donnees._last_day} :\n')
                if not self.avg[nom] == None:
                    fichier.write(f'plus value sur la période          {self.avg[nom]:+5}%\n')
                fichier.write(f'moyenne journalière suivi intégral {self.avg_d_log[nom] :+5}%\n')
                if self.panel_filtre.get(nom).get('Log_ror').count() > 250:
                    fichier.write(f'moyenne annuel suivi intégral      {self.avg_a_log[nom] :+5}%\n')
                
                fichier.write(f'moyenne journalière suivi sommé    {self.avg_d_dis[nom]:+5}%\n')
                if self.panel_filtre.get(nom).get('Dis_ror').count() > 250:
                    fichier.write(f'moyenne annuelle suivi sommé       {self.avg_a_dis[nom]:+5}%\n')
        fichier.close()

    def to_xlsx(self):
        for nom, objet in self._portefeuille._selecteur._groupe_de_titres.items():
            if (not isinstance(objet, Indice)) :#| (not isinstance(objet, Indice) & (not self.avg[nom] == None)) :
                if self.panel_filtre.get(nom).get('Log_ror').count() > 250:
                    pass
                if self.panel_filtre.get(nom).get('Dis_ror').count() > 250:
                    pass
                self.synoptique = self.synoptique.append({'Nom':nom,
                          'Prix':float(self.price[nom]), 
                          'Achat': str(self.date_d_analyse_debut.date()) if \
                              self.date_d_analyse_debut.date() > \
                                  pd.to_datetime(objet._donnees._first_day) \
                                      else objet._donnees._first_day,
                          'Vente': str(self.date_d_analyse_fin.date()) if self.date_d_analyse_fin.date() < pd.to_datetime(objet._donnees._last_day) else objet._donnees._last_day,
                          'Perf':float(self.avg[nom]/100) ,
                          '5 ans': float(self.avg5[nom]/100),
                          '3 ans': float(self.avg3[nom]/100) if self.avg3 != None else 'N/A' ,
                          '1er janv': float(self.avg1[nom]/100),
                          'Moy/ans':float(self.avg_a_log[nom]/100),
                          'Mois':float(self.avg25j[nom]/100),
                          'Semaine':float(self.avg5j[nom]/100),
                          'Séance':float(self.perf_instantane[nom]/100), 
                          'Rôle': 'Offensif' if float(self.beta.get(nom).get('CAC 40')) > 0.75 else 'Défensif',
                          'Secteur': self.df.loc[self.df['Nom']== nom]['Secteur'].iloc[0] if len(self.df.loc[self.df['Nom']== nom]['Secteur'].values) > 0 else '',
                          'Activité': self.df.loc[self.df['Nom']== nom]['Activité'].iloc[0] if len(self.df.loc[self.df['Nom']== nom]['Activité'].values) > 0 else '',
                          'Cac 40':float(self.avg_cac40[nom]/100),
                          'Avis': '⇗' if (self.predicted.get(nom).get('5') == True ) else '⇘'                          
                                              },ignore_index=True)
            self.synoptique['Nom'] = self.synoptique['Nom'].astype('str')
            self.synoptique['Achat'] = self.synoptique['Achat'].astype('str')
            self.synoptique['Vente'] = self.synoptique['Vente'].astype('str')
            self.synoptique['Prix'] = self.synoptique['Prix'].astype('float')
            self.synoptique['Perf'] = self.synoptique['Perf'].astype('float')
            self.synoptique['Séance'] = self.synoptique['Séance'].astype('float')
            self.synoptique['Rôle'] = self.synoptique['Rôle'].astype('str')
            self.synoptique['Cac 40'] = self.synoptique['Cac 40'].astype('float')
            
        # Set Pandas engine to xlsxwriter
        writer = pd.ExcelWriter(self.date_du_jour_de_fin_de_l_analyse + '_synoptique.xlsx', engine='xlsxwriter')
        
        # Convert the dataframe to an XlsxWriter Excel object.
        self.synoptique.to_excel(writer, sheet_name='Sheet1', index=True)
        
        # Get the xsxwriter objects from the dataframe writer object.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # Conditional formatting 
        format0 = workbook.add_format({'align':'center'})
        format1 = workbook.add_format({'num_format':'##,###.##€','align':'center'})
        format2 = workbook.add_format({'num_format':'##,###.##%','align':'center'})
        format3 = workbook.add_format({'font_color':'green','align':'center'})
        format4 = workbook.add_format({'font_color':'red','align':'center'})
        worksheet.set_column('A:A', 10, format0)
        # Nom
        worksheet.set_column('B:B', 37, format0)
        # Prix actuel
        worksheet.set_column('C:C', 9, format1)
        # Achat
        worksheet.set_column('D:D', 9, format0)
        # Vente
        worksheet.set_column('E:E', 9, format0)
        # Perf 
        worksheet.set_column('F:F', 9, format2)
        # Cac 40
        worksheet.set_column('G:G', 12, format2)#, format2)
        # 5 ans 
        worksheet.set_column('H:H', 9, format2)
        # 3 ans
        worksheet.set_column('I:I', 9, format2)
        # 1er janv
        worksheet.set_column('J:J', 9, format2)
        # Moy
        worksheet.set_column('K:K', 9, format2)
        # Mois 
        worksheet.set_column('L:L', 9, format2)
        # Semaine
        worksheet.set_column('M:M', 9, format2)
        # Perf du Jour
        worksheet.set_column('N:N', 9, format2)
        # Tendance
        worksheet.set_column('O:O', 9, format0)
        # Rôle
        worksheet.set_column('P:P', 9, format0)
        # Secteur
        worksheet.set_column('Q:Q', 19)
        worksheet.conditional_format('C2:C600', {'type': '3_color_scale'})
        worksheet.conditional_format('E2:E600', {'type': 'data_bar'})
        worksheet.conditional_format('F2:F600', {'type': 'data_bar'})
        worksheet.conditional_format('G2:G600', {'type': 'data_bar'})
        worksheet.conditional_format('H2:H600', {'type': 'data_bar'})
        worksheet.conditional_format('I2:I600', {'type': 'data_bar'})
        worksheet.conditional_format('J2:J600', {'type': 'data_bar'})
        worksheet.conditional_format('K2:K600', {'type': 'data_bar'})
        worksheet.conditional_format('L2:L600', {'type': 'data_bar'})
        worksheet.conditional_format('M2:M600', {'type': 'data_bar'})

        
        worksheet.conditional_format('N2:N600', {'type': 'data_bar'})
        
        worksheet.conditional_format('O2:O600', {'type':'text','criteria':'containing','value': '⇗','format': format3})
        worksheet.conditional_format('O2:O600', {'type':'text','criteria':'containing','value': '⇘','format': format4})
        worksheet.conditional_format('P2:P600', {'type':'text','criteria':'containing','value': 'Offensif','format': format3})
        worksheet.conditional_format('P2:P600', {'type':'text','criteria':'containing','value': 'Défensif','format': format4})
      
        worksheet.write(0, 0, self.date_du_jour_de_fin_de_l_analyse)

        # Close worksheet
        workbook.close()
    
    def __str__(self):
        for nom, objet in self._portefeuille._selecteur._groupe_de_titres.items():
            if (not isinstance(objet, Indice)) :
                print(f'****************************\nPour {nom}  aujourd\'hui: {self.perf_instantane[nom]:+5}% -> {self.price[nom]:5}€')
                print(f'sur période du  {self.date_d_analyse_debut.date()} au {self.date_d_analyse_fin.date()} :')
                if not self.avg[nom] == None:
                    print(f'plus value sur la période          {self.avg[nom]:+5}%')
                print(f'moyenne journalière suivi intégral {self.avg_d_log[nom] :+5}%')
                #print(self.panel_filtre.get(nom).get('Log_ror').count())
                if self.panel_filtre.get(nom).get('Log_ror').count() > 250:
                    print(f'moyenne annuel suivi intégral      {self.avg_a_log[nom] :+5}%')
                
                print(f'moyenne journalière suivi sommé    {self.avg_d_dis[nom]:+5}%')
                if self.panel_filtre.get(nom).get('Dis_ror').count() > 250:
                    print(f'moyenne annuelle suivi sommé       {self.avg_a_dis[nom]:+5}%')
                if (not isinstance(objet, Indice)):
                    for nb in NOMBRE:
                        print(f'prédiction                      {self.predicted.get(nom).get(str(nb)):+5}')
        return '\n'
    
    def transform(self):
        for nom, objet in self._portefeuille._selecteur._groupe_de_titres.items():
            self.panel_predict.update({nom:copy.deepcopy(objet._donnees._panel.loc[(pd.to_datetime(objet._donnees._panel.index) > FILTRE)])})#.
            self.panel_predict.get(nom)['sma_hlong'] = self.panel_predict.get(nom)['Adj Close'].rolling(window=25, min_periods=25).mean()
            self.panel_predict.get(nom)['sma_long']  = self.panel_predict.get(nom)['Adj Close'].rolling(window=10, min_periods=10).mean()
            self.panel_predict.get(nom)['sma_short'] = self.panel_predict.get(nom)['Adj Close'].rolling(window=5, min_periods=5).mean()
            self.panel_predict.get(nom)['ewm_hlong'] = self.panel_predict.get(nom)['Adj Close'].ewm(span=25).mean()
            self.panel_predict.get(nom)['ewm_long'] = self.panel_predict.get(nom)['Adj Close'].ewm(span=10).mean()
            self.panel_predict.get(nom)['ewm_short'] = self.panel_predict.get(nom)['Adj Close'].ewm(span=5).mean()
        self.stock_action()
    
    def stock_action(self):
        col = []
        for nb in NOMBRE:
            col.append(str(nb)+'jours')
        for nom, objet in self._portefeuille._selecteur._groupe_de_titres.items():
            dfend = pd.DataFrame(columns=col,dtype='bool')
            for nb in NOMBRE:
                nj = nb #nombre_de_jours
                source = pd.DataFrame(self.panel_predict.get(nom))
                X = copy.deepcopy(source.iloc[30:,:])
                X= X.reset_index()
                X['Target'] = X['Adj Close'] > X['Adj Close'].shift(nj)
                X['SH/SL'] = X['sma_hlong'] > X['sma_long'] 
                X['SL/SS'] = X['sma_long'] > X['sma_short'] 
                X['SH/SS'] = X['sma_hlong'] > X['sma_short'] 

                X['EH/EL'] = X['ewm_hlong'] > X['ewm_long']
                X['EL/ES'] = X['ewm_long'] > X['ewm_short']
                X['EH/ES'] = X['ewm_hlong'] > X['ewm_short']
                y = copy.deepcopy(X['Target'])
                del X['Date']
                del X['Target']
                pd.set_option('precision', 4)
                pd.set_option('max_columns', 9)
                pd.set_option('display.width', None)
                
                gnb = GaussianNB()
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
                gnb.fit(X_train, y_train)
                y_pred = gnb.fit(X_train, y_train).predict(X_test)
                value = X[-1:]
                money = gnb.predict(value)
                dfend[str(nj)+' jours'] = pd.Series(money.flatten())
            predictions = {}
            for nb in NOMBRE:
                predictions.update({str(nb): dfend.iloc[-1][str(nb) + ' jours']})
            self.predicted.update({nom:predictions})
                               
    
    def risk_stock(self, nom, objet):
#              + '\n------------- Son ror_log vaut : ' +\
        """
        Search and calculation of the volatility of a stock
        """
        self.risk.update({nom:round((self.panel_filtre.get(nom).get('Log_ror').std() * 250 ** 0.5) * 10, 1)})
        if self.panel_filtre.get(nom).get('Log_ror').count() < 250:
            self.risk.update({nom:0})   
        
    
    def indice_ror(self, nom, objet):
            # Moyenne entre les dates indiquées en entrée du programme en instanciant le Selecteur
        self.avg_cac40.update({nom:round(((self.indice_filtre.get('CAC 40').get('Adj Close')[-1] / \
                                        self.indice_filtre.get('CAC 40').get('Adj Close')[0])-1) * 100, 2)})
    
    def ror(self, nom, objet):
        # Retour sur Investissement brut
        if not self.panel_filtre.get(nom).get('Adj Close').empty:
            # Moyenne entre les dates indiquées en entrée du programme en instanciant le Selecteur
            self.avg.update({nom:round(((self.panel_filtre.get(nom).get('Adj Close')[-1] / \
                                        self.panel_filtre.get(nom).get('Adj Close')[0])-1) * 100, 2)})
        else:
            self.avg.update({nom:None})
            
        # Moyenne sur 25 jours
        self.panel.update({nom:copy.deepcopy(objet._donnees._panel.
                                                             loc[(pd.to_datetime(objet._donnees._panel.index) > pd.to_datetime(objet._donnees._panel.index[-1]) - pd.tseries.offsets.Day(25))])})
        nombre_de_lignes_posterieur = self.panel[nom].Open.count()
        
        if not self.panel_filtre.get(nom).get('Adj Close').empty:
            self.avg25j.update({nom:round(((self.panel.get(nom).get('Adj Close')[-1] / \
                                        self.panel.get(nom).get('Adj Close')[0])-1) * 100, 2)})
        else:
            self.avg25j.update({nom:None})            
        
        # Moyenne sur 5 jours
        self.panel.update({nom:copy.deepcopy(objet._donnees._panel.
                                                             loc[(pd.to_datetime(objet._donnees._panel.index) > pd.to_datetime(objet._donnees._panel.index[-1]) - pd.tseries.offsets.Day(5))])})
        nombre_de_lignes_posterieur = self.panel[nom].Open.count()
        
        if not self.panel_filtre.get(nom).get('Adj Close').empty:
            self.avg5j.update({nom:round(((self.panel.get(nom).get('Adj Close')[-1] / \
                                        self.panel.get(nom).get('Adj Close')[0])-1) * 100, 2)})
        else:
            self.avg5j.update({nom:None})            
        
        # Moyenne sur la dernière année
        self.panel.update({nom:copy.deepcopy(objet._donnees._panel.
                                                             loc[(pd.to_datetime(objet._donnees._panel.index) > pd.to_datetime(objet._donnees._panel.index[-1]) - pd.tseries.offsets.YearEnd(1))])})
        nombre_de_lignes_posterieur = self.panel[nom].Open.count()
        
        if not self.panel_filtre.get(nom).get('Adj Close').empty:
            self.avg1.update({nom:round(((self.panel.get(nom).get('Adj Close')[-1] / \
                                        self.panel.get(nom).get('Adj Close')[0])-1) * 100, 2)})
        else:
            self.avg1.update({nom:None})
            
        self.panel.update({nom:copy.deepcopy(objet._donnees._panel.
                                                             loc[(pd.to_datetime(objet._donnees._panel.index) > pd.to_datetime(objet._donnees._panel.index[-1]) - pd.tseries.offsets.Day(3 * 365))])})
        
        nombre_de_lignes_anterieur = self.panel[nom].Open.count()
        
        if nombre_de_lignes_anterieur > nombre_de_lignes_posterieur:
            self.avg3.update({nom:round(((self.panel.get(nom).get('Adj Close')[-1] / \
                                        self.panel.get(nom).get('Adj Close')[0])-1) * 100, 2)})
        else:
            self.avg3.update({nom:0})
       
        nombre_de_lignes_posterieur = self.panel[nom].Open.count()
        self.panel.update({nom:copy.deepcopy(objet._donnees._panel.
                                                             loc[(pd.to_datetime(objet._donnees._panel.index) > pd.to_datetime(objet._donnees._panel.index[-1]) - pd.tseries.offsets.Day(5 * 365))])})
        nombre_de_lignes_anterieur = self.panel[nom].Open.count()
        if nombre_de_lignes_anterieur > nombre_de_lignes_posterieur:
            self.avg5.update({nom:round(((self.panel.get(nom).get('Adj Close')[-1] / \
                                        self.panel.get(nom).get('Adj Close')[0])-1) * 100, 2)})
        else:
            self.avg5.update({nom:0})
        nombre_de_lignes_posterieur = self.panel[nom].Open.count()
        self.panel.update({nom:copy.deepcopy(objet._donnees._panel.
                                                             loc[(pd.to_datetime(objet._donnees._panel.index) > pd.to_datetime(objet._donnees._panel.index[-1]) - pd.tseries.offsets.Day(10 * 365))])})
        nombre_de_lignes_anterieur = self.panel[nom].Open.count()

        if nombre_de_lignes_anterieur > nombre_de_lignes_posterieur:
            self.avg10.update({nom:round(((self.panel.get(nom).get('Adj Close')[-1] / \
                                        self.panel.get(nom).get('Adj Close')[0])-1) * 100, 2)})
        else:
            self.avg10.update({nom:0})
        
    def dis_ror(self, nom):
        try:
            self.panel_filtre.get(nom)['Dis_ror'] = (self.panel_filtre.get(nom).get('Adj Close') / \
                                            self.panel_filtre.get(nom).get('Adj Close')\
                                            .shift(1))-1
            self.avg_d_dis.update({nom:round(self.panel_filtre.get(nom).get('Dis_ror').mean() * 100, 2)})
            self.avg_a_dis.update({nom:round(self.panel_filtre.get(nom).get('Dis_ror').mean() * 250 * 100, 2)})
        except:
            self.panel_filtre.get(nom)['Dis_ror']= (self.panel_filtre.get(nom).get('Close') / \
                                            self.panel_filtre.get(nom).get('Close')\
                                            .shift(1))-1
            self.avg_d_dis.update({nom:round(self.panel_filtre.get(nom).get('Dis_ror').mean() * 100, 2)})
            self.avg_a_dis.update({nom:round(self.panel_filtre.get(nom).get('Dis_ror').mean() * 250 * 100, 2)})
        if self.panel_filtre.get(nom).get('Dis_ror').count() < 250:
            self.avg_a_dis.update({nom:0})
            
    def log_ror(self, nom):

        try:
            self.panel_filtre.get(nom)['Log_ror'] = np.log( \
                                            self.panel_filtre.get(nom).get('Adj Close') / \
                                            self.panel_filtre.get(nom).get('Adj Close')\
                                            .shift(1))
            
            self.avg_d_log.update({nom:round(self.panel_filtre.get(nom).get('Log_ror').mean() * 100, 2)})
            self.avg_a_log.update({nom:round(self.panel_filtre.get(nom).get('Log_ror').mean() * 250 * 100, 2)})
        except:
            self.panel_filtre.get(nom)['Log_ror']= np.log( \
                                            self.panel_filtre.get(nom).get('Close') / \
                                            self.panel_filtre.get(nom).get('Close')\
                                            .shift(1))
            self.avg_d_log.update({nom:round(self.panel_filtre.get(nom).get('Log_ror').mean() * 100, 2)})
            self.avg_a_log.update({nom:round(self.panel_filtre.get(nom).get('Log_ror').mean() * 250 * 100, 2)})
        if self.panel_filtre.get(nom).get('Log_ror').count() < 250:
            self.avg_a_log.update({nom:0})    
    
    def prediction(self, nombre_d_annees_d_historique):
        #bêta, ror, prix actuel, prix future
        print('Synthese')
        
    def performance(self, liste_date):
        #comme la synthèse mais avec une date d’achat pour chaque action
        print('Calcul la performance d\'un portefeuille d\'après des dates d\'achat')
        
    def graphique(self):
        #monte carlo simulation, évolution du prix, mva
        print('Graphique')