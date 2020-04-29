from network import Network
from time import sleep

n = Network()
data = n.getP().split(',')

player = int(data[3])
numbers = [data[0], data[1], data[2]]
counter = int(data[player])
print(counter)

while True:
    if player == 0:
        counter += 1
    elif player == 1:
        counter -= 1
    elif player == 2:
        counter += 2

    otherCounterss = n.send(str(counter)).split(',')
    x=[]
    for c in otherCounterss:
        if c != '':
            x.append(str(c))
    sleep(0.5)


    print(str(counter) + ' | ' + x[0] + ' | ' + x[1])
