# R07 — provino del giunto M3

**Pronto per la stampa del solo provino PLA**, separato dal casco. Due piccoli pezzi per provare ingresso del dado, foro liscio, gioco laterale della linguetta e montaggio con M3 × 16 + rondella. Stessa sezione 9,2 × 3,2 mm e tasca esagonale 5,85 × 4,3 mm del progetto R07.

[G-code del provino](stampa/PLA_BASIC_ECC2/BOREO_R07_PROVINO_GIUNTO_PLA_ECC2_04.gcode) · [Progetto ElegooSlicer](stampa/PLA_BASIC_ECC2/BOREO_R07_PROVINO_GIUNTO_PLA_ECC2_04.3mf)

Centauri Carbon 2 Combo, ugello 0,4 mm, PEI testurizzato, ELEGOO PLA Basic, 220/60 °C, strati 0,20 mm, 4 pareti, 35% gyroid, 5 strati sopra/sotto. **Nessun brim.** Piccoli supporti nella tasca dado, accessibili da sotto, da rimuovere dopo raffreddamento. Avviso PLA conservato: sportello aperto e/o vetro superiore rimosso. Usare le impostazioni del progetto salvato.

Stime ElegooSlicer 1.5.3.5: **15 min 13 s, 3,84 g**, inclusi supporti; 73 strati controllati. La presenza delle due piccole guide porta il massimo Z a 14,6 mm nella quantizzazione degli strati.

Montaggio: inserire il dado nella tasca sotto il blocchetto; appoggiare la linguetta fra le guide corte, allineare i fori e montare rondella + vite dall'alto. La tasca deve trattenere il dado contro la rotazione senza doverlo martellare. Il foro plastico è liscio. Serrare solo leggermente: verificare il funzionamento e la possibilità di smontaggio, senza prove di carico.

Se dado o linguetta non scorrono, segnalare quale punto tocca prima di ristampare tutta la R07. Il provino **non dimostra resistenza del supporto, tenuta a caldo o compatibilità col casco**.

25 controlli di geometria dei due esportati superati; controlli di struttura 3MF e file di stampa nel report finale del pacchetto. Generazione e slicing riproducibili dal sorgente nella cartella superiore:

```sh
python sorgenti/provino_giunto.py --slice
```

Ferramenta non inclusa nella stampa: 1 vite M3 × 16, 1 rondella 3,2 × 7 × 0,5 mm, 1 dado autobloccante M3 DIN 985, chiave 5,5 mm, altezza 4 mm. La [guida principale R07](../README.md) descrive materiali e montaggio.
