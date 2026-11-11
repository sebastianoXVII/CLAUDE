# T15: Emendamento 2, rotture del dato (pre-registrazione)

**Data:** 2026-11-11, prima di qualunque calcolo di rendimento della strategia.

Integra `T15_trend_following_diversificato.md` (versione originale ed Emendamento 1, entrambi invariati). Tutto ciò che non è scritto qui resta come prima.

## Cosa si è visto prima di scrivere questa regola
Si sono visti solo i livelli di prezzo e il controllo descrittivo di qualità (`research/data/daily_quality.py`), e solo su **6 strumenti su 23**: NSXUSD, SPXUSD, GRXEUR, EURUSD, GBPUSD, XAUUSD. Gli altri 17 non erano ancora scaricati: la regola qui sotto è quindi cieca rispetto a loro. Nessun P&L, segnale o posizione è stato calcolato.

**Anomalia trovata.** Il file **GRXEUR (DAX)** contiene, dal **2020-06-15 al 2023-12-01**, un'altra serie:
- i livelli sono fra 2.950 e 4.430, contro circa 12.000 prima e circa 16.400 dopo;
- le barre per giorno scendono da circa 1.330 a circa 840.

Livelli e orari sono compatibili con l'Euro Stoxx 50. È un'ipotesi basata sui livelli e non verificata; ETXEUR finisce proprio a inizio 2019. Ai due bordi del tratto i rendimenti "giornalieri" sarebbero −73% (2020-06-15) e +271% (2023-12-04).

Si sono visti anche movimenti estremi ma **reali**, che vanno tenuti:
- Brexit (GBPUSD −8%, 2016-06-24);
- crollo dell'oro (−9%, 2013-04-15);
- COVID (marzo 2020).

## Regola 1 — Rotture del dato (generale, per tutti i 23 strumenti)
Sui giorni validi (definizione invariata: almeno 120 barre M1):
1. un giorno con **close ≤ 0** è non valido e crea una rottura (caso WTI dell'aprile 2020, se presente nel file);
2. c'è una rottura fra due giorni validi consecutivi se **|ln(close_t / close_t−1)| > ln 2**, cioè se il prezzo raddoppia o si dimezza in un giorno.

   Nessuno dei 23 mercati, sui prezzi di chiusura, si muove così in un giorno reale. Il caso più estremo atteso è il franco svizzero del 15/01/2015, con un movimento di circa il 15–20% in chiusura, che resta ben sotto la soglia.

**Effetto di una rottura.** La serie si spezza in **segmenti indipendenti**:
- lo strumento esce dal portafoglio (N_t) dall'ultimo giorno del segmento precedente;
- nel nuovo segmento rientra solo dopo **252 giorni validi di storia del segmento stesso**, con segnale e volatilità ricalcolati da zero (la volatilità EWMA riparte dal segmento);
- il rendimento a cavallo della rottura non entra mai nel P&L;
- l'uscita forzata non paga costo di transazione, come per l'uscita a fine dati dell'Emendamento 1.

## Regola 2 — Tratto sostituito del DAX
Il tratto **GRXEUR 2020-06-15 → 2023-12-01** è **escluso**: non è il DAX. I suoi giorni sono trattati come non validi, con una rottura all'inizio e una alla fine. Il DAX rientra solo dopo 252 giorni validi dal 2023-12-04, quindi a fine 2024.

L'esclusione tocca solo l'hold-out: l'in-sample 2011–2019 non è toccato.

## Limiti dichiarati
- **Sostituzioni simili non rilevabili.** La regola non intercetta sostituzioni di serie con livelli simili, né salti sotto la soglia.
- **Salti di roll di WTI e Brent.** Eventuali salti mensili dovuti al cambio di contratto restano nei dati e non si correggono. Sono un limite noto anche dei CFD reali, che li compensano con un accredito o addebito che qui non si modella.
- **Altre anomalie.** Il controllo descrittivo sui 23 strumenti completi si esegue comunque prima dell'in-sample. Se trova un'anomalia di natura diversa da queste, serve un Emendamento 3, registrato prima dell'in-sample e motivato solo dal dato, mai dal P&L.
