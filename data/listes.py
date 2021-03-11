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

# Commands to make true if they’re named in the text :
# YAHOO & DBASE : write xlsx files into the sqlite database
# INV & DBASE & YAHOO: keep database up-to-date and write it in xlsx
# MAJ & DBASE & YAHOO: update the database
# MAJ & DBASE & YAHOO & INV: take all historic data from the internet

YAHOO = False  # Read from Yahoo xlsx stock files
BOURSORAMA = False  # Read from Boursorama plain text stock files
DBASE = True  # Read from database
MAJ = False  # Update database from internet
INV = False  # Transform database in xlsx format, for each stocks in portfolio
DROP = False  # Delete what is written in the portfolio
DAILY = False  # To work before the end of the day, before 18 h 00 (Paris)

NOMBRE = [5]  # Number of day to forecast
ANS_A_ANALYSER = 10 # Number of years to back into the past
DATE_DU_JOUR = datetime.now().date().strftime('%Y-%m-%d')
DATE_DE_DERNIERE_SEANCE = np.datetime_as_string(np.busday_offset(
    DATE_DU_JOUR,
    offsets=-1,
    roll='forward'))
DATE_MAJ = DATE_DU_JOUR if pd.to_datetime(DATE_DU_JOUR + ' 18:00:30') < datetime.now() else DATE_DE_DERNIERE_SEANCE
FILTRE = np.busday_offset(np.datetime64(DATE_MAJ), offsets=-ANS_A_ANALYSER * 52, weekmask='1000000',
                          roll='forward')  # 1 year is equal to 250 days
DB_PATH = "data/finan_yahoo.sqlite"
XLSX_PATH = os.path.dirname(r'./Xlsx_Stock_Files/')
TXT_PATH = os.path.dirname(r'./Txt_Stock_Files/')


def liste_indices():
    indices = {
        'CAC 40': '^FCHI'
        # 'DAX':'^GDAXI',
        # 'Sbf 120':'^SBF120',
        # 'NASDAQ':'^IXIC',
        # 'Europe Developed Real Estate':'IFEU',
        # 'MSCI WORLD INDEX FUTURES':'MWL=F'
    }
    return indices


def liste_bitcoins():
    bitcoins = {
        'BITCOIN': 'BTC-EUR',
        'FREELANCE': 'ALFRE.PA'
    }
    return bitcoins


def liste_action_pme():
    action = {
        'ABC ARBITRAGE': 'ABCA.PA',
        'AB SCIENCE': 'AB.PA',
        'ACTIA GROUP': 'ATI.PA',
        'ALBIOMA': 'ABIO.PA',
        'ARCHOS': 'JXR.PA',
        'ARTMARKET-COM-SA': 'PRC.PA',
        'BIGBEN INTERACTIVE': 'BIG.PA',
        'CHARGEURS': 'CRI.PA',
        'CLARANOVA': 'CLA.PA',
        'DBV TECHNOLOGIES': 'DBV.PA',
        'EKINOPS': 'EKI.PA',
        'EOS IMAGING': 'EOSI.PA',
        'ERYTECH PHARMA': 'ERYP.PA',
        'EXEL INDUSTRIES': 'EXE.PA',
        'GECI INTERNATIONAL': 'GECP.PA',
        'GENFIT': 'GNFT.PA',
        'GETLINK SE': 'GET.PA',
        'GL EVENTS': 'GLO.PA',
        'GROUPE GORGE': 'GOE.PA',
        'HAULOTTE GROUP': 'PIG.PA',
        'HEXAOM': 'HEXA.PA',
        'INNATE PHARMA': 'IPH.PA',
        'INTERPARFUMS': 'ITP.PA',
        'JACQUET METALS': 'JCQ.PA',
        'LATECOERE': 'LAT.PA',
        'LAURENT PERRIER': 'LPE.PA',
        'LE BELIER': 'BELI.PA',
        'LECTRA': 'LSS.PA',
        'LEXIBOOK': 'ALLEX.PA',
        'LNA SANTE': 'LNA.PA',
        'LUMIBIRD': 'LBIRD.PA',
        'MANUTAN INTL': 'MAN.PA',
        'MARIE BRIZARD WINE': 'MBWS.PA',
        'MAUNA KEA TECHN': 'MKEA.PA',
        'MAUREL PROM': 'MAU.PA',
        'METABOLIC EXPLORER': 'METEX.PA',
        'NANOBIOTIX': 'NANO.PA',
        'NICOX': 'COX.PA',
        'PHARMAGEST INTERAC': 'PHA.PA',
        'POXEL': 'POXEL.PA',
        'PLASTIC OMNIUM': 'POM.PA',
        'MAISONS MONDE': 'MDM.PA',
        'KAUFMAN BROAD': 'KOF.PA',
        'DEVOTEAM': 'DVT.PA',
        'COFACE': 'COFA.PA',
        'CELLECTIS': 'ALCLS.PA',
        'ALD': 'ALD.PA',
        'PSB INDUSTRIES': 'PSB.PA',
        'SECHE ENVIRONNEMEN': 'SCHP.PA',
        'SES IMAGOTAG SA': 'SESL.PA',
        'SOITEC': 'SOI.PA',
        'SOPRA STERIA GROUP': 'SOP.PA',
        'SQLI': 'SQI.PA',
        'SWORD GROUP': 'SWP.PA',
        'TFF GROUP': 'TFF.PA',
        'TRIGANO': 'TRI.PA',
        'VALNEVA SE': 'VLA.PA',
        'VERIMATRIX': 'VMX.PA',
        'VIRBAC SA': 'VIRP.PA',
        'VRANKEN POMMERY': 'VRAP.PA',
        'WAVESTONE': 'WAVE.PA'
    }
    return action


def liste_action_pea():
    action = {
        'ACCOR': 'AC.PA',
        'ADOCIA': 'ADOC.PA',
        'AEROPORTS PARIS': 'ADP.PA',
        'AIRBUS SE': 'AIR.PA',
        'AIR FRANCE KLM': 'AF.PA',
        'AIR LIQUIDE': 'AI.PA',  #
        'AKKA TECHNOLOGIES': 'AKA.PA',
        'AKWEL': 'AKW.PA',
        'ALSTOM': 'ALO.PA',
        'ALTAMIR': 'LTA.PA',
        'AMUNDI': 'AMUN.PA',
        'ALTAREA': 'ALTA.PA',
        'ALTEN': 'ATE.PA',
        'ARGAN': 'ARG.PA',
        'ARKEMA': 'AKE.PA',
        # 'ARTMARKET':'PRC.PA',
        # 'ASML':'ASME.F',
        'ATOS': 'ATO.PA',
        'AUBAY': 'AUB.PA',
        'AUDIOVALLEY RG': 'ALAVY.PA',  #
        'AXA': 'CS.PA',
        'AXWAY SOFTWARE': 'AXW.PA',  #
        'BENETEAU': 'BEN.PA',
        'BIC': 'BB.PA',
        'BIOMERIEUX': 'BIM.PA',
        # 'BLOCKCHAIN GROUP':'ALTBG.PA',
        # 'BLUESOLUTIONS':'BLUE.PA',
        'BNP PARIBAS': 'BNP.PA',
        # 'BOIRON':'BOI.PA',
        # 'BOLLORE':'BOL.PA',
        'BONDUELLE': 'BON.PA',
        'BOUYGUES': 'EN.PA',
        'BUREAU VERITAS': 'BVI.PA',
        'CAPGEMINI': 'CAP.PA',
        'CAPELLI': 'CAPLI.PA',
        'CARMILA': 'CARM.PA',
        'CARREFOUR': 'CA.PA',
        'CASINO GUICHARD': 'CO.PA',
        'CEGEDIM': 'CGM.PA',
        'CGG': 'CGG.PA',
        'CHRISTIAN DIOR': 'CDI.PA',
        'CIE ALPES': 'CDA.PA',
        'CNIM GROUPE SA': 'COM.PA',
        # 'CNP ASSURANCES':'CNP.PA',
        # 'COFACE':'COFA.PA',
        'COLAS': 'RE.PA',
        'COVIVIO': 'COV.PA',
        'CREDIT AGRICOLE': 'ACA.PA',
        'GROUPE CRIT': 'CEN.PA',
        'DANONE': 'BN.PA',
        'DASSAULT AVIATION': 'AM.PA',
        'DASSAULT SYSTEMES': 'DSY.PA',
        'DELTA PLUS GROUP': 'DLTA.PA',
        'DERICHEBOURG': 'DBG.PA',
        # 'DONTNOD':'ALDNE.PA',
        'EDENRED': 'EDEN.PA',
        'EDF': 'EDF.PA',
        'EIFFAGE': 'FGR.PA',
        'ELIOR GROUP': 'ELIOR.PA',
        'ENGIE': 'ENGI.PA',
        'ERAMET': 'ERA.PA',
        'ESSILORLUXOTTICA': 'EL.PA',
        'ESSO': 'ES.PA',
        'EURAZEO': 'RF.PA',
        'EUROFINS SCIENTIF': 'ERF.PA',
        'EURONEXT': 'ENX.PA',
        'EUROPACORP': 'ECP.PA',
        'EUROPCAR MOBILITY': 'EUCAR.PA',
        'EURO RESSOURCES': 'EUR.PA',
        'EUTELSAT COMMUNICA': 'ETL.PA',
        'FAURECIA': 'EO.PA',
        # 'FDJ':'FDJ.PA',
        'FFP': 'FFP.PA',
        'FINANCIERE ODET': 'ODET.PA',
        'FNAC DARTY': 'FNAC.PA',
        'GAZTRANSPORT TECHN': 'GTT.PA',
        'GECINA': 'GFC.PA',
        'GENKYOTEX': 'GKTX.PA',
        'GLOBAL BIOENERGIES': 'ALGBE.PA',
        'GRAINES VOLTZ': 'GRVO.PA',
        'HERMES INTL': 'RMS.PA',
        'ICADE': 'ICAD.PA',
        'ID LOGISTICS': 'IDL.PA',
        'ILIAD': 'ILD.PA',
        'IMERYS': 'NK.PA',
        'INGENICO GROUP': 'ING.PA',
        'IPSEN': 'IPN.PA',
        'IPSOS': 'IPS.PA',
        'JC DECAUX': 'DEC.PA',
        'KERING': 'KER.PA',
        'KLEPIERRE': 'LI.PA',
        'KORIAN': 'KORI.PA',
        'LAFARGEHOLCIM LTD': 'LHN.PA',
        'LAGARDERE': 'MMB.PA',
        'LEGRAND': 'LR.PA',
        # 'LEXIBOOKLINGUIST':'ALLEX.PA',
        'LISI': 'FII.PA',
        "LOREAL": 'OR.PA',
        'LVMH': 'MC.PA',
        'MANITOU BF': 'MTU.PA',  #
        # 'MAURELPROM':'MAU.PA',
        'MERCIALYS': 'MERY.PA',
        'MERSEN': 'MRN.PA',
        'M6': 'MMT.PA',
        'MICHELIN': 'ML.PA',
        'NATIXIS': 'KN.PA',
        'NEOEN': 'NEOEN.PA',
        'NEXANS': 'NEX.PA',
        'NEXITY': 'NXI.PA',
        'NOKIA': 'NOKIA.PA',
        'OENEO': 'SBT.PA',
        'ONXEO': 'ONXEO.PA',
        'ORANGE': 'ORA.PA',
        'ORPEA': 'ORP.PA',
        'PERNOD RICARD': 'RI.PA',
        'PEUGEOT': 'UG.PA',
        "PIERRE VACANCES": 'VAC.PA',
        'PROLOGUEREGROUPE': 'PROL.PA',
        'PUBLICIS GROUPE': 'PUB.PA',
        'QUADIENT SA': 'QDT.PA',
        'RALLYE': 'RAL.PA',
        'RAMSAY GEN SANTE': 'GDS.PA',
        'REMY COINTREAU': 'RCO.PA',
        'RENAULT': 'RNO.PA',
        'REXEL': 'RXL.PA',
        'ROTHSCHILD CO': 'ROTH.PA',
        'RHI MAGNESITA': 'RHF.F',
        'RUBIS': 'RUI.PA',
        'SAFRAN': 'SAF.PA',
        'SAINT GOBAIN': 'SGO.PA',
        'SANOFI': 'SAN.PA',
        'SARTORIUS STEDIM': 'DIM.PA',
        'SAVENCIA': 'SAVE.PA',
        'SCHLUMBERGER': 'SLB.PA',
        'SCHNEIDER ELECTRIC': 'SU.PA',
        'SEB': 'SK.PA',
        'SOCIETE GENERALE': 'GLE.PA',
        'SODEXO': 'SW.PA',
        'SPIE': 'SPIE.PA',
        'STEF': 'STF.PA',
        'STMICROELECTRONICS': 'STM.PA',
        'SUEZ': 'SEV.PA',
        'SYNERGIE': 'SDG.PA',
        'TECHNIPFMC': 'FTI.PA',
        'TELEPERFORMANCE': 'TEP.PA',
        'TF1': 'TFI.PA',
        'THALES': 'HO.PA',
        'TOUR EIFFEL': 'EIFF.PA',
        'TRANSGENE': 'TNG.PA',
        'UBISOFT ENTERTAIN': 'UBI.PA',
        'VALEO': 'FR.PA',
        'VALLOUREC': 'VK.PA',
        'VEOLIA ENVIRONNEMENT': 'VIE.PA',
        'VETOQUINOL': 'VETO.PA',
        'VICAT': 'VCT.PA',
        'VILMORIN CIE': 'RIN.PA',
        'VINCI': 'DG.PA',
        'VIVENDI': 'VIV.PA',
        'WEDIA': 'ALWED.PA',
        'WENDEL': 'MF.PA',
        'WORLDLINE': 'WLN.PA',
        'XPO LOGISTICS EURO': 'XPO.PA',
        'X-FAB SILICON FOUN': 'XFAB.PA'
    }
    return action


def liste_fonds():
    liste_fonds = {
        'CM-CIC DYNAMIQUE EUROPE (C)': '0P00000UNH.F',
        'CM-CIC DYNAMIQUE INTERNATIONAL (C)': '0P00000FMT.F',
        'CM-CIC ENTREPRENEURS EUROPE (C)': '0P00000Q4Z.F',
        'CM-CIC EQUILIBRE EUROPE (D)': '0P00000Q4D.F',
        'CM-CIC EQUILIBRE EUROPE (C)': '0P00001NLK.F',
        'CM-CIC EQUILIBRE INTERNATIONAL (RC)': '0P00000FOV.F',
        'CM-CIC EURO EQUITIES (C)': '0P00001PDS.F',
        'CM-CIC EURO MID CAP (C)': '0P00000FET.F',
        'CM-CIC EUROPE GROWTH (C)': '0P00001PDT.F',
        'CM-CIC EUROPE RENDEMENT (RC)': '0P0000Z816.F',
        'CM-CIC EUROPE RENDEMENT (RD)': '0P0000Z817.F',
        'CM-CIC EUROPE VALUE (C)': '0P00000FEJ.F',
        'CM-CIC FRANCE EQUITIES (C)': '0P00001PDW.F',
        'CM-CIC GLOBAL EMERGING MARKETS (RC)': '0P00000LT0.F',
        'CM-CIC GLOBAL LEADERS (RC)': '0P000152US.F',
        'CM-CIC HIGH YIELD 2021 (C)': '0P000163YV.F',
        'CM-CIC HIGH YIELD SHORT DURATION (C)': '0P00013MDM.F',
        'CM-CIC INDICIEL AMERIQUE 500 (C)': '0P00001NLH.F',
        'CM-CIC INDICIEL JAPON 225 (C)': '0P00008IB9.F',
        'CM-CIC MONE ISR (RC)': 'PRC.PA',
        'CM-CIC OBJECTIF ENVIRONNEMENT (C)': '0P00000FS2.F',
        'CM-CIC OBLI PAYS EMERGENTS (C)': '0P00001PDY.F',
        'CM-CIC PIERRE (C)': '0P00008Y84.F', 'CM-CIC PME-ETI ACTIONS (C)': '0P000125M7.F',
        'CM-CIC SILVER ECONOMIE (C)': '0P000175VV.F',
        'CM-CIC TEMPERE EUROPE (C)': '0P000123DC.F',
        'CM-CIC TEMPERE INTERNATIONAL (RC)': '0P00001NLL.F',
        'FLEXIGESTION 20-70 (C)': '0P00000Q7R.F',
        'FLEXIGESTION 50-100 (C)': '0P00000Q5G.F',
        'FLEXIGESTION PATRIMOINE (C)': '0P00005W9T.F',
        # Fonds responsable
        'CM-CIC OBJECTIF ENVIRONNEMENT': '0P00000FS2.F',
        'CM-CIC OBLI ISR': '0P0000Q1L3.F',
        'SOCIAL ACTIVE ACTIONS': '0P00016NIH.F',
        'SOCIAL ACTIVE OBLIGATIONS': '0P00016NIN.F',
        'SOCIAL ACTIVE MONETAIRE': '0P00016NIL.F',
        'SOCIAL ACTIVE DIVERSIFIE': '0P00016NII.F',
        'SOCIAL ACTIVE TEMPERE SOLIDAIRE': '0P00016NIO.F',
        'SOCIAL ACTIVE EQUILIBRE SOLIDAIRE': '0P00016NIK.F',
        'SOCIAL ACTIVE DYNAMIQUE SOLIDAIRE': '0P00016NIJ.F',
        'SOCIAL ACTIVE OBLI SOLIDAIRE': '0P00016NIM.F',
        # Fonds impact social
        'CM-CIC FRANCE EMPLOI': '0P00000FRO.F',
        # Épargne salariale
        'CM-CIC PERSPECTIVE ACTIONS EUROPE A': '0P0000U0J7.F',
        'CM-CIC PERSPECTIVE CONVICTION MONDE A': '0P0000U0ZP.F',
        'CM-CIC PERSPECTIVE OR ET MAT': '0P0000U0JA.F',
        'CM-CIC PERSPECTIVE PAYS EMERGENTS': '0P00016NKY.F',
        'CM-CIC PERSPECTIVE CONVICTION EUROPE A': '0P00016NKX.F',
        'CM-CIC PERSPECTIVE IMMO': '0P0000U0J9.F',
        'CM-CIC PERSPECTIVE CERTITUDE': '0P00016NKU.F',
        'CM-CIC PERSPECTIVE MONETAIRE B': '0P0000U0FQ.F',
        'CM-CIC PERSPECTIVE OBLI CT A': '0P0000U0FR.F',
        'CM-CIC PERSPECTIVE OBLI LT A': '0P0000U0FU.F',
        'CM-CIC PERSPECTIVE OBLI MT A': '0P0000U0FT.F',
        'CM-CIC STRATEGIE TRESO P': '0P00016NKV.F'

    }
    return liste_fonds


# Below there are lines for the Tabular Reporting File Creation
# Many information as hyperlinks toward the internet


"""
liste = {}
liste.update(liste_action_pea())#.update(liste_action_pme()).update(liste_fonds_cic()).update(liste_bitcoins())
liste.update(liste_action_pme())
sim= pd.read_excel('Strategie_PME.xlsx')
data = copy.deepcopy(sim)
data['Laposte'] = data['Nom']
data['Lerevenu'] = data['Nom']
data['Laposte'] = data['Laposte'].apply(lambda x:'https://www.qwant.com/?q=site:https:%2f%2fwww.easybourse.com%2faction-societe%2f'+" ".join(x.split()).replace(' ','-')+'&t=web&client=ext-firefox-hp' )
data['Lerevenu'] = data['Lerevenu'].apply(lambda x: 'https://bourse.lerevenu.com/cours-de-bourse/fiche-valeur-synthese/'+ "-".join(x.split()) + '/' + liste[x].replace('.PA','-FR') if x in liste else '')
data.to_excel('New_sim.xlsx')
"""
