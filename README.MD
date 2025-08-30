Network Notification Widget
===========================

Popis
-----
Tento Python widget slouží k zobrazování notifikací ve firemní síti.

- Načítá zprávy ze serveru (server.py) a zobrazuje je ve widgetu na ploše.
- Každá nová zpráva má ikonu 📢 u prvního řádku zprávy.
- Widget zobrazuje také lokální IP adresu počítače.
- Pokud je widget minimalizovaný a přijde nová zpráva, automaticky se rozbalí.
- Widget lze minimalizovat do malé ikony na okraji obrazovky.

Funkce
------
- Přehledné zobrazování aktivních zpráv.
- Podpora víceřádkových zpráv – pouze první řádek má ikonu.
- Systémové oznámení (notifikace Windows).
- Zobrazení lokální IP adresy (např. 192.168.x.x).
- Minimalizace a obnovení widgetu.

Instalace
---------
1. Nainstalujte Python 3.x.
2. Nainstalujte požadované balíčky:
   pip install PyQt5 requests
3. Spusťte widget:
   python widget.py
4. Spusťte server poskytující notifikace (server.py) – doporučeno přes WSGI server
   (např. gunicorn, waitress) nebo jiný webserver podporující Python.

Přizpůsobení
------------
- SERVER_URL – změňte URL serveru, odkud widget stahuje zprávy.
- LINE_LENGTH – délka řádku zprávy.
- WIDGET_WIDTH – šířka widgetu.
- MARGIN – prostor kolem widgetu.

Distribuce
----------
Widget lze převést na EXE pomocí pyinstaller a rozeslat na všechny stanice v síti:

   pyinstaller --onefile --noconsole widget.py

Server (server.py) lze nasadit na centrální server jako webovou službu. 
Widget potom získává zprávy z centrálního serveru a zobrazuje je lokálně.

Služba ve Windows
-----------------
Widget lze spustit jako službu pomocí nssm nebo jiného Windows service manageru.
Tím zajistíte, že poběží na pozadí a automaticky se spustí po startu systému.
