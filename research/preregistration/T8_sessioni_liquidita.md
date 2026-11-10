# T8 — Concetti di sessione e liquidità del committente (pre-registrazione)

**Stato:** PRE-REGISTRATO; dati 24 ore non ancora disponibili (OANDA in verifica). **Data:** 2026-11-10.
**Fonte delle ipotesi:** i concetti indicati dal committente: box di sessione Asia/Londra/NY, presa di liquidità pre-Londra, POI, IFVG, order e breaker block, rottura del box Asia su NQ, Wyckoff, multi-timeframe, failed auction. Per ognuno si usa la definizione canonica retail (ICT/SMC/Market Profile), tradotta in regole meccaniche **senza parametri da ottimizzare**. Dove esistono più definizioni si sceglie quella più diffusa, dichiarata qui sotto.

## 1. Dati e convenzioni
- **Strumento principale:** NQ (OANDA `NAS100_USD`, M1 mid, 24 ore). **Secondario:** ES (`SPX500_USD`), solo riportato, non decisionale.
- **Orari ET** (orario di New York, con ora legale):
  - Asia range = 20:00–23:59 del giorno precedente (definizione ICT "Asian range");
  - killzone di Londra = 02:00–04:59;
  - killzone di NY = 08:30–10:59;
  - sessione regolare NY = 09:30–15:59.
- **Trend sul timeframe alto (HTF):** rialzista se il close giornaliero delle 16:00 del giorno precedente è sopra la sua media mobile a 20 giorni, ribassista se è sotto.
- **Esecuzione:** simulatore conservativo di T4 (stop prima del target nella stessa barra, stop all'open in caso di gap), 1 trade al giorno per ipotesi, chiusura forzata alle 15:55.
- **Costi** per round trip: NQ 0,45 punti (MNQ 0,85), CFD 2 punti; stress 2×.
- **Campioni:** in-sample dall'inizio dei dati al 2023-12-31; hold-out dal 2024-01-01, vincolato al verdetto in-sample.

## 2. Ipotesi (5) × varianti (2: senza filtro, con filtro HTF) = 10 test, famiglia unica con Holm
- **H8a — Sweep di Londra dell'Asia (presa di liquidità pre-Londra, "Judas swing").**
  - Evento: fra le 02:00 e le 04:59 il prezzo supera l'high (o il low) dell'Asia range, poi una barra a 5 minuti chiude di nuovo dentro il range entro 30 minuti dallo sweep.
  - Ingresso: al close di quella barra, in direzione opposta allo sweep.
  - Stop: estremo dello sweep. Target: lato opposto dell'Asia range.
  - Uscita: al più tardi alle 11:00.
  - Variante HTF: si opera solo se la direzione del trade coincide con il trend HTF.
- **H8b — Rottura del box Asia su NQ: accettazione o riassorbimento** (regola esposta dal committente).
  - Evento: fra le 03:00 e le 10:59, prima barra a 5 minuti che chiude oltre il box Asia.
  - Se le 3 barre a 5 minuti successive chiudono tutte oltre il box (**accettazione**): ingresso nella direzione della rottura al close della terza barra, stop a metà box, target 2R.
  - Se invece una di quelle 3 barre chiude di nuovo dentro il box (**riassorbimento**): ingresso in direzione opposta al close di quella barra, stop all'estremo della rottura, target il lato opposto del box.
  - Variante HTF: come sopra.
- **H8c — Sweep di un POI a NY e inversione** (POI = high/low della sessione di Londra 02:00–08:29).
  - Evento: fra le 09:30 e le 10:59 il prezzo supera l'high (o il low) di Londra, poi una barra a 5 minuti chiude di nuovo dentro.
  - Ingresso: in direzione opposta. Stop all'estremo dello sweep, target 2R.
  - Variante HTF: come sopra.
  - Copre anche lo "spring" e l'"upthrust" di Wyckoff e la *failed auction* agli estremi.
- **H8d — IFVG (Inverse Fair Value Gap) nella killzone di NY.**
  - Evento: un FVG a 5 minuti (definizione di T4) formato dopo le 08:30 viene **invalidato**, cioè una barra a 5 minuti chiude completamente oltre il gap dalla parte opposta.
  - Ingresso: al primo ritorno al bordo del gap invalidato, nella direzione dell'invalidazione, entro le 11:30.
  - Stop: oltre il lato opposto del gap. Target: 2R.
- **H8e — Order block, retest dopo uno spostamento.**
  - Evento: fra le 08:30 e le 10:59 una barra a 5 minuti con range ≥ 2× la media delle 20 barre a 5 minuti precedenti e corpo ≥ 70% del range (**displacement**). L'order block è l'ultima barra a 5 minuti di colore opposto prima del displacement.
  - Ingresso: al primo ritorno nell'order block entro le 12:00, nella direzione del displacement.
  - Stop: oltre l'order block. Target: 2R.
  - Il breaker block è la variante dell'order block invalidato: non si testa a parte, per contenere il numero di test.

## 3. Criteri
**In-sample.** Un test sopravvive solo se valgono TUTTE queste condizioni:
1. t di Newey-West (5 lag) **> 3** sul P&L giornaliero netto (0 nei giorni senza trade);
2. p corretto con Holm sui 10 test < 0,05;
3. media > 0 con stress 2×;
4. almeno 2/3 degli anni positivi;
5. almeno 150 trade.

**Hold-out.** Solo per i sopravvissuti: t > 2 e media > 0 con stress 2×.

**Combinazioni.** Solo se **almeno due** ipotesi sopravvivono si testa la loro combinazione. Lo si fa con una nuova pre-registrazione, sull'hold-out non ancora usato da nessuna delle due.

## 4. Fuori dalla famiglia (motivato)
- **Macro, COT, report delle banche, dichiarazioni:** sono informazioni settimanali o a evento, e servono come **filtri**, non come segnali intraday. Si testeranno come filtro pre-registrato sulle sole ipotesi sopravvissute, per esempio escludendo i giorni con news ad alto impatto o usando il segno del posizionamento COT dei non-commercial.
- **Supply/demand:** coincide con l'order block (H8e) e con i livelli già testati in T2.
- **Multi-timeframe:** è incorporato come filtro HTF in tutte le ipotesi.

## 5. Diario
Ogni trade va in `journal.sqlite` (strategia `T8_<ipotesi>`), con screenshot che mostrano i box di sessione Asia/Londra/NY, i livelli e la presa di liquidità, MFE/MAE ed etichette di contesto. Serve anche per la ricerca dei trade simili.
