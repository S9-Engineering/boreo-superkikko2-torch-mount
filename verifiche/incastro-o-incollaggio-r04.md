# R04 — aggancio nelle feritoie o base incollata?

Valutazione del 15 ottobre 2026. Requisiti utente: 5 °C, umidità relativa 100%, anche immersione; preferenza per aggancio meccanico, senza elastici, colle o bicomponenti. Nessun nuovo foro nel casco. Si mantengono farfalla e U metallica originali.

**Scelta di sviluppo: aggancio meccanico positivo nelle feritoie, subordinato a geometria e appoggi reali. L'incollaggio della base non è oggi dimostrato sufficiente e non viene selezionato.** Non è stata eseguita alcuna prova di tenuta, immersione o compatibilità del casco.

## Vincolo specifico del BOREO

Il [manuale ufficiale BOREO A0074700C, §5](https://www.petzl.com/on/demandware.static/-/Sites-petzl-master-catalog/default/dw79a6bf57/media/product/technical-notice-BOREO-2_068Tx000001zLa1IAE.pdf) limita pitture, solventi e adesivi, con eccezioni per adesivi a base acquosa e autocollanti Petzl, e sconsiglia fissaggi fuori dalle raccomandazioni del fabbricante. La [FAQ ufficiale BOREO](https://www.petzl.com/ie/en/sport/products/mens-climbing-mountaineering-helmets/boreo/BOREO_SPO_a2m68000000PBAgAAO.html) tratta gli adesivi delle etichette: non è un'approvazione di un giunto strutturale artigianale per sostenere la Superkikko2.

Un adesivo dichiarato compatibile con ABS generico o resistente all'acqua non è per questo compatibile con calotta, finitura ed eventuale contatto accidentale con EPP/EPS dell'esemplare. Viceversa, la dicitura “a base acquosa” non dimostra da sola né idoneità strutturale né scarsa resistenza all'acqua dopo essiccazione: servono dati del prodotto e dell'applicazione specifica. Non sono raccomandati primer, carteggiatura o solventi sulla calotta per preparare un incollaggio.

Petzl commercializza un [HELMET ADAPT adesivo](https://www.petzl.com/us/en/tactical/products/accessories-for-headlamps/helmet-adapt/HELMET-ADAPT-PRO_MIL_a2mTx000000mlizIAA.html) per determinate lampade. Questo mostra che un montaggio adesivo può essere progettato per un impiego definito; non qualifica una base FDM artigianale, un adesivo diverso, la Superkikko2 o l'immersione richiesta.

## Confronto fisico

| Aspetto | Meccanismo nelle feritoie | Base incollata |
| --- | --- | --- |
| Ritenuta | Battute/fermi e chiusura esterna possono fornire un vincolo positivo, senza dipendere da un sottile gancio elastico. | Dipende da due interfacce adesive, strato adesivo e materiale superficiale di casco/base. |
| 5 °C e umidità 100% | Restano da verificare materiale, tolleranze, deformazioni, montaggio e tenuta bagnata. L'acqua non rimuove di per sé una battuta correttamente trattenuta. | Distinguere temperatura/umidità di posa e maturazione da quelle d'esercizio. Umidità elevata e superfici condensate rendono una posa generica non qualificata. |
| Immersione | Valutare ritenuta, corrosione, svitamento, sabbia/fango, drenaggio e carichi in acqua. | “Resistente all'acqua” non specifica da solo immersione, durata, profondità, bordi esposti e carico applicato durante l'immersione. |
| Leva della torcia | Va contrastata con appoggi e distanze reali; non scaricare tutto sul bordo sottile di una feritoia. | La leva tende a sollevare un bordo del giunto. L'area nominale incollata e la sola resistenza a taglio non dimostrano la tenuta al distacco progressivo. |
| Calore | La farfalla può scaldare base, fermi e viteria; materiale e serraggio restano da verificare. | Si aggiunge il comportamento a caldo e nel tempo dell'adesivo. Il freddo dell'acqua non prova che il precedente funzionamento in aria calda sia innocuo. |
| Ispezione/manutenzione | Smontaggio e controllo di fermi, appoggi e viti più accessibili, se progettati correttamente. | Parte dell'interfaccia è nascosta; la rimozione potrebbe richiedere interventi non adatti alla calotta. |

Le valutazioni della tabella sono ragionamento progettuale, non risultati sperimentali. Non si assume che tutti gli adesivi falliscano al freddo o in immersione: esistono prodotti per condizioni specifiche, ma non è stata individuata e qualificata una combinazione per questo casco/base/torcia.

## Riscontro su documentazione di adesivi industriali

La [TDS 3M VHB 5907, revisione febbraio 2026](https://multimedia.3m.com/mws/media/2366682O/3m-vhb-tape-5907.pdf), esempio della famiglia 5952, richiede superfici asciutte senza condensa e indica minimo di posa 10 °C. Dopo corretta applicazione il comportamento a freddo è una questione distinta. I dati ambientali riguardano provini e modalità specifici; non certificano il nostro giunto. Questi numeri non prescrivono né posa né trattamento sul casco.

Il [bollettino 3M sulla durata](https://multimedia.3m.com/mws/media/1042522O/3m-vhb-tape-durability-technical-bulletin.pdf), pagina 3, documenta 4945 su alluminio/alluminio dopo oltre dieci anni in acqua e riporta anche possibile diminuzione del picco di forza intorno al 40% dopo esposizione prolungata al bagnato. Non trasferire il risultato ad ABS del BOREO/PETG FDM, ad altro nastro o a carico immerso a 5 °C. Resistenza all'acqua tecnicamente possibile e qualificazione del nostro attacco sono due conclusioni diverse.

Non sono stati acquistati o selezionati nastri 3M. La documentazione serve a valutare il piano B, non ad approvare un adesivo sulla calotta.

## Meccanismo da sviluppare

1. Sella esterna sagomata con battute per la farfalla e appoggi sul casco da individuare. La geometria deve contrastare sia la rotazione laterale sia il beccheggio.
2. Due fermi indipendenti attraversano le aperture esistenti e vengono trattenuti con fissaggi accessibili dall'esterno. La ritenuta resta meccanica; non dipende soltanto dall'attrito, dall'elasticità dello stampato o da adesivi frenafiletti.
3. Dentro rimangono superfici sottili, larghe, lisce e arrotondate. Per il fermo si confrontano FDM e lamiera in base a spessore disponibile e contatti reali; una lamiera non è automaticamente compatibile con il casco.
4. Gli elementi di chiusura devono avere battute definite: stringere la vite non deve comprimere progressivamente la schiuma. Devono restare liberi girotesta, cinghie, imbottiture e dissipatore.

Due fermi distanziati a sinistra/destra non bastano da soli a bloccare ogni rotazione. Il momento del peso avanzato vale `M=F·e`: occorrono anche reazioni distanziate in altezza/profondità. Indicativamente, una coppia di reazioni distanti `h` richiede una forza `C=M/h`. Si tratta di equilibrio, non di una pressione ammissibile dei bordi del casco.

## Quando fermare il concetto delle feritoie

- Nessuna superficie resistente raggiungibile per i pattini senza caricare o comprimere la schiuma.
- Necessità di allargare/tagliare feritoie, forzare la calotta o interferire con il corretto posizionamento sulla testa.
- Carico concentrato sul bordo di un'apertura o nessuna battuta utile per contrastare la leva, senza possibilità di verificare il comportamento del casco.

Un fermo stampato troppo debole può richiedere diversa sezione, percorso più corto o un componente metallico: non dimostra che l'intero principio meccanico sia debole. Se invece manca un appoggio compatibile sul casco, irrobustire il fermo non risolve quel limite.

## Piano B adesivo: condizioni ancora aperte

Prima di considerarlo sufficiente servirebbero una combinazione specifica compatibile con le indicazioni Petzl, superficie e curvatura effettive della base, preparazione ammessa sulla calotta, condizioni di posa e completa maturazione, dati di tenuta al distacco e al creep, prove su umido/freddo/immersione e alla temperatura di contatto della farfalla. Il peso reale del gruppo, leva e carichi di servizio restano da rilevare.

Durata/profondità dell'immersione, tipo di acqua e temperatura massima della base sono ancora ignoti. Non è selezionata alcuna colla, resina o nastro e non è autorizzata la sua applicazione al casco.

**Decisione attuale:** prima dimostrare montabilità e appoggi dell'aggancio meccanico; mantenere l'incollaggio come alternativa condizionata, senza attribuirgli resistenza per esclusione.
