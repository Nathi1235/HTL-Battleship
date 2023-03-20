# HTL-Battleship
A Battleship-Game based on Python for School

## Current Functionality
```
A GUI to register as a new user or login as an existing user.
Password Confirmation in th Register-Window is also included.
```

## Funktionen
### GUI:
* Client-Liste (Sichtbar: Name, Gespielte Spiele, Gewonnene Spiele), sortiert nach Gewonnene Spiele pro Gespielte Spiele
* Schiffe über GUI platzieren (Position, Rotation)
* Spiel GUI (eigenes Feld oben, gegnerisches Feld zum Schießen unten)
* Nach Spiel wieder beim Startscreen
* Statistik (Wie viele Schiffe getroffen, evtl. Prozentsatz von zerstörten Schiffen)
* Soundtrack und Bilder
### Schiffe:
* Schiffe sind verschieden groß
* Mindestens 8 Schiffe
* Jedes Schiff hat einen Namen und einen Typ
### Logik:
* Über Netzwerk (Spieler muss eindeutig erkennbar sein, d.h. Name oder ID)
* 15 Sekunden Timer pro Schuss 
* Server updatet Spielerdaten
* Spielfeldgröße fix
* 2 Minuten-Timer für Platzierung der Schiffe

## Einteilung
### Login Page
* User Erstellen/login
* Speichen von Daten Wins/Games, Name, Passwort(Verschlüsselt)
* Gui + Graphics für Hauptscreen

### Game Logic Server
*Spielfeld Management
* Spielablauf
* Networking
* Multiprocessing/threading

### Gui Clients + Game Logic
* Schiffe platzieren
* Gui

### Matchmaking
* Random/Play with friend
