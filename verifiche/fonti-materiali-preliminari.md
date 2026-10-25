# Materiali e formule per uno screening preliminare della R03

Ricerca del 15 ottobre 2026. **Nessuna modifica del CAD e nessuna approvazione del supporto.** Marca, variante, colore e lotto della bobina PETG Pro dell'utente non sono confermati. I dati seguenti non diventano proprietà misurate del pezzo R03.

## ELEGOO PETG Pro: dati dichiarati dal produttore

La [pagina ufficiale ELEGOO EU](https://eu.elegoo.com/products/petg-pro-filament-1-75mm-colored-10kg) contiene questi dati nel JSON HTML `specification-wrapper`, letto direttamente; il testo indicizzato omette alcuni valori Z.

| Proprietà dichiarata | X–Y | Z |
| --- | ---: | ---: |
| Resistenza a trazione | 40 ± 2 MPa | 25 ± 3 MPa |
| Allungamento a rottura | 7,6 ± 1,1% | 5,8 ± 1,7% |
| Resistenza a flessione | 70 ± 2 MPa | 42 ± 3 MPa |
| Modulo a flessione | 2.111 ± 119 MPa | 1.846 ± 145 MPa |

Riporta inoltre **HDT 73 °C a 0,45 MPa**. Mancano Young a trazione, norma, condizioni del provino e significato statistico del ±. Non ho trovato curve creep/fatica. Le impostazioni raccomandate non identificano le condizioni dei provini. [Fonte ELEGOO EU](https://eu.elegoo.com/products/petg-pro-filament-1-75mm-colored-10kg).

Esiste una discrepanza con la [pagina globale ELEGOO in inglese](https://www.elegoo.com/en-gb/products/petg-pro-filament-1-75mm-colored-1kg), che dichiara trazione X–Y ≥37 MPa, flessione 67 MPa, modulo a flessione 1.800 MPa e deformazione termica 66 °C a 0,45 MPa. La pagina non spiega se dipenda da revisione, campione o metodo diverso. Non fondere le due serie e non sceglierne una come certificato della bobina disponibile.

## Orientamento, tempo e temperatura

La guida ufficiale [Stratasys, Design Considerations: FDM Additive Manufacturing Tooling](https://www.stratasys.com/contentassets/1a0cc7a8e7d14f29ac972189bfeade4c/dg_fdm_designconsiderationsfdmtooling_0718a.pdf?v=48fbe5), sezioni 2.2.3 e 2.3.1, descrive la deformazione progressiva dei termoplastici sotto carico prolungato e la minore resistenza interstrato in Z. Raccomanda di considerare orientamento, geometria e raccordi. È una guida generale FDM, non una caratterizzazione del PETG Pro ELEGOO. Il carico di serraggio permanente e il calore della torcia richiedono perciò verifiche distinte dal solo peso statico. L'HDT non è una temperatura di servizio continuo garantita.

Come esempio di caratterizzazione più completa, la [TDS ufficiale Polymaker PETG V1.0](https://polymaker.com/wp-content/uploads/Polymaker-PETG_TDS_EN_V1.0.pdf) distingue Young e modulo a flessione, X–Y e Z, cita ISO 527/178, disegna i provini e dichiara le condizioni di produzione: 240 °C, piano 80 °C, 100% riempimento e ventola spenta. Precisa che i valori tipici servono al confronto e dipendono dalle condizioni di stampa. **È un altro prodotto: nessuno dei suoi numeri è trasferito alla R03 o alla bobina dell'utente.**

## Scenari ipotetici: E = 1 GPa e soglie 5/10 MPa

Questi valori sono plausibili come **ipotesi modificabili per uno screening di sensibilità**. Non sono tensioni ammissibili ricavate da una norma o da prove del supporto.

- **E = 1.000 MPa:** inferiore ai moduli a flessione ELEGOO riportati sopra; può rappresentare uno scenario di rigidezza ridotta per il modello semplificato. Non è il modulo di Young misurato del pezzo, né un limite inferiore garantito dopo ore di carico, riscaldamento o umidità.
- **5 e 10 MPa:** corrispondono rispettivamente al 20% e al 40% del valore centrale di trazione Z dichiarato, 25 MPa. Questi rapporti sono soltanto confronti aritmetici, **non coefficienti di sicurezza dimostrati**. Mancano prove di creep, fatica, urto, adesione interstrato e dispersione del processo reale.
- Il superamento di una soglia di screening segnala un problema nello scenario adottato; un risultato inferiore non convalida l'uso sul casco. Tenere separate tensione nominale di trave, picco locale presso raccordi/fori e pressione di contatto della vite. Non applicare la stessa soglia automaticamente a trazione, taglio e pressione.

## Formule e limiti del modello

Per una mensola rettilinea prismatica, piccole deformazioni e comportamento elastico lineare:

`M_max = F L`, `sigma_max = M_max c / I`, `I_rettangolo = b h³ / 12`, `delta_punta = F L³ / (3 E I)`.

Riferimenti primari didattici: [MIT, Stresses: Beams in Bending](https://ocw.mit.edu/courses/1-050-solid-mechanics-fall-2004/8f0200f4ca3236383a2ef048c7ec4c40_emech9_04.pdf), capitolo 9, e [MIT, Deflections Due to Bending](https://ocw.mit.edu/courses/1-050-solid-mechanics-fall-2004/f9a4d5764b9b0f51ffaacbdf69f7aed8_emech10_04.pdf), capitolo 10. L'asse di flessione decide quale quota è `h`: lo spessore piccolo compare al cubo nella flessione nella direzione debole. La R03 curva, rastremata e con contatti incerti non coincide con questa mensola; usarla come confronto dichiarato, non come FEA della staffa.

Per la torsione di una sezione rettangolare non usare automaticamente il momento polare della sezione circolare. [MIT, Stresses/Deflections: Shafts in Torsion](https://ocw.mit.edu/courses/1-050-solid-mechanics-fall-2004/8c30fdf15d9d50c02f4215903c847d7f_emech8_04.pdf), §8.5, fornisce per lati `2a ≤ 2b`:

`tau_max = T / [k2 (2a)² (2b)]`, `theta = T L / [k1 G (2a)³ (2b)]`.

I coefficienti dipendono dal rapporto dei lati. Anche `G` non è stato misurato: derivarlo da `E/[2(1+nu)]` aggiungerebbe l'ipotesi di isotropia e un Poisson assunto, poco adatti a rappresentare automaticamente uno stampato FDM.

Per i fori, [MIT, Mechanical Principles of Wheelchair Design](https://ocw.mit.edu/courses/ec-721-wheelchair-design-in-developing-countries-spring-2009/e2b7b868b2f7a30cdf36747c3edeea0a_MITEC_721S09_read04_mechprinc.pdf), pagina 23, mostra una concentrazione circa 3 presso un foro circolare in una piastra tesa. **Non attribuire Kt = 3 al foro caricato da una vite della R03:** bordo vicino, contatto, serraggio, geometria e strati cambiano il caso. Restano da valutare sezione netta, schiacciamento locale, strappo verso il bordo e distacco fra strati.

## Dati ancora necessari

Bobina identificata e sua scheda aggiornata; processo e orientamento di stampa; massa completa della torcia, baricentro e bracci di leva; direzioni e durata dei carichi; contatti reali del ponte; ferramenta e serraggio; temperatura presso le orecchie. Lo screening non cambia lo stato **bozza non funzionale** e non autorizza stampa o impiego.

## Conclusione termica

Non ho trovato una temperatura continua massima o una curva di resistenza/creep a caldo per ELEGOO PETG Pro; la bobina disponibile resta da identificare. **HDT e Vicat non sono temperature ammissibili di esercizio continuo:** [UL descrive HDT e Vicat](https://www.ul.com/services/heat-resistance-tests-plastics) come prove su provino sotto carico mentre la temperatura aumenta; per l'invecchiamento prolungato tratta invece programmi LTTA e indice RTI nella [risorsa sulle prestazioni a temperatura elevata](https://www.ul.com/resources/critical-plastics-performance-elevated-temperatures). La [scheda Superkikko2](https://www.kikkolamp.com/superkikko2) dichiara 130 g per il corpo lampada e un dissipatore, ma non pubblica la temperatura massima dei fissaggi: la massa da sola non risolve il dimensionamento termomeccanico e non attribuiamo temperature ipotetiche al prodotto. Per conoscere la temperatura dell'interfaccia è preferibile una sonda a contatto ben accoppiata; una lettura IR richiede emissività e riflessi controllati, soprattutto su metallo lucido, come spiega [FLIR](https://www.flir.com/discover/professional-tools/how-does-emissivity-affect-thermal-imaging/). Non presumere un'emissività dalla sola colorazione. Anche una soluzione ibrida con orecchie metalliche richiede verifica: il metallo può condurre calore fino al giunto polimerico, quindi non è una soluzione termica automatica. Servono temperatura reale e comportamento sotto carico a quella temperatura.
