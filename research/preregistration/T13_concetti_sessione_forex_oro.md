# T13 — Concetti di sessione del committente su forex e oro (pre-registrazione)

**Stato:** PRE-REGISTRATO; nessun dato di questi strumenti scaricato o guardato. **Data:** 2026-11-10.

## 1. Perché
- Il committente vuole sapere se i suoi concetti funzionano su CFD forex e oro.
- I concetti ICT/SMC (Asian range, Judas swing di Londra, killzone) nascono proprio sul forex: è il loro terreno naturale.
- Servono anche strumenti candidati per la diversificazione sui conti prop, dove FundedNext permette il trading su CFD.

## 2. Strumenti (scelti PRIMA di guardare, solo 3)
| Strumento | Fonte | Perché |
|---|---|---|
| **EURUSD** | HistData M1 | coppia più liquida, spread minimo |
| **GBPUSD** | HistData M1 | la più "londinese", tradizionale terreno dei setup di sessione |
| **XAUUSD** | HistData M1 | oro, molto tradato dai retail, poco correlato con gli indici |

## 3. Regole
**Identiche a T8 con gli emendamenti 1–4**, cioè il codice di `research/t8_engine.py` senza modifiche:
- 5 ipotesi: H8a sweep di Londra dell'Asia, H8b rottura del box Asia con accettazione o riassorbimento, H8c sweep del range di Londra a NY, H8d IFVG, H8e order block;
- 2 varianti: senza filtro e con filtro HTF.

Stessi orari ET, stessa esecuzione conservativa e stessa inclusione dei giorni (barra delle 15:59 ET e almeno 300 barre fra 09:30 e 15:59). Anche le chiusure anticipate NYSE restano escluse: non hanno senso per il forex, ma si mantengono per non toccare il codice, e lo si dichiara.

## 4. Costi (round trip, in unità di prezzo; stima su un conto prop CFD raw spread + commissione)
| | Spread medio + commissione | Costo base | Stress 2× |
|---|---|---|---|
| EURUSD | circa 0,3 pip + 0,7 pip | **0,00010** (1,0 pip) | 0,00020 |
| GBPUSD | circa 0,6 pip + 0,7 pip | **0,00013** (1,3 pip) | 0,00026 |
| XAUUSD | circa 0,20 $ + 0,15 $ | **0,35 $/oz** | 0,70 $ |

Sono stime da verificare sul conto reale prima di qualsiasi uso.

## 5. Campioni e criteri
- **Dati:** HistData dal 2010-01-01. Fuso EST fisso UTC−5, senza ora legale, convertito in ET come in T8 emendamento 4.
- **In-sample:** 2010-01-01 → 2023-12-31. Hold-out: dal 2024-01-01 alla fine dei dati disponibili quando si esegue.
- **Famiglia:** 3 strumenti × 10 test = **30 test, correzione di Holm sui 30**.
- **Un test sopravvive in-sample se valgono TUTTE queste condizioni:**
  1. t di Newey-West (5 lag) > 3 sul P&L giornaliero netto (0 nei giorni senza trade);
  2. p corretto con Holm < 0,05;
  3. media > 0 con stress 2×;
  4. almeno 2/3 degli anni positivi;
  5. almeno 150 trade.
- **Hold-out, solo per i sopravvissuti:** t > 2 e media > 0 con stress 2×. Se l'hold-out ha meno di 200 giorni, si dichiara INCONCLUSIVO, non sopravvissuto.

## 6. Esito
- **Nessun sopravvissuto:** i concetti di sessione sono morti anche sul forex e sull'oro, nella loro forma meccanica canonica.
- **Uno o più sopravvissuti:** vanno a hold-out e poi al forward test. Le combinazioni si valutano solo con una nuova pre-registrazione.

## 7. Diario
Tutti i trade in-sample vanno in `journal.sqlite` (strategia `T13_<strumento>_<ipotesi>`), con screenshot dei box Asia/Londra/NY.
