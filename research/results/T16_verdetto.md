# T16: Numeri tondi (Osler) su EURUSD, GBPUSD, XAUUSD, verdetto

**Esito: MORTO, 0 test su 12 sopravvissuti.** **Data:** 2026-11-12.

L'in-sample 2010–2019 è stato eseguito una sola volta (lock `T16_insample.started`), in circa 100 secondi. L'hold-out 2020–2024 **non è stato calcolato** e resta intatto.

## Test pre-registrati (in-sample, al netto dei costi)
Gross per trade: pip per il forex, $/oz per l'oro.

| Test | Trade | t NW | Gross medio per trade | Costo per trade | Anni positivi |
|---|---|---|---|---|---|
| EURUSD 00 rimbalzo | 3.800 | −5,76 | **−1,1 pip** | 1,0 pip | 0/10 |
| EURUSD 00 superamento | 3.303 | −2,29 | +0,1 pip | 1,0 pip | 3/10 |
| EURUSD 50 rimbalzo | 3.791 | −2,21 | +0,1 pip | 1,0 pip | 2/10 |
| EURUSD 50 superamento | 3.226 | −3,09 | −0,4 pip | 1,0 pip | 1/10 |
| GBPUSD 00 rimbalzo | 4.925 | −5,62 | **−0,6 pip** | 1,3 pip | 0/10 |
| GBPUSD 00 superamento | 4.189 | −3,39 | +0,1 pip | 1,3 pip | 0/10 |
| GBPUSD 50 rimbalzo | 5.003 | −2,91 | +0,3 pip | 1,3 pip | 3/10 |
| GBPUSD 50 superamento | 4.253 | −4,07 | −0,4 pip | 1,3 pip | 2/10 |
| Oro 50 $ rimbalzo | 1.370 | −4,96 | **−0,30 $** | 0,35 $ | 0/10 |
| Oro 50 $ superamento | 1.141 | −1,06 | +0,19 $ | 0,35 $ | 3/10 |
| Oro 10 $ rimbalzo | 5.718 | −6,31 | −0,01 $ | 0,35 $ | 0/10 |
| Oro 10 $ superamento | 4.691 | −4,59 | +0,05 $ | 0,35 $ | 1/10 |

Tutti i t sono negativi e tutti i p di Holm valgono 1. Nessun test ha un gross medio superiore al costo.

## Certificazione del livello: tondo contro controllo (descrittiva, non decisionale)
Gross medio per trade sui livelli di controllo C (x,xx25 e x,xx75; per l'oro, multipli di 5 $ non di 10 $), con il t di Welch della differenza A − C:

| | Rimbalzo: A / C | Welch A−C | Superamento: A / C | Welch A−C |
|---|---|---|---|---|
| EURUSD | −1,1 / +0,7 pip | **−3,8** | +0,1 / −0,8 pip | +1,6 |
| GBPUSD | −0,6 / +1,2 pip | **−4,1** | +0,1 / −1,0 pip | +2,2 |
| Oro | −0,30 / +0,11 $ | **−2,6** | +0,19 / −0,17 $ | +1,9 |

**Cosa dicono questi dati:**
- **I numeri tondi sono davvero diversi dai livelli neutri,** in modo statisticamente netto, ma al contrario della credenza retail. Sui "00" il prezzo **non rimbalza**: lo **attraversa** più spesso che sui livelli neutri. Il superamento di un numero tondo prosegue un po' più che su un livello neutro, coerente con le "cascate di stop" di Osler.
- **L'effetto è minuscolo:** frazioni di pip (pochi centesimi sull'oro), sempre sotto lo spread. **Esiste, ma non è sfruttabile** con costi retail.
- **Cautele:**
  - il t di Welch tratta i trade come indipendenti, ma trade dello stesso giorno possono essere correlati;
  - i confronti sono 6, senza correzione;
  - è una diagnostica, non un test pre-registrato con soglia.
- **Lo scostamento positivo sui livelli di controllo** (rimbalzo da +0,7 a +1,2 pip lordi) è una generica inversione di breve periodo dopo un movimento di 20 pip. È un'osservazione, non un'ipotesi testata. Anche così resta sotto il costo per GBPUSD e appena sopra per EURUSD (0,7 pip contro 1,0 di costo: comunque netto negativo). Non si apre un nuovo test su questo, perché sarebbe un'ipotesi generata dagli stessi dati.

## Interpretazioni dichiarate
- **Barra che arma e tocca insieme** (finding minore della revisione finale). L'evento richiede un armamento in una barra precedente più recente dell'ultimo tocco. La barra che arma e tocca insieme blocca anche l'evento della barra successiva. È la lettura letterale di spec e piano, fissata prima dei dati. Sui random walk realistici la differenza è nulla: servono barre M1 di ampiezza ≥ 20 pip (3 $ sull'oro).
- **Lettura delle barre successive al 2019.** L'in-sample legge da disco anche le barre post-2019, che però vengono scartate prima di qualunque calcolo, come in T15.

## Processo
- Pre-registrazione `research/preregistration/T16_numeri_tondi.md`, prima dei dati.
- Codice in TDD: 244 test.
- Revisione finale indipendente: nessun problema critico o importante. `level_events` è stato verificato contro una macchina a stati indipendente su 9.764 eventi sintetici, con 0 differenze.

## Conclusione
Un livello "tondo" non è un punto di inversione sfruttabile. È statisticamente diverso da un livello neutro, ma l'effetto, che va per giunta nel verso dell'attraversamento e non del rimbalzo, vale frazioni di pip ed è sotto i costi.
