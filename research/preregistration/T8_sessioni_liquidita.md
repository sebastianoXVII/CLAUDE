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

## Emendamento 1 — chiarimenti di implementazione registrati PRIMA di qualsiasi dato
- **Barre a 5 minuti:** allineate alla mezzanotte ET; l'etichetta è l'inizio della barra; la barra "chiude" all'etichetta + 5 minuti; l'ingresso avviene al suo close e la simulazione parte dalla barra a 1 minuto successiva.
- **H8a:** vale anche lo sweep con wick, cioè la barra dello sweep che chiude già dentro il range. "Entro 30 minuti" significa che la barra che chiude dentro inizia al massimo 25 minuti dopo l'inizio della barra dello sweep. Lo stop è l'estremo fra la barra dello sweep e quella d'ingresso. Conta solo il primo sweep; se il rientro non avviene in tempo, quel giorno non si opera.
- **H8b:** se dopo la rottura non ci sono 3 barre a 5 minuti disponibili nella finestra, non si opera. Lo stop del riassorbimento è l'estremo fra la barra di rottura e quella di rientro.
- **H8c:** lo sweep va cercato fra le 09:30 e le 10:55 (inizio barra), e il rientro può avvenire nella stessa barra o in una successiva della finestra.
- **H8d:** si usa il **primo FVG** (fra quelli formati dalle 08:30, su 3 barre a 5 minuti contigue) **che viene invalidato**. Ingresso al tocco del bordo dalle 11:29 in poi non ammesso; nella barra d'ingresso si controlla solo lo stop.
- **H8e:** conta solo il **primo displacement** della finestra (servono 20 barre a 5 minuti precedenti per la media). Se l'order block non viene ritestato entro le 11:59, quel giorno non si opera.
- **Tutte:** rischio nullo significa nessun trade.

## Emendamento 2 — 2026-11-10, da code review, registrato PRIMA di qualsiasi dato 24 ore
1. **H8d, scelta causale del FVG.** Si calcola il momento d'invalidazione di ogni FVG la cui barra 1 inizia fra le 08:30 e le 10:59 (killzone di NY). Si usa il FVG **invalidato per primo nel tempo**; a parità, quello formato prima. Ingresso al primo tocco del bordo entro la barra delle **11:28** compresa, cioè non dalle 11:29 in poi. Se il bordo non viene toccato, quel giorno **non si opera**: non si passa a un altro FVG.
2. **Prezzo già fuori dal range all'inizio della finestra.** Lo sweep (H8a, H8c) e la rottura (H8b) valgono solo se il close della barra a 1 minuto **precedente l'apertura della finestra** sta dentro il range di riferimento:
   - H8a: la barra delle 01:59, rispetto all'Asia range;
   - H8b: la barra delle 02:59, rispetto al box Asia;
   - H8c: la barra delle 09:29, rispetto al range di Londra.

   Altrimenti quel giorno non si opera. Uno sweep, per definizione, parte da dentro il range.
3. **H8a.** Il rientro si cerca fino a 25 minuti dopo l'inizio della barra dello sweep, anche oltre le 04:55. Lo sweep stesso deve iniziare entro le 04:55.
4. **H8b.**
   - L'accettazione richiede che le 3 barre successive chiudano tutte **oltre lo stesso lato** della rottura.
   - Se una delle 3 barre chiude oltre il lato **opposto** del box (cioè attraversa tutto il box), quel giorno non si opera.
   - Le 3 barre devono essere contigue, da 5 minuti l'una dopo l'altra; se non lo sono, quel giorno non si opera.
5. **H8e.** Conta solo il primo displacement. Se non c'è un order block, cioè nessuna barra di colore opposto prima del displacement, quel giorno non si opera.
6. **Costi.**
   - Costo **decisionale**: NQ 0,45 punti, con stress 2× > 0. Deve inoltre restare > 0 con il costo MNQ di 0,85, come in T7.
   - Il costo CFD di 2 punti si riporta a parte, non è decisionale.
   - ES (SPX500) è solo riportato, con costo 0,5 punti, e la sua assenza nei dati non blocca il test.
7. **Note dichiarate:**
   - con il filtro HTF si scarta il primo segnale del giorno se va contro il trend, senza cercarne un altro allineato;
   - a parità fra close e media il trend vale −1;
   - l'inclusione di un giorno richiede la barra delle 15:59 e almeno 300 barre RTH, cioè una selezione sulla qualità dei dati, indipendente dai rendimenti;
   - gli screenshot mostrano anche il box NY 09:30–15:59.

## Emendamento 3 — 2026-11-10, cambio di fonte registrato PRIMA di qualsiasi dato 24 ore
- **Dati:** si usa Dukascopy `USATECHIDXUSD` (CFD sul Nasdaq-100, candele BID a 1 minuto, 24 ore, tick volume) al posto di OANDA `NAS100_USD`, dal primo giorno disponibile. ES (`USA500IDXUSD`) è solo riportato, se scaricato.
- **Campioni:**
  - In-sample: dall'inizio al 2023-12-31.
  - Hold-out: dal 2024-01-01.
  - Criteri invariati.
- **Costi:**
  - Costo decisionale invariato: NQ 0,45 punti, più il controllo con MNQ 0,85.
  - Lo spread CFD Dukascopy è implicito nei prezzi BID, che stanno sotto il mid di circa mezzo spread. Su un round trip con ingresso e uscita al BID si compensa, ed è dichiarato come approssimazione.

## Emendamento 4 — 2026-11-10, cambio di fonte registrato PRIMA di qualsiasi dato 24 ore
- **Motivo:** Dukascopy limita il download al punto di renderlo impraticabile (dopo oltre un'ora nessun anno completato). HistData invece blocca lo scaricamento automatico dal suo sito, che non si aggira.
- **Fonte:** HistData `NSXUSD` (CFD sul Nasdaq-100, barre a 1 minuto, 24 ore). Si usa la copia pubblica che l'autore del progetto `philipperemy/FX-1-Minute-Data` ha messo su Google Drive, condivisa apposta per essere scaricata. ES è sostituito da `SPXUSD`, solo riportato.
- **Fuso orario:** HistData usa l'EST fisso (UTC−5) **senza ora legale**, con il timestamp all'inizio della barra. Le barre si convertono in UTC e poi in America/New_York, per far restare valide le finestre ET di T8.
- **Volume:** è assente o nullo, e T8 non lo usa. Il resto (regole, costi, criteri) è invariato.
- **Campioni:**
  - in-sample: dal primo giorno disponibile (atteso fine 2010) al 2023-12-31;
  - hold-out: dal 2024-01-01 alla fine dei dati disponibili quando si esegue l'hold-out.

  L'hold-out è più corto del previsto (circa 1 anno). Lo si dichiara prima: se l'in-sample promuove qualcosa, l'hold-out 2025–26 arriverà dal forward test o da un'altra fonte.
- **Prezzi:** sono quotazioni del broker che fornisce i dati a HistData, verosimilmente BID come per Dukascopy. Lo spread si compensa sul round trip, ed è dichiarato come approssimazione.
