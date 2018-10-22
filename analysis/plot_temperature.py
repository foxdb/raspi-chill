import matplotlib.pyplot as plt
import csv
from datetime import datetime, timestamp

x = []
y = []

# datetime.strptime('20181022_12-18-17', '%Y%m%d_%H-%M-%S')

with open('/home/ben/perso/temp.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

plt.plot(x, y, label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()
