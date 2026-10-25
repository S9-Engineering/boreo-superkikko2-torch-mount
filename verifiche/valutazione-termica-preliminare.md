# Superkikko2: calore e dimensionamento della staffa

Valutazione del 15 ottobre 2026. **Il calore e il serraggio entrano nel dimensionamento insieme al peso. La R03 rimane una bozza di forma. Nessuna geometria modificata o stampa avviata.**

## Dati disponibili e dati mancanti

Kikko dichiara **130 g per il corpo lampada**, con corpo e dissipatore in alluminio e U originale in acciaio inox. Nella [scheda ufficiale Superkikko2](https://www.kikkolamp.com/superkikko2) non sono pubblicate temperatura massima del corpo o degli attacchi laterali, curva di riscaldamento o condizioni di un eventuale controllo termico. I 4000 K sono temperatura di colore della luce e non temperatura fisica della lampada. La massa dell'esemplare e la composizione esatta dei 130 g non sono state misurate.

Per il PETG Pro, la [pagina ELEGOO globale](https://www.elegoo.com/en-gb/products/petg-pro-filament-1-75mm-colored-1kg) riporta deformazione termica a 66 °C sotto 0,45 MPa; la [pagina ELEGOO EU](https://eu.elegoo.com/products/petg-pro-filament-1-75mm-colored-10kg) riporta HDT 73 °C sotto 0,45 MPa. Non e chiarita la differenza fra queste pubblicazioni e non e confermata la bobina dell'utente. Non trattare i numeri come un intervallo di servizio garantito.

L'HDT misura una deformazione prefissata durante una prova sotto carico con temperatura crescente: non e la temperatura di fusione ne una garanzia di tenuta per ore di un componente serrato. [Definizione e condizioni del test, UL](https://www.ul.com/services/heat-resistance-tests-plastics). La valutazione di esposizione prolungata al calore richiede dati distinti. [UL, prestazioni delle plastiche a temperatura elevata](https://www.ul.com/resources/critical-plastics-performance-elevated-temperatures).

## Meccanismo da controllare

Il corpo caldo puo trasferire calore per contatto alle orecchie e attraverso viti e rondelle; la superficie vicina al dissipatore puo essere scaldata anche dall'aria e dall'irraggiamento. E un percorso fisico possibile, non una temperatura calcolata o misurata della R03. Separare il contatto dal dissipatore aiuta a mantenerne libera la dissipazione, ma non elimina automaticamente il percorso attraverso le viti.

Lo stampato puo perdere rigidezza e deformarsi progressivamente senza fondere. Il peso sollecita i bracci; il serraggio esercita inoltre pressione permanente sui fori, con possibile ovalizzazione e perdita di precarico. La [guida FDM Stratasys](https://www.stratasys.com/contentassets/1a0cc7a8e7d14f29ac972189bfeade4c/dg_fdm_designconsiderationsfdmtooling_0718a.pdf?v=48fbe5), sezione 2.2.3, descrive il creep dei termoplastici sotto carico prolungato. Aumentare soltanto lo spessore non dimostra la compatibilita termica.

## Collegamento con il calcolo meccanico

Il [calcolo riproducibile](../sorgenti/calcola_carichi_preliminari.py) e il [risultato JSON](carichi-preliminari.json) distinguono massa nominale 130 g e massa di progetto **assunta** di 200 g.

| Caso | Forza totale | Momento con leva assunta 70 mm |
| --- | ---: | ---: |
| 130 g, statico | 1,275 N | 0,089 Nm |
| 200 g, statico | 1,961 N | 0,137 Nm |
| 200 g, scenario equivalente 5g | 9,807 N | 0,686 Nm |
| 200 g, scenario equivalente 10g | 19,613 N | 1,373 Nm |

5g e 10g sono scenari scelti per sensibilita, non accelerazioni misurate, norme applicabili o prova di resistenza agli urti. Non rappresentano un impiglio del cavo. La leva reale e la distanza fra appoggio effettivo e baricentro, non una dimensione dedotta dalle foto.

Una mensola esterna ipotetica **6 mm di spessore × 18 mm di altezza**, lunga 70 mm, con 70% del carico di 200 g a 5g su un solo braccio, modulo assunto 1 GPa e moltiplicatore ipotetico di tensione 2, produce nel confronto: circa **8,90 MPa** sull'asse debole e **2,42 mm** di freccia elastica lineare. Sono numeri di un comparatore di trave retta, non risultati del CAD completo; non dimostrano che quella sezione sia sufficiente per la R03. A 10g i valori raddoppiano. Un moltiplicatore 2 non limita automaticamente le concentrazioni reali.

La radice da 1,2 mm della R03 e particolarmente sensibile alla flessione laterale e alla torsione del braccio curvo. Un ponte interno sottile puo rimanere un obiettivo soltanto definendo un appoggio e un percorso di carico reali: ispessire le sole orecchie lascia la radice sottile nel percorso del carico.

Non e disponibile una curva `E(T)` o una resistenza ammissibile in funzione di temperatura e durata per il pezzo stampato. Anche il comparatore con E = 1 GPa non e un limite inferiore garantito a caldo. Non assegnare quindi oggi uno spessore funzionale definitivo.

## Misura discriminante e alternative

La misura utile e la **temperatura presso i fissaggi laterali e sul futuro contatto con il polimero**, insieme alla temperatura del dissipatore e dell'ambiente. Prima rilevazione sul gruppo originale, senza alterare il casco o sostituire la U con la bozza. Usare una sonda di contatto idonea, montaggio stabile, dissipatore libero e condizioni/tempi consentiti dal fabbricante. Registrare riscaldamento e massimo osservato, includendo l'eventuale riduzione automatica di potenza; una durata fissa non dimostra da sola il raggiungimento del regime. Nessuna prova e stata eseguita.

Un termometro IR su superfici metalliche puo risentire dell'emissivita e delle riflessioni; non ricavare la temperatura dalla sensazione al tatto. Non coprire le alette per provocare un surriscaldamento. Una prova in acqua non rappresenta la dissipazione in aria.

Se il contatto termico risultasse incompatibile col PETG specifico sotto carico, valutare un'interfaccia metallica presso i perni e un inserto stampato piu distante, oppure il mantenimento della U originale con nuovo adattatore. Sono alternative da valutare con l'utente: nessuna delle due modifica automaticamente la richiesta attuale di U diretta. Il metallo conduce a sua volta calore e il successivo collegamento con il polimero deve essere verificato; una singola rondella isolante non elimina il ponte termico della vite. Un eventuale polimero diverso richiederebbe scheda specifica, compatibilita di stampa e prove a caldo.

**Conclusione operativa:** completare la temperatura dei contatti e i dati della bobina prima di congelare materiale, spessori e fissaggio diretto. Peso e forma sono gia valutabili con ipotesi; la tenuta a caldo della soluzione interamente stampata resta aperta.
