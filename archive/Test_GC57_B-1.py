# **** GC57 test contenitore chiave Q-1 (B-1 sul saggio)
# **** Per funzionare questo programma ha bisogno di installare la libreria gmpy2 "pip install gmpy2"
from math import gcd,log
from random import randint, seed
import time
from gmpy2 import next_prime as nprime
from gmpy2 import is_prime as isprime

# **** imposto il seme di ricerca random
T=int(time.time())
seed(T)

# **** definisco il ciclo di ripetizione per entrambi i cicli inseriti
rip=1
# *------------------------------------------------------------------------------------------------
# **** imposta due numeri a caso: possono esssere numeri primi, pari, dispari, digitati a mano, ecc.
#      Mantenere i numeri distanti tra loro in cifre se non si impongono degli esponenti. In ogni caso
#      qs deve essere superiore in cifre rispetto a ps. Modificare e aumentare il valore dei numeri
#      nel caso il campo risultasse piccolo
ps = 546332996785237687623412
qs = 2987486298763287623867672576352376569
# *------------------------------------------------------------------------------------------------
# **** imposto gli esponenti. Se gli esponenti vengono posti a 1, il programma utilizzarà i numeri
# **** inseriti sopra così come sono. Se gli esponenti sono superiori a 1, il programma utilizzerà i numeri elevati alla potenza inserita
# **** Gli esponenti servono solo ad aumentare i numeri testati per evitare di scrivere un numero molto grande per intero
p=ps**1
q=qs**1
# *------------------------------------------------------------------------------------------------
# **** Calcolo la chiave e l'intervallo
print("---------------------------------------------------------------------")
chiave = q - 1
print("chiave Q-1 =", chiave)
campo = (chiave // (((p + 1) * (q + 1)) % chiave)) * 2
print("campo =", campo, " = ", " 2**", int(log(campo, 2)))
# *------------------------------------------------------------------------------------------------
# **** Variabili progressione: Questo identificherà il contenitore e produrrà un confronto tra
#      contenitore selezionato per la scelta dei due numeri primi e contenitore identificato nella ricerca della fattorizzazione
#      La ripetizione si svolge in base al parametro rip posto all'inizio. In caso di rip=1, tutto verrà testato
#      nel contenitore 0
v1, v2 = 0, 1

# *------------------------------------------------------------------------------------------------
# **** identifico i numeri primi partendo dal contenitore zero
#      Nota importante: Se i due contenitori v1 e v2 non risultano uguali, l'operazione di fattorizzazione cercherà di
#      portarla a buon fine cercando negli altri contenitori. Questa incongruenza sui contenitori si presenta spesso sui
#      numeri piccoli. Aumentate gli esponenti anche in modo consistente per testare i contenitori su numeri grandi
#      L'esempio di default così come impostato mantiene i contenitori allineati
for i in range(rip):
    trovato = False
    p_campo = randint(campo*v1, campo*v2)
    q_campo = randint(campo*v1, campo*v2)
    primo1 = nprime(p + p_campo)
    primo2=  nprime(q + q_campo)
    n=primo1*primo2
    for k in range(rip):
        r=gcd(n,(n%chiave)+chiave*k)
        if r!=1:
            print("---------------------------------------------------------------------")
            print()
            print("Test divisore 1: ", isprime(r))
            print("Test divisore 2: ", isprime(n//r))
            print("divisore       : ", r)
            print("contenitore k  : ",k)
            print("contenitore v1 : ",v1)
            print()
            print("Semiprimo analizzato: ",n)
            print()
            trovato = True
            break
    if not trovato:
        print("attenzione: nessun divisore trovato per il contenitore :",v1)
        break
    v1+=1
    v2+=1
