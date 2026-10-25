# BOREO / Superkikko2 — provini R08 per chiudere le quote

**Pronto per la stampa dei soli provini PLA**. Due piatti separati in ELEGOO PLA Basic: prima la piccola dima delle asole, poi base a due appoggi e ponte interno. Sono prove geometriche da tenere a mano: non montare la torcia affidandone il peso al PLA e non accenderla durante queste prove.

[Anteprima dei tre pezzi](anteprime/PROVA_R08_PLA_anteprima.png) · [Dima delle asole](anteprime/DIMA_INTERASSE.png)

## Cosa stampare

| Piatto | Pezzi | Stima reale ElegooSlicer | Scopo |
| --- | --- | --- | --- |
| **A — Dima** | Una U con due piolini | **5 min 2 s · 1,33 g** | Verificare insieme posizione e passaggio delle asole della farfalla |
| **B — Base e ponte** | Base con due appoggi piani, ponte interno R07 | **1 h 15 min 30 s · 20,20 g** | Provare feritoie, bordo inferiore, appoggi della farfalla, spazio per rivetti e accesso al giunto |

File pronti, per la sola configurazione indicata sotto:

- [G-code A — dima](stampa/PLA_BASIC_ECC2/A_DIMA/BOREO_R08_A_DIMA_PLA_BASIC_ECC2_04.gcode) · [Progetto slicer A](stampa/PLA_BASIC_ECC2/A_DIMA/BOREO_R08_A_DIMA_PLA_BASIC_ECC2_04.3mf).
- [G-code B — base e ponte](stampa/PLA_BASIC_ECC2/B_BASE_PONTE/BOREO_R08_B_BASE_PONTE_PLA_BASIC_ECC2_04.gcode) · [Progetto slicer B](stampa/PLA_BASIC_ECC2/B_BASE_PONTE/BOREO_R08_B_BASE_PONTE_PLA_BASIC_ECC2_04.3mf).

Entrambi i 3MF sono **veri progetti ElegooSlicer**, con impostazioni, materiale e percorso incorporato. Gli altri tre 3MF nella cartella `stampa/`, con `SOLO_GEOMETRIA` nel nome, contengono soltanto geometria e disposizione. Gli STL/STEP sono separati per pezzo, una copia ciascuno, in millimetri e già orientati sul piano. Il ponte è geometricamente identico alla R07: se già stampato e integro è riutilizzabile; il G-code B comprende comunque una copia del ponte.

## Prima prova: dima A

Dima verde da **63,5 × 20 × 2,8 mm**, con pelle 1,6 mm e due piolini **Ø 1,6 mm**, alti 1,2 mm, interasse **57,5 mm**. Nascono in verticale dal piano, senza supporti; non vanno montati sulla base o usati come viti. Piolini corti per limitare l'inserimento nel gruppo della lampada.

A lampada spenta e appoggiata sul tavolo, avvicinare la dima alla faccia metallica rivolta al casco, piolini verso le due asole laterali. Tenere la traversa della U sopra i piolini, nella zona libera dai rivetti. Verificare che **entrino contemporaneamente e che la dima resti piana**, senza allargare le gambe, piegarla o spingere. Se un piolino arriva contro il corpo lampada, fermarsi: questo contatto non va confuso con un errore di interasse.

La luce delle asole è **2 mm dichiarati dall'utente**. Il gioco nominale del piolino è **0,4 mm diametrale, 0,2 mm radiale**. Quindi un ingresso libero conferma un allineamento compatibile con questo gioco, non una misura al centesimo né la compatibilità di una vite commerciale. Non sono state misurate la dimensione reale dei piolini stampati o la calibrazione della macchina.

**Da riportare:** entrano entrambi insieme sì/no; ciascuno entra singolarmente sì/no; la dima resta piana sì/no. Se non entrano insieme, una foto frontale appoggiata al metallo aiuta a capire direzione ed entità dello scostamento. Una fotografia di profilo mostra eventuali contatti con rivetti o corpo lampada.

## Seconda prova: base e ponte B

La base blu mantiene curva e ingombro esterno nominali della R07, circa **102,8 × 25,6 × 46 mm**, ma è aperta al centro e in alto. Due colonne frontali da **8 × 34 mm**, con facce sullo stesso piano Y = 8 mm, appoggiano localmente sotto le alette metalliche. Interasse nominale57,5mm; asole orizzontali di prova lunghe3mm e alte1,9mm, per un futuro fissaggio più piccolo delle M3. Regolazione nominale del centro di una vite1,6mm rispetto al centro geometrico: fino a0,7mm lungoX e0,15mm lungoZ (massimi considerati separatamente); non è una tolleranza di stampa verificata. La lunghezza3mm comprende i terminali semicircolari.

Al centro rimane libero nel CAD un volume di **48 mm di larghezza × 29,9 mm di altezza**, fra Z4,1 e34 e fra Y−10 e20: non si impone una profondità di appoggio dei rivetti ancora ignota. Confermare sul metallo che nessun rivetto o componente della lampada faccia contatto prima dei due appoggi. La base non comprende una sede aderente a tutta la sagoma della farfalla.

Il ponte arancio conserva **pelle radiale1,2mm, altezza16mm, bordo inferiore a Z21mm come la R06**, crescita solo verso l'alto. Terminali **9,2 × 3,2 mm**, passo84mm assunto per le feritoie del casco. Sono quote geometriche della R07 conservate e verificate per confronto CAD, non nuove misure del casco.

Sequenza, a casco fermo e non indossato:

1. Dopo raffreddamento, rimuovere i supporti dal fondo dei ripiani esterni e dalle tasche dado. Il ponte non richiede supporti. Pulire soltanto residui di stampa, senza modificare casco o metallo.
2. Provare il ponte da solo: terminali liberi nelle feritoie, senza piegarli; confronto con il bordo inferiore della vecchia dima arancione; nessun nuovo contatto col cuscinetto per effetto dello sviluppo verso l'alto. Se serve forza, interrompere e annotare dove tocca.
3. Infilare la base sui terminali. Senza ferramenta si può tenere a mano. Per verificare il giunto si riutilizza la soluzione R07: **2 viti M3 × 16, 2 rondelle 3,2 × 7 × 0,5, 2 dadi autobloccanti M3 chiave5,5 e altezza4mm**, tutti all'esterno. Tasca dado5,85mm fra facce, profondità4,3. Inserire i dadi da sotto e avvitare dall'alto soltanto fino al contatto leggero, senza piegare gli stampati o comprimere la schiuma. L'accesso e il dado richiedono prova con la ferramenta reale.
4. Sostenendo sempre la lampada con la mano o col tavolo, avvicinare la sua farfalla alle due colonne piane. Verificare che **i due appoggi tocchino insieme**, le asole metalliche cadano sopra i passaggi stampati e il centro rimanga libero dai rivetti. Si può spostare verticalmente il metallo entro la sua asola, senza usare il peso della lampada come carico di prova.
5. Annotare quanto occorre alzare o abbassare il metallo rispetto ai fori stampati e quali parti toccano. Inviare una vista frontale e una di profilo con i pezzi tenuti a mano. Se disponibile, misurare con il calibro **lo spessore della lamiera fra le due facce**: i2mm del bordo laterale sono una quota distinta.

Non servono ora viti M1,6 per questa prova. Le **M3 del giunto ponte/base non passano nelle asole metalliche da2mm**. Il fissaggio funzionale farfalla/base e la sua ferramenta restano da definire dopo queste prove. Il foro stampato alto1,9mm è solo un provino di posizione/regolazione: non implica che il futuro giunto sia già convalidato.

## Configurazione di stampa

**ELEGOO Centauri Carbon 2 Combo — ugello0,4mm — PEI testurizzato — ELEGOO PLA Basic**, come le prove precedenti. Slicer **ElegooSlicer1.5.3.5**, CLI interna ElegooSlicer-2.4.2; profili macchina/filamento specifici ECC2 conservati dalla R07, macro invariate. Processo di prova: **strati0,20mm**, primo0,20; **3 pareti, 20% gyroid, 3 strati sopra/sotto**; 220°C ugello, 60°C piano; parete esterna50mm/s, interna80, infill100, primo25; limite12mm³/s. Impostazioni di partenza, non una nuova calibrazione fisica.

**Brim disattivato** in entrambi i piatti, nessun raft né torre di spurgo. A senza supporti; B con supporti normali aderenti, solo dal piano, rimovibili da sotto e dall'apertura della cornice. Piano pulito e controllo dell'adesione del primo strato restano necessari: l'assenza di brim riduce il margine contro il distacco dei pezzi sottili. I supporti locali non sono il bordo continuo della precedente R06.

**Avviso PLA conservato:** `bed_temperature_too_high_than_filament`. Stampare con sportello aperto e/o vetro superiore rimosso. Vedi [avviso originale](verifiche/avviso_PLA_camera.json). Nessuna modifica ai parametri di transizione vetrosa per nascondere l'avviso. Nessun profilo globale utente modificato.

## Verifiche e limite del risultato

115 controlli geometrici sui file riaperti, inclusi STEP/STL, corpi attesi, mesh chiuse/manifold, normali, volumi, degeneri/duplicati e screening delle autointersezioni non adiacenti. Il confronto CAD conferma ponte identico alla R07; campionati piolini/interasse, fori, appoggi, scarico e giunto esterno. [Report](verifiche/geometria.json). Lo screening non costituisce una prova matematica completa delle autointersezioni.

Slicing reale controllato: 14 strati per A, 230 per B, primo strato, piolini, passaggi e supporti presenti come previsto; zero isole di parete candidate nello screening raster finale. La cornice è stata allargata verso l’interno attorno ai passaggi M3 per eliminare due piccole partenze sospese individuate nella prima versione, poi tutti gli esportati interessati, le anteprime e lo slicing sono stati rigenerati e ricontrollati.. Report separati per [A](verifiche/slicing/A_DIMA/report.json) e [B](verifiche/slicing/B_BASE_PONTE/report.json). I due G-code sono generati esclusivamente dallo slicer e coincidono con i percorsi incorporati nei rispettivi 3MF. Geometria e trasformazioni dei tre 3MF geometrici sono verificate nel controllo finale del pacchetto. Slicing, tempi e consumi non sono prove di stampa fisica.

Se queste prove passano, possiamo chiudere la **geometria** della base e del fissaggio. Materiale funzionale, serraggio, ritenuta, carichi e temperatura restano da verificare prima dell'uso reale con la torcia. PLA destinato qui soltanto al controllo dimensionale, niente uso in grotta o immersione. R06 ha il riscontro di inserimento dell'utente; R08, ponte R07 e nuova dima non sono ancora fisicamente verificati in questo rilascio. Nessuna stampa avviata o inviata alla macchina.

## Rigenerazione

Python3.11 e dipendenze in [requisiti.txt](sorgenti/requisiti.txt). Parametri, provenienza del rilievo e STEP originale del ponte sono inclusi in `sorgenti/`. Dalla cartella R08:

```sh
python sorgenti/genera.py
python sorgenti/verifica.py
python sorgenti/crea_anteprime.py
python sorgenti/prepara_slicing_pla.py --piatto A_DIMA
python sorgenti/prepara_slicing_pla.py --piatto B_BASE_PONTE
python sorgenti/verifica_pacchetto.py
```

Una modifica geometrica richiede rigenerazione e ripetizione dei controlli e dello slicing interessati; aggiornare stime e documentazione dopo i nuovi report.
