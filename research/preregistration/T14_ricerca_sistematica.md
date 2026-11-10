# T14 — Ricerca sistematica di predicibilità intraday su 5 mercati (pre-registrazione)

**Stato:** PRE-REGISTRATO, nessun rendimento guardato. **Data:** 2026-11-10.

## 1. Perché
Dopo circa 80 test, i concetti presi dalla letteratura e dal mondo retail sono tutti morti o deboli: T7 è INCONCLUSIVO con Sharpe 0,55. Il committente ha delegato la scelta di mercato e strategia.

Invece di testare un'idea alla volta, si cerca **in modo sistematico** dentro una griglia **finita, decisa ora**, di segnali intraday a motivazione economica:
- stagionalità oraria;
- momentum e reversal di breve periodo;
- condizionamento sui movimenti grandi.

La difesa contro le scoperte casuali è la divisione in tre periodi: **scoperta**, poi **convalida** con correzione per test multipli, poi **hold-out** mai toccato. Il periodo successivo si calcola solo per i segnali sopravvissuti al precedente.

## 2. Dati
- HistData a 1 minuto (timezone verificata: ora di New York con ora legale):

  | File | Dati dal |
  |---|---|
  | `NSXUSD` (Nasdaq-100 → NQ) | 2010-11 |
  | `SPXUSD` (S&P 500 → ES) | 2010-01 |
  | `EURUSD` | 2010-01 |
  | `GBPUSD` | 2010-01 |
  | `XAUUSD` | 2010-01 |

  Tutti fino al 2024-12-31. Non c'è volume.
- **Periodi:**

  | Periodo | Date |
  |---|---|
  | Scoperta | inizio → 2017-12-31 |
  | Convalida | 2018-01-01 → 2021-12-31 |
  | Hold-out | 2022-01-01 → 2024-12-31 |

- **Cosa si è già visto su questi dati, dichiarato:** T8 e T13 hanno usato 2010–2023 per i setup di sessione H8a–H8e (breakout e sweep dei box Asia e Londra). T7 ha usato NSXUSD 2010–2016 per la Noise Area. Nessuno di questi è un segnale della griglia T14. Il difetto dei dati di feb–lug 2023 è gestito dalla regola di inclusione dei giorni.

## 3. Giorni validi
- **Indici (NSXUSD, SPXUSD):** sessione NYSE senza chiusura anticipata, con almeno 300 barre fra 09:30 e 15:59 ET.
- **Forex e oro:** da lunedì a venerdì, escluso il 25 dicembre e il 1° gennaio, con almeno 768 barre (80%) fra 00:00 e 15:59 ET.

## 4. Prezzi
P(t) = close dell'ultima barra con timestamp in [t−5 min, t−1 min], cioè l'ultimo prezzo noto all'istante t. Se manca, P(t) è indefinito e quel giorno quella configurazione non opera. I tempi possono cadere nel giorno precedente: si usano le 16:00 del giorno precedente per gli indici e le 18:00 del giorno precedente per forex e oro.

## 5. Griglia (finita, fissata ora)
**Entrate (E):**
- indici: 09:30, 10:00, …, 15:30 (13);
- forex e oro: 00:00, 00:30, …, 15:00 ET (31).

**Holding (H), uscita a P(E+H):**
- indici: H ∈ {30, 60, 120} minuti con uscita ≤ 16:00, più H = "close" (uscita a P(16:00)) solo se 16:00 − E > 120 minuti;
- forex e oro: H ∈ {30, 60, 120} con uscita ≤ 16:30.

Coppie (E, H): **44 per ogni indice** e **92 per forex e oro**.

**Lookback (L)** per il segnale r_L = P(E)/P(E−L) − 1:
- L ∈ {30, 60, 120 minuti, "ancora"};
- "ancora" è dalle 16:00 del giorno precedente per gli indici e dalle 18:00 del giorno precedente per forex e oro.

**Famiglie:**
- **S (stagionalità):** trade ogni giorno valido nella direzione d.
- **M (momentum o reversal):** lato = d × segno(r_L). Nessun trade se r_L = 0.
- **MC (M condizionato):** come M, ma solo se |r_L| > l'80° percentile di |r_L| sui 60 giorni validi **strettamente precedenti** della stessa configurazione. Servono almeno 40 osservazioni, altrimenti non si opera.

La direzione d ∈ {+1, −1} si sceglie in scoperta, come il segno del P&L lordo medio. Il test è quindi a due code: è un grado di libertà dichiarato, assorbito dalla soglia t > 3.

**Numero di configurazioni:**

| Strumento | S | M e MC | Totale |
|---|---|---|---|
| Ogni indice | 44 | 44 × 4 × 2 = 352 | **396** |
| Forex e oro | 92 | 92 × 4 × 2 = 736 | **828** |

**Totale: 2 × 396 + 3 × 828 = 3.276 configurazioni.** Il codice verifica questo numero.

## 6. P&L e costi
Il P&L giornaliero, per configurazione, è lato × (P(uscita) − P(E)) − costo, oppure 0 se quel giorno non si opera. Al massimo 1 trade al giorno per configurazione.

| Strumento | Costo per round trip | Valore |
|---|---|---|
| NQ | 0,45 pt | 20 $ a punto |
| ES | 0,5 pt | 50 $ a punto |
| EURUSD | 0,00010 | lotto 100k |
| GBPUSD | 0,00013 | lotto 100k |
| XAUUSD | 0,35 $/oz | 100 oz |

Gli stress test usano 2× il costo. Statistica: t di Newey-West con 5 lag sul P&L giornaliero netto, giorni validi del periodo, zeri inclusi (`t1_engine.nw_t`).

## 7. Regole di selezione
**Stadio 1 — Scoperta (inizio → 2017).** Per ogni configurazione si sceglie d. Passa alla convalida se valgono TUTTE:
1. t_NW netto > **3,0**;
2. media netta con costo 2× > 0;
3. almeno 150 trade;
4. almeno 2/3 degli anni con somma netta > 0. Un anno con meno di 60 giorni validi si accorpa al successivo.

Si tengono al massimo **10 configurazioni per strumento**, quelle con t più alto. Con 3.276 test e t > 3 a due code ci si aspettano circa 9 falsi positivi sotto l'ipotesi nulla: la convalida serve a eliminarli.

**Stadio 2 — Convalida (2018–2021), calcolata solo per chi ha superato lo stadio 1.** Con d congelato, sopravvive se valgono:
- p unilaterale (dal t_NW) significativo con **Holm** al 5% su tutte le configurazioni entrate nello stadio 2;
- media con costo 2× > 0;
- almeno 2 anni su 4 positivi.

**Stadio 3 — Hold-out (2022–2024), esecuzione unica, solo per chi ha superato lo stadio 2.** Una configurazione è **EDGE CANDIDATO** se valgono:
- t_NW > 1,65 con Holm sui sopravvissuti;
- media con costo 2× > 0;
- almeno 2 anni su 3 positivi.

Si riporta anche il t sull'intero periodo 2010–2024.

**Esiti:**
- **Nessun EDGE CANDIDATO:** la griglia T14 è chiusa e lo si dichiara.
- **Almeno un EDGE CANDIDATO:** si passa a simulazione con le regole prop e forward test in demo, minimo 3 mesi, prima di qualsiasi spesa.

Nessun parametro si ritocca dopo aver visto i dati.

## 8. Esecuzione
Tre invocazioni separate (`scoperta`, `convalida`, `holdout`), ognuna con un file di guardia: non si riesegue, e ogni stadio rifiuta di partire se lo stadio precedente non ha scritto il suo file. Lo stadio di scoperta **non calcola nulla dopo il 2017-12-31**. Codice sviluppato con TDD e revisionato in modo indipendente prima di qualsiasi esecuzione.

## Emendamento 1 — 2026-11-10, dalla code review, registrato PRIMA di qualsiasi calcolo di rendimento
Il revisore ha fatto solo controlli strutturali sui prezzi, cioè se un prezzo esiste a un dato orario. Nessun P&L è stato calcolato.
1. **Ancora degli indici.** Con la definizione originale, "16:00 del giorno di calendario precedente", il lunedì P è indefinito nel 100% dei casi, perché la domenica alle 16:00 non ci sono barre, e lo stesso vale nei giorni dopo un festivo. Nuova definizione: **P(16:00) della sessione NYSE precedente**. È il rendimento dalla chiusura della sessione precedente, che era l'intento.
2. **Ancora di forex e oro.** L'oro non quota fra le 17:00 e le 18:00 ET, quindi P(18:00) esiste solo nello 0,2–5% dei giorni. Nuova ancora per tutti e tre gli strumenti: **P(18:10) del giorno di calendario precedente**. La copertura fino al 2017 è del 98,8–99,9%: è stato misurato solo se il prezzo esiste.
3. **Dati dichiarati.** SPXUSD parte dal **2010-11-14**, non dal 2010-01 come scritto nella §2. Nel 2012–2014 e nel 2017 ha meno giorni validi (229–234). La regola di inclusione dei giorni usa barre successive all'entrata: è un condizionamento sulla sola disponibilità dei dati, ereditato dai test precedenti e dichiarato.
4. **Integrità.** All'avvio di ogni stadio si crea un file `T14_<stadio>.started`. Se esiste, lo stadio non riparte, anche dopo un crash. Il file dei risultati viene scritto prima di ogni altro file accessorio.

Tutto il resto è invariato, compreso il numero di 3.276 configurazioni.
