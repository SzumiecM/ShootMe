from ZADANKOnetwork import Network
from time import sleep

n = Network()
data = n.getP()
print(data)
data = data.split(',')

player = int(data[2])
numbers = [data[0], data[1]]
counter = int(data[player])
print(counter)

while counter > 0 and counter < 1000:
    if player == 0:
        counter += 1
    elif player == 1:
        counter -= 1

    otherCounter = n.send(str(counter))
    sleep(0.5)

    print(str(counter) + ' | ' + otherCounter)
