from network import Network
from time import sleep

#TODO przeanalizuj co dzieje się w pliku network.py
# wykonywane działania są analogiczne do tych wykonywanych na serwerze, na początku łączymy się z owym serwerem,
# a następnie przeprowadzamy wymianę danych jednocześnie odbierając przychodzące i wysyłając lokalne
# Utwórz obiekt Network jako n i odbierz początkowe dane wysłane z serwera (zapisz je w zmiennej data)
n = Network()
data = n.getP()

data = data.split(',')

player = int(data[2])
numbers = [data[0], data[1]]
counter = int(data[player])
print(counter)

while counter > 0 and counter < 1000:
    #TODO utwórz dwie instrukcje warunkowe określające jak dany klient będzie się zachowywał ze swoimi lokalnymi danymi
    # Niech gracz o indeksie 0 zwiększa swoją liczbę (counter) a gracz o indeksie 1 ją zmniejsza
    if player == 0:
        counter += 1
    elif player == 1:
        counter -= 1

    #TODO po przeprowadzeniu lokalnych operacji wyślij na serwer aktualizację swojej liczby, a odpowiedź zapisz
    # w zmiennej otherCounter
    otherCounter = n.send(str(counter))
    sleep(0.5)

    print(str(counter) + ' | ' + otherCounter)
