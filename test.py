from dataclasses import dataclass
from PIL import Image
import customtkinter as ctk
import os
from datetime import datetime
from typing import Optional, List
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set customtkinter appearance mode and color theme
ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Dataclass-Definitionen müssen vor ihrer Verwendung stehen
@dataclass
class Kategorie:
    Frage1: int
    Frage2: int
    Frage3: int

@dataclass
class Fragebogen:
    Kategorie1: Kategorie
    Kategorie2: Kategorie
    Kategorie3: Kategorie

@dataclass
class Eintrag:
    Abteilung: str
    Rolle: str
    Fragebogen: Fragebogen
    Feedback: Optional[str]
    Zeitstempel: datetime

@dataclass
class UmfrageErgebnisse:
    Eintraege: List[Eintrag]

def buttonAnmelden_click():
    if textPasswort.get() == "":
        #Der Login Frame wird versteckt
        frameAnmelden.pack_forget()
        #Der Willkommen Frame wird angezeigt
        frameWillkommen.pack(expand=True, fill='both')
    else:
        labelAnmelden.config(text="Passwort falsch!", fg='red')
        textPasswort.delete(0, "end")  # Eingabefeld leeren bei falschem Passwort

def buttonWillkommen_click():
    frameWillkommen.pack_forget()
    framePersoenlicheDaten.pack(expand=True, fill='both')
        
def buttonPersönlicheDaten_click():
    framePersoenlicheDaten.pack_forget()
    frameÜbergangFragebogen.pack(expand=True, fill='both')

def buttonÜbergangFragebogen_click():
    frameÜbergangFragebogen.pack_forget()
    frameFragebogenKat1.pack(expand=True, fill='both')
    
def buttonFragebogenKat1_click():
    frameFragebogenKat1.pack_forget()
    frameFragebogenKat2.pack(expand=True, fill='both')

def buttonFragebogenKat2_click():
    frameFragebogenKat2.pack_forget()
    frameFragebogenKat3.pack(expand=True, fill='both')

def buttonFragebogenKat3_click():
    frameFragebogenKat3.pack_forget()
    frameFeedback.pack(expand=True, fill='both')

def buttonFeedback_click():
    frameFeedback.pack_forget()
    AntwortenSpeichern()  # Speichert die aktuellen Antworten
    frameAuswertung.pack(expand=True, fill='both')




root = ctk.CTk()
root.title("Mitarbeiterumfrage")
root.geometry("1200x800")

# Frame für Startseite mit allen Widgets - zentriert
frameStartseite = ctk.CTkFrame(root)
frameStartseite.pack(expand=True, fill='both', padx=20, pady=20)

pil_image = Image.open("hintergrund.png")
# Bild auf angemessene Größe skalieren
pil_image = pil_image.resize((300, 200))  # Breite x Höhe
ctk_image = ctk.CTkImage(pil_image, size=(300, 200))

#region Anmeldebildschirm

# Container für zentrierte Inhalte
frameAnmelden = ctk.CTkFrame(frameStartseite, width=400, height=300)
frameAnmelden.place(relx=0.5, rely=0.5, anchor='center')


    
# Fallback ohne Bild
labelAnmelden = ctk.CTkLabel(frameAnmelden, text="Anmelden!", 
                          font=ctk.CTkFont(size=18, weight="bold"),image=ctk_image, compound="center")

labelAnmelden.pack(pady=(30, 20))

# Passwort-Label
labelPasswort = ctk.CTkLabel(frameAnmelden, text="Bitte Passwort eingeben:", 
                        font=ctk.CTkFont(size=12))
labelPasswort.pack(pady=(0, 10))

# Passwort-Eingabefeld mit Entry statt Text für bessere Usability
textPasswort = ctk.CTkEntry(frameAnmelden, width=200, font=ctk.CTkFont(size=12), 
                       show='*', justify='center')
textPasswort.pack(pady=(0, 20))

# Enter-Taste bindet sich an die button_click Funktion
textPasswort.bind('<Return>', lambda event: buttonAnmelden_click())

# Button mit verbessertem Styling
buttonAnmelden = ctk.CTkButton(frameAnmelden, text="Anmelden", 
                  command=buttonAnmelden_click,
                  font=ctk.CTkFont(size=12, weight="bold"),
                  width=120, height=35)
buttonAnmelden.pack(pady=10)
#endregion

#region Willkommen

#erstellen neues frames für die Willkommensnachricht
frameWillkommen = ctk.CTkFrame(frameStartseite)

#Willkomensüberschrift
labelWillkommen = ctk.CTkLabel(frameWillkommen, text="Willkommen zur Mitarbeiterumfrage!", 
                           font=ctk.CTkFont(size=20, weight="bold"))
labelWillkommen.pack(pady=(30, 0))

#Willkommensnachricht
labelWillkommenNachricht = ctk.CTkLabel(frameWillkommen, text="Im Folgenden wollen wir Sie ein wenig besser kennen lernen...",
                                        font=ctk.CTkFont(size=14))
labelWillkommenNachricht.pack(pady=(10, 20))
# Button zum Fortfahren
buttonWillkommen = ctk.CTkButton(frameWillkommen, text="Weiter", 
                             command=buttonWillkommen_click,
                             font=ctk.CTkFont(size=12, weight="bold"))
buttonWillkommen.pack(pady=(20, 0))
#endregion

#region persönliche Daten
# Hier können weitere Frames für persönliche Daten hinzugefügt werden
framePersoenlicheDaten = ctk.CTkFrame(frameStartseite)

LabelAbteilung = ctk.CTkLabel(framePersoenlicheDaten, text="Abteilung:", 
                          font=ctk.CTkFont(size=12))
LabelAbteilung.pack(pady=(20, 10))
#DropDown für die Abteilung
abteilungen = ["Vertrieb", "Marketing", "Entwicklung", "Support"]
abteilung_var = ctk.StringVar(value=abteilungen[0])  # Standardwert
abteilung_dropdown = ctk.CTkOptionMenu(framePersoenlicheDaten, variable=abteilung_var, values=abteilungen)
abteilung_dropdown.pack(pady=(0, 20))
#dropdown welche Rolle im Unternehmen
LabelRolle = ctk.CTkLabel(framePersoenlicheDaten, text="Rolle im Unternehmen:", 
                      font=ctk.CTkFont(size=12))
LabelRolle.pack(pady=(10, 10))
rollen = ["Mitarbeiter", "Teamleiter", "Azubi/Praktikant"]
rolle_var = ctk.StringVar(value=rollen[0])  # Standardwert
rolle_dropdown = ctk.CTkOptionMenu(framePersoenlicheDaten, variable=rolle_var, values=rollen)
rolle_dropdown.pack(pady=(0, 20))

#button weiter
buttonPersönlicheDaten = ctk.CTkButton(framePersoenlicheDaten, text="Weiter", 
                                    command=buttonPersönlicheDaten_click,
                                    font=ctk.CTkFont(size=12, weight="bold"))
buttonPersönlicheDaten.pack(pady=(20, 0))
#endregion

#region Übergang zu Fragebogen
#frame für Übergang zum Fragebogen
frameÜbergangFragebogen = ctk.CTkFrame(frameStartseite)   
#Übergangsüberschrift   
labelÜbergang = ctk.CTkLabel(frameÜbergangFragebogen, text="Vielen Dank für Ihre Angaben!", 
                          font=ctk.CTkFont(size=20, weight="bold"))
labelÜbergang.pack(pady=(30, 0))    

#Übergangsnachricht
labelÜbergangNachricht = ctk.CTkLabel(frameÜbergangFragebogen, text="Sie können nun mit dem Fragebogen fortfahren.",
                                  font=ctk.CTkFont(size=14))
labelÜbergangNachricht.pack(pady=(10, 20))
#Slider erklärung
labelSliderErklärung = ctk.CTkLabel(frameÜbergangFragebogen, text="Bitte bewerten Sie die folgenden Aussagen auf einer Skala von 1 (stimme nicht zu) bis 5 (stimme voll zu):",
                                font=ctk.CTkFont(size=12),
                                wraplength=600)
labelSliderErklärung.pack(pady=(10, 20))    

# Button zum Fortfahren zum Fragebogen
buttonÜbergangFragebogen = ctk.CTkButton(frameÜbergangFragebogen, text="Zum Fragebogen", 
                                      command=buttonÜbergangFragebogen_click,
                                      font=ctk.CTkFont(size=12, weight="bold"))
buttonÜbergangFragebogen.pack(pady=(20, 0))
#endregion

#region Fragebogen Kategorie 1 
frameFragebogenKat1 = ctk.CTkFrame(frameStartseite)
# Kategorieüberschrift
labelFragebogenKat1 = ctk.CTkLabel(frameFragebogenKat1, text="Kategorie 1: Arbeitsumfeld und Zusammenarbeit", 
                                font=ctk.CTkFont(size=20, weight="bold"))
labelFragebogenKat1.pack(pady=(30, 20))

# Frage 1
labelFrage1 = ctk.CTkLabel(frameFragebogenKat1, text="Ich fühle mich an meinem Arbeitsplatz wohl und sicher.",
                       font=ctk.CTkFont(size=14),
                       wraplength=600)
labelFrage1.pack(pady=(10, 5))

# Skala-Anzeige für Frage 1
frame_skala1 = ctk.CTkFrame(frameFragebogenKat1, fg_color="transparent")
frame_skala1.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala1, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 1
sliderFrage1 = ctk.CTkSlider(frameFragebogenKat1, from_=1, to=5, number_of_steps=4)
sliderFrage1.set(3)  # Standardwert
sliderFrage1.pack(pady=(0, 20))

# Frage 2
labelFrage2 = ctk.CTkLabel(frameFragebogenKat1, text="Die Zusammenarbeit mit meinen Kollegen funktioniert gut.",
                       font=ctk.CTkFont(size=14),
                       wraplength=600)
labelFrage2.pack(pady=(10, 5))

# Skala-Anzeige für Frage 2
frame_skala2 = ctk.CTkFrame(frameFragebogenKat1, fg_color="transparent")
frame_skala2.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala2, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 2
sliderFrage2 = ctk.CTkSlider(frameFragebogenKat1, from_=1, to=5, number_of_steps=4)
sliderFrage2.set(3)  # Standardwert
sliderFrage2.pack(pady=(0, 20))

#frage 3
labelFrage3 = ctk.CTkLabel(frameFragebogenKat1, text="Ich bekomme die Unterstützung, die ich für meine Arbeit benötige.", 
                       font=ctk.CTkFont(size=14),
                       wraplength=600)
labelFrage3.pack(pady=(10, 5))

# Skala-Anzeige für Frage 3
frame_skala3 = ctk.CTkFrame(frameFragebogenKat1, fg_color="transparent")
frame_skala3.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala3, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 3
sliderFrage3 = ctk.CTkSlider(frameFragebogenKat1, from_=1, to=5, number_of_steps=4)
sliderFrage3.set(3)  # Standardwert
sliderFrage3.pack(pady=(0, 20))

#button für nächste Kategorie
buttonFragebogenKat1 = ctk.CTkButton(frameFragebogenKat1, text="Weiter zur nächsten Kategorie", 
                                 command=buttonFragebogenKat1_click,
                                 font=ctk.CTkFont(size=12, weight="bold"))
buttonFragebogenKat1.pack(pady=(20, 0))
#endregion

#region Fragebogen Kategorie 2
frameFragebogenKat2 = ctk.CTkFrame(frameStartseite)

#überschrift für die zweite Kategorie
labelFragebogenKat2 = ctk.CTkLabel(frameFragebogenKat2, text="Kategorie 2: Kommunikation und Information",
                                font=ctk.CTkFont(size=20, weight="bold"))
labelFragebogenKat2.pack(pady=(30, 20))

# Frage 1
labelFrage1Kat2 = ctk.CTkLabel(frameFragebogenKat2, text="Ich erhalte regelmäßig Informationen über wichtige Entwicklungen im Unternehmen.",
                            font=ctk.CTkFont(size=14),
                            wraplength=600)
labelFrage1Kat2.pack(pady=(10, 5))

# Skala-Anzeige für Frage 1 Kat2
frame_skala1_kat2 = ctk.CTkFrame(frameFragebogenKat2, fg_color="transparent")
frame_skala1_kat2.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala1_kat2, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 1 Kategorie 2
sliderFrage1Kat2 = ctk.CTkSlider(frameFragebogenKat2, from_=1, to=5, number_of_steps=4)
sliderFrage1Kat2.set(3)  # Standardwert
sliderFrage1Kat2.pack(pady=(0, 20))

# Frage 2
labelFrage2Kat2 = ctk.CTkLabel(frameFragebogenKat2, text="In meinem Arbeitsumfeld ist eine offene Meinungsäußerung möglich",
                            font=ctk.CTkFont(size=14),
                            wraplength=600)
labelFrage2Kat2.pack(pady=(10, 5))

# Skala-Anzeige für Frage 2 Kat2
frame_skala2_kat2 = ctk.CTkFrame(frameFragebogenKat2, fg_color="transparent")
frame_skala2_kat2.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala2_kat2, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 2 Kategorie 2
sliderFrage2Kat2 = ctk.CTkSlider(frameFragebogenKat2, from_=1, to=5, number_of_steps=4)
sliderFrage2Kat2.set(3)  # Standardwert
sliderFrage2Kat2.pack(pady=(0, 20))

#frage 3
labelFrage3Kat2 = ctk.CTkLabel(frameFragebogenKat2, text="Ich weiß, was von mir erwartet wird und welche Ziele ich verfolge.",
                            font=ctk.CTkFont(size=14),
                            wraplength=600)
labelFrage3Kat2.pack(pady=(10, 5))

# Skala-Anzeige für Frage 3 Kat2
frame_skala3_kat2 = ctk.CTkFrame(frameFragebogenKat2, fg_color="transparent")
frame_skala3_kat2.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala3_kat2, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 3 Kategorie 2
sliderFrage3Kat2 = ctk.CTkSlider(frameFragebogenKat2, from_=1, to=5, number_of_steps=4)
sliderFrage3Kat2.set(3)  # Standardwert
sliderFrage3Kat2.pack(pady=(0, 20))

#weiter Button für die nächste Kategorie
buttonFragebogenKat2 = ctk.CTkButton(frameFragebogenKat2, text="Weiter zur nächsten Kategorie",
                                    command=buttonFragebogenKat2_click,
                                    font=ctk.CTkFont(size=12, weight="bold"))
buttonFragebogenKat2.pack(pady=(20, 0))
#endregion

#region Fragebogen Kategorie 3
# Hier können weitere Frames für die nächste Kategorie hinzugefügt werden
frameFragebogenKat3 = ctk.CTkFrame(frameStartseite)

# Kategorieüberschrift
labelFragebogenKat3 = ctk.CTkLabel(frameFragebogenKat3, text="Kategorie 3: Entwicklung und Wertschätzung",
                                font=ctk.CTkFont(size=20, weight="bold"))
labelFragebogenKat3.pack(pady=(30, 20))

# Frage 1
labelFrage1Kat3 = ctk.CTkLabel(frameFragebogenKat3, text="Meine Leistung wird anerkannt und wertgeschätzt.",
                            font=ctk.CTkFont(size=14),
                            wraplength=600)
labelFrage1Kat3.pack(pady=(10, 5))

# Skala-Anzeige für Frage 1 Kat3
frame_skala1_kat3 = ctk.CTkFrame(frameFragebogenKat3, fg_color="transparent")
frame_skala1_kat3.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala1_kat3, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 1 Kategorie 3
sliderFrage1Kat3 = ctk.CTkSlider(frameFragebogenKat3, from_=1, to=5, number_of_steps=4)
sliderFrage1Kat3.set(3)  # Standardwert
sliderFrage1Kat3.pack(pady=(0, 20))

#Frage 2
labelFrage2Kat3 = ctk.CTkLabel(frameFragebogenKat3, text="Ich sehe Möglichkeiten, mich fachlich oder persönlich weiterzuentwickeln.",
                            font=ctk.CTkFont(size=14),
                            wraplength=600)
labelFrage2Kat3.pack(pady=(10, 5))

# Skala-Anzeige für Frage 2 Kat3
frame_skala2_kat3 = ctk.CTkFrame(frameFragebogenKat3, fg_color="transparent")
frame_skala2_kat3.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala2_kat3, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 2 Kategorie 3
sliderFrage2Kat3 = ctk.CTkSlider(frameFragebogenKat3, from_=1, to=5, number_of_steps=4)
sliderFrage2Kat3.set(3)  # Standardwert
sliderFrage2Kat3.pack(pady=(0, 20))

# Frage 3
labelFrage3Kat3 = ctk.CTkLabel(frameFragebogenKat3, text="Ich bin stolz, Teil dieses Unternehmens zu sein.",
                            font=ctk.CTkFont(size=14),
                            wraplength=600)
labelFrage3Kat3.pack(pady=(10, 5))

# Skala-Anzeige für Frage 3 Kat3
frame_skala3_kat3 = ctk.CTkFrame(frameFragebogenKat3, fg_color="transparent")
frame_skala3_kat3.pack(pady=(0, 2))
for i in range(1, 6):
    label_num = ctk.CTkLabel(frame_skala3_kat3, text=str(i), font=ctk.CTkFont(size=10))
    label_num.grid(row=0, column=i-1, padx=(20, 20))

#slider für Frage 3 Kategorie 3
sliderFrage3Kat3 = ctk.CTkSlider(frameFragebogenKat3, from_=1, to=5, number_of_steps=4)
sliderFrage3Kat3.set(3)  # Standardwert
sliderFrage3Kat3.pack(pady=(0, 20))

# Button zum Abschließen des Fragebogens
buttonFragebogenKat3 = ctk.CTkButton(frameFragebogenKat3, text="Fragebogen abschließen",
                                    command=buttonFragebogenKat3_click,
                                    font=ctk.CTkFont(size=12, weight="bold"))
buttonFragebogenKat3.pack(pady=(20, 0))




#endregion

#region Feedback 
frameFeedback = ctk.CTkFrame(frameStartseite)
# Feedback-Überschrift
labelFeedback = ctk.CTkLabel(frameFeedback, text="Vielen Dank für Ihre Teilnahme!",
                          font=ctk.CTkFont(size=20, weight="bold"))
labelFeedback.pack(pady=(30, 0))        
# Feedback-Nachricht
labelFeedbackNachricht = ctk.CTkLabel(frameFeedback, text="Wir freuen uns über Ihr Feedback.",
                                    font=ctk.CTkFont(size=14))
labelFeedbackNachricht.pack(pady=(10, 20))  

#Text für optionales Feedback
labelOptionalesFeedback = ctk.CTkLabel(frameFeedback, text="Optional: Haben Sie noch Anmerkungen oder Vorschläge?",
                                    font=ctk.CTkFont(size=12))
labelOptionalesFeedback.pack(pady=(10, 0))
textOptionalesFeedback = ctk.CTkTextbox(frameFeedback, height=100, width=400, font=ctk.CTkFont(size=12))
textOptionalesFeedback.pack(pady=(0, 20))
# Button zum Beenden der Umfrage und weiter zur Auswertung
buttonFeedback = ctk.CTkButton(frameFeedback, text="Feedback abschließen und Auswertung anzeigen",
                            command=buttonFeedback_click,
                            font=ctk.CTkFont(size=12, weight="bold"))
buttonFeedback.pack(pady=(20, 0))

#endregion             

#region Auswertung
#frame für die Auswertung
frameAuswertung = ctk.CTkFrame(frameStartseite)

labelAuswertung = ctk.CTkLabel(frameAuswertung, text="Auswertung der Umfrage",
                            font=ctk.CTkFont(size=20, weight="bold"))
labelAuswertung.pack(pady=(30, 0))

# Auswertung anzeigen mit matplotlib Visualisierung
def AuswertungAnzeigen():
    Antworten = AntwortenLesen()
    
    # Clear any existing widgets in frameAuswertung
    for widget in frameAuswertung.winfo_children():
        if widget != labelAuswertung:  # Keep the title
            widget.destroy()
    
    if not Antworten:
        # Falls keine vorherigen Antworten vorhanden sind, zeige nur aktuelle Antwort
        result_text = "Vielen Dank für Ihre Teilnahme!\n\nIhre Antworten wurden gespeichert.\nFür eine Auswertung werden mehrere Teilnehmer benötigt."
        
        # Textfeld für die Nachricht
        textAuswertung = ctk.CTkTextbox(frameAuswertung, height=200, width=600, font=ctk.CTkFont(size=12))
        textAuswertung.insert("0.0", result_text)
        textAuswertung.pack(pady=(20, 10))
        
        # Button zum Beenden der Umfrage
        buttonAuswertungBeenden = ctk.CTkButton(frameAuswertung, text="Umfrage beenden",
                                            command=root.quit,
                                            font=ctk.CTkFont(size=12, weight="bold"))
        buttonAuswertungBeenden.pack(pady=(10, 0))
    else:
        # Durchschnittswerte für jede Kategorie berechnen
        kategorie1_durchschnitt = {
            "Wohlfühlen am Arbeitsplatz": sum(eintrag.Fragebogen.Kategorie1.Frage1 for eintrag in Antworten) / len(Antworten),
            "Zusammenarbeit mit Kollegen": sum(eintrag.Fragebogen.Kategorie1.Frage2 for eintrag in Antworten) / len(Antworten),
            "Erhaltene Unterstützung": sum(eintrag.Fragebogen.Kategorie1.Frage3 for eintrag in Antworten) / len(Antworten)
        }
        kategorie2_durchschnitt = {
            "Informationsfluss": sum(eintrag.Fragebogen.Kategorie2.Frage1 for eintrag in Antworten) / len(Antworten),
            "Offene Meinungsäußerung": sum(eintrag.Fragebogen.Kategorie2.Frage2 for eintrag in Antworten) / len(Antworten),
            "Klarheit über Erwartungen": sum(eintrag.Fragebogen.Kategorie2.Frage3 for eintrag in Antworten) / len(Antworten)
        }
        kategorie3_durchschnitt = {
            "Anerkennung der Leistung": sum(eintrag.Fragebogen.Kategorie3.Frage1 for eintrag in Antworten) / len(Antworten),
            "Entwicklungsmöglichkeiten": sum(eintrag.Fragebogen.Kategorie3.Frage2 for eintrag in Antworten) / len(Antworten),
            "Stolz auf das Unternehmen": sum(eintrag.Fragebogen.Kategorie3.Frage3 for eintrag in Antworten) / len(Antworten)
        }

        # Matplotlib Figure erstellen
        # Ampelanzeige für jede Kategorie
AmpelAnzeigenKategorie(frameAuswertung, sum(kategorie1_durchschnitt.values()) / len(kategorie1_durchschnitt), "Kategorie 1")
AmpelAnzeigenKategorie(frameAuswertung, sum(kategorie2_durchschnitt.values()) / len(kategorie2_durchschnitt), "Kategorie 2")
AmpelAnzeigenKategorie(frameAuswertung, sum(kategorie3_durchschnitt.values()) / len(kategorie3_durchschnitt), "Kategorie 3")
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Auswertung der Mitarbeiterumfrage - {len(Antworten)} Teilnehmer', fontsize=16, fontweight='bold')
        
        # 1. Balkendiagramm für Kategorie-Durchschnitte
        categories = ['Arbeitsumfeld &\nZusammenarbeit', 'Kommunikation &\nInformation', 'Entwicklung &\nWertschätzung']
        avg_scores = [
            sum(kategorie1_durchschnitt.values()) / 3,
            sum(kategorie2_durchschnitt.values()) / 3,
            sum(kategorie3_durchschnitt.values()) / 3
        ]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        bars = axes[0,0].bar(categories, avg_scores, color=colors, alpha=0.7)
        axes[0,0].set_title('Durchschnittsbewertung nach Kategorien', fontweight='bold')
        axes[0,0].set_ylabel('Bewertung (1-5)')
        axes[0,0].set_ylim(0, 5)
        axes[0,0].grid(True, alpha=0.3)
        
        # Werte auf Balken anzeigen
        for bar, score in zip(bars, avg_scores):
            axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                          f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Detailansicht Kategorie 1
        questions_k1 = list(kategorie1_durchschnitt.keys())
        scores_k1 = list(kategorie1_durchschnitt.values())
        
        bars_k1 = axes[0,1].barh(questions_k1, scores_k1, color='#3498db', alpha=0.7)
        axes[0,1].set_title('Arbeitsumfeld und Zusammenarbeit', fontweight='bold')
        axes[0,1].set_xlabel('Bewertung (1-5)')
        axes[0,1].set_xlim(0, 5)
        axes[0,1].grid(True, alpha=0.3)
        
        # Werte an Balken anzeigen
        for bar, score in zip(bars_k1, scores_k1):
            axes[0,1].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                          f'{score:.2f}', ha='left', va='center', fontweight='bold')
        
        # 3. Detailansicht Kategorie 2
        questions_k2 = list(kategorie2_durchschnitt.keys())
        scores_k2 = list(kategorie2_durchschnitt.values())
        
        bars_k2 = axes[1,0].barh(questions_k2, scores_k2, color='#e74c3c', alpha=0.7)
        axes[1,0].set_title('Kommunikation und Information', fontweight='bold')
        axes[1,0].set_xlabel('Bewertung (1-5)')
        axes[1,0].set_xlim(0, 5)
        axes[1,0].grid(True, alpha=0.3)
        
        # Werte an Balken anzeigen
        for bar, score in zip(bars_k2, scores_k2):
            axes[1,0].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                          f'{score:.2f}', ha='left', va='center', fontweight='bold')
        
        # 4. Detailansicht Kategorie 3
        questions_k3 = list(kategorie3_durchschnitt.keys())
        scores_k3 = list(kategorie3_durchschnitt.values())
        
        bars_k3 = axes[1,1].barh(questions_k3, scores_k3, color='#2ecc71', alpha=0.7)
        axes[1,1].set_title('Entwicklung und Wertschätzung', fontweight='bold')
        axes[1,1].set_xlabel('Bewertung (1-5)')
        axes[1,1].set_xlim(0, 5)
        axes[1,1].grid(True, alpha=0.3)
        
        # Werte an Balken anzeigen
        for bar, score in zip(bars_k3, scores_k3):
            axes[1,1].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                          f'{score:.2f}', ha='left', va='center', fontweight='bold')
        
        # Layout anpassen
        plt.tight_layout()
        
        # Canvas für matplotlib in tkinter
        canvas_frame = ctk.CTkFrame(frameAuswertung)
        canvas_frame.pack(pady=(20, 10), fill="both", expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Zusätzliche Statistik-Infos
        overall_avg = (sum(avg_scores) / 3)
        info_text = f"Gesamtdurchschnitt: {overall_avg:.2f}/5.0  |  Teilnehmer: {len(Antworten)}"
        
        # Beste und schlechteste Kategorie
        best_category_idx = avg_scores.index(max(avg_scores))
        worst_category_idx = avg_scores.index(min(avg_scores))
        info_text += f"\nBeste Kategorie: {categories[best_category_idx]} ({avg_scores[best_category_idx]:.2f})"
        info_text += f"\nVerbesserungsbedarf: {categories[worst_category_idx]} ({avg_scores[worst_category_idx]:.2f})"
        
        info_label = ctk.CTkLabel(frameAuswertung, text=info_text, font=ctk.CTkFont(size=12), 
                                 wraplength=800)
        info_label.pack(pady=(10, 10))
                # --- Ampelanzeige je nach Gesamtdurchschnitt ---
        ampelFarbe = "grey"
        if overall_avg <= 2:
            ampelFarbe = "red"
        elif overall_avg < 5:
            ampelFarbe = "yellow"
        else:
            ampelFarbe = "green"

        ampel_canvas = ctk.CTkCanvas(frameAuswertung, width=60, height=180, bg="white", highlightthickness=0)
        ampel_canvas.pack(pady=(10, 10))

        # Drei Kreise für die Ampel
        # Rot oben, Gelb Mitte, Grün unten
        ampel_canvas.create_oval(10, 10, 50, 50, fill="red"   if ampelFarbe=="red"   else "#550000", outline="")
        ampel_canvas.create_oval(10, 65, 50, 105, fill="yellow" if ampelFarbe=="yellow" else "#555500", outline="")
        ampel_canvas.create_oval(10, 120, 50, 160, fill="green" if ampelFarbe=="green" else "#003300", outline="")
        ampel_canvas.create_text(30, 170, text="Ampel", font=("Arial", 10))
        
        # Buttons für verschiedene Ansichten
        button_frame = ctk.CTkFrame(frameAuswertung)
        button_frame.pack(pady=(10, 10))
        
        buttonGaugeView = ctk.CTkButton(button_frame, text="Gauge-Ansicht",
                                       command=AuswertungGaugeAnzeigen,
                                       font=ctk.CTkFont(size=10, weight="bold"))
        buttonGaugeView.pack(side="left", padx=(0, 10))
        
        # Button zum Beenden der Umfrage
        buttonAuswertungBeenden = ctk.CTkButton(button_frame, text="Umfrage beenden",
                                                command=root.quit,
                                                font=ctk.CTkFont(size=12, weight="bold"))
        buttonAuswertungBeenden.pack(side="left")

def create_gauge_chart(ax, value, title, color):
    """Erstellt ein Gauge-Diagramm für einen Wert zwischen 1-5"""
    # Gauge-Parameter
    theta = np.linspace(0, np.pi, 100)
    
    # Hintergrund-Bogen (Skala 1-5)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=8, alpha=0.3)
    
    # Farbiger Bogen für den aktuellen Wert
    value_theta = np.linspace(0, (value-1)/4 * np.pi, 50)
    ax.plot(np.cos(value_theta), np.sin(value_theta), color=color, linewidth=8)
    
    # Skala-Markierungen
    for i in range(1, 6):
        angle = (i-1)/4 * np.pi
        x, y = np.cos(angle), np.sin(angle)
        ax.plot([x*0.9, x*1.1], [y*0.9, y*1.1], 'k-', linewidth=2)
        ax.text(x*1.2, y*1.2, str(i), ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Zeiger
    angle = (value-1)/4 * np.pi
    x, y = 0.8 * np.cos(angle), 0.8 * np.sin(angle)
    ax.plot([0, x], [0, y], color='red', linewidth=3)
    ax.plot(0, 0, 'o', color='red', markersize=8)
    
    # Wert-Text
    ax.text(0, -0.3, f'{value:.2f}', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(0, -0.5, title, ha='center', va='center', fontsize=12, fontweight='bold', wrap=True)
    
    # Achsen-Einstellungen
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.7, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

def AuswertungGaugeAnzeigen():
    """Alternative Auswertung mit Gauge-Diagrammen"""
    Antworten = AntwortenLesen()
    
    if not Antworten or len(Antworten) == 0:
        return
    
    # Clear existing widgets
    for widget in frameAuswertung.winfo_children():
        if widget != labelAuswertung:
            widget.destroy()
    
    # Durchschnittswerte berechnen
    kategorie1_avg = (
        sum(eintrag.Fragebogen.Kategorie1.Frage1 for eintrag in Antworten) +
        sum(eintrag.Fragebogen.Kategorie1.Frage2 for eintrag in Antworten) +
        sum(eintrag.Fragebogen.Kategorie1.Frage3 for eintrag in Antworten)
    ) / (len(Antworten) * 3)
    
    kategorie2_avg = (
        sum(eintrag.Fragebogen.Kategorie2.Frage1 for eintrag in Antworten) +
        sum(eintrag.Fragebogen.Kategorie2.Frage2 for eintrag in Antworten) +
        sum(eintrag.Fragebogen.Kategorie2.Frage3 for eintrag in Antworten)
    ) / (len(Antworten) * 3)
    
    kategorie3_avg = (
        sum(eintrag.Fragebogen.Kategorie3.Frage1 for eintrag in Antworten) +
        sum(eintrag.Fragebogen.Kategorie3.Frage2 for eintrag in Antworten) +
        sum(eintrag.Fragebogen.Kategorie3.Frage3 for eintrag in Antworten)
    ) / (len(Antworten) * 3)
    
    # Gauge-Charts erstellen
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'Kategorie-Durchschnitte - Gauge-Ansicht ({len(Antworten)} Teilnehmer)', 
                 fontsize=16, fontweight='bold')
    
    categories = [
        (kategorie1_avg, 'Arbeitsumfeld &\nZusammenarbeit', '#3498db'),
        (kategorie2_avg, 'Kommunikation &\nInformation', '#e74c3c'),
        (kategorie3_avg, 'Entwicklung &\nWertschätzung', '#2ecc71')
    ]
    
    for i, (value, title, color) in enumerate(categories):
        create_gauge_chart(axes[i], value, title, color)
    
    plt.tight_layout()
    
    # Canvas für matplotlib in tkinter
    canvas_frame = ctk.CTkFrame(frameAuswertung)
    canvas_frame.pack(pady=(20, 10), fill="both", expand=True)
    
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Buttons für verschiedene Ansichten
    button_frame = ctk.CTkFrame(frameAuswertung)
    button_frame.pack(pady=(10, 10))
    
    buttonDetailedView = ctk.CTkButton(button_frame, text="Detailansicht",
                                      command=AuswertungAnzeigen,
                                      font=ctk.CTkFont(size=10, weight="bold"))
    buttonDetailedView.pack(side="left", padx=(0, 10))
    
    buttonAuswertungBeenden = ctk.CTkButton(button_frame, text="Umfrage beenden",
                                           command=root.quit,
                                           font=ctk.CTkFont(size=12, weight="bold"))
    buttonAuswertungBeenden.pack(side="left")
    
    def AmpelAnzeigenKategorie(frame, avg_score, title):
    """Zeigt eine Ampel basierend auf dem Durchschnittswert einer Kategorie an."""
    ampelFarbe = "grey"
    if avg_score <= 2:
        ampelFarbe = "red"
    elif avg_score < 5:
        ampelFarbe = "yellow"
    else:
        ampelFarbe = "green"

    # Canvas für die Ampel
    ampel_frame = ctk.CTkFrame(frame)
    ampel_frame.pack(pady=(10, 10))
    ampel_canvas = ctk.CTkCanvas(ampel_frame, width=60, height=180, bg="white", highlightthickness=0)
    ampel_canvas.pack(pady=(10, 5))

    # Drei Kreise für die Ampel
    ampel_canvas.create_oval(10, 10, 50, 50, fill="red" if ampelFarbe == "red" else "#550000", outline="")
    ampel_canvas.create_oval(10, 65, 50, 105, fill="yellow" if ampelFarbe == "yellow" else "#555500", outline="")
    ampel_canvas.create_oval(10, 120, 50, 160, fill="green" if ampelFarbe == "green" else "#003300", outline="")
    ampel_canvas.create_text(30, 170, text=title, font=("Arial", 10, "bold"))

#endregion
# Funktino zum serialisieren der Antworten und speichern in XML mit der dataclass Eintrag
def AntwortenSpeichern():
    # Erstellen eines Eintrags mit den Antworten
    eintrag = Eintrag(
        Abteilung=abteilung_var.get(),
        Rolle=rolle_var.get(),
        Fragebogen=Fragebogen(
            Kategorie1=Kategorie(
                Frage1=round(sliderFrage1.get()),
                Frage2=round(sliderFrage2.get()),
                Frage3=round(sliderFrage3.get())
            ),
            Kategorie2=Kategorie(
                Frage1=round(sliderFrage1Kat2.get()),
                Frage2=round(sliderFrage2Kat2.get()),
                Frage3=round(sliderFrage3Kat2.get())
            ),
            Kategorie3=Kategorie(
                Frage1=round(sliderFrage1Kat3.get()),
                Frage2=round(sliderFrage2Kat3.get()),
                Frage3=round(sliderFrage3Kat3.get())
            )
        ),
        Feedback=textOptionalesFeedback.get("0.0", "end").strip() or None,
        Zeitstempel=datetime.now()
    )

    # Lese existierende Daten oder erstelle neues Root-Element
    xml_file = "umfrage_ergebnisse.xml"
    if os.path.exists(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
    else:
        root = ET.Element("UmfrageErgebnisse")

    # Neuen Eintrag hinzufügen
    entry_element = ET.SubElement(root, "Eintrag")
    
    ET.SubElement(entry_element, "Abteilung").text = eintrag.Abteilung
    ET.SubElement(entry_element, "Rolle").text = eintrag.Rolle
    
    fragebogen_element = ET.SubElement(entry_element, "Fragebogen")
    
    for kategorie_name, kategorie in zip(["Kategorie1", "Kategorie2", "Kategorie3"], 
                                         [eintrag.Fragebogen.Kategorie1, 
                                          eintrag.Fragebogen.Kategorie2, 
                                          eintrag.Fragebogen.Kategorie3]):
        kat_element = ET.SubElement(fragebogen_element, kategorie_name)
        ET.SubElement(kat_element, "Frage1").text = str(kategorie.Frage1)
        ET.SubElement(kat_element, "Frage2").text = str(kategorie.Frage2)
        ET.SubElement(kat_element, "Frage3").text = str(kategorie.Frage3)

    if eintrag.Feedback:
        ET.SubElement(entry_element, "Feedback").text = eintrag.Feedback
    
    ET.SubElement(entry_element, "Zeitstempel").text = eintrag.Zeitstempel.isoformat()

    # Speichern der XML-Datei
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)



#XMLDatei lesen und deserialisieren mit der dataclass Eintrag und die einträge als Liste zurückgeben
def AntwortenLesen():
    if not os.path.exists("umfrage_ergebnisse.xml"):
        return []

    tree = ET.parse("umfrage_ergebnisse.xml")
    root = tree.getroot()

    eintraege = []
    for entry_element in root.findall("Eintrag"):
        abteilung = entry_element.find("Abteilung").text
        rolle = entry_element.find("Rolle").text
        
        fragebogen_element = entry_element.find("Fragebogen")
        kategorie1 = Kategorie(
            Frage1=int(fragebogen_element.find("Kategorie1/Frage1").text),
            Frage2=int(fragebogen_element.find("Kategorie1/Frage2").text),
            Frage3=int(fragebogen_element.find("Kategorie1/Frage3").text)
        )
        kategorie2 = Kategorie(
            Frage1=int(fragebogen_element.find("Kategorie2/Frage1").text),
            Frage2=int(fragebogen_element.find("Kategorie2/Frage2").text),
            Frage3=int(fragebogen_element.find("Kategorie2/Frage3").text)
        )
        kategorie3 = Kategorie(
            Frage1=int(fragebogen_element.find("Kategorie3/Frage1").text),
            Frage2=int(fragebogen_element.find("Kategorie3/Frage2").text),
            Frage3=int(fragebogen_element.find("Kategorie3/Frage3").text)
        )

        feedback = entry_element.find("Feedback")
        feedback_text = feedback.text if feedback is not None else None

        zeitstempel = datetime.fromisoformat(entry_element.find("Zeitstempel").text)

        eintrag = Eintrag(
            Abteilung=abteilung,
            Rolle=rolle,
            Fragebogen=Fragebogen(
                Kategorie1=kategorie1,
                Kategorie2=kategorie2,
                Kategorie3=kategorie3
            ),
            Feedback=feedback_text,
            Zeitstempel=zeitstempel
        )
        
        eintraege.append(eintrag)

    return eintraege
   
#endregion   
    


    

root.mainloop()
