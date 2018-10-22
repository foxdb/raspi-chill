import matplotlib.pyplot as plt
import csv
from datetime import datetime

x = []
y = []

DATE_FORMAT = '%Y%m%d_%H-%M-%S'

with open('./temperature.log', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    initial_date = datetime.strptime(next(reader)[0], DATE_FORMAT)
    initial_temp = float(next(reader)[1])

    x.append(0)
    y.append(initial_temp)

    for row in reader:
        timedelta = datetime.strptime(row[0], '%Y%m%d_%H-%M-%S') - initial_date
        x.append(timedelta.total_seconds() / 60 / 60)
        y.append(float(row[1]))

plt.plot(x, y, label='try 1 - 90 seconds cycles, 1 jug')
plt.ylim(0, 30)

# identify min and max with horizontal lines
# plt.axhline(y=min(y))
# plt.axhline(y=max(y))

ymax = max(y)
xposmax = y.index(ymax)
xmax = x[xposmax]

ymin = min(y)
xposmin = y.index(ymin)
xmin = x[xposmin]

plt.annotate('max ' + str(ymax), xy=(xmax, ymax), xytext=(xmax, ymax+2),
             arrowprops=dict(arrowstyle="->",
                             connectionstyle="arc3"),
             )

plt.annotate('min ' + str(ymin), xy=(xmin, ymin), xytext=(xmin, ymin-2),
             arrowprops=dict(arrowstyle="->",
                             connectionstyle="arc3"),
             )

# legends, labels
plt.xlabel('Time (h)')
plt.ylabel('Temperature (C)')
plt.title(
    'Fermenting chamber temperature\nStart date: ' + str(initial_date))
plt.legend()
plt.show()
