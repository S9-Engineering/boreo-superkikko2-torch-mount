# Farfalla Superkikko2 — rilievo e aggiornamento delle asole

**Stato: riferimento CAD preliminare da completare, non una base pronta per lo slicer o per la stampa.** Sette foto originali del calibro archiviate con SHA-256. Integrata la conferma diretta dell'utente: foro/asola da **2 mm** e bordo metallico accanto da **2 mm**. Nessuna modifica ai file di stampa R06/R07 e nessuna stampa avviata.

[Schema aggiornato](anteprime/rilievo_quote.png) · [Riferimento STEP, non stampare](riferimenti-CAD-NON-STAMPARE/FARFALLA_STIMA_NON_STAMPARE.step) · [Riferimento GLB, non stampare](riferimenti-CAD-NON-STAMPARE/FARFALLA_STIMA_NON_STAMPARE.glb)

## Interasse ricavato

La larghezza totale dalla foto1 è circa **63,5 mm**. La luce dell'asola e la larghezza del bordo esterno sono dichiarate entrambe **2 mm** dall'utente. Assumendo le due alette uguali, ogni centro è a `2 + 2/2 = 3 mm` dal rispettivo bordo esterno della lamiera:

**Interasse = 63,5 − 3 − 3 = circa 57,5 mm.**

Formula generale: `I = W − b_sx − b_dx − (a_sx + a_dx)/2`, dove `W` è l'ingombro totale della lamiera, `b` il bordo esterno di ciascuna asola e `a` la larghezza libera del foro. Per asole e bordi uguali: `I = W − 2b − a`.

L'interasse è **calcolato**, non misurato direttamente. La sola fascia di lettura fotografica W63–64 mm trasferisce I57–58 mm, a parità delle quote dichiarate. Non è una tolleranza strumentale certificata. I centri nominali nel riferimento sono **X = −28,75 e +28,75 mm**. Non riutilizzare per questa misura i63mm delle feritoie del casco.

I2mm del bordo **nel piano della farfalla** non sono lo spessore della lamiera fra le due facce. Quest'ultima misura rimane ignota.

## Quote e provenienza

| Fonte | Grandezza | Dato usato |
| --- | --- | --- |
| Foto1 | Larghezza esterna totale | circa63,5 mm, lettura indicativa |
| Conferma diretta utente | Luce delle asole verticali | **2 mm**, applicati ai due lati per simmetria |
| Conferma diretta utente | Bordo esterno accanto all'asola | **2 mm**, applicati ai due lati per simmetria |
| Calcolo | Interasse asole verticali | **circa57,5 mm** |
| Foto5 | Larghezza traversina superiore | circa31 mm |
| Foto6 | Distanza presa dai becchi, probabilmente sommità T / bordo inferiore traversa centrale | circa36 mm; estremi ancora da confermare |
| Foto7 | Larghezza collo centrale | circa10,5 mm |

Le cifre fotografiche non hanno precisione al centesimo: angolo di ripresa, nonio e contatti restano limiti del rilievo. Le letture originarie sono conservate come storico; l'aggiornamento dell'utente è separato. [Dati e originali](sorgenti/letture-foto.json).

## CAD aggiornato

Il solido parametrico usa larghezza totale63,5, traversina31, collo10,5, **asole laterali2 e interasse57,5 mm**. Le precedenti ipotesi di asole3,2 e interasse56,5 sono state sostituite.

**Altezza totale44,5 mm, spessore lamiera1,5 mm, lunghezza delle asole26,4 mm, bordo interno2 mm e raccordi rimangono ipotesi illustrative.** La larghezza esterna di ogni aletta nel disegno è6 mm: 2 esterni dichiarati + 2 di foro dichiarati + 2 interni assunti. La quota reale del bordo interno non serve alla formula dell'interasse; serve invece a riprodurre esattamente l'intera sagoma. L'asola superiore resta illustrativa, non misurata. Rivetti omessi in altezza. [Parametri con provenienza distinta](sorgenti/parametri-riferimento.json).

STEP esportato riaperto: un solido valido e volume positivo. GLB in metri verificato contro lo STEP per scala, mesh chiusa, normali e volume. [Report rigenerato](verifiche/riferimento.json). Questi controlli non provano accuratezza sul metallo reale, montaggio o resistenza.

## Effetto sul fissaggio della base

Le asole da2mm **non consentono il passaggio delle M3**. Un'M2 nominale da2mm non dà gioco nominale: non è selezionata automaticamente. Per un collegamento passante senza modificare la farfalla, una **M1,6 con rondella e dado metallico è un candidato**, ancora da verificare su componenti reali, accesso e carico. Le guide dimensionali dei produttori riportano passaggi di1,8–2,0mm per M1,6: [TR Fastenings](https://www.trfastenings.com/Knowledge-Base/Engineering-Data/tapping-sizes-and-clearance-holes), [Accu](https://www.accu.co.uk/p/449-tapping-drill-size-chart-clearance-holes). Sono raccomandazioni dimensionali, non una verifica di resistenza della nostra struttura.

**Le M3 della R07 continuano a unire ponte interno e base esterna**: è un giunto distinto dalle future viti farfalla/base. Dimensioni ridotte del foro non autorizzano nuovi fori nel metallo o nel casco.

La futura base conserva ponte unico, limite inferiore R06 e giunto esterno bullonato. Faccia verso la farfalla con due appoggi locali sotto le asole e scarico centrale per rivetti; assi nominali laterali a57,5 mm. Una piccola regolazione orizzontale può assorbire la lettura fotografica ancora approssimata. Appoggi, regolazione e fori non sono ancora rilasciati per stampa.

## Quote ancora aperte

Per chiudere appoggi, scarichi e pacco di serraggio resta **lo spessore reale della lamiera fra le due facce**, distinto dal bordo nel piano. Restano utili una vista di profilo lato casco e la sporgenza dei rivetti, oltre alla conferma dei contatti della foto6. Larghezza e interasse delle asole non vengono più richiesti come dati totalmente mancanti: sono rispettivamente dichiarati e calcolati.

Materiale, carichi e temperatura rimangono da verificare prima dell'uso funzionale. Questo rilievo non contiene una nuova base o un nuovo G-code.

## Riproduzione

Python3.11, CadQuery2.8.0, trimesh5.1.1, NumPy e Matplotlib; versioni in [requisiti.txt](sorgenti/requisiti.txt). Dalla cartella del rilievo:

```sh
python sorgenti/ricostruisci_riferimento.py
```

Il comando rigenera STEP/GLB, anteprima e report, senza azioni sulla stampante.
