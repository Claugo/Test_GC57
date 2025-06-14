# GC57 — Materiale sperimentale di supporto

Questo repository contiene i programmi di supporto sperimentale al saggio sul metodo **GC57** sviluppato da Claudio Govi

GC57 propone un approccio logico-sperimentale alla fattorizzazione istantanea di semiprimi e alla derivazione di chiavi crittografiche, basato su proprietà numeriche non convenzionali.

## Finalità del materiale

I due programmi inclusi permettono di riprodurre gli esperimenti descritti nel saggio, eseguendo la fattorizzazione di semiprimi generati artificialmente tramite due diverse tipologie di chiave:

- **Chiave B-1**
- **Chiave logaritmica**

Questi strumenti hanno esclusivamente finalità sperimentali e di verifica teorica.

## Contenuto del repository
- `Test_GC57_B-1.py` — Programma sperimentale per testare la chiave B-1.
- `Test_GC57_log.py` — Programma sperimentale per testare la chiave logaritmica.
- 'Test_interfaccia_B-1.py -- Aggiunto questo programma per eseguire il test con la chiave B-1 con una interfaccia grafica
- `README.md` — Questo documento.

---

## Requisiti per l’esecuzione

- Python 3.10 o superiore
- Libreria `gmpy2`

Installazione dipendenze:

```bash
pip install gmpy2
