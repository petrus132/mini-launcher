import random
import time

liczba = random.randint(1, 50)
gamewin = False
proby = 10
calkowite_proby = proby

while proby > 0:
    zgadywana = int(input("Zgadnij liczbę >>> "))
    if zgadywana == liczba:
        gamewin = True
        break
    elif zgadywana > liczba:
        print("Liczba jest mniejsza")
        proby -= 1
    else:
        print("Liczba jest większa")
        proby -= 1

if gamewin:
    print(
        "Zgadłaś, liczba =",
        liczba,
        "ilość prób:",
        calkowite_proby - proby + 1
    )
else:
    print("Przegrałaś")

time.sleep(5)
