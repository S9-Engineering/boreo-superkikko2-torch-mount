# BOREO / Superkikko2 — R10 arrotondata, logo S9 e ponte2mm

**Pronto per la stampa dei soli prototipi in ELEGOO PETG Pro.** La resistenza funzionale, l’appoggio reale e la temperatura non sono convalidati. Nessuna stampa avviata. R10 sostituisce R09 per la nuova prova; conservate tutte le revisioni precedenti.

[Anteprima R10](anteprime/PROVA_R10_PETG_anteprima.png) · [Provino dell’appoggio e dei supporti](anteprime/PROVINO_SUPPORTI.png)

## Due progetti da stampare in ordine

| Piatto | Contenuto | File completo ElegooSlicer | Stima dello slicing, supporti inclusi |
| --- | --- | --- | --- |
| **A — prima prova** | Ponte interno2mm + provino appoggio destro con logo/tasca dado | [3MF A](stampa/PETG_PRO_ECC2/A_PROVINO_PONTE/BOREO_R10_A_PROVINO_PONTE_PETG_PRO_ECC2_04.3mf) · [G-code A](stampa/PETG_PRO_ECC2/A_PROVINO_PONTE/BOREO_R10_A_PROVINO_PONTE_PETG_PRO_ECC2_04.gcode) | **55min8s ·12,41g** |
| **B — base** | Piastra arrotondata con logo S9 e tre passaggi farfalla | [3MF B](stampa/PETG_PRO_ECC2/B_BASE_ARROTONDATA/BOREO_R10_B_BASE_ARROTONDATA_PETG_PRO_ECC2_04.3mf) · [G-code B](stampa/PETG_PRO_ECC2/B_BASE_ARROTONDATA/BOREO_R10_B_BASE_ARROTONDATA_PETG_PRO_ECC2_04.gcode) | **1h58min41s ·30,30g** |

A contiene il ponte che si userà con B: **non occorre ristamparlo**. Il piccolo provino è una sezione della base vera per valutare distacco supporti, accesso al dado e leggibilità del logo; non si monta con B. Stime su densità1,25g/cm³ del profilo, non masse misurate.

I due3MF sopra sono progetti nativi con macchina, filamento, impostazioni e percorso incorporato. Gli altri3MF con SOLO_GEOMETRIA nel nome contengono solo geometria/disposizione. STL e STEP per pezzo sono in stampa, una copia ciascuno, orientati in millimetri. I tre pezzi presenti nella disposizione geometrica generale non costituiscono un unico piatto di lavoro: stampare A e B separati.

## Modifiche di forma

Piastra di appoggio nominale67,5×46×5mm con **raccordi da5mm** agli angoli; arrotondate anche le estremità della cornice con raggio6mm. Ingombro della base circa102,8×25,6×46mm. Superficie verso la farfalla ancora sul pianoY8, tre passaggi e scarichi rivetti conservati. Rinforzato l’unione dei raccordi laterali con il pannello. Le teste dei rivetti devono rimanere libere: dimensioni/posizioni degli scarichi12×12mm sono provvisorie, non rilevate con misura diretta.

**Logo S9 estruso2,00mm** sul fianco esterno del supporto destro, pianoX49 e rilievo fino aX51, largo16mm e alto7,80mm circa. Questa posizione lascia libera tutta la faccia di appoggio della farfalla, i passaggi e la parte interna del casco. Il logo è fuso alla base, stesso PETG, senza cambio colore. Sorgente SVG originale incluso e hash verificato; il parser legge solo coordinate geometriche M/L/Z, con semplificazione massima0,025mm per evitare microsegmenti. L’extrusione comprende0,05mm interni di fusione: il rilievo esterno resta2mm.

Ponte: pelle curva **2mm**, altezza16mm, bordo inferiore Z21 e superiore Z37. Conservata la curva esternaR92; crescita di0,8mm verso la testa rispetto aR09, da verificare. Terminali nelle feritoie9,2×3,2 e assi±42 invariati, con riscontro CAD nel tratto esterno. Il solo prototipo R06 aveva il riscontro di ingresso dell’utente con flessione; non attribuire quel risultato al ponte R10 da2mm. [Valutazione dello spessore](verifiche/valutazione-ponte-2mm.md).

## Prima di stampare B

A freddo, staccare i supporti dal provino e verificare: distacco senza strappare il pezzo; assenza di pezzi saldati sui fianchi; fondo dei ripiani non cedevole; tasca dado libera e dado M3 reale inseribile da sotto; logo leggibile. Una certa rugosità sui contatti rimane possibile. Le nuove distanze supporti sono **da provare**, non una soluzione fisicamente dimostrata. [Indagine dei residui](verifiche/indagine-supporti.md).

Provare il ponte2mm nel casco fermo, non indossato: terminali senza forzatura, stessa quota inferiore della vecchia dima arancione R06, nessun contatto fastidioso con cuscinetto o testa. Se entra solo flettendo le alette o comprimendo la schiuma, interrompere. L’aumento a2mm non deve diventare un nuovo serraggio sul casco.

Dopo esito positivo stampare B. Usare il ponte di A e il giunto esterno già previsto:2viti M3×16,2rondelle3,2×7×0,5,2dadi autobloccanti M3 AF5,5/H4 in tasche AF5,85/profondità4,3. Componenti grigi nell’anteprima sono riferimenti metallici schematici, non da stampare. Serraggio funzionale ancora da definire: per la prova solo contatto leggero, niente compressione della schiuma.

Avvicinare farfalla e lampada spenta sostenendole a mano o sul tavolo. Tre passaggi3×1,9mm, lateraliX±28,75/Z22,6 e superioreX0/Z41,5. Luce metallica2mm confermata anche in alto, ma posizione superioreZ41,5 ancora assunta. Interasse57,5 calcolato dalla larghezza fotografica circa63,5, non misurato direttamente. La dima a tre piolini R09 rimane valida se già stampata. Spessore della lamiera e sporgenza dei rivetti ancora da rilevare. Una vite M1,6 con rondella/dado è una candidata, non ferramenta funzionale approvata; M3 non passa nelle asole metalliche2mm. I tre fori stampati sono predisposizioni geometriche, non filettature o sedi autofilettanti.

## Impostazioni e preparazione

**Centauri Carbon2 Combo, ugello0,4mm, PEI testurizzato, ELEGOO PETG Pro confermato dall’utente.** ElegooSlicer1.5.3.5 / motore CLI2.4.2. Macchina/macro identiche R09; profilo specifico PETG Pro compatibile ECC2. Caricare PETG Pro nel canale selezionato, non usare i G-code PLA precedenti. Materiale asciutto e piano pulito; se serve essiccazione seguire etichetta/scheda della bobina, non un tempo generico. Nessuna configurazione TPU o multicolore.

Strato e primo strato0,20mm; **5pareti,30%gyroid,5strati sopra e sotto**. Ugello240°C, PEI65°C, portata massima5mm³/s, flusso0,98 del profilo. Parete esterna40/interna60/infill70/primo25mm/s; ponti25, supporti45 e interfaccia30mm/s. Ventola normale10–40%, primi3strati senza, sbalzi90% come profilo. Flusso/anticipo pressione/temperature sono valori iniziali del profilo, non calibrazioni misurate sulla bobina dell’utente. Parametri termici entro l’intervallo pubblicato nella [scheda ELEGOO](https://www.elegoo.com/products/petg-pro-filament-1-75mm-colored-1kg).

**Brim disattivato**, nessun raft o torre. Supporti normali snug dal piano per base e provino, **nessun supporto sul ponte**. Distanza superiore/inferioreZ0,40mm, lateraleXY0,55mm,2strati di interfaccia con spaziatura0,5mm. Rispetto aR09 più margine di distacco; possibile peggioramento della superficie inferiore, da valutare prima sul provino. Non disattivare tutti i supporti: i ripiani esterni e le tasche dado ne richiedono. Lasciare raffreddare prima della rimozione. Nessun avviso dello slicer nei due file finali.

## Verifiche e limiti

141 controlli geometrici superati sui file riaperti: mesh chiuse/manifold, normali, volume, frammenti, facce degeneri/duplicate e screening delle autointersezioni non adiacenti, STEP, scala/unità/trasformazioni, giochi e assieme, rilievo logo2mm, raggi e passaggi. [Report geometria](verifiche/geometria.json). Lo screening non è prova matematica completa delle autointersezioni. I progetti nativi sono riaperti dal controllo del pacchetto e il G-code esterno coincide con quello incorporato.

Slicing reale di tutti135+230strati renderizzato e rivisto: primo strato, pareti/fori, lettere del logo, supporti, aperture e ponti sugli scarichi presenti. Zero isole candidate nel risultato finale. Nel primo provino una striscia della piastra tagliata partiva sospesa; il provino è stato ristretto per eliminarla e tutti gli esportati/slicing/anteprime ricontrollati. Riferimenti ai percorsi: [A](verifiche/slicing/A_PROVINO_PONTE/report.json), [B](verifiche/slicing/B_BASE_ARROTONDATA/report.json), [logo](verifiche/logo_percorsi.json). Queste verifiche non dimostrano finitura o distacco reale.

**PETG e2mm sono una nuova prova, non una garanzia di tenuta della torcia.** Restano da verificare montaggio, carico, serraggio, ritenuta, comportamento prolungato e temperatura dei contatti, anche nell’uso umido/immerso. Non accendere la torcia o affidarne il peso al prototipo prima di queste verifiche. La piastra plastica non è un dissipatore; il contatto completo può ridurre lo scambio del metallo con aria/acqua. Nessun foro, colla o elastico aggiunto al casco. Nessuna prova di compatibilità protettiva.

## Riproduzione

Dipendenze in sorgenti/requisiti.txt, CadQuery2.8 e trimesh5.1.1; script/parametri/SVG modificabili inclusi. Da questa cartella:

```sh
python sorgenti/genera.py
python sorgenti/verifica.py
python sorgenti/crea_anteprime.py
python sorgenti/prepara_slicing_petg.py --piatto A_PROVINO_PONTE
python sorgenti/prepara_slicing_petg.py --piatto B_BASE_ARROTONDATA
python sorgenti/verifica_logo_percorsi.py
python sorgenti/verifica_pacchetto.py
```

Dopo una modifica rigenerare tutti i derivati e completare nuovamente i controlli e la revisione visiva prima della stampa. Report complessivo in verifiche/pacchetto.json; stato della consegna in verifiche/STATO_CONSEGNA.json.
