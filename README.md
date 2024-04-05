# Skippo/Eniro GPX delta
Exportering av Skippo/Eniro blir endast en jättestor gpx-fil.  
När man importerar den i Navionics boating blir det dubletter med tidigare
importeringar. Vansinne utbryter...

För att råda bot på detta skapar detta program en delta-gpx från föregående.
Importerar man delta-gpx så elimineras problemet med dubletter.

Principen är att man exporterar från eniro till google drive. 
Detta program körs på vilken dator som helst som har google drive installerat.
Programmet övervakar nya exporter och gör då en ny delta-gpx.
Denna kan då importeras till Navionics boating.
