# Revisione meccanica preliminare della bozza R03

Data: 15 ottobre 2026. Ambito: solo modulo anteriore Superkikko2, batteria esclusa. Nessuna modifica CAD, FEM o prova fisica eseguita.

**La R03 rimane una bozza di forma.** Le sezioni sottili di partenza non possono essere approvate tramite il solo peso della lampada: servono posizione del baricentro, contatti reali con il casco, interfaccia dei perni, materiale e processo di stampa. Il modello curvo trasmette anche torsione sotto il solo carico verticale. I numeri seguenti sono confronti condizionati, non tensioni ammissibili, carichi garantiti o certificazione del casco.

## Riferimento geometrico e tracciabilita

Letti `parametri_assunti.json` e `genera_modello.py` attuali. I controlli Bezier finali sono **(60,0), (59,10), (36,30), (36,44.5) mm**, con raccordo locale nominale 0.15 mm. Sono questi i dati usati qui. I precedenti controlli preliminari (59.8,-0.1), (51,5) non sono utilizzati; i momenti derivati da quella lettura sono superati.

- Ponte: raggio centrolinea 110 mm, corda 120 mm, altezza Z 12 mm, spessore radiale 1.2 mm.
- Bracci: altezza Z 12 mm; spessore nel piano XY variabile da 1.2 a 4 mm con legge progressiva, non costante.
- Orecchie: spessore X 4 mm, profilo YZ 18 × 16 mm raccordato; fori coassiali X nominali Ø4.5 mm, asse y=50 e z=8 mm. Luce fra facce interne 68 mm.
- Tutte queste quote sono **assunte**, non rilevate sul casco o sull'interfaccia reale SK2.

Hash dei file letti:

- `sorgenti/parametri_assunti.json`: `ab4790fc3bd3bfcf2ed34093f1f284c386d009f9d5a9eb93f3dd98242ce0f741`
- `sorgenti/genera_modello.py`: `33ff0d602f8a7e8cd84d2ae9eccffd24cd93b41ea43c4ee558038d5fd4884b26`
- `stampa/BOZZA_R03_NON_USO.stl`: `37160b175b7ffc6b856ddcb227e332373807eb1f2f76e37bea41854926b96d59`
- `stampa/BOZZA_R03_NON_USO.step`: `a991208766e9a84c9734935d9b8e916bd2de50bb853dabbadd678538ddf2dd20`

Gli hash dei quattro esportati STL/STEP/GLB/3MF attuali coincidono con `report_generazione.json` e `verifica_indipendente.json`. Tali due report non registrano gli hash dei sorgenti: gli hash di sorgente e parametri sopra fissano il riferimento di questa revisione e non dimostrano da soli una rigenerazione byte per byte.

## Massa e scenari di carico

Il [produttore KikkoLamp](https://www.kikkolamp.com/superkikko2) dichiara **130 g per il corpo lampada** e descrive separatamente staffa inox a U, cavo e dissipatore. La pagina non fornisce una tolleranza di massa o un bilancio che chiarisca l'inclusione di ogni accessorio. Per il progetto senza staffa originale e senza batteria, 130 g e un riferimento preliminare; **200 g e soltanto uno scenario scelto** per massa anteriore, non una pesata o un limite garantito.

Si usa g0=9.80665 m/s² e `F_tot = m × k × g0`. I livelli 1g, 5g, 10g sono accelerazioni equivalenti risultanti ipotetiche; 1g rappresenta il carico statico gravitazionale, 5g/10g non sono prove normative o una simulazione di urto. Non sono sommati automaticamente a un ulteriore 1g. Per la prima tabella `Fi=F_tot/2`: ripartizione esattamente simmetrica fra i bracci, da non assumere per un impiglio o per appoggi asimmetrici.

## Sezioni: confronto fra flessione verticale e nel piano

Per una sezione rettangolare ideale di altezza h in Z e spessore t nel piano XY:

- Flessione verticale, asse forte orizzontale normale al percorso: `I_f = t h³/12`, `Z_f = t h²/6`.
- Flessione nel piano XY, asse debole Z: `I_d = h t³/12`, `Z_d = h t²/6`.
- Tensione nominale apparente di sola flessione: `sigma = M/Z`, con N e mm, quindi MPa.

| Sezione ideale | I forte mm⁴ | Z forte mm³ | I debole mm⁴ | Z debole mm³ |
| --- | ---: | ---: | ---: | ---: |
| Radice/ponte 1.2 × 12 mm | 172.8 | 28.8 | 1.728 | 2.88 |
| Tratto braccio 4 × 12 mm | 576 | 96 | 64 | 32 |
| Candidato esterno 6 × 18 mm, non CAD R03 | 2916 | 324 | 324 | 108 |

Nella sezione 1.2 × 12 il rapporto `I_f/I_d=100`: la sensibilita geometrica alla flessione laterale e molto maggiore. Passare da 1.2 a 4 mm a parita di altezza aumenta I forte di 3.33 volte e I debole di 37.04 volte; non elimina pero la radice sottile rimasta a monte. Questi rapporti non sono un coefficiente di sicurezza.

## Carico verticale: scomposizione sulla tangente reale della radice

Si isola il braccio destro e si ipotizza una radice **fittiziamente incastrata** presso l'inizio del Bezier. Centro della sezione A=(60,0,6), punto del carico preliminare B=(36,50,8) mm. Applicare il peso in B e un'ipotesi: il vero baricentro della lampada e ignoto. La tangente locale e t=(-0.09950372,0.99503719,0), la normale nel piano n=(-0.99503719,-0.09950372,0).

Per forza verticale (0,0,-Fi):

- `r = B-A = (-24,50,2) mm`.
- `M = r × F = (-50Fi,-24Fi,0) Nmm`.
- Flessione forte `M_f = M·n = 52.13994877 Fi Nmm`.
- Torsione locale `T = M·t = -18.90570661 Fi Nmm`.
- Momento risultante `|M| = 55.46169850 Fi Nmm`.

Il dislivello di 2 mm non aggiunge momento con una forza esclusivamente verticale. Il momento risultante non va applicato interamente a Z forte: include una componente di torsione. La scomposizione vettoriale segue il metodo di [MIT, David Roylance, Shear and Torsion, eq.6–7](https://web.mit.edu/course/3/3.11/www/modules/torsion.pdf).

| Massa g | Livello g | F totale N | Fi N | M forte/braccio Nmm | T assoluta/braccio Nmm | Sigma forte nominale radice 1.2 × 12 MPa |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 130 | 1 | 1.2749 | 0.6374 | 33.236 | 12.051 | 1.154 |
| 130 | 5 | 6.3743 | 3.1872 | 166.178 | 60.256 | 5.770 |
| 130 | 10 | 12.7486 | 6.3743 | 332.357 | 120.511 | 11.540 |
| 200 | 1 | 1.9613 | 0.9807 | 51.132 | 18.540 | 1.775 |
| 200 | 5 | 9.8066 | 4.9033 | 255.659 | 92.701 | 8.877 |
| 200 | 10 | 19.6133 | 9.8066 | 511.318 | 185.402 | 17.754 |

La colonna sigma comprende **solo flessione forte**: niente torsione, concentrazioni, contatto, fatica, creep o anisotropia della stampa. Non e un giudizio di resistenza. Con il baricentro ipoteticamente 20 mm piu avanti in Y, i coefficienti diventano `M_f=72.04069257Fi` e `T=-16.91563223Fi`; per 200 g/10g la sola sigma forte nominale alla radice diventa 24.530 MPa. Questa posizione del baricentro non e misurata.

Il ponte ha la stessa sezione nominale 1.2 × 12 ma non gli si puo assegnare automaticamente il momento del singolo braccio. Il suo stato dipende dalla distribuzione degli appoggi sul casco, dallo scorrimento e dalla deformazione dell'intera U. Non si e applicata la formula di torsione di un albero circolare alla sezione rettangolare; il riferimento MIT distingue espressamente le sezioni non circolari.

## Carichi laterali e longitudinali: scenari separati

Sempre con meta forza per braccio e radice fittizia, un'accelerazione lungo X genera una componente principale di momento nel piano `|M_z|=50Fi`; lungo Y si ottiene `|M_z|=24Fi`. Le componenti dovute ai 2 mm in Z, i termini assiali e l'interazione con torsione non sono combinati. Le tabelle sono **scenari separati**, non somme di tensioni o carichi contemporanei. Un impiglio di un solo braccio o il tiro del cavo non sono rappresentati dalla semplice massa equivalente.

| Massa g | Livello g | Mz per carico X Nmm | Sigma debole X radice MPa | Mz per carico Y Nmm | Sigma debole Y radice MPa |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 130 | 1 | 31.872 | 11.067 | 15.298 | 5.312 |
| 130 | 5 | 159.358 | 55.333 | 76.492 | 26.560 |
| 130 | 10 | 318.716 | 110.665 | 152.984 | 53.119 |
| 200 | 1 | 49.033 | 17.025 | 23.536 | 8.172 |
| 200 | 5 | 245.166 | 85.127 | 117.680 | 40.861 |
| 200 | 10 | 490.332 | 170.254 | 235.360 | 81.722 |

Questi valori apparenti rendono visibile la debolezza geometrica della sezione sottile nei confronti del momento nel piano. Non dimostrano dove o a quale carico il pezzo reale cederebbe; se grandi deformazioni, contatti o redistribuzioni compaiono, il modello lineare a piccole deformazioni perde validita.

## Orecchie e perni: verifica distinta ancora necessaria

Il foro Ø4.5 e una quota ipotetica, non l'identificazione della vite SK2. Nella sagoma nominale centrata, il legamento netto verticale e 5.75 mm sopra e sotto il foro; quello longitudinale centrale e 6.75 mm. La sezione 12 × 4 piena del braccio non descrive l'orecchia forata.

Come semplice scala di carico, l'area proiettata di contatto ideale per foro e `t d = 4 × 4.5 =18 mm²`. Per 200 g/10g simmetrici `Fi/(td)=0.545 MPa`. Non e la pressione massima reale: gioco, appoggi della vite, rondelle, precarico e deformazione locale possono cambiarla. Il serraggio delle viti laterali per trattenere l'inclinazione puo imporre un carico estraneo al solo peso, non calcolabile qui senza geometria e procedura di serraggio. Mancano anche distanza dal dissipatore, temperatura al contatto e spazio per l'inclinazione.

## Calore: vincolo prioritario ancora non validato

La Superkikko2 ha corpo e dissipatore metallici: il collegamento diretto ai perni laterali crea un possibile percorso di conduzione **corpo lampada → vite/perno/rondella → polimero dell'orecchia**. Il trasferimento esiste anche senza contatto ampio con il dissipatore; distanza, irraggiamento e aria calda possono contribuire. Non sono note la temperatura del corpo presso i perni, quella del contatto polimero o la durata del regime caldo, quindi non si assegnano temperature operative ammissibili.

Peso continuo e precarico di serraggio agiscono mentre il materiale si scalda. Un polimero puo mostrare deformazione nel tempo (creep) e rilassamento del precarico prima della fusione: il foro o il piano sotto rondella possono cambiare forma e la regolazione della lampada allentarsi. Per questo un controllo a temperatura ambiente, anche soddisfacente nel modello a trave, non chiude il problema. Rondelle o distanziali isolanti sarebbero soltanto ipotesi da verificare: non eliminano automaticamente il ponte termico della vite o gli altri percorsi.

La scelta della soluzione fisica deve quindi precedere l'approvazione delle sezioni: misurare temperatura e durata presso l'interfaccia durante funzionamento rappresentativo, poi verificare deformazione e tenuta del serraggio nella stessa condizione. Nessuna prova termica o di creep e stata eseguita; i calcoli sotto sono soltanto un riferimento meccanico preliminare.

## Candidato 6 × 18 mm all'esterno: confronto condizionato

Controllo indipendente dello scenario proposto dal coordinatore: sezione rettangolare **costante** t=6 e h=18 mm; massa 0.2 kg; k=5; quota sul braccio piu caricato q=0.7; leva perpendicolare L=70 mm. Si ottiene `P=q m k g0=6.864655 N` e `M=480.52585 Nmm`. L=70 non e la lunghezza esatta del Bezier: include un'ipotesi di maggiore leva/baricentro. q=0.7 non copre automaticamente una reazione interamente su un braccio.

| Modello a mensola rettilinea uniforme e incastro ideale | Asse forte | Asse debole |
| --- | ---: | ---: |
| I mm⁴ | 2916 | 324 |
| Z mm³ | 324 | 108 |
| Sigma nominale M/Z MPa | 1.4831 | 4.4493 |
| Sigma moltiplicata per Kt=2 ipotetico MPa | 2.9662 | 8.8986 |
| Freccia PL³/(3EI) con E=1000 MPa, mm | 0.2692 | 2.4224 |

Confermati quindi circa **8.9 MPa e 2.4 mm nell'asse debole** di questo modello. E=1 GPa e Kt=2 sono scenari matematici; non sono proprieta verificate del filamento stampato o un fattore di concentrazione calcolato sul raccordo. Soglie di confronto come 10 o 5 MPa non sono ammissibili certificati. A 10g i risultati lineari di questa tabella raddoppiano; mantenendo 5g ma caricando un solo braccio con q=1, il valore con Kt=2 nell'asse debole diventa 12.7123 MPa. Non e una verifica di superamento di un limite materiale.

La sezione 6 × 18 puo essere una **base di confronto per la parte esterna**, subordinata a passaggio nelle aperture, ingombri e libertà del dissipatore. La sua mensola uniforme non modella la R03 rastremata, la torsione o la cedevolezza dell'appoggio. Lasciare una radice libera di 1.2 mm in serie a un braccio esterno spesso mantiene quella radice come elemento determinante. La freccia calcolata non e una previsione dello spostamento finale della torcia.

## Modifiche minime da valutare, preservando la zona della testa

1. Prima definire **dove il carico entra realmente nel casco** e cosa impedisce alla U di scorrere o ruotare. Il casco non e un incastro dimostrato. Un appoggio sulla schiuma o il semplice attrito non possono essere sostituiti nel calcolo con un vincolo rigido senza verifica.
2. Conservare l'intenzione di fascia interna sottile, senza aggiungere spessore verso la testa, ma non affidarle una funzione di mensola libera per tutta la torcia. Occorre verificare un appoggio e una geometria di trattenimento che non comprimano la schiuma e non interferiscano con il sistema del casco.
3. Concentrare l'eventuale aumento di sezione e raccordi **nel tratto esterno dopo le aperture**, vicino alla vera sezione di reazione. Per la flessione nel piano conta fortemente lo spessore t; aumentare soltanto l'altezza Z non risolve nella stessa misura quel modo di deformazione. Non basta irrobustire solo le orecchie lontane dalla radice.
4. Prevedere appoggi locali per vite/rondelle e un'interfaccia di serraggio definita; verificare che il serraggio non avvenga flettendo le orecchie contro il corpo della torcia. Mantenere spazio reale dal dissipatore in tutta l'inclinazione.
5. Per passare al dimensionamento fisico servono almeno: massa anteriore pesata e baricentro/ingombro nella posizione d'uso, interfaccia laterale dei perni e gioco, percorso delle aperture e contatto di reazione, materiale specifico e processo/temperatura. Solo dopo si possono verificare un prototipo sul banco, la deformazione residua e gli effetti del serraggio, senza usarlo in attivita.

Non sono state assegnate proprieta meccaniche a PLA, PETG Pro o TPU per nome generico. Le proprieta FDM dipendono anche da orientamento e processo, come discusso nella [ricerca primaria NASA sulla caratterizzazione FDM](https://ntrs.nasa.gov/api/citations/20160006047/downloads/20160006047.pdf); quei risultati non forniscono ammissibili per questo filamento o questa stampante.

**Stato finale: revisione di calcoli semplificati e scenari ipotetici completata; nessuna resistenza, idoneita del casco o prontezza per la stampa dimostrata.**
