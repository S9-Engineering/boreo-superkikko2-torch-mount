# BOREO — R12, nervature dalla fascia alle alette, provino PLA

**Pronto per la stampa del solo provino ELEGOO PLA Basic.** Questa revisione corregge il verso dei rinforzi della R11: le nervature stanno **sotto i bracci dal lato verso la torcia**, collegando la fascia curva alle alette. Il retro verso la testa torna libero, senza i talloni della R11. Fascia centrata28,8mm e pelle2mm conservate. Nessuna stampa inviata o avviata.

**[Progetto completo ElegooSlicer3MF](stampa/PLA_BASIC_ECC2/BOREO_R12_PONTE_CENTRATO_RINFORZATO_PLA_BASIC_ECC2_04.3mf)** · [G-code](stampa/PLA_BASIC_ECC2/BOREO_R12_PONTE_CENTRATO_RINFORZATO_PLA_BASIC_ECC2_04.gcode) · [Anteprima della correzione](anteprime/PROVINO_R12_anteprima.png).

Stima reale **50min4s /13,76g PLA**, supporti inclusi. Un unico pezzo. Il3MF sopra conserva profili/impostazioni/percorso dello slicer; quello con SOLO_GEOMETRIA nel nome contiene solo modello e disposizione. STL e STEP sono in stampa, millimetri, già orientati. La base esterna R10 non è ristampata né modificata.

## Forma corretta e vincolo delle feritoie

Due nervature longitudinali sotto i bracci:larghezza6mm,lunghezza nominale12mm dalla curva esterna verso la torcia,altezza di progetto fino1,2mm sotto le alette. Punta mantenuta0,4mm per non terminare con un bordo matematicamente nullo. Il profilo è rastremato, collegato alla fascia e fuso al braccio. Nessuna parte aggiunta attraversa la superficie interna di raggio90:il retro verso la testa resta liscio.

Lo spessore del braccio resta3,2mm ma **la zona con nervatura arriva fino a4,4mm complessivi di progetto**. Questo è un ingombro nuovo dentro il primo tratto del passaggio del casco. Il rilievo manuale indicava una luce minima5mm in una zona del foro:non conosciamo il profilo lungo tutto il canale,né la sua inclinazione,nè il gioco dell’esemplare stampato. Non dedurre quindi un inserimento garantito dai soli0,6mm nominali di differenza. Le nervature basse sono una prova per limitare l’aumento di sezione; efficacia portante non dimostrata.

Le alette rimangono larghe9,2mm,assiX±42,foriØ3,4 adY8,estremità adY14. Il tratto oltre il raggio105 è confrontato nel CAD con R10 e resta invariato. Fra i raggi92 e105 invece lo spessore cresce localmente per il rinforzo:la dichiarazione R11 di passante invariato oltre raggio92 **non si applica aR12**. Non modificare o forzare il casco per adattarlo al provino.

Fascia daZ8,2 a37,alette centrate aZ22,6:altezza28,8,pelle2mm,raggio esterno92. Crescita sotto rispetto aR10 ancora12,8mm,quindi controllare cuscinetto e regolazione interna. I rinforzi risultano sotto nella posa stampata,sopra capovolgendo lo stesso pezzo. Il CAD conferma assenza di interferenza con la base esterna R10 in entrambi i versi;il canale reale del casco resta da provare.

## Procedura di prova

A freddo,rimuovere i supporti generati dallo slicer sotto i bracci,lasciando le due nervature rastremate presenti nell’anteprima. Sono parti del modello,non residui dei supporti. Verificare che il fondo delle nervature e delle alette non abbia residui saldati che aumentino lo spessore.

Provare a casco fermo prima col rinforzo sotto e poi sopra. L’ingresso deve essere libero,senza piegare le alette o comprimere la schiuma. Se il nuovo rinforzo si arresta all’imbocco o più avanti,fermarsi e annotare il punto:questa misura decide la geometria successiva. Controllare i due margini della fascia28,8mm,cuscinetto e regolazione. Se disponibile,provare l’accoppiamento manuale con la base R10 e accessibilità dei fori. Non servono nuovi fori,colle o elastici.

Torcia spenta sostenuta a mano o sul tavolo. Questa prova verifica la forma e l’inserimento; non è una prova del peso della torcia,sicurezza protettiva,ritenuta,urti,calore,uso in grotta o immersione. Non è stato eseguito un calcolo o un test che dimostri che la nervatura1,2mm risolva il cedimento.

## Stampa verificata digitalmente

**ELEGOO Centauri Carbon2 Combo,ugello0,4mm,PEI testurizzato,ELEGOO PLA Basic.** Profili macchina e filamento identici R11/R09 PLA. ElegooSlicer1.5.3.5,CLI2.4.2. Strati0,20mm,5pareti,30%gyroid,5strati superiori e inferiori. Ugello220°C,piano60°C,limite volumetrico12mm³/s,velocità parete esterna50/interna80/infill100/primo25mm/s. Parametri di partenza del profilo,non nuove calibrazioni fisiche.

**Supporti normali snug dal piano necessari sotto i bracci** e il profilo delle nervature;due torri accessibili da rimuovere sul pezzo smontato. DistanzaZ0,40mm,XY0,55mm,2strati interfaccia/spaziatura0,5mm,velocità supporti45/interfaccia30mm/s. Distacco e finitura reali ancora da verificare. Brim,raft e torre disattivati. Piano pulito e verifica dell’adesione iniziale necessari.

Avviso PLA `bed_temperature_too_high_than_filament` conservato: **sportello aperto e/o vetro superiore rimosso**. Nessun valore alterato per nascondere l’avviso. [Riscontro](verifiche/avviso_PLA_camera.json).

## Controlli e limiti

62 controlli geometrici superati sui file esportati riaperti:CAD valido/un solido,mesh chiusa/manifold,normali/volume,degeneri/duplicati/frammenti,screening di autointersezioni,scale/unità/pose STEP-STL-GLB-3MF,fascia centrata,pelle2mm,raggio92,rinforzi esterni e retro libero,ingombri campionati entro4,4mm,tratto oltre raggio105 invariato e accoppiamento base R10 nei due versi. [Report](verifiche/geometria.json). Screening delle autointersezioni non matematicamente completo.

Slicing reale144strati tutti renderizzati e rivisti:primo strato,pareti,profilo dei rinforzi,fori e supporti presenti;zero isole candidate. Progetto nativo riaperto nel controllo del pacchetto,G-code esterno uguale a quello incorporato. [Slicing](verifiche/slicing/report.json). Non è una verifica di finitura,inserimento o resistenza fisica. Stato completo in verifiche/STATO_CONSEGNA.json,controllo finale in verifiche/pacchetto.json. R12 non è ancora stampata o provata nel casco.

## Rigenerazione

Python3.11,CadQuery2.8,trimesh5.1.1,dipendenze in sorgenti/requisiti.txt;parametri e script inclusi. Da questa cartella:

```sh
python sorgenti/genera.py
python sorgenti/verifica.py
python sorgenti/crea_anteprime.py
python sorgenti/prepara_slicing_pla.py
python sorgenti/verifica_pacchetto.py
```

Dopo ogni modifica rigenerare tutti gli esportati e ripetere controlli,slicing e revisione visiva. Le revisioni precedenti restano come storico.
