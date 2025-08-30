<h1>Network Notification Widget</h1>

<h2>Popis</h2>
<p>Tento Python widget slouží k zobrazování notifikací ve firemní síti.</p>
<ul>
  <li>Načítá zprávy ze serveru (<code>server.py</code>) a zobrazuje je ve widgetu na ploše.</li>
  <li>Každá nová zpráva má ikonu 📢 u první řádky zprávy.</li>
  <li>Widget zobrazuje také <strong>lokální IP adresu</strong> počítače.</li>
  <li>Pokud je widget minimalizovaný a přijde nová zpráva, automaticky se rozbalí.</li>
  <li>Widget lze minimalizovat do malé ikony na okraji obrazovky.</li>
</ul>

<h2>Funkce</h2>
<ul>
  <li>Přehledné zobrazování aktivních zpráv.</li>
  <li>Podpora víceřádkových zpráv – pouze první řádek má ikonu.</li>
  <li>Systémové oznámení (notifikace Windows).</li>
  <li>Zobrazení lokální IP adresy (např. 192.168.x.x).</li>
  <li>Minimalizace a obnovení widgetu.</li>
</ul>

<h2>Instalace</h2>
<ol>
  <li>Nainstalujte Python 3.x.</li>
  <li>Nainstalujte požadované balíčky:
    <pre><code>pip install PyQt5 requests</code></pre>
  </li>
  <li>Spusťte widget:
    <pre><code>python widget.py</code></pre>
  </li>
  <li>Spusťte server poskytující notifikace (<code>server.py</code>) – doporučeno přes WSGI server (např. <code>gunicorn</code>, <code>waitress</code>) nebo jiný webserver podporující Python.</li>
</ol>

<h2>Přizpůsobení</h2>
<ul>
  <li><code>SERVER_URL</code> – změňte URL serveru, odkud widget stahuje zprávy.</li>
  <li><code>LINE_LENGTH</code> – délka řádku zprávy.</li>
  <li><code>WIDGET_WIDTH</code> – šířka widgetu.</li>
  <li><code>MARGIN</code> – prostor kolem widgetu.</li>
</ul>

<h2>Distribuce</h2>
<p>Widget lze převést na <strong>EXE</strong> pomocí <code>pyinstaller</code> a rozeslat na všechny stanice v síti:</p>
<pre><code>pyinstaller --onefile --noconsole widget.py</code></pre>

<p>Server (<code>server.py</code>) lze nasadit na centrální server jako <strong>webovou službu</strong>. Widget potom získává zprávy z centrálního serveru a zobrazuje je lokálně.</p>

<h2>Služba ve Windows</h2>
<p>Widget lze spustit jako službu pomocí <strong>nssm</strong> nebo jiného Windows service manageru. Tím zajistíte, že poběží na pozadí a automaticky se spustí po startu systému.</p>
