#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:17:40 2020
Dictionnaire des valeurs et de leur mnémonic ISIN
@author: romain Boyrie
"""
import numpy as np
import pandas as pd
from datetime import datetime
import os.path
import copy
# YAHOO & DBASE : mettre les fichiers xlsx en base
# INV & DBASE & YAHOO: mettre la base à jour en fichier Xlsx
# MAJ & DBASE & YAHOO: mettre la base à jour à partir de l’internet
# MAJ & DBASE & YAHOO & INV: prendre tout l’historique de à partir de l’internet
YAHOO = False # Lire les fichiers xlsx
BOURSORAMA = False # Lire les fichiers txt
DBASE = True # Lire la base de données
MAJ =  False # Mettre à jour la base de données à partir de source web
INV = False # Mettre la base en fichier Xlsx
DROP = False # Supprimer
DAILY = False # Opérer sur le marché quotidien
NOMBRE = [5] # Jours de prédiction
ANS_A_ANALYSER = 10
DATE_DU_JOUR = datetime.now().date().strftime('%Y-%m-%d') 
DATE_DE_DERNIERE_SEANCE = np.datetime_as_string(np.busday_offset(\
                                                                 DATE_DU_JOUR,
                                                                 offsets=-1, 
                                                                 roll='forward'))
DATE_MAJ = DATE_DU_JOUR if pd.to_datetime(DATE_DU_JOUR + ' 18:00:30') < datetime.now() else DATE_DE_DERNIERE_SEANCE
FILTRE = np.busday_offset(np.datetime64(DATE_MAJ),offsets=-ANS_A_ANALYSER * 52,weekmask='1000000',roll='forward')#1 an vaut 250 jours
DB_PATH = "data/finan_yahoo.sqlite"
XLSX_PATH = os.path.dirname(r'./Xlsx_Stock_Files/')
TXT_PATH = os.path.dirname(r'./Txt_Stock_Files/')

def liste_indices():
    
    indices = {
        'CAC 40': '^FCHI', 
        #'DAX':'^GDAXI',
        #'Sbf 120':'^SBF120',
        #'NASDAQ':'^IXIC', 
       # 'Europe Developed Real Estate':'IFEU',
      #  'MSCI WORLD INDEX FUTURES':'MWL=F'
        } 
    return indices

def liste_bitcoins():
    
    bitcoins = {
        'BITCOIN': 'BTC-EUR',
        'FREELANCE':'ALFRE.PA'
        } 
    
    return bitcoins

def liste_action_pme():
    
    action = {
             'ABC ARBITRAGE':'ABCA.PA',
             'AB SCIENCE':'AB.PA',
             'ACTIA GROUP':'ATI.PA',
             'ALBIOMA':'ABIO.PA',
             'ARCHOS':'JXR.PA',
             'ARTMARKET-COM-SA':'PRC.PA',                   #
             'BIGBEN INTERACTIVE':'BIG.PA',
             'CHARGEURS':'CRI.PA',
             'CLARANOVA':'CLA.PA',
             'DBV TECHNOLOGIES':'DBV.PA',                   #
             'EKINOPS':'EKI.PA',
             'EOS IMAGING':'EOSI.PA',                       #
             'ERYTECH PHARMA':'ERYP.PA',                    #
             'EXEL INDUSTRIES':'EXE.PA',                    #
             'GECI INTERNATIONAL':'GECP.PA',                #
             'GENFIT':'GNFT.PA',
             'GETLINK SE':'GET.PA',                         #
             'GL EVENTS':'GLO.PA',                          #
             'GROUPE GORGE':'GOE.PA',                       #
             'HAULOTTE GROUP':'PIG.PA',
             'HEXAOM':'HEXA.PA',
             'INNATE PHARMA':'IPH.PA',                      #
             'INTERPARFUMS':'ITP.PA',
             'JACQUET METALS':'JCQ.PA',                     #
             'LATECOERE':'LAT.PA',
             'LAURENT PERRIER':'LPE.PA',                    #
             'LE BELIER':'BELI.PA',                         #
             'LECTRA':'LSS.PA',
             'LEXIBOOK':'ALLEX.PA',                         #
             'LNA SANTE':'LNA.PA',                          #
             'LUMIBIRD':'LBIRD.PA',
             'MANUTAN INTL':'MAN.PA',              #
             'MARIE BRIZARD WINE':'MBWS.PA',    #
             'MAUNA KEA TECHN':'MKEA.PA',            #
             'MAUREL PROM':'MAU.PA',                     #
             'METABOLIC EXPLORER':'METEX.PA',               #
             'NANOBIOTIX':'NANO.PA',
             'NICOX':'COX.PA',
             'PHARMAGEST INTERAC':'PHA.PA',      
             'POXEL':'POXEL.PA',
             'PLASTIC OMNIUM':'POM.PA',
             'MAISONS MONDE':'MDM.PA',
             'KAUFMAN BROAD':'KOF.PA',
             'DEVOTEAM':'DVT.PA',
             'COFACE':'COFA.PA',
             'CELLECTIS':'ALCLS.PA',
             #'BOLLORE':'BOL.PA', # donnees stoppé le 7/07/2020
             'ALD':'ALD.PA',#
             'PSB INDUSTRIES':'PSB.PA',                     #
             'SECHE ENVIRONNEMEN':'SCHP.PA',               #
             'SES IMAGOTAG SA':'SESL.PA',                   #
             'SOITEC':'SOI.PA',
             #'SOLOCAL':'LOCAL.PA',
             'SOPRA STERIA GROUP':'SOP.PA',                 #
             'SQLI':'SQI.PA',                          #
             'SWORD GROUP':'SWP.PA',                        #
             'TFF GROUP':'TFF.PA',                          #
             'TRIGANO':'TRI.PA',
             'VALNEVA SE':'VLA.PA',                         #
             'VERIMATRIX':'VMX.PA',
             'VIRBAC SA':'VIRP.PA',                         #
             'VRANKEN POMMERY':'VRAP.PA',          #
             'WAVESTONE':'WAVE.PA'
              }
    return action

def liste_action_pea():
    action = {
             'ACCOR':'AC.PA',
             'ADOCIA':'ADOC.PA',
             'AEROPORTS PARIS':'ADP.PA',
             'AIRBUS SE':'AIR.PA',
             'AIR FRANCE KLM':'AF.PA',
             'AIR LIQUIDE':'AI.PA',                         #
             'AKKA TECHNOLOGIES':'AKA.PA',
             'AKWEL':'AKW.PA',
             'ALSTOM':'ALO.PA',
             'ALTAMIR':'LTA.PA',
            'AMUNDI':'AMUN.PA',
            'ALTAREA':'ALTA.PA',
            'ALTEN':'ATE.PA',
            'ARGAN':'ARG.PA',
            'ARKEMA':'AKE.PA',
            #'ARTMARKET':'PRC.PA',
            #'ASML':'ASME.F',    
            'ATOS':'ATO.PA',
            'AUBAY':'AUB.PA',
            'AUDIOVALLEY RG':'ALAVY.PA',                    #
            'AXA':'CS.PA',
            'AXWAY SOFTWARE':'AXW.PA',                      #
            'BENETEAU':'BEN.PA',
            'BIC':'BB.PA',
            'BIOMERIEUX':'BIM.PA',
            #'BLOCKCHAIN GROUP':'ALTBG.PA',
            #'BLUESOLUTIONS':'BLUE.PA',
            'BNP PARIBAS':'BNP.PA',
            #'BOIRON':'BOI.PA',
            #'BOLLORE':'BOL.PA',
            'BONDUELLE':'BON.PA',
            'BOUYGUES':'EN.PA',
            'BUREAU VERITAS':'BVI.PA',
            'CAPGEMINI':'CAP.PA',
            'CAPELLI':'CAPLI.PA',
            'CARMILA':'CARM.PA',
            'CARREFOUR':'CA.PA',
            'CASINO GUICHARD':'CO.PA',
            'CEGEDIM':'CGM.PA',
            'CGG':'CGG.PA',
            'CHRISTIAN DIOR':'CDI.PA',
            'CIE ALPES':'CDA.PA',                 #
            'CNIM GROUPE SA':'COM.PA',                      #
            #'CNP ASSURANCES':'CNP.PA',
            #'COFACE':'COFA.PA',
            'COLAS':'RE.PA',
            'COVIVIO':'COV.PA',
            'CREDIT AGRICOLE':'ACA.PA',
            'GROUPE CRIT':'CEN.PA',                         #
            'DANONE':'BN.PA',
            'DASSAULT AVIATION':'AM.PA',
            'DASSAULT SYSTEMES':'DSY.PA',                       #
            'DELTA PLUS GROUP':'DLTA.PA',                       #
            'DERICHEBOURG':'DBG.PA',
            #'DONTNOD':'ALDNE.PA',
            'EDENRED':'EDEN.PA',
            'EDF':'EDF.PA',                   #
            'EIFFAGE':'FGR.PA',
            'ELIOR GROUP':'ELIOR.PA',                       #
            'ENGIE':'ENGI.PA',
            'ERAMET':'ERA.PA',
            'ESSILORLUXOTTICA':'EL.PA',                     #
            'ESSO':'ES.PA',
            'EURAZEO':'RF.PA',
            'EUROFINS SCIENTIF':'ERF.PA',                 #
            'EURONEXT':'ENX.PA',                     #
            'EUROPACORP':'ECP.PA',
            'EUROPCAR MOBILITY':'EUCAR.PA',        #
             'EURO RESSOURCES':'EUR.PA',
             'EUTELSAT COMMUNICA':'ETL.PA',           #
             'FAURECIA':'EO.PA',
             #'FDJ':'FDJ.PA',
             'FFP':'FFP.PA',
             'FINANCIERE ODET':'ODET.PA',
             'FNAC DARTY':'FNAC.PA',                        #
             'GAZTRANSPORT TECHN':'GTT.PA',            #
             'GECINA':'GFC.PA',
             'GENKYOTEX':'GKTX.PA',
             'GLOBAL BIOENERGIES':'ALGBE.PA',
             'GRAINES VOLTZ':'GRVO.PA',
             'HERMES INTL':'RMS.PA',
             'ICADE':'ICAD.PA',
             'ID LOGISTICS':'IDL.PA',                       #
             'ILIAD':'ILD.PA',
             'IMERYS':'NK.PA',
             'INGENICO GROUP':'ING.PA',                     #
             'IPSEN':'IPN.PA',
             'IPSOS':'IPS.PA',
             'JC DECAUX':'DEC.PA',                       #
             'KERING':'KER.PA',
             'KLEPIERRE':'LI.PA',
             'KORIAN':'KORI.PA',
             'LAFARGEHOLCIM LTD':'LHN.PA',                #
             'LAGARDERE':'MMB.PA',
             'LEGRAND':'LR.PA',
             #'LEXIBOOKLINGUIST':'ALLEX.PA',
             'LISI':'FII.PA',
             "LOREAL":'OR.PA',
             'LVMH':'MC.PA',
             'MANITOU BF':'MTU.PA',                         #
             #'MAURELPROM':'MAU.PA',
             'MERCIALYS':'MERY.PA',
             'MERSEN':'MRN.PA',
             'M6':'MMT.PA',
             'MICHELIN':'ML.PA',
             'NATIXIS':'KN.PA',
             'NEOEN':'NEOEN.PA',
             'NEXANS':'NEX.PA',
             'NEXITY':'NXI.PA',
             'NOKIA':'NOKIA.PA',
             'OENEO':'SBT.PA',
             'ONXEO':'ONXEO.PA',
             'ORANGE':'ORA.PA',
             'ORPEA':'ORP.PA',
             'PERNOD RICARD':'RI.PA',                       #
             'PEUGEOT':'UG.PA',
             "PIERRE VACANCES":'VAC.PA',                  #
             'PROLOGUEREGROUPE':'PROL.PA',               #
             'PUBLICIS GROUPE':'PUB.PA',                    #
             'QUADIENT SA':'QDT.PA',                        #
             'RALLYE':'RAL.PA',
             'RAMSAY GEN SANTE':'GDS.PA',                   #
             'REMY COINTREAU':'RCO.PA',                     #
             'RENAULT':'RNO.PA',
             'REXEL':'RXL.PA',
             'ROTHSCHILD CO':'ROTH.PA',
             'RHI MAGNESITA':'RHF.F',
             'RUBIS':'RUI.PA',
             'SAFRAN':'SAF.PA',
             'SAINT GOBAIN':'SGO.PA',
             'SANOFI':'SAN.PA',
             'SARTORIUS STEDIM':'DIM.PA',
             'SAVENCIA':'SAVE.PA',
             'SCHLUMBERGER':'SLB.PA',
             'SCHNEIDER ELECTRIC':'SU.PA' ,                    # 
             'SEB':'SK.PA',
             'SOCIETE GENERALE':'GLE.PA',
             'SODEXO':'SW.PA',
             'SPIE':'SPIE.PA',
             'STEF':'STF.PA',
             'STMICROELECTRONICS':'STM.PA',
             'SUEZ':'SEV.PA',
             'SYNERGIE':'SDG.PA',
             'TECHNIPFMC':'FTI.PA',
             'TELEPERFORMANCE':'TEP.PA',
             'TF1':'TFI.PA',
             'THALES':'HO.PA',
             'TOUR EIFFEL':'EIFF.PA',
             'TRANSGENE':'TNG.PA',
             'UBISOFT ENTERTAIN':'UBI.PA',
             'VALEO':'FR.PA',
             'VALLOUREC':'VK.PA',
             'VEOLIA ENVIRONNEMENT':'VIE.PA',
             'VETOQUINOL':'VETO.PA',
             'VICAT':'VCT.PA',
             'VILMORIN CIE':'RIN.PA',
             'VINCI':'DG.PA',
             'VIVENDI':'VIV.PA',
             'WEDIA':'ALWED.PA',
             'WENDEL':'MF.PA',
             'WORLDLINE':'WLN.PA',  
             'XPO LOGISTICS EURO':'XPO.PA',
             'X-FAB SILICON FOUN':'XFAB.PA'
             }
    return action
def liste_fonds():

    liste_fonds ={

        }
    return liste_fonds


### To add adress in reporting
# liste = {}
# liste.update(liste_action_pea())#.update(liste_action_pme()).update(liste_fonds_cic()).update(liste_bitcoins())
# liste.update(liste_action_pme())
# sim= pd.read_excel('Strategie_PME.xlsx')
# data = copy.deepcopy(sim)
# data['Laposte'] = data['Nom']
# data['Lerevenu'] = data['Nom']
# data['Laposte'] = data['Laposte'].apply(lambda x:'https://www.qwant.com/?q=site:https:%2f%2fwww.easybourse.com%2faction-societe%2f'+" ".join(x.split()).replace(' ','-')+'&t=web&client=ext-firefox-hp' )
# data['Lerevenu'] = data['Lerevenu'].apply(lambda x: 'https://bourse.lerevenu.com/cours-de-bourse/fiche-valeur-synthese/'+ "-".join(x.split()) + '/' + liste[x].replace('.PA','-FR') if x in liste else '')
# data.to_excel('New_sim.xlsx')
