# Osservazioni sulle foto dell'utente

Data di ricezione: **15 ottobre 2026**. Originali in `sorgenti/riferimenti/foto-utente/`.

Aggiornamento **16 ottobre 2026**: ricevuto e archiviato uno [schizzo quotato dell'utente](../sorgenti/riferimenti/rilievi-utente/2026-10-16-feritoie-spessore.jpg). Trascrizione in [rilievi/2026-10-16-feritoie.json](../sorgenti/rilievi/2026-10-16-feritoie.json): bordo superiore 35 mm, inferiore 3 cm = 30 mm, lato obliquo 10 mm e lato corto 5 mm della feritoia interna disegnata. I 63 mm sono **fra i bordi più vicini**, come confermato dall'utente, non un interasse. I 18 mm indicano casco più schiuma; punto e direzione di misura non precisati. La sagoma non è assunta in scala, i quattro numeri non identificano da soli il rettangolo attraversabile e non si attribuiscono automaticamente a entrambe le aperture.

La direzione successiva alla bozza R04 è ora **piastra interna unica curva**, mantenendo due terminali e la stessa interfaccia esterna. Non è ancora un CAD nuovo. Le quote ricevute non hanno modificato STL, STEP, 3MF o anteprime della R04.

## Riscontri visivi

| Foto | Osservazioni | Limiti |
| --- | --- | --- |
| [1](../sorgenti/riferimenti/foto-utente/Foto-1.jpg) | Etichetta Petzl BOREO, M/L, 53–61 cm, 330 g; schiuma interna, girotesta e fettucce visibili. Presente anche un elemento metallico interno nella parte superiore dell'immagine. | Non si legge codice prodotto/data; funzione e collegamento dell'elemento metallico non dimostrati. |
| [2](../sorgenti/riferimenti/foto-utente/Foto-2.jpg) | Due aperture oblique nella zona anteriore interna e una fascia/fascetta nera vicino al loro margine inferiore; schiuma intorno ai passaggi, imbottitura frontale e sommitale visibili. | Nessuna scala; profondità, percorso completo e spazio libero per i fermi non determinabili. Non si identifica un appoggio strutturale libero sulla calotta. |
| [3](../sorgenti/riferimenti/foto-utente/Foto-3.jpg) | Vista laterale del montaggio: torcia alettata, staffa metallica con vite laterale; apertura del casco e fascetta nera. | Marca/modello e filetto non confermati; non si deduce il percorso completo del fissaggio. |
| [4](../sorgenti/riferimenti/foto-utente/Foto-4.jpg) | Vista esterna frontale/superiore: U metallica intorno alla torcia, farfalla con un'asola orizzontale superiore e due asole laterali quasi verticali; fascetta nera trasversale e due piccoli fissaggi centrali. Sopra è presente un accessorio separato con scritta OSMO. | Asole e ingombri non quotati; spazio per viti/rondelle/utensile e corrispondenza con i contatti interni non dimostrati. La scritta OSMO identifica un altro accessorio e non va usata per identificare la torcia. |

## Bozza CAD disponibile R04 — meccanismo con fermi separati

La bozza R04 conserva **farfalla e U metalliche originali**. Una base/sella esterna stampata porta la farfalla tramite due punti nelle **asole laterali esistenti** e battute di posizione; i fissaggi centrali farfalla/U restano nel gruppo originale. Non è previsto forare la farfalla o il casco.

Due fermi interni separati si collegano alla base attraverso le feritoie. Viti accessibili dall'esterno, senza teste di vite verso la testa all'interno. Le foto non dimostrano ancora appoggi adatti, accessibilità, sequenza di inserimento o possibilità di serraggio senza comprimere la schiuma. Il confronto fra fermi FDM e lamiera è aperto: il requisito è molto sottile, non uno spessore numerico già definito.

Per il CAD e le esportazioni disponibili vedere [bozza-R04/README.md](../bozza-R04/README.md). Le quote della R04 sono assunte e i suoi fermi da 1,2 mm sono dime di forma. La variante con piastra interna unica resta da modellare sui rilievi.

### Dati attivi mancanti

- Sagoma e spessore della farfalla; larghezza/lunghezza/interasse delle asole laterali e posizione utile delle viti.
- Spazio per teste, rondelle e utensile vicino alla U metallica, mantenendo l'inclinazione della lampada.
- Quote delle feritoie e zone effettive d'appoggio di sella esterna, collegamenti e due fermi interni.
- Ingombro interno massimo e interferenze con schiuma, imbottiture, cinghie e girotesta.
- Massa e baricentro del gruppo, temperatura reale dei contatti farfalla/sella e comportamento sotto carico.

## Storico R02/R03 — attacco diretto superato

Durante R02/R03 l'utente aveva sostituito la scelta iniziale di conservare la staffa con questa istruzione: «Anche la staffa u, avviterò direttamente ai lati della torcia quindi prevedi una U che entra direttamente nel casco e mette due fori ai lati». Questa scelta è stata a sua volta superata dalla R04.

Il concetto R02 sostituiva piastra asolata e U con un unico corpo stampato: ponte interno, bracci passanti e orecchie con due fori laterali coassiali. L'interfaccia prevista era quella dei due punti laterali di inclinazione della Superkikko2, visibili nella foto 3. I due fissaggi centrali della foto 4 non erano usati.

Le foto non dimostravano la montabilità della U rigida monopezzo attraverso entrambe le aperture. La bozza R03 con quote assunte resta conservata come storico, non come geometria della R04.

### Dati dell'attacco diretto, conservati come storico non attivo

- Quote delle facce laterali della torcia, asse di inclinazione e ferramenta per i fori della nuova U.
- Rilievo in millimetri delle aperture e della zona di appoggio, compresa la profondità e la forma locale.
- Sequenza d'inserimento della U monopezzo attraverso entrambe le aperture senza forzare i componenti del casco.
- Massa del gruppo da sostenere e spazio necessario per regolarne l'inclinazione.
- Verifica delle interferenze con schiume, imbottiture, cinghie e girotesta.

Non è stata ricavata alcuna misura da pixel, dita o dimensioni presunte della ferramenta. Non è stato diagnosticato lo stato di conservazione del casco dalle foto e non è stata verificata la compatibilità protettiva di alcun inserto.
