# BOREO — R07, prototipo con giunto M3

**Pronto per la stampa del prototipo in PLA Basic. Non è ancora il supporto funzionale finale della torcia.** La base è grezza: sagoma e fissaggi della farfalla originale devono essere rilevati. R07 aggiunge un giunto smontabile a bulloni e recepisce la prova fisica riferita dall'utente sulla R06.

## Cosa cambia dopo la prova

- Ponte interno unico: stessa curvatura e stesso spessore radiale **1,2 mm** della R06, altezza aumentata da **4 a 16 mm solo verso l'alto**. Il bordo inferiore resta esattamente a Z = 21 mm nel riferimento dell'assieme R06: usare il vecchio pezzo arancione come riferimento sul casco. Altezza superiore di 16 mm proposta, ancora da provare rispetto a cinghie e imbottitura.
- Linguette: **9,2 × 3,2 mm** invece di 10 × 4 mm; riduzione di 0,8 mm in entrambe le dimensioni, non un gioco misurato. Fondo conservato a Z = 21; lati raccordati. Interasse **84 mm** e raggi del precedente scenario conservati, senza trasformarli in un rilievo reale.
- Linguette prolungate all'esterno e forate **Ø 3,4 mm** per il giunto; la porzione con vite non rimane dentro il casco.
- Base esterna curva piena, ingombro circa **102,80 × 25,61 × 46 mm**, con due appoggi esterni e sedi dadi. Il suo retro non sporge all'interno della curva di appoggio nominale. Rifilo radiale di 0,02 mm, esplicito nei parametri, risolve superfici coincidenti del CAD; parete curva nominale circa 3,98 mm.
- La base **non contiene fori o guide attribuiti alla farfalla**. Non montare la torcia su questa versione.

[Anteprima dell'assieme](anteprime/PROVA_R07_PLA_anteprima.png) · [Dettaglio del fissaggio](anteprime/viste/assemblato.png)

## Giunto scelto

Due linguette attraversano le feritoie esistenti e i passaggi nella base. All'esterno ognuna appoggia su un ripiano della base. Una vite verticale attraversa rondella, linguetta e ripiano e raggiunge un dado autobloccante in una sede esagonale aperta da sotto. La sede impedisce al dado di ruotare; il dado si può sostituire.

**Il serraggio chiude linguetta e ripiano fra loro, senza usare il casco o la schiuma come pacco da comprimere.** La ritenuta è data dalle due viti, non dall'attrito delle linguette incastrate nelle feritoie. Nel CAD sono verificate assenza di interferenze, traiettoria d'inserimento dei dadi da sotto e passaggi delle viti. Mancano le verifiche sul casco reale e con la torcia.

Ferramenta commerciale, **non da stampare**:

| Quantità | Componente | Dimensioni previste |
| --- | --- | --- |
| 2 | Vite a testa cilindrica con esagono incassato M3 × 16 | Passo 0,5 mm; lunghezza sotto testa 16 mm; testa Ø 5,5 × 3 mm |
| 2 | Rondella piana M3 | Foro Ø 3,2, esterno Ø 7, spessore 0,5 mm |
| 2 | Dado autobloccante basso M3, tipo DIN 985 | Chiave 5,5 mm, altezza massima 4 mm |

Preferenza di progetto: ferramenta inox A4, da confermare sui componenti acquistati. La [scheda dimensionale Accu del dado M3 A4](https://www.accu.co.uk/hexagon-nylon-locking-nuts/7957-HNN-M3-A4) riporta chiave 5,5 mm, spessore 4 mm e passo 0,5 mm. La tasca stampata è da **5,85 mm fra facce**, profondità **4,3 mm**: sovramisura di 0,35 mm totale fra facce, 0,175 mm per faccia opposta, non un gioco radiale. Il foro vite ha **0,4 mm di gioco diametrale nominale** rispetto a M3. Il passaggio delle linguette nella base ha **0,35 mm per lato**.

Questo giunto evita di affidare lo smontaggio ripetuto a una filettatura ricavata nella plastica. Ho scelto dadi sostituibili e rondelle al posto di autofilettanti o filetti stampati. Gli autobloccanti contrastano lo svitamento, ma **non eliminano il rilassamento della plastica sotto serraggio**, né dimostrano resistenza a caldo o agli urti. Non è definita una coppia di serraggio funzionale.

## File da usare

- [G-code del prototipo PLA](stampa/PLA_BASIC_ECC2/BOREO_R07_DIMA_PLA_BASIC_ECC2_04.gcode), generato esclusivamente dallo slicer.
- [Progetto ElegooSlicer completo](stampa/PLA_BASIC_ECC2/BOREO_R07_DIMA_PLA_BASIC_ECC2_04.3mf), con geometria, disposizione, impostazioni, filamento e percorso incorporato.
- [STL base grezza](stampa/R07_BASE_GREZZA_PROTOTIPO_PLA.stl) e [STL ponte](stampa/R07_PONTE_TERMINALE_PROTOTIPO_PLA.stl): una copia ciascuno, già orientati, unità millimetri.
- [3MF solo geometrico](stampa/R07_DUE_PEZZI_SOLO_GEOMETRIA.3mf), distinto dal progetto dello slicer; STEP per pezzo nella stessa cartella.

La ferramenta grigia negli assiemi è **schematica, priva di filetto, esclusa da STL e piatto di stampa**. Non ci sono torcia o casco ricostruiti.

## Piccolo provino consigliato prima del pezzo completo

Il [provino del giunto](provino-giunto/README.md) verifica dado e accoppiamento M3 in **15 min 13 s e 3,84 g** (stime dello slicer), separatamente dal casco. Include G-code e progetto 3MF verificati. È utile prima di ristampare tutta la base; non è una prova di resistenza.

## Bordo o alone sul piano

Nel progetto R06 il brim era intenzionale: **4 mm**, gap di distacco **0,1 mm**, per aumentare l'adesione delle dime sottili. Se il bordo osservato è una pellicola piatta attorno al pezzo, corrisponde probabilmente a questo aiuto di stampa, da rimuovere. R07 e provino hanno il brim disattivato nei soli progetti consegnati: i profili globali dell'utente non sono stati modificati. Restano i supporti locali indicati sotto.

Un bordo gonfio che fa parte del pezzo può invece essere un allargamento del primo strato (piede d'elefante). Per distinguerlo serve una foto ravvicinata del difetto. Non è stata diagnosticata né modificata la calibrazione della stampante. Riferimenti: [brim](https://help.prusa3d.com/article/skirt-and-brim_133969), [compensazione del primo strato](https://help.prusa3d.com/article/elephant-foot-compensation_114487).

## Stampa del prototipo

Configurazione: **ELEGOO Centauri Carbon 2 Combo, ugello 0,4 mm, PEI testurizzato, ELEGOO PLA Basic**. Profili macchina e filamento derivano dai profili specifici ECC2 già verificati nella R06; macro macchina conservate. Impostazioni proposte di processo, senza una nuova calibrazione fisica.

Slicer **ElegooSlicer 1.5.3.5**, CLI interna ElegooSlicer-2.4.2. **0,20 mm**, primo strato 0,20 mm; **4 pareti, 35% gyroid, 5 strati superiori e inferiori**. PLA 220 °C, piano 60 °C; parete esterna 50 mm/s, interna 80, infill 100, primo strato 25; limite volumetrico 12 mm³/s.

**Brim disattivato, nessun raft e nessuna torre di spurgo.** Supporti normali aderenti alla forma, solo dal piano, sotto i due ripiani esterni. Sono necessari in questo orientamento e raggiungibili da sotto; rimuoverli dopo raffreddamento, anche dalle aperture inferiori delle tasche dado. Non sono alette funzionali del modello. Il ponte non richiede supporti. Controllare adesione su PEI pulito: eliminare il brim riduce il margine contro il distacco, soprattutto per il ponte sottile.

Stime reali dello slicer, inclusi supporti: **1 h 46 min 45 s, 32,42 g**, 230 strati. Le stime non sono tempi o consumi misurati sulla macchina.

**Avviso PLA conservato:** `bed_temperature_too_high_than_filament`. Aprire lo sportello e/o rimuovere il vetro superiore durante la stampa PLA, come indicato dallo slicer. Non sono state modificate la transizione vetrosa del profilo o le macro per nascondere l'avviso. [Dettaglio dell'avviso](verifiche/avviso_PLA_camera.json).

## Montaggio di prova

1. Lasciare raffreddare e rimuovere i supporti esterni. Controllare i fori e le tasche: eliminare solo residui di stampa, senza allargarli a caso.
2. Prima del casco, provare i dadi nelle sedi e verificare a mano l'accoppiamento dei due pezzi. La vite deve avvitarsi nel dado metallico: il foro plastico è liscio, non va filettato o usato con un'autofilettante.
3. Sul casco non indossato, introdurre delicatamente il ponte come nella R06. Il bordo inferiore deve restare alla stessa quota del vecchio pezzo arancione. Se occorre piegare o forzare per inserirlo, fermarsi e annotare dove tocca: non allargare feritoie né comprimere le schiume.
4. Infilare la base sulle linguette dall'esterno. Verificare che appoggi senza spingere sul casco; gli appoggi esterni devono incontrare le linguette senza doverle piegare con il serraggio.
5. Inserire i dadi da sotto, con l'inserto di nylon rivolto verso l'uscita inferiore della vite, e tenerli in sede con un dito. Dall'alto introdurre rondella e vite. Avvitare a mano fino al contatto leggero, senza deformare gli stampati. Il dado offre resistenza quando la vite raggiunge il nylon: non confonderla con un impuntamento della filettatura.
6. Controllare visivamente l'uscita del filetto dal nylon; nel CAD M3 × 16 sporge circa 2 mm oltre il dado nominale. Verificare sulla ferramenta reale che non restino estremità taglienti accessibili o interferenze. Per smontare, svitare dall'alto e recuperare i dadi da sotto.

Questa prova verifica l'accoppiamento e l'accessibilità della ferramenta, **senza caricare la torcia, senza usarla in grotta e senza prove sul casco indossato**.

## Stato delle verifiche e passi aperti

78 controlli geometrici superati sugli esportati riaperti: scala e corpi, STL chiusi/manifold con normali coerenti e volume positivo, duplicati/degeneri, screening delle autointersezioni non adiacenti, STEP e pose di stampa, 3MF con unità/trasformazioni, GLB e interferenze. Lo screening non è una dimostrazione matematica completa delle autointersezioni. Riferimento al [report geometrico](verifiche/geometria.json).

Slicing reale completato: primo strato e tutti i 230 strati controllati, linguette/fori e sedi presenti, supporti solo esterni raggiungibili. Nessuna isola di parete candidata nello screening raster. L'avviso PLA resta esplicito. Il dettaglio include [supporti e tasche dadi](anteprime/slicing/dettagli_giunto.png); report in [verifiche/slicing/report.json](verifiche/slicing/report.json).

**Solo R06 ha il riscontro fisico dell'utente**, descritto in [prova-fisica-R06.json](sorgenti/rilievi/prova-fisica-R06.json). Non equivale a prova di resistenza o convalida del casco. R07 non ancora stampata o provata. Nessuna stampa avviata o inviata alla macchina.

Per il supporto funzionale restano: verifica passaggi/comfort R07, carichi e ritenuta del ponte sottile, sagoma/asole/spessore della farfalla, spazio utensili con U e torcia, massa/baricentro del gruppo sostenuto, temperatura effettiva presso la base e scelta del filamento specifico. PLA è qui solo materiale del prototipo. PETG Pro è un candidato da verificare rispetto a temperatura, serraggio e acqua: non è un materiale finale già convalidato.

## Riproduzione

Sorgenti in `sorgenti/`, parametri in [parametri.json](sorgenti/parametri.json), dipendenze in [requisiti.txt](sorgenti/requisiti.txt). Python 3.11; comandi dalla cartella R07:

```sh
python sorgenti/genera.py
python sorgenti/verifica.py
python sorgenti/crea_anteprime.py
python sorgenti/prepara_slicing_pla.py
python sorgenti/dettagli_giunto.py
python sorgenti/provino_giunto.py --slice
python sorgenti/verifica_pacchetto.py
```

La generazione non modifica R06 e non avvia la stampante. Ogni variazione geometrica richiede rigenerazione, verifica e nuovo slicing. Eventuali tempi/stato nella documentazione devono seguire i nuovi report.
