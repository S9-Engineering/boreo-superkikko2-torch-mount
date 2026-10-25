# BOREO / Superkikko2 — R09 piastra continua e tre fissaggi

**Pronto per la stampa dei soli provini in ELEGOO PLA Basic.** R09 sostituisce R08 per la nuova richiesta: appoggio piano completo della farfalla e terzo fissaggio all’aletta superiore. Non è il supporto funzionale definitivo e non è un dissipatore. Nessuna stampa avviata.

[Anteprima](anteprime/PROVA_R09_PLA_anteprima.png) · [Dima a tre piolini](anteprime/DIMA_INTERASSE.png)

## File da stampare

| Piatto | Progetto completo ElegooSlicer | Stima reale, inclusi supporti |
| --- | --- | --- |
| A — dima a tre piolini | [3MF A](stampa/PLA_BASIC_ECC2/A_DIMA/BOREO_R09_A_DIMA_PLA_BASIC_ECC2_04.3mf) · [G-code A](stampa/PLA_BASIC_ECC2/A_DIMA/BOREO_R09_A_DIMA_PLA_BASIC_ECC2_04.gcode) | **6 min 3 s · 1,59 g** |
| B — piastra e ponte | [3MF B](stampa/PLA_BASIC_ECC2/B_BASE_PONTE/BOREO_R09_B_BASE_PONTE_PLA_BASIC_ECC2_04.3mf) · [G-code B](stampa/PLA_BASIC_ECC2/B_BASE_PONTE/BOREO_R09_B_BASE_PONTE_PLA_BASIC_ECC2_04.gcode) | **1 h 41 min 4 s · 28,63 g** |

I due 3MF sopra sono progetti dello slicer con macchina, filamento, impostazioni e percorso incorporato. Gli altri 3MF con SOLO_GEOMETRIA nel nome conservano soltanto geometria e disposizione. STL e STEP separati per ogni pezzo sono nella cartella stampa, già orientati, una copia ciascuno, in millimetri.

**Stampare prima A.** Se i tre piolini entrano insieme e la dima resta piana si passa a B. Se il piolino superiore non corrisponde, annotare lo scostamento e correggere la posizione prima di stampare B: non flettere o forzare la dima. La R08 con due appoggi resta uno storico, non include il nuovo punto superiore.

## Quote e ipotesi

Piastra di appoggio continua **67,5 × 46 × 5 mm**, faccia piana verso la farfalla, raccordi sui bordi. Ingombro della base completa circa **102,8 × 25,6 × 46 mm**. Rimangono due scarichi passanti **12 × 12 mm** con angoli raccordati, centri X±14,5/Z13,5, per evitare che i rivetti diventino punti di appoggio. Posizione e dimensione degli scarichi sono **provvisorie**: la sporgenza reale dei rivetti non è stata misurata. Piastra continua significa sostegno della sagoma metallica salvo questi scarichi e i tre passaggi; non garanzia di contatto su una farfalla eventualmente piegata.

Tre passaggi orizzontali di prova **3 × 1,9 mm**: laterali a X±28,75/Z22,6 e superiore X0/Z41,5. I due centri laterali sono a **57,5 mm**, calcolati dalla larghezza fotografica circa63,5, bordo esterno2 e luce2. I 2 mm delle asole laterali **e dell’asola superiore** sono confermati dall’utente il22 ottobre2026. L’altezza dell’asola superiore è una quota distinta dalla posizione del suo centro: **Z41,5 resta assunta**, derivata dalla sagoma illustrativa alta44,5, ancora da rilevare. Anche la distanza verticale fra i tre punti è da verificare con la dima.

La dima misura **63,5 × 24,9 × 2,8 mm**: corpo1,6 e tre pioliniØ1,6 alti1,2, interasse laterale57,5, terzo piolino18,9mm sopra la linea dei laterali. Gioco nominale dei piolini nelle asole2mm:0,4mm diametrale/0,2mm radiale. Non è una misura di precisione o una convalida delle viti reali. Provare singolarmente i piolini se l’ingresso simultaneo fallisce; se un piolino tocca il corpo lampada, interrompere senza interpretarlo come errore di interasse.

I passaggi nella base sono predisposizioni dimensionali per un futuro fissaggio di piccolo diametro. Una vite M1,6 passante con rondella e dado metallico è una candidata da verificare; **non comprare o scegliere ferramenta definitiva sulla sola base del provino**. Non sono filettature o sedi per autofilettanti. Le M3 del giunto casco/base non passano nelle asole metalliche da2mm. Nessun foro nuovo sul casco o sulla farfalla.

Il ponte interno rimane identico geometricamente alla R07/R08: pelle radiale1,2mm, altezza16mm, bordo inferiore Z21 identico alla R06 e crescita solo verso l’alto, terminali9,2×3,2 e interasse84mm assunto per il casco. Nessun aumento dello spessore interno per aggiungere la piastra. Non è ancora fisicamente verificato: l’unico riscontro fisico precedente riguarda R06, con terminali al limite e flessione.

## Prova di appoggio

Con lampada spenta sul tavolo, provare la dima dalla faccia della farfalla rivolta al casco. I tre piolini devono entrare senza piegare la dima. Registrare prima i due laterali, poi lo scostamento del superiore. Il gioco delle asole metalliche permette regolazione verticale; la dima non definisce da sola la posizione finale della lampada.

Su B, rimuovere tutti i supporti da ripiani e tasche dado. Provare prima il ponte nel casco fermo e non indossato, confrontando il limite inferiore con la vecchia dima arancione R06 e verificando il cuscinetto. Inserire la base sui terminali senza tirare la schiuma. Giunto esterno invariato: **2 viti M3×16,2 rondelle3,2×7×0,5,2 dadi autobloccanti M3 AF5,5/H4**; sedi AF5,85/profondità4,3 aperte da sotto. Solo contatto leggero per la prova, niente coppia funzionale prescritta. Il montaggio con la ferramenta reale resta da verificare; si può tenere il provino a mano.

Avvicinare la farfalla alla piastra sostenendo sempre la lampada con la mano o col tavolo. Verificare contatto della traversa, collo, estremità laterali e T superiore; nessun rivetto deve toccare prima delle superfici metalliche piane. I tre passaggi devono restare raggiungibili anche sul retro per il futuro dado/rondella: registrare se una parte del casco o del gruppo lampada li rende inaccessibili. Non flettere il metallo per farlo aderire. Servono vista frontale, vista di profilo, eventuale luce sotto un righello e spessore della lamiera fra le facce, ancora sconosciuto. Le due finestre non rappresentano quote dei rivetti già misurate.

## Calore: distinzione necessaria

L’appoggio completo offre una superficie meccanica più estesa. **PLA e PETG ordinari non sono dissipatori:** uno studio sperimentale sui polimeri FFF riporta per diversi campioni valori di conducibilità bassi, nell’ordine dei decimi di W/(m·K), dipendenti da materiale, riempimento e temperatura. Questi valori non sono dati misurati della bobina ELEGOO dell’utente. [Studio originale, Materials2025](https://www.mdpi.com/1996-1944/18/17/3950).

Inferenza progettuale: coprire il retro metallico con la piastra plastica può ridurre lo scambio con aria o acqua e aumentare la temperatura locale; non si può attribuire alla R09 un miglioramento termico. Serve misurare la temperatura della farfalla, nei tre contatti con lo stampato e presso il dissipatore con montaggio originale, nelle condizioni ammesse dal produttore. La [scheda Superkikko2](https://www.kikkolamp.com/superkikko2) indica corpo/dissipatore in alluminio ma non fornisce la temperatura dei nuovi contatti.

Se l’obiettivo comprende realmente dissipare il calore su un’area maggiore, occorre valutare una piastra metallica con superfici esposte e collegamento termico definito; materiale, area, spessore, interfacce e collegamento alla plastica vanno dimensionati e verificati. Non è inclusa né simulata una piastra metallica nella R09. Non collocare un metallo caldo a contatto con la schiuma del casco. Il mantenimento della farfalla/U originali non dimostra da solo compatibilità termica.

**Non accendere la torcia sul provino PLA e non affidargli il peso.** I test geometrici precedono scelta del materiale funzionale, serraggio, carichi, ritenuta e uso in umidità/immersione. Non sono dimostrate prestazioni protettive del casco modificato.

## Stampa verificata digitalmente

ELEGOO Centauri Carbon2 Combo, ugello0,4mm, PEI testurizzato, ELEGOO PLA Basic, profili specifici ECC2 da R08. ElegooSlicer1.5.3.5, motore CLI2.4.2. Strati e primo strato0,20mm;3pareti;20%gyroid;3strati sopra/sotto;220°C ugello/60°C piano;esterno50/interno80/infill100/primo25mm/s,limite12mm³/s. Parametri di partenza riutilizzati, non nuova calibrazione fisica.

**Senza brim** e senza raft/torre; A senza supporti, B con supporti normali aderenti dal piano, locali rimovibili dal fondo e dalle tasche dado. Il ponte si stampa verticale sulla sua sottile base curva, come R07. Piano pulito e osservazione dell’adesione iniziale restano necessari. Avviso PLA conservato `bed_temperature_too_high_than_filament`: **sportello aperto e/o vetro superiore rimosso**, come da profilo, senza falsificare i parametri del materiale.

128 controlli geometrici superati sui file riaperti, incluse mesh chiuse/manifold, normali, volumi positivi, degeneri, duplicati, screening di autointersezioni non adiacenti, STEP, unità/trasformazioni, passaggi, scarichi, piani di appoggio e confronto del ponte con R07. [Report](verifiche/geometria.json). Screening delle autointersezioni non equivale a prova matematica completa. Slicing reale:14+230strati, tutto il percorso renderizzato e rivisto, nessuna isola di parete candidata, tre piolini presenti nell’ultimo strato A; supporti accessibili e ponti sui due scarichi limitati alla loro luce. I due progetti nativi sono riaperti nello slicer dal controllo del pacchetto e il G-code esterno coincide con quello incorporato. Riscontro nel file verifiche/pacchetto.json.

## Riproduzione

Dipendenze in sorgenti/requisiti.txt, parametri e STEP del ponte originale inclusi. Python3.11 con CadQuery2.8.0, trimesh5.1.1. Eseguire in ordine dalla cartella:

```sh
python sorgenti/genera.py
python sorgenti/verifica.py
python sorgenti/crea_anteprime.py
python sorgenti/prepara_slicing_pla.py --piatto A_DIMA
python sorgenti/prepara_slicing_pla.py --piatto B_BASE_PONTE
python sorgenti/verifica_pacchetto.py
```

Dopo ogni modifica rigenerare esportati, anteprime e slicing, ripetere la revisione visiva e i controlli. R09 è pronta soltanto per la stampa dei provini, non ancora stampata o provata fisicamente.
