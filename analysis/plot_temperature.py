import matplotlib.pyplot as plt
import csv
from datetime import datetime


DATE_FORMAT = '%Y%m%d_%H-%M-%S'


def add_plot(logFile, title):
    x = []
    y = []

    with open(logFile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        initial_date = datetime.strptime(next(reader)[0], DATE_FORMAT)
        initial_temp = float(next(reader)[1])

        x.append(0)
        y.append(initial_temp)

        for row in reader:
            timedelta = datetime.strptime(
                row[0], '%Y%m%d_%H-%M-%S') - initial_date
            x.append(timedelta.total_seconds() / 60 / 60)
            y.append(float(row[1]))

    plt.plot(x, y, label=title)
    plt.ylim(0, 30)

    ymax = max(y)
    xposmax = y.index(ymax)
    xmax = x[xposmax]

    ymin = min(y)
    xposmin = y.index(ymin)
    xmin = x[xposmin]

    plt.annotate('max ' + title + ' ' + str(ymax), xy=(xmax, ymax), xytext=(xmax, ymax+2),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3"),
                 )

    plt.annotate('min ' + title + ' ' + str(ymin), xy=(xmin, ymin), xytext=(xmin, ymin-2),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3"),
                 )


# plt.subplot(211)

# - poor insulation (main compartiment, top)
# - one frozen jug
# add_plot('data/temp_1.csv', 'try1')

# - glued more things, added duct tape
# - one not completely frozen jug
# add_plot('data/temperature.log', 'try2')

add_plot('data/temp_3.csv', 'try3')
add_plot('data/temperature.log', 'try4')
# legends, labels
plt.xlabel('Time (h)')
plt.ylabel('Temperature (C)')
plt.title('Fermenting chamber temperature')

# plt.subplot(212)
# add_plot('data/temperature.log', 'try2')

plt.legend()
plt.show()
