# BOREO / Superkikko2 — R13 completa, ELEGOO PETG Pro

**Pronto per la stampa del prototipo completo in PETG Pro.** Un solo piatto contiene il ponte interno R12 centrato e rinforzato e la base esterna R10 arrotondata, con logo S9 estruso 2 mm e tre predisposizioni per la farfalla originale. Una copia di ciascun pezzo. Geometrie conservate e ricontrollate nell'assieme. Nessuna stampa inviata o avviata.

**[Apri il progetto completo ElegooSlicer](stampa/PETG_PRO_ECC2/BOREO_R13_COMPLETO_PETG_PRO_ECC2_04.3mf)** · [G-code PETG](stampa/PETG_PRO_ECC2/BOREO_R13_COMPLETO_PETG_PRO_ECC2_04.gcode) · [Anteprima](anteprime/BOREO_R13_COMPLETO_PETG.png).

Stima reale dello slicer: **2 h 55 min 19 s e 44,23 g**, supporti inclusi, un solo filamento, senza torre di spurgo. Massa stimata con densità 1,27 g/cm³, non pesata. Il 3MF indicato sopra è un progetto nativo con profili, impostazioni e percorso incorporato. [R13_COMPLETO_SOLO_GEOMETRIA.3mf](stampa/R13_COMPLETO_SOLO_GEOMETRIA.3mf) contiene solo modelli e disposizione, senza impostazioni di stampa.

## Parti e quote

| Pezzo | Quantità | Dimensioni massime STL in posa di stampa | File separati |
| --- | --- | --- | --- |
| Ponte interno centrato, geometria R12 | 1 | 104,98 × 50,05 × 28,80 mm | [STL](stampa/R13_PONTE_CENTRATO_PETG.stl) · [STEP](stampa/R13_PONTE_CENTRATO_PETG.step) |
| Base esterna arrotondata, geometria R10 | 1 | 102,80 × 25,61 × 46,00 mm | [STL](stampa/R13_BASE_APPOGGI_PETG.stl) · [STEP](stampa/R13_BASE_APPOGGI_PETG.step) |

Il ponte ha fascia curva alta **28,8 mm**, pelle radiale **2 mm**, raggio esterno 92 mm e alette centrate. Le alette sono larghe 9,2 mm e alte 3,2 mm, con fori Ø3,4 mm ad assi X ±42 / Y8. Le due nervature stanno dal lato delle alette, verso la torcia: larghe 6 mm, lunghezza nominale esterna 12 mm, alte fino a 1,2 mm sotto i bracci; punta 0,4 mm. **Ingombro verticale locale fino a 4,4 mm**, da provare nelle feritoie. Il retro verso la testa è liscio, senza i talloni R11. La fascia si estende da Z8,2 a Z37: il vecchio limite inferiore R06 è superato dalla successiva scelta dell'utente di centrare le alette.

La base conserva pannello di appoggio 67,5 × 46 × 5 mm, angoli R5 e cornice R6, due scarichi rivetti e tre passaggi di fissaggio. **Logo S9 sul fianco esterno, rilievo 2 mm**, stesso filamento della base. Non è richiesto un secondo colore; arancione e blu nell'anteprima distinguono soltanto i pezzi. La parte grigia rappresenta la ferramenta e non si stampa.

## Stampa

Configurazione: **ELEGOO Centauri Carbon 2 Combo, ugello 0,4 mm, PEI testurizzato, ELEGOO PETG Pro**. Il nome interno del profilo è `Elegoo Centauri Carbon 2 0.4 nozzle`. ElegooSlicer 1.5.3.5, motore CLI 2.4.2. Il profilo macchina e le macro sono conservati dal progetto PETG R10; non provengono dal profilo della prima Centauri Carbon.

- Strato e primo strato **0,20 mm**; **5 pareti**, **30% gyroid**, 5 strati superiori e inferiori.
- Ugello **240 °C**, piano **65 °C**, portata massima **5 mm³/s**. Parete esterna 40 / interna 60 / riempimento 70 / primo strato 25 mm/s; ponti 25 mm/s.
- Ventola normale 10–40%, primi 3 strati spenta, sbalzi 90% dal profilo precedente. Flusso filamento 0,98 e anticipo pressione 0,1 sono valori del profilo, non calibrazioni eseguite sulla bobina dell'utente.
- Supporti normali **snug dal solo piano**, sotto i due bracci del ponte e i ripiani della base. Distanza Z superiore/inferiore **0,40 mm**, distanza laterale **0,55 mm**, 2 strati di interfaccia, spaziatura 0,5 mm, velocità supporti 45 / interfaccia 30 mm/s.
- **Brim, raft, skirt e torre di spurgo disattivati**. Due pezzi separati, stampa per strato. Non sostituire questi file con i vecchi G-code PLA.

Temperature entro gli intervalli della [scheda ufficiale ELEGOO PETG Pro](https://www.elegoo.com/products/petg-pro-filament-1-75mm-colored-1kg), consultata il 23 ottobre 2026: ugello 230–260 °C, raccomandato 240 °C; piano 65–75 °C. La densità è aggiornata a 1,27 g/cm³. Gli altri valori restano punti di partenza del profilo locale, non valori universali o calibrati.

Caricare PETG Pro nel canale scelto, controllare il materiale selezionato nello slicer e usare filamento asciutto. Per eventuale essiccazione seguire le indicazioni della bobina/produttore. Piano pulito e controllo dell'adesione iniziale. Lasciare raffreddare prima del distacco dal piano e dei supporti. Le maggiori distanze di separazione possono facilitare la rimozione ma lasciare una superficie inferiore meno regolare: il risultato fisico non è ancora verificato. Rimuovere i supporti sui pezzi separati; **le nervature rastremate sotto i bracci fanno parte del ponte e vanno conservate**.

## Montaggio e ferramenta

Il collegamento fra ponte e base conserva **2 viti M3 × 16, 2 rondelle 3,2 × 7 × 0,5 mm e 2 dadi autobloccanti M3 DIN 985, chiave 5,5 mm / altezza 4 mm**. I dadi entrano dal basso nelle tasche chiave 5,85 mm, profonde 4,3 mm. Gioco nominale della sede dell'aletta: **0,35 mm per lato**; foro Ø3,4 per vite nominale Ø3, gioco diametrale 0,4 mm. Tasca dado: 0,35 mm di differenza complessiva fra facce, circa 0,175 mm per lato. Sono giochi di progetto, da controllare dopo la stampa PETG.

Provare prima il ponte nel casco fermo, senza forzare, piegare le alette o comprimere la schiuma. Verificare entrambi i versi del ponte, il cuscinetto e la nuova estensione della fascia. Pulire eventuali residui di supporto che aumentano la sezione nelle feritoie. Inserire la base sui terminali e la ferramenta; il CAD verifica passaggi, traiettoria dei dadi e assenza di interferenze in entrambe le pose del ponte. Nessun foro, colla o elastico aggiunto al casco. Per la prova dimensionale fermarsi al contatto leggero, senza precaricare o schiacciare il casco; coppia funzionale non ancora definita.

**Il fissaggio della farfalla è distinto dal giunto M3:** le asole metalliche hanno luce 2 mm, quindi M3 non passa. La base ha tre predisposizioni passanti 3 × 1,9 mm: due a X ±28,75 / Z22,6 e una superiore X0 / Z41,5. Una vite M1,6 con rondella e dado resta una candidata da verificare sul metallo; non sono presenti filettature stampate e non è definita una vite autofilettante. Non usare i rivetti come punti di appoggio né allargare le asole metalliche per adattarle al modello.

L'interasse laterale 57,5 mm deriva dalla larghezza fotografica circa 63,5 mm e dalle luci/bordi di 2 mm confermati; non è una misura diretta dell'interasse. Posizione verticale dell'asola superiore, spessore della lamiera e sporgenza dei rivetti sono ancora da confermare. Queste quote sono modificabili in [parametri_base.json](sorgenti/parametri_base.json). L'appoggio della farfalla è continuo salvo scarichi rivetti e passaggi; **il PETG non è un dissipatore** e non abbiamo misurato la temperatura dei contatti. Il contatto completo non dimostra un migliore raffreddamento.

## Verifiche e stato

[Geometria](verifiche/geometria.json): **140 controlli superati** sui file esportati riaperti, due solidi stampabili separati, mesh chiuse/manifold, normali e volumi, facce degeneri/duplicate, frammenti e screening di autointersezioni. Scala e pose coerenti fra STEP/STL/GLB/3MF; nessuna riparazione mesh. Confronto CAD con i riferimenti: base identica R10, ponte identico R12. Verificati fascia 2 mm, centratura, rinforzi, passaggi, logo 2 mm, appoggio, scarichi, accesso ai dadi e assenza di interferenze. Lo screening delle autointersezioni non è una prova matematica completa.

[Slicing](verifiche/slicing/report.json): **230 strati**, tutti renderizzati e rivisti; primo strato, supporti, rinforzi, ponti, pareti e fori presenti. Zero isole candidate e nessun avviso. [Logo nei percorsi](verifiche/logo_percorsi.json): S e 9 presenti su 39 strati ciascuno. [Controllo finale](verifiche/pacchetto.json): **98 controlli superati**, profili, unità, trasformazioni e mesh del progetto nativo, quantità, riapertura in ElegooSlicer e identità del G-code esterno con quello incorporato.

**Stato: pronto per la stampa del prototipo completo; non stampato e verificato.** Non sono ancora convalidati l'inserimento della R12 nelle feritoie, la finitura dei supporti in PETG, il fissaggio reale della farfalla, la tenuta al peso/urti/tempo né il comportamento con lampada calda, umidità o immersione. Il riscontro positivo dell'utente sul precedente pezzo arancione non costituisce una prova fisica della R13. Fare la prima verifica a freddo con torcia spenta sostenuta sul tavolo. Stato strutturato in [STATO_CONSEGNA.json](verifiche/STATO_CONSEGNA.json).

## Sorgenti e riproduzione

Python 3.11, CadQuery 2.8, trimesh 5.1.1; dipendenze in [requisiti.txt](sorgenti/requisiti.txt). Il progetto include sorgenti geometrici e parametri separati per base e ponte, SVG originale, riferimenti STEP, sorgenti delle verifiche e profili dello slicer. Non richiede le cartelle delle revisioni precedenti per rigenerare.

```sh
python sorgenti/genera.py
python sorgenti/verifica.py
python sorgenti/crea_anteprime.py
python sorgenti/prepara_slicing_petg.py
python sorgenti/verifica_logo_percorsi.py
# Aprire e rivedere le anteprime di tutti gli strati e annotare l'esito nel report.
python sorgenti/verifica_pacchetto.py
```

Dopo ogni modifica rigenerare gli esportati, rifare slicing e revisione visiva e aggiornare lo stato. L'eventuale rigenerazione del G-code avviene esclusivamente tramite ElegooSlicer.
