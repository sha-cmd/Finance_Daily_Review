# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 18:24:18 2020
Fait les calculs pour le portefeuille
@author: romain Boyrie
"""
from objects.singleton import SingletonType

class Reporter(metaclass=SingletonType):
    """Intéraction avec l’utilisateur
    """
    def __init__(self, portefeuille):
        self.builder = None

    @property
    def report(self):
        return self.builder.report
    
    def construct_report(self, builder):
        self.builder = builder
        steps = (builder.prepare_text, 
                 builder.prepare_figure, 
                 builder.add_date, 
                 builder.compiler)
        [step() for step in steps]

    def validate_style(self, builders):
        try:
            input_msg = 'Voulez vous un report [e]xcel or [t]ex? '
            report_style = input(input_msg)
            builder = builders[report_style]()
            valid_input = True
        except KeyError:
            error_msg = 'Impossible de créer votre rapport'
            print(error_msg)
            return (False, None)
        return (True, builder)

class Analyse:
    """Affichage du déroulement du calcul
    """
    def __init__(self):
        print('analyse')
        
    def __str__(self):
        return self.nom

    def prepare_info(self, calcul):
        self.calcul = calcul
        print(f'le calcul {self.calcul.name} est en cours pour {self}...')
        # time.sleep(STEP_DELAY)
        print(f'le calcul {self.calcul.name} est terminé')

class ExcelBuilder:
    """"Construction du fichier tableur excel"""
    def __init__(self):
        print('Excel Builder')
    
    @property
    def report(self):
        self.report = 'report'
    
    @report.setter
    def report(self, value):
        self.report = value
    
    def prepare_text(self):
        print('Preparing Text')
        
    def prepare_figure(self):
        print('Preparing figure')
        
    def add_date(self):
        print('Adding date')
        
    def compiler(self):
        print('Compiling')
        
class TexBuilder:    
    """Processus de création du rapport au format Tex"""

    def __init__(self):
        print('Tex Builder')
        self.report

    def prepare_text(self):
        print('Preparing Text')
        
    def prepare_figure(self):
        print('Preparing figure')
        
    def add_date(self):
        print('Adding date')
        
    def compiler(self):
        print('Compiling')

    @property
    def report(self):
        self.report

    @report.setter
    def report(self, value):
        self.report = value
