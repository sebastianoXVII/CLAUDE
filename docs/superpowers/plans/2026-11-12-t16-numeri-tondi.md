# T16 Numeri tondi — Piano di implementazione

> **Per chi esegue:** sotto-skill richiesta: superpowers:executing-plans (esecuzione nativa, scelta del quant lead, perché i task dipendono strettamente l'uno dall'altro e il committente ha delegato il come). La revisione indipendente avviene sull'intero branch prima dell'esecuzione. I passi usano le checkbox (`- [ ]`).

**Obiettivo:** motore e runner che calcolano i 12 test pre-registrati di T16 e la diagnostica di controllo, con un'esecuzione in-sample unica.

**Architettura:**
- `research/t16_engine.py` contiene le funzioni pure: livelli, giorni validi, eventi per livello e per giorno, trade e P&L giornaliero.
- `research/run_t16.py` contiene configurazione, caricamento, preflight, guardie e lock, statistica, regole e output JSON. Lo schema è quello di `run_t15.py`.

**Tecnologie:** numpy, pandas, `t1_engine.nw_t` e `t1_engine.holm`, `scipy.stats` (norm, Welch), pytest.

**Specifica:** `research/preregistration/T16_numeri_tondi.md`. Design: `docs/superpowers/specs/2026-11-12-t16-numeri-tondi-design.md`.

## Vincoli globali (valori esatti dalla specifica)
**Dati e giorni:**
- File `data/bars/{XAUUSD,EURUSD,GBPUSD}_1m_24h.parquet`, indice UTC con timestamp di inizio barra, convertito a `America/New_York`.
- Giorno di trading = data di (ts_ET + 7h). Valido se il giorno della settimana è < 5, non è il 25/12 né l'1/1, e le barre sono ≥ 1000.

**Livelli, in unità intere** (forex: pip = prezzo × 10.000; oro: centesimi = prezzo × 100):

| | Forex | Oro |
|---|---|---|
| Tier A | multipli di 100 | multipli di 5000 |
| Tier B | multipli di 50, non di 100 | multipli di 1000, non di 5000 |
| Controllo C | multipli di 25, non di 50 | multipli di 500, non di 1000 |
| D | 20 | 300 |
| δ | 5 | 100 |

**Esecuzione:**
- entrata al close della barra dell'evento, T = ts + 1 min, ammessa solo con T fra 02:00 e 15:59 ET;
- uscita al close dell'ultima barra con ts in [ts + 56, ts + 60] min; se non c'è, il trade si scarta;
- nessuna sovrapposizione: un evento si accetta se T ≥ T del trade precedente accettato + 60 min.

**Costi** per round trip: EURUSD 0,00010, GBPUSD 0,00013, XAUUSD 0,35. Lo stress usa 2×.

**Periodi:**
- in-sample 2010-01-01 → 2019-12-31;
- hold-out 2020-01-01 → 2024-12-31.

**Criteri:**
- in-sample: t > 3, Holm su 12 < 0,05, stress > 0, almeno 6 anni positivi, almeno 200 trade;
- hold-out: t > 1,65, stress > 0, almeno 3 anni positivi.

## Focus della revisione
1. **Prezzo esattamente uguale al livello.** I float sono a 4–5 decimali: il confronto usa la tolleranza 1e-9 e il livello si ricava da interi.
2. **Barra che arma e tocca insieme** (close ≤ L − D e high ≥ L): non genera l'evento in quella barra. L'armamento vale solo per le barre successive.
3. **Bordi della finestra.** La barra delle 15:58 (T = 15:59) è ammessa; quella delle 15:59 (T = 16:00) no; quella delle 01:59 (T = 02:00) è ammessa.
4. **Buco nei dati dopo l'entrata.** Se non c'è una barra in [ts + 56, ts + 60], il trade si scarta e non blocca il trade successivo.
5. **Cambio di giorno.** Un armamento del giorno precedente non vale nel giorno nuovo, perché lo stato si azzera.

---

### Task 1: livelli e giorni validi
**File:** creare `research/t16_engine.py` e `research/tests/test_t16_engine.py`.

**Produce:**
- `levels(lo: float, hi: float, scale: int, step: int, excl: tuple[int, ...]) -> np.ndarray`: prezzi float dei multipli di `step` in unità `scale` dentro [lo, hi], esclusi i multipli dei valori in `excl`;
- `trading_day(idx_et: pd.DatetimeIndex) -> np.ndarray` (datetime64[D]);
- `valid_days(bars_et: pd.DataFrame) -> pd.DatetimeIndex`.

**Passi:**
- [ ] Scrivere i test:
  - `levels(1.0960, 1.1110, 10000, 100, ())` restituisce `[1.1, 1.11]`;
  - `levels(1.0940, 1.1060, 10000, 50, (100,))` restituisce `[1.095, 1.105]`;
  - `levels(1.0990, 1.1030, 10000, 25, (50,))` restituisce `[1.1025]`;
  - oro: `levels(1243, 1262, 100, 1000, (5000,))` restituisce `[1260.0]`;
  - `trading_day`: le 17:00 ET del giovedì appartengono al venerdì;
  - `valid_days`: esclude sabato, 25/12 e i giorni con meno di 1000 barre.
- [ ] Eseguire i test: devono fallire (RED).
- [ ] Implementare con aritmetica intera: `k` da `ceil(lo*scale/step)` a `floor(hi*scale/step)`, poi `k*step/scale`.
- [ ] Test verdi (GREEN), poi commit.

### Task 2: eventi per livello in un giorno
**Consuma** gli array di un giorno: `high`, `low`, `close` (float64).

**Produce:** `level_events(high, low, close, L: float, D: float, delta: float, kind: str) -> list[tuple[int, int]]`, cioè una lista (indice barra, lato) con `kind` in {"R", "S"}.
- R dal basso → lato −1; R dall'alto → lato +1.
- S dal basso → lato +1; S dall'alto → lato −1.

**Algoritmo**, per ogni direzione:
- `arm` = close ≤ L − D (dal basso) oppure close ≥ L + D (dall'alto);
- `hit`:
  - R: high ≥ L − 1e-9 (dal basso) oppure low ≤ L + 1e-9 (dall'alto);
  - S: high ≥ L + δ − 1e-9 (dal basso) oppure low ≤ L − δ + 1e-9 (dall'alto);
- `prev_arm[i]` = indice massimo j < i con arm, altrimenti −1; `prev_hit[i]` = indice massimo j < i con hit, altrimenti −1;
- evento in i se hit[i] e prev_arm[i] ≥ 0 e prev_arm[i] > prev_hit[i].

**Passi:**
- [ ] Scrivere i test:
  - rimbalzo dal basso: armamento alla barra 1, tocco alla barra 4, quindi `[(4, -1)]`;
  - un secondo tocco senza riarmo non genera evento;
  - dopo il riarmo un nuovo tocco genera un secondo evento;
  - la barra che arma e tocca insieme non genera evento (Focus 2);
  - simmetria dall'alto;
  - S: superamento di δ dal basso dà lato +1; un tocco di L senza superamento non genera evento S;
  - nessun armamento, nessun evento.
- [ ] RED, poi implementazione vettoriale con `np.maximum.accumulate`, poi GREEN, poi commit.

### Task 3: trade di un giorno e P&L giornaliero
**Produce:**
- `day_trades(day_bars_et: pd.DataFrame, lv: np.ndarray, D, delta, kind, cost) -> pd.DataFrame` con colonne `entry_time, side, level, p_in, p_out, gross, net`;
- `daily_pnl(trades: pd.DataFrame, days: pd.DatetimeIndex, cost_mult: float) -> pd.Series`, cioè la somma per giorno di (gross − cost_mult × cost), con zero nei giorni senza trade.

**Regole:**
- livelli rilevanti: solo quelli in [low_giorno − D − δ, high_giorno + D + δ];
- finestra 02:00 ≤ T ≤ 15:59;
- uscita in [ts + 56, ts + 60]; senza barra il trade si scarta prima della selezione;
- selezione greedy in ordine di (ts, livello, lato), accettando l'evento se T ≥ T del precedente + 60.

**Passi:**
- [ ] Scrivere i test:
  - un evento con uscita a +60: `gross = lato × (p_out − p_in)` e `net = gross − cost`;
  - bordi della finestra (Focus 3);
  - buco nei dati in uscita: il trade si scarta e l'evento successivo resta valido (Focus 4);
  - due eventi a 30 minuti l'uno dall'altro su livelli diversi: si tiene solo il primo;
  - `daily_pnl`: zeri nei giorni senza trade; con `cost_mult` = 2 la media netta si riduce esattamente del costo per trade;
  - lo stato si azzera fra un giorno e l'altro (Focus 5), testato in `run_t16` (task 4) tramite la funzione per periodo.
- [ ] RED, implementazione, GREEN, commit.

### Task 4: runner
**File:** creare `research/run_t16.py` e `research/tests/test_t16_run.py`.

**Produce:**
- `INSTR` = dict sym → dict(`cost`, `scale`, `D`, `delta`, `A` = (step, excl), `B`, `C`);
- `PERIODS`;
- `load(sym, end) -> DataFrame ET` (barre con trading_day ≤ end);
- `trades_for(bars_et, sym, tier, kind) -> DataFrame`, che scorre i giorni validi uno alla volta;
- `evaluate(trades, days, cost, s, e) -> dict` con i campi t_nw, p_one, media, stress_mean, per_anno, years_pos, n_trades, media_lorda_trade;
- `insample_pass(m) -> bool` e `holdout_pass(m) -> bool`;
- `controls(...)`: Welch A−C e B−C sul gross per trade;
- `preflight(stage)`;
- `main(argv)`.

**Guardie:**
- se il JSON esiste, uscita con "già eseguito";
- se `T16_<stage>.started` esiste, uscita con un messaggio che contiene "lock";
- poi il preflight (file presenti; prima data ≤ 2010-01-31; ultima ≥ 2019-12-30 per l'in-sample, ≥ 2024-12-30 per l'hold-out);
- poi la scrittura del lock.

L'hold-out richiede `T16_insample.json` e calcola solo i sopravvissuti; se non ce ne sono, termina senza lock.

**Passi:**
- [ ] Scrivere i test:
  - costi e parametri uguali alla specifica;
  - 12 chiavi di test;
  - regole in-sample e hold-out ai bordi (t = 3 non passa; 199 trade non passano);
  - `load` tronca al periodo;
  - le guardie e il lock;
  - preflight con file mancante;
  - end-to-end sintetico: una serie costruita con rimbalzi deterministici su 1,1000 dà t > 0 per R, Tier A, EURUSD, e il JSON contiene `p_holm` e `controlli`.
- [ ] RED, implementazione, GREEN, poi suite completa, poi commit.

### Task 5: revisione e run unico
- [ ] Revisione indipendente da subagente sul diff di T16, solo con dati sintetici. Correggere i finding con TDD.
- [ ] Verifica: `pytest -q research/tests/` tutto verde, `preflight("insample")` OK.
- [ ] `python3 research/run_t16.py insample`, una volta sola, poi verdetto in `research/results/T16_verdetto.md`, commit e push.
- [ ] Hold-out solo per i sopravvissuti.
