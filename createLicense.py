import requests
import json
import random
import string
from datetime import datetime, timedelta

# Discord-Webhook-URL einfügen
webhook_url = "YOUR-WEBHOOK-HERE"

# Dateiname für die Lizenzdatei
filename = "lizenzen.txt"

print()
print()

name = input("Auf wen soll die Lizenz registriert werden? > ")
expiration = int(input("Wie lange soll die Lizenz gültig sein? > "))

print()
print()

# Funktion zur Erstellung einer neuen Lizenz
def neue_lizenz():
    # Zufällige Lizenz-ID generieren
    lizenz_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    # Ablaufdatum berechnen
    ablaufdatum = datetime.now() + timedelta(days=expiration)
    # Lizenz-Dictionary erstellen
    lizenz = {"Username": name,"License": lizenz_id, "Expiration_Date": ablaufdatum.strftime('%Y-%m-%d')}
    return lizenz

# Neue Lizenz erstellen
neue_lizenz = neue_lizenz()

# Lizenzdaten in Datei schreiben
with open(filename, "a") as f:
    f.write(json.dumps(neue_lizenz))
    f.write("\n")

# Lizenz-Code und Ablaufdatum an Discord-Webhook senden
embed = {
    "title": "Neue Lizenz erstellt",
    "color": 65280,  # Grün
    "fields": [
        {
            "name": "Username",
            "value": name
        },
        {
            "name": "Lizenz-Code",
            "value": neue_lizenz['License']
        },
        {
            "name": "Ablaufdatum",
            "value": neue_lizenz['Expiration_Date']
        }
    ]
}

# Payload erstellen
payload = {
    "embeds": [embed]
}

# POST-Anfrage an den Webhook senden
response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

# HTTP-Statuscode ausgeben
print(response.status_code)
