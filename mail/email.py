# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 14:23:04 2020
Ce programme analyse et crée un rapport financier
@author: romain Boyrie
"""

import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from data.listes import DATE_MAJ


class Facteur:
    def __init__(self):
        pass        
    def send(self, destinataire):
        subject = "Les cours de Bourse du jour"
        body = "\tBonjour,\n\tTu trouveras les informations d’aujourd’hui en pj"
        sender_email = "titi@toto.email"
        receiver_email = destinataire
        password = ""
        
        # Création d’une entête d’un message multiparties
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails
        
        # Ajout d’un corps à l’email
        message.attach(MIMEText(body, "plain"))
        
        filename = DATE_MAJ + "_synoptique.xlsx"  # Dans le répertoire d’exécution du script
        
        # Ouvrir le fichier en byte mode pour lecture (read/byte)
        with open(filename, "rb") as attachment:
            # Ajouter le fichier comme application/octet-stream
            # Ainsi le client pourra télécharger le fichier
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        # Encodage des caractères du mail en ASCII
        encoders.encode_base64(part)
        
        # Ajout d’un entête (header) par paire de clé/valeur.
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        
        # Ajout de la pièce attachée et conversion du message comme chaîne de caractère
        message.attach(part)
        text = message.as_string()
        
        # Connection au serveur et envoi sécurisé du courriel
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("[fournisseur webmail]", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
