Readme Auswertungsskripte:

Mit den Python-Skripten k�nnen die eigenen Kontodaten ausgewertet werden, wobei am Ende der Auswertung eine aufbereitete Excel-Datei steht sowie mehrere Plots zur Auswertung im jpg-Format ausgegeben werden.
Basis s�mtlicher Auswertung ist die Zuordnung einzelner Buchungen zu Kostengrupper/-kategorien. Daf�r wird die Excel-Zuordnungstabelle genutzt. Wichtig ist, dass der Suchtext klein und zusammengeschrieben wird, Satzzeichen (./?!-_:;,) bleiben erhalten.
Das Skript nimmt den Buchungstext und entfernt Leerzeichen und Gro�buchstaben zur eindeutigen Zuordenbarkeit. Kategorien (rechte Spalte) k�nnen mehr oder weniger frei gew�hlt werden, allerdings werden "Lohn","Einzahlungen" f�r bestimmte Zuordnungen 
ben�tigt. Insofern sollten diese Namen nicht ver�ndert werden. Gleiches gilt f�r "Miete" und "Aktiengesch�fte","ETFS / Wertpapiersparen". Sofern Vorg�nge in diesen Bereichen erfolgt sind, sollten sie auch diesen Kategorien zugeordnet werden,
um enntsprechende Plots zu erhalten. Um entsprechende Kategorien bilden zu k�nnen, m�ssen die einzelnen Buchungen einmal durchgesehen werden, um Wiederholungen zu erkennen und entsprechend zuzuschl�sseln.
Alle Buchungen ohne entsprechende Schl�sselw�rter werden unter "Sonstiges" kategorisiert.

Wichtig vor der Auswertung ist, auf die Frage des Datenordners den genauen Dateipfad des Ordners anzugeben, in dem sich die *.csv-Dateien befinden (Linux: /.../.../, Windows: C:\..\...\..\). Auf die Frage des 
Dateinamens ist der komplette Dateiname mit Dateiendung einzugeben, sonst bricht das Skript ab.

Es gibt drei Skripte zur Anwendung auf Kontodaten:

1) Kontoauswerter_comdirect.py:
Girokontodaten und Kreditkartendaten der Comdirect k�nnen damit aggregiert und ausgewertertet werden. Beide Datens�tze m�ssen online separat als *.csv ausgeleitet werden, im Skript erfolgt dann die Abfrage, ob Kreditkartendaten
zus�tzlich in den Datensatz eingelesen werden sollen. Sollte Urlaub als Kategorie vorhanden sein, werden alle Buchungen dazu als separates Excel-Tabellenblatt ausgegeben. Das Skript greift auf das erste Tabellenblatt der Zuordnungstabelle
zu.

2) Kontoauswerter_DKB_giro.py:
Mit diesem Skript werden nur die Girokontodaten der DKB ausgewertet. Eine Auswertung der Kreditkartendaten erfolgt �ber ein separates Skript, da ich die DKB-Kreditkarte fast ausschlie�lich zur Bargeldabhebung nutze und daher eine andere Zuordnungstabelle
(nach Orten) verwendet wird. Auch in diesem Skript werden Urlaube separat ausgeleitet.

3) Kontoauswerter_DKB_KK.py:
Dieses Skript dient lediglich dazu Bargeldabhebungen nach Orten zu kategorisieren. Zus�tzlich k�nnen noch die ausgeleiteten Urlaubskosten aus den Girokonten hinzugenommen werden, sodass auch eine detaillierte Ausgaben�bersicht zu den
Urlauben erfolgen kann. Eine prozentuale Aufteilung der Kosten als Tortendiagramm erfolgt hier nicht, da dies in meinen Augen f�r reine Ortskategorien nicht sonderlich hilfreich ist.

4) Plotter_adjusteddata.py:

Dieses Skript dient dazu neue Plots zu erstellen, sofern die aus einem der anderen Skripte ausgeleitete Auswertungstabelle h�ndisch noch einmal ver�ndert wurde (z.B. die Kategorisierung manuell angepasst wurde). Es k�nnen dieselben Plots ausgegeben werden,
wie in den anderen Skripten.


