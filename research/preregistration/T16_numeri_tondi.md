# T16: Numeri tondi, rimbalzo e accelerazione (Osler), su XAUUSD, EURUSD, GBPUSD (pre-registrazione)

**Stato:** PRE-REGISTRATO, nessun rendimento guardato. **Data:** 2026-11-12. Design approvato dal committente il 2026-11-12.

## 1. Perché
Il committente chiede se esista qualcosa che "certifichi" un livello di liquidità. La base empirica più solida è Osler, costruita sugli ordini reali di una banca sul forex:
- **Osler (2003, *Journal of Finance*), "Currency Orders and Exchange Rate Dynamics".** Gli ordini di presa di profitto si concentrano **sui** numeri tondi, e il prezzo tende a **invertire** lì.
- **Osler (2005, *Journal of International Money and Finance*), "Stop-loss orders and price cascades".** Gli stop si concentrano **appena oltre** i numeri tondi, e dopo il superamento il movimento tende ad **accelerare**.

I dati di Osler risalgono a fine anni '90 e gli effetti erano piccoli. Si verifica se oggi esistono ancora, e se sono abbastanza grandi da superare i costi.

**La "certificazione"** è il confronto con livelli di controllo non tondi (§4).

## 2. Dati
HistData M1 2010-01 → 2024-12, nei file `data/bars/{XAUUSD,EURUSD,GBPUSD}_1m_24h.parquet`: indice UTC con timestamp di inizio barra, convertito in ora di New York.

**Già visto su questi dati, dichiarato:**
- T8 e T13: breakout e sweep dei box delle sessioni di Asia e Londra;
- T14: griglia di stagionalità e momentum intraday;
- T15: barre giornaliere di EURUSD, GBPUSD e XAUUSD.

Nessun test ha usato i numeri tondi.

**Giorno di trading.** Va dalle 17:00 ET del giorno precedente alle 16:59 ET, ed è etichettato con la data di chiusura. È **valido** se cade da lunedì a venerdì, non è il 25 dicembre né il 1° gennaio, e ha **almeno 1.000 barre**.

## 3. Livelli
| Strumento | Tier A | Tier B (esclusi i livelli A) | Controllo C (esclusi A e B) |
|---|---|---|---|
| EURUSD, GBPUSD | multipli di 0,0100 ("00") | multipli di 0,0050 ("50") | multipli di 0,0025 (x,xx25 e x,xx75) |
| XAUUSD | multipli di 50 $ | multipli di 10 $ | multipli di 5 $ (x5) |

**Distanze:**

| | EURUSD, GBPUSD | XAUUSD |
|---|---|---|
| Distanza di armamento D | 0,0020 | 3,00 $ |
| Superamento δ | 0,0005 | 1,00 $ |

## 4. Eventi
Si lavora sulle barre M1 del giorno di trading valido. Lo stato di ogni livello L riparte da zero all'inizio di ogni giorno di trading.

**Armamento.**
- L è **armato dal basso** dopo una barra con close ≤ L − D.
- L è **armato dall'alto** dopo una barra con close ≥ L + D.
- La barra che arma deve essere **precedente** a quella dell'evento.

**Evento R (rimbalzo, prese di profitto).**
- Si verifica alla prima barra con high ≥ L dopo un armamento dal basso, oppure con low ≤ L dopo un armamento dall'alto.
- Deve esserci un armamento più recente dell'ultima barra che ha toccato L.
- **Direzione contro l'avvicinamento:** short se L è stato raggiunto dal basso, long se dall'alto.

**Evento S (stop, accelerazione).**
- Si verifica alla prima barra con high ≥ L + δ dopo un armamento dal basso, oppure con low ≤ L − δ dopo un armamento dall'alto.
- Deve esserci un armamento più recente dell'ultimo superamento.
- **Direzione del superamento:** long dal basso, short dall'alto.

**Entrata e uscita.**
- **Entrata** al close della barra dell'evento, cioè all'istante T = timestamp + 1 min. Si entra solo se T è fra 02:00 e 15:59 ET compresi.
- **Uscita** a P(T + 60 min): il close dell'ultima barra con timestamp in [T + 55, T + 59] min. Se manca, il trade si scarta, ed è un condizionamento sulla sola disponibilità del dato (dichiarato).
- **Nessuna sovrapposizione:** per ogni (strumento, tier, evento) si può avere al massimo un trade aperto. Gli eventi che arrivano mentre un trade è aperto si ignorano. Si scorrono in ordine di tempo, considerando insieme tutti i livelli del tier.

**Direzione.** È fissata dalla teoria di Osler e non si sceglie sui dati: i test sono a **una coda**.

## 5. P&L e costi
- **P&L di un trade:** lato × (P_uscita − P_entrata) − costo. I costi sono per round trip, come in T14:

  | EURUSD | GBPUSD | XAUUSD |
  |---|---|---|
  | 0,00010 | 0,00013 | 0,35 $/oz |

  Lo stress usa costi 2×.
- **P&L giornaliero:** somma dei trade entrati quel giorno di trading. I giorni validi senza trade contano zero.
- **Statistica:** t di Newey-West con 5 lag sul P&L giornaliero netto (`t1_engine.nw_t`). Il p unilaterale si ricava dal t con la distribuzione normale.

## 6. Test e criteri
I **test sono 12**: 3 strumenti × 2 tier (A, B) × 2 eventi (R, S). La correzione di **Holm** si applica su tutti e 12.

**In-sample, 2010-01-01 → 2019-12-31.** Un test sopravvive se valgono TUTTE:
1. t_NW netto > **3,0** e p di Holm < 0,05;
2. media netta con costi 2× > 0;
3. almeno **6 anni positivi su 10**;
4. almeno **200 trade**.

**Hold-out, 2020-01-01 → 2024-12-31.** Si calcola solo per i sopravvissuti, in un'esecuzione unica. Un test è **EDGE** se valgono:
- t > 1,65;
- media con costi 2× > 0;
- almeno **3 anni positivi su 5**.

**Certificazione del livello (descrittiva, non decisionale).** Per ogni strumento ed evento si applicano le stesse regole ai livelli di controllo C. Si riportano due grandezze:
- il P&L lordo medio per trade su A, su B e su C;
- il t di Welch della differenza A − C e B − C, per trade e al lordo.

Un livello "tondo" è speciale solo se differisce dal controllo.

**Potenza, dichiarata prima.** Gli effetti di Osler erano di pochi pip, mentre i costi sono di 1–1,3 pip sul forex. Per questo **la probabilità di superare t > 3 al netto è bassa**. Se il risultato è positivo ma sotto soglia, l'esito è "INCONCLUSIVO" e non si mette denaro.

## 7. Esecuzione
- Due invocazioni separate (`insample`, `holdout`), ognuna con un file di guardia e un lock di avvio `T16_<stadio>.started`.
- L'in-sample non legge barre successive al 2019-12-31.
- Il codice si sviluppa con TDD e passa una code review indipendente prima dell'esecuzione.
- Nessun parametro si ritocca dopo aver visto i dati.
