# Ponte interno da1,2 a2mm — valutazione preliminare

R09 aveva una pelle curva di1,2mm. R10 porta la pelle a2mm, mantiene raggio esterno92mm e lo stesso intervallo angolare, quindi conserva la curva rivolta al casco. Il raggio interno passa da90,8 a90mm: **0,8mm in più verso la testa**, da verificare insieme al cuscinetto. Bordo inferiore Z21 e sviluppo solo verso l’alto fino aZ37 invariati. Le linguette nelle feritoie restano9,2×3,2mm, con assi X±42: non vengono ingrossate per adattare il ponte.

Il peso del filamento non indica da solo solidità o rigidità. Materiale, sezione, verso degli strati, radici dei bracci, appoggi e carichi contano insieme. Il PETG è una scelta plausibile per tenacità e parti meccaniche, non una garanzia di minore flessione. Non è stata misurata la rigidezza della bobina PLA o PETG dell’utente.

Confronto illustrativo di una striscia rettangolare, stessa larghezza e stesso materiale: I=b*t^3/12; da1,2 a2mm il momento d’inerzia cresce di(2/1,2)^3=4,63. Questo è un confronto di sezione nella flessione attraverso lo spessore, **non** una stima di4,63volte il carico ammissibile del ponte curvo. Non considera vincoli della schiuma, giunzione alle alette, anisotropia, urti, impigli o deformazione prolungata. Non è una simulazione FEA.

Il volume CAD del ponte completo cresce da4561 a5970mm³ circa, comprendendo alette e fori. Le impostazioni R10 usano5pareti e30%gyroid; nel tratto sottile prevalgono i perimetri. Non dichiarare la struttura stampata piena o isotropa.

La [scheda ELEGOO PETG Pro](https://www.elegoo.com/products/petg-pro-filament-1-75mm-colored-1kg) consultata il22ottobre2026 riporta modulo a flessione1800MPa e deformazione termica66°C sotto0,45MPa: sono dati del prodotto pubblicato, non del nostro pezzo stampato. L’HDT non è temperatura di servizio garantita. Non è disponibile una temperatura misurata dei tre contatti della farfalla; anche in PETG l’appoggio completo non diventa un dissipatore. Serve una verifica del montaggio, poi di carico/serraggio/ritenuta e temperatura prima dell’uso reale. Il casco e la lampada non sono stati modificati, forati o provati in questa sessione.
