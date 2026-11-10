# T3 — Drift overnight all'apertura europea (ES 02:00–03:00 ET): **ucciso sulla carta, prima dei dati**

**Data:** 2026-11-10. Nessun dato di T3 è stato guardato. Questa analisi usa solo l'effetto pubblicato e i costi.

## Ipotesi
Boyarchenko, Larsen e Whelan (NY Fed): il rendimento overnight di ES si concentra nell'ora 02:00–03:00 ET (08:00–09:00 in Italia), con circa il 3,6% annuo attribuito a quell'ora (dalle note di ricerca, `02_predicibilita_intraday.md`). **[NV: entità e finestra esatta sono da verificare sul paper.]**

## Conto costi contro effetto
- Effetto lordo: 3,6% / 252 ≈ **1,43 bp al giorno**.
- Costo di un round trip su ES pieno (0,33 punti, come in T1): 1,32 bp con SPX a 2.500, 0,82 bp a 4.000, 0,60 bp a 5.500. I costi si mangiano **dal 42% al 92% dell'effetto**. Sui micro (0,49 punti) va peggio.
- Netto realistico, con SPX a 4.000: circa +0,6 bp al giorno. Con una deviazione standard oraria fra 0,12% e 0,25% [stima], lo Sharpe per trade netto è fra 0,024 e 0,050.
- Giorni necessari per t = 3: **da circa 3.600 a circa 15.000, cioè da 14 a 61 anni.**

## Verdetto
Anche se l'effetto pubblicato fosse vero e intatto, **dopo i costi retail non è dimostrabile con t > 3 in nessun orizzonte utile**. Anche se esistesse, darebbe circa 3–4 $ al giorno per contratto ES: troppo poco rispetto al rischio di coda e alle regole delle prop. **Non lo si testa.** Prima di spendere tempo sui dati serve un'ipotesi con un effetto lordo atteso di molte volte il costo.

## Lezione di metodo (vale per tutto il programma)
Ogni ipotesi futura passa prima da questo filtro sulla carta: effetto lordo atteso / costo ≥ 3, e numero di eventi disponibili sufficiente per t > 3. Le ipotesi che non lo superano non si testano.
