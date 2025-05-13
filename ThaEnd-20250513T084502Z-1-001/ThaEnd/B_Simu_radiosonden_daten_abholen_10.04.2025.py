# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 10:44:16 2025

@author: david
"""

import pandas as pd
import requests
import urllib3
from datetime import datetime
from io import StringIO

# =============================
# 1. Radiosonde-Daten abrufen (für Dichte und Wind)
# =============================
# santa crus de tenerife (spanien): 60018
# berlin lindenberg: 10393

station = "60018"
now = datetime.utcnow()
obs_hour = 0 if now.hour < 12 else 12
obs_date = now.replace(hour=obs_hour, minute=0, second=0, microsecond=0)
date_str = obs_date.strftime("%Y-%m-%d %H:%M:%S")
# Hier wird als Beispiel ein fester Zeitpunkt (2025-04-09 0:00:00) genutzt
station = "60018"
url = f"https://weather.uwyo.edu/wsgi/sounding?datetime=2025-04-09%200:00:00&id={station}&src=FM35&type=TEXT:LIST"
print(url)


# SSL-Überprüfung deaktivieren (nur in der Entwicklung!)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
response = requests.get(url, verify=False)
html_text = response.text

# Extrahiere den <PRE>-Block und suche nach dem Tabellenheader "PRES"
pre_start = html_text.find('<PRE>')
pre_end = html_text.find('</PRE>', pre_start)
pre_text = html_text[pre_start + len('<PRE>'):pre_end]
start = pre_text.find('PRES')
table_text = pre_text[start:]
data_lines = table_text.split('\n')
# Entferne leere Zeilen und Zeilen, die mit '-----' beginnen
cleaned_lines = [line for line in data_lines if line.strip() and not line.startswith('-----')]
cleaned_data = "\n".join(cleaned_lines)

# Erstelle einen DataFrame aus den Radiosondendaten; es werden die Spalten: PRES, HGHT, TEMP, DRCT, SPED benötigt
radiosonde_df = pd.read_csv(StringIO(cleaned_data), sep=r'\s+')
for col in ['PRES', 'HGHT', 'TEMP', 'DRCT', 'SPED']:
    radiosonde_df[col] = pd.to_numeric(radiosonde_df[col], errors='coerce')
radiosonde_df.sort_values('HGHT', inplace=True)
# Es werden nur Zeilen beibehalten, in denen alle benötigten Werte vorhanden sind
radiosonde_df = radiosonde_df.dropna(subset=['TEMP', 'DRCT', 'SPED'])
 
print("Radiosondendaten (Kurzüberblick):")
print(radiosonde_df[['PRES', 'HGHT', 'TEMP', 'DRCT', 'SPED']].head())

# Speichern des DataFrame in eine Excel-Datei (ohne Index)
output_file = f"radiosonde_data_{station}.xlsx"

radiosonde_df.to_excel(output_file, index=False)
print(f"Excel-Datei '{output_file}' wurde erfolgreich erzeugt.")

