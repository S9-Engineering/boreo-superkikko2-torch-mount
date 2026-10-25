# BOREO — R11, provino del ponte centrato con rinforzi

**Pronto per la stampa del solo provino in ELEGOO PLA Basic.** Un pezzo arancione nelle anteprime, mostrato in due versi. Base della torcia, logo e ferramenta non vanno ristampati in questa prova e non sono inclusi nel piatto. Nessuna stampa inviata o avviata.

[Progetto completo ElegooSlicer3MF](stampa/PLA_BASIC_ECC2/BOREO_R11_PONTE_CENTRATO_RINFORZATO_PLA_BASIC_ECC2_04.3mf) · [G-code](stampa/PLA_BASIC_ECC2/BOREO_R11_PONTE_CENTRATO_RINFORZATO_PLA_BASIC_ECC2_04.gcode) · [Anteprima con i due versi](anteprime/PROVINO_R11_anteprima.png).

Stima reale dello slicer **52min10s e13,94g PLA**, inclusi i supporti. Il3MF sopra è un vero progetto dello slicer con macchina/filamento/impostazioni/percorso incorporato. Il file R11_PONTE_SOLO_GEOMETRIA.3mf contiene invece soltanto geometria e disposizione. STL e STEP separati dello stesso unico pezzo sono nella cartella stampa, in millimetri e già orientati sul piano.

## Cambiamento richiesto

L’utente ha riferito che il pezzo arancione precedente funziona anche capovolto, anzi meglio. La revisione dell’esemplare fisico non è specificata. R11 usa come riferimento geometrico R10 e porta la fascia a **28,8mm di altezza**, simmetrica rispetto alla metà delle alette. Pelle curva2mm e raggio esterno92mm conservati.

La faccia superiore della fascia rimane aZ37; la metà delle alette è aZ22,6 e il nuovo bordo inferiore è aZ8,2:14,4mm di fascia per lato rispetto alla metà. Le alette, spesse3,2mm, lasciano **12,8mm di fascia libera sopra e sotto**. La parte inferiore cresce quindi di12,8mm rispetto aR10. La precedente indicazione di non scendere oltre la dima arancione era relativa a un’altra configurazione: questa nuova prova segue la richiesta esplicita di allungare anche l’altro verso, ma il cuscinetto e la testa devono essere ricontrollati.

A ciascuna radice sono aggiunti **un tallone e una nervatura triangolare**, entrambe su un solo verso verticale. In posa di riferimento le nervature sono sotto le alette; capovolgendo il medesimo pezzo risultano sopra. Larghezza nervatura6mm, profilo nominale alto8mm con raccordi0,5mm; altezza effettiva circa7,2mm dopo i raccordi. I talloni proseguono la radice per3,5mm radialmente verso la testa: il raggio locale interno scende da90 a86,5mm. Il resto della fascia conserva lo spessore2mm. Questa sporgenza interna va provata per comfort e interferenze.

Rinforzi e talloni sono mantenuti **dietro il raggio92**, sul lato interno della fascia. Non sono nervature che attraversano il casco. La parte passante conserva esattamente la geometria R10:larghezza9,2mm,spessore3,2mm,assiX±42,foriØ3,4mm adY8,estremità adY14. Evitiamo così di ingrossare la sezione che entrava già al limite nelle feritoie. Le nervature irrigidiscono geometricamente l’attacco alla fascia: **non dimostrano che l’intera aletta possa sostenere la torcia**. Materiale finale, portata, serraggio, urti, deformazione nel tempo e temperatura rimangono aperti.

## Prova nel casco

Dopo completo raffreddamento, rimuovere i due supporti di stampa dal tratto sotto le alette e gli eventuali piccoli contatti presso le radici. Sono strutture generate dallo slicer, distinte dalle nervature del modello: confrontare con l’anteprima prima di staccare materiale. Non eliminare le nervature triangolari fuse al ponte.

Provare il pezzo a casco fermo, prima con nervature sotto, poi con nervature sopra. Inserire senza piegare le alette o comprimere la schiuma. Verificare entrambi i nuovi margini della fascia, cuscinetto, regolazione interna e talloni/nervature verso la testa. Annotare quale verso funziona meglio e dove eventualmente tocca. Il riscontro sul vecchio pezzo capovolto non dimostra lo spazio per la nuova fascia28,8mm.

Se è disponibile la base esterna R10, verificare manualmente che i due terminali si inseriscano e che i fori rimangano accessibili. La compatibilità con quella base è verificata nel CAD in entrambi i versi, non sul casco reale. La ferramenta esterna rimane la precedente M3; per questo controllo non occorre serrare o affidare il peso della torcia al provino. Torcia spenta, sostenuta a mano o sul tavolo.

## Stampa

**ELEGOO Centauri Carbon2 Combo,ugello0,4mm,PEI testurizzato,ELEGOO PLA Basic.** Profili macchina e filamento conservati dalla R09 PLA. Slicer ElegooSlicer1.5.3.5,CLI2.4.2. Strati e primo strato0,20mm,5pareti,30%gyroid,5strati superiori/inferiori. Ugello220°C,piano60°C,portata massima12mm³/s;esterno50/interno80/infill100/primo25mm/s. Parametri del profilo, non nuove calibrazioni fisiche.

Pezzo verticale sulla base curva come esportato, nervature sotto le radici. **Supporti normali snug dal piano necessari sotto le alette**, ora a metà altezza: non disattivarli. Tutti i supporti sono accessibili sul pezzo prima del montaggio. Separazione verticale0,40mm,laterale0,55mm,2strati di interfaccia,spaziatura0,5mm,velocità interfaccia30/supporti45mm/s. Valori iniziali per ridurre l’adesione già segnalata; distacco e superficie inferiore reali ancora da verificare. Non attribuire il problema dei residui a un guasto della stampante senza nuove prove.

Brim,raft e torre di spurgo disattivati. Piano pulito e verifica dell’adesione del primo strato necessari, essendo la fascia sottile. Avviso PLA conservato `bed_temperature_too_high_than_filament`: **sportello aperto e/o vetro superiore rimosso**. Nessuna modifica al valore di transizione vetrosa per nascondere l’avviso. [Riscontro dell’avviso](verifiche/avviso_PLA_camera.json).

## Verifiche disponibili

59 controlli geometrici superati sui file finali riaperti:CAD valido e un solo solido,mesh chiusa/manifold,normali/volumi,degeneri/duplicati/frammenti,screening autointersezioni non adiacenti,scale e pose STEP/STL/GLB/3MF,fascia centrata e simmetrica,pelle2mm,raggio92,rinforzi su un solo verso,fori e sezioni passanti invariati oltre raggio92. Compatibilità CAD con base R10 verificata sia normale sia capovolta. [Report geometrico](verifiche/geometria.json). Lo screening non è prova matematica completa delle autointersezioni.

Slicing reale di144strati:primo strato,perimetri,nervature,talloni,fori e passaggi/supporti renderizzati e rivisti;zero isole di parete candidate. Il3MF nativo è riaperto nel controllo finale e ilG-code esterno coincide con quello incorporato. [Report dello slicing](verifiche/slicing/report.json). Tempi e consumo sono stime, non risultati di una stampa fisica.

R11 non è ancora stampata o provata nel casco. Questi controlli non convalidano resistenza,ritenuta,calore,uso in grotta/immersione o prestazioni protettive del casco. Stato completo in verifiche/STATO_CONSEGNA.json e verifica del pacchetto in verifiche/pacchetto.json.

## Riproduzione

Python3.11,CadQuery2.8,trimesh5.1.1 e dipendenze in sorgenti/requisiti.txt. Parametri,script e riferimenti STEP R10 inclusi. Da questa cartella:

```sh
python sorgenti/genera.py
python sorgenti/verifica.py
python sorgenti/crea_anteprime.py
python sorgenti/prepara_slicing_pla.py
python sorgenti/verifica_pacchetto.py
```

Dopo una modifica rigenerare tutti i derivati e ripetere controlli e revisione visiva. Nessun file delle precedenti revisioni è sostituito da questo provino.
