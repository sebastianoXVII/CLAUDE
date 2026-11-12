# T16: numeri tondi (Osler), design breve

**Approvato dal committente il 2026-11-12.** Le regole complete e congelate sono in `research/preregistration/T16_numeri_tondi.md`.

## Perché
Il committente chiede se qualcosa "certifichi" un livello di liquidità. La base empirica è Osler (2003, 2005), con gli ordini reali di una banca:
- le prese di profitto si concentrano sui numeri tondi, dove il prezzo tende al rimbalzo;
- gli stop si concentrano appena oltre, dove il prezzo tende all'accelerazione.

Si verifica se oggi esiste un edge netto. La certificazione è il confronto con livelli di controllo non tondi.

## Obiettivi
**Goal:** un verdetto statistico sui 12 test (3 strumenti × 2 tier × 2 eventi), più la diagnostica tondo-contro-controllo.

**Non-goal:**
- ottimizzare orizzonte, distanze o filtri;
- altri strumenti.

**Anti-goal:** un risultato "positivo" ottenuto ritoccando regole o costi dopo aver visto i dati.

## Approcci considerati
| Approccio | Esito | Motivo |
|---|---|---|
| (1) Entrata al close della barra dell'evento, uscita a tempo fisso di 60 minuti | **Scelto** | Nessun parametro di gestione; esecuzione realistica |
| (2) Entrata con ordine limit esatto sul livello | Scartato | Il fill è ottimistico (la coda sul livello non è modellabile con M1) |
| (3) Stop e target | Scartato | Aggiungono parametri e gradi di libertà |

## Decisioni del committente
- strumenti XAUUSD, EURUSD, GBPUSD;
- design breve approvato: livelli 00/50 e 50 $/10 $, distanza D, superamento δ, 60 minuti, periodi e criteri.

## Decisioni mie, dichiarate
- finestra di entrata 02:00–15:59 ET;
- un trade alla volta per test;
- stato dei livelli azzerato ogni giorno;
- giorni validi con almeno 1.000 barre;
- trade scartato se manca il prezzo di uscita.

## Al costruttore
- motore vettoriale numpy per livello, senza numba;
- riuso di `t1_engine.nw_t` e `holm`;
- struttura del runner come in T15 (guardie, lock, preflight).
