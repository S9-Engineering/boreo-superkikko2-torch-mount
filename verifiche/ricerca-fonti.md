# Fonti e limiti della ricerca

Consultazione: **15 ottobre 2026**. Ricerca di scheda attuale, manuale, disegni/CAD e accessori per illuminazione. I dati di catalogo non costituiscono un rilievo dell'esemplare dell'utente.

| Fonte | Riscontro utile | Limite |
| --- | --- | --- |
| [BOREO, scheda Petzl Italia](https://www.petzl.com/it/it/sport/prodotti/caschi-arrampicata-e-alpinismo-uomo/boreo/BOREO_SPO_a2m68000000PBAgAAO.html) | Famiglia A042VA; due taglie; girotesta, masse e materiali; fermalampada anteriori ed elastico posteriore | Nessuna quota interna o disegno quotato dei passaggi nelle risorse consultate |
| [BOREO, nota A0074700C del 15/02/2023](https://www.petzl.com/on/demandware.static/-/Sites-petzl-master-catalog/default/dw79a6bf57/media/product/technical-notice-BOREO-2_068Tx000001zLa1IAE.pdf) | Manuale collegato dalla scheda attuale; precauzioni sulle modifiche e sui fissaggi non raccomandati | Gli schemi d'uso non sono disegni CAD quotati; non misurarli come se fossero in scala |
| [FAQ Petzl sulla foratura](https://www.petzl.com/IT/it/Sport/FAQ/Posso-forare-il-casco-per-installare-un-lampada-frontale-o-un-supporto-specifico) | La deroga citata riguarda il supporto speleologico sul BOREO precedente al 2023 | Non estendere la deroga alla generazione attuale o a fissaggi artigianali |
| [Attacco per casco da speleologia E55940](https://www.petzl.com/IT/it/Sport/Lampade-frontali/Attacco-per-casco-da-speleologia) | Compatibilità espressa con BOREO prima del 2023 | Non è il riferimento per la geometria interna del casco attuale |
| [DUO HELMET ADAPT E103BB00](https://www.petzl.com/us/en/sport/products/accessories-for-headlamps/duo-helmet-adapt/DUO-HELMET-ADAPT_SPO_a2m68000000XZeqAAG.html) | Piastre rimovibili esterne per DUO RL/S; collegamenti ufficiali a STL frontale/posteriore | Accessorio diverso dall'inserto richiesto; compatibilità con altre torce non dimostrata |
| [DUO HELMET ADAPT, nota E0154800A02 del 16/05/2024](https://www.petzl.com/on/demandware.static/-/Sites-petzl-master-catalog/default/dw451f77fa/media/product/technical-notice_DUO%20HELMET%20ADAPT-1_068Tx000003whJ1IAI.pdf) | La sezione per riproduzione indica SLS PA12 per il frontale, SLS per il posteriore ed elastico tondo da 3 mm | Non è un profilo FDM né una convalida di PLA/PETG/TPU sulla Centauri Carbon 2 Combo |

## CAD e STL

Non è stato identificato un modello pubblico del **casco BOREO attuale con interno verificabile dimensionalmente**. L'assenza di risultati nella ricerca non prova che tale modello non esista. Eventuali mesh per visualizzazione non possono sostituire quote o rilievo senza una verifica indipendente.

I due collegamenti STL dell'accessorio DUO HELMET ADAPT sono pubblicati sulla [pagina italiana Petzl](https://www.petzl.com/IT/it/Sport/Lampade-frontali/DUO-HELMET-ADAPT). L'accesso iniziale ha restituito 404 per gli URL versionati della nuova pagina; i collegamenti ufficiali legacy seguenti hanno invece restituito HTTP 200 a richieste HEAD con reindirizzamento verso media.petzl.com:

- [Frontale E0137800](https://www.petzl.com/sfc/servlet.shepherd/version/download/068Tx000000rai5IAA), dimensione dichiarata dal server: 8.098.184 byte.
- [Posteriore E0137900](https://www.petzl.com/sfc/servlet.shepherd/version/download/068Tx000000ralJIAQ), dimensione dichiarata dal server: 6.909.984 byte.

I file non sono stati scaricati o analizzati geometricamente. Nessuno rappresenta la calotta o le schiume del BOREO. La pubblicazione con indicazioni di riproduzione non è stata trattata come una licenza generale per modificare o redistribuire il disegno.

È stato individuato anche un [modello commerciale 3DModels.org h3dA309108](https://3dmodels.org/sv/3d-models/petzl-boreo-climbing-helmet/): la scheda descrive una mesh poligonale ricavata dalle proporzioni di un oggetto generico. Non fornisce prova di corrispondenza alla generazione attuale né quote interne per accoppiamenti; non è stato acquistato o usato.

## Dati ancora non verificati

Taglia, riferimento e anno dell'esemplare; forma e quote locali; attacco e massa della torcia; passaggio delle alette; spazio effettivo per l'inserto; risposta del fabbricante sulla soluzione richiesta. Nessuna geometria, mesh, resistenza, tolleranza o stampa è stata verificata in questa fase.

## Ricerca integrativa richiesta dall'utente: modello del casco

È stata ripetuta la ricerca mirata di CAD, STL, STEP e scansioni del BOREO, includendo cataloghi commerciali e repository di stampa. Non è stato trovato un modello completo che documenti geometria interna, taglia M/L e corrispondenza alla generazione dell'esemplare fotografato.

Il candidato commerciale resta [3DModels.org h3dA309108](https://3dmodels.org/sv/3d-models/petzl-boreo-climbing-helmet/). Il risultato è indicizzato come modello del casco, ma l'accesso diretto durante la ricerca integrativa ha restituito 403. Non sono stati acquistati file né verificati interno, scala o taglia. L'esistenza della scheda non costituisce una prova di accuratezza per l'accoppiamento.

È stata rintracciata e letta nel browser anche la fonte originale di un adattatore segnalato dagli indici:

- **[Scurion petzl boreo caving adapt — Thingiverse 6967502](https://www.thingiverse.com/thing:6967502)**, autore **goiko_tt**, pubblicato il **3 marzo 2025**.
- Descrizione: adattatore frontale per lampada Scurion su casco Petzl BOREO CAVING.
- Un file: `Scurion_petzl_boreo_caving_adapter_front.stl`, dimensione indicata **276,8 kB**. Licenza dichiarata **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**. Download offerto senza prezzo; file non scaricato né analizzato geometricamente.
- Il render mostra una piastra esterna con fori e linguetta; nessun modello del casco, scansione dell'interno o ponte interno. Nella scheda non sono documentati taglia, generazione del BOREO, quote di curvatura o montaggio sul casco. Non dimostra compatibilità con il normale BOREO M/L dell'utente o con la Superkikko2.

L'adattatore è quindi un riferimento per la ricerca di accessori esistenti, non una fonte già utilizzabile per ricavare la curva interna richiesta.

### Verifica del fissaggio dell'adattatore Thingiverse

Su richiesta dell'utente è stato ispezionato anche il modello nel viewer 3D ruotabile. Si vedono tre sedi a gradino e una linguetta/gradini sul bordo superiore. La sola geometria non identifica quali elementi uniscano lampada, eventuale platina preesistente e casco. La descrizione dell'autore non contiene istruzioni o foto di montaggio: **il meccanismo di aggancio non è confermato**. Non è stata dimostrata né una necessità di foratura né la possibilità di montarlo direttamente sul BOREO normale.

La [scheda ufficiale BOREO CAVING](https://www.petzl.com/us/en/sport/products/caving-helmets/boreo-caving/BOREO-CAVING_SPO_a2m68000000PBAbAAO.html) conferma la presenza di piastre anteriori/posteriori preinstallate per DUO RL/S. Questo distingue il casco nominato dall'autore dal BOREO fotografato dall'utente, ma non dimostra che il suo STL usi quelle piastre. Non attribuire alla linguetta una funzione di scatto o una specifica interfaccia senza ulteriore riscontro.

È stato azionato il download del singolo file nel browser; non è stato individuato un file locale da ispezionare e il browser è poi diventato indisponibile all'automazione. Non è stata quindi eseguita un'analisi indipendente del file esportato o una prova dell'accoppiamento.
