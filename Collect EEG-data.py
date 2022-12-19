# *******************  IMPORTING MODULES ********************
from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server
from timeit import default_timer as timer

# *********************  G L O B A L S *********************
alpha = beta = delta = theta = gamma = [-1, -1, -1, -1]
all_waves = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

ip = "0.0.0.0"
port = 5000

filePath = 'Blinks/no.csv'
filePath2 = 'Blinks/'

f = open(filePath, 'a+')
header = 'timestamp,A9,A7,A8,A10,B9,B7,B8,B10,D9,D7,D8,D10,T9,T7,T8,T10,G9,G7,G8,G10\n'

current_file = ''
current_event = 0
row = 0
count = 0

secs = 2
start = timer()
recording = False
record_many = True

rec_dict = {
    "1": 2,
    "no": 2,
}


# ****************** EEG-handlers ******************

def alpha_handler(address: str, *args):
    global alpha, beta, delta, theta, gamma

    if (len(args) == 5):
        for i in range(1, 5):
            all_waves[i - 1] = args[i]


def beta_handler(address: str, *args):
    global alpha, beta, delta, theta, gamma

    if (len(args) == 5):
        for i in range(1, 5):
            all_waves[i - 1 + 4] = args[i]


def delta_handler(address: str, *args):
    global alpha, beta, delta, theta, gamma

    if (len(args) == 5):
        for i in range(1, 5):
            all_waves[i - 1 + 8] = args[i]


def theta_handler(address: str, *args):
    global alpha, beta, delta, theta, gamma

    if (len(args) == 5):
        for i in range(1, 5):
            all_waves[i - 1 + 12] = args[i]


def gamma_handler(address: str, *args):
    global alpha, beta, delta, theta, gamma
    global record_many

    if (len(args) == 5):
        for i in range(1, 5):
            all_waves[i - 1 + 16] = args[i]

    if record_many == False:
        for i in range(0, 19):
            f.write(str(all_waves[i]) + ",")
        f.write(str(all_waves[19]))
        f.write("\n")
    else:
        show_event()


# ********* Showing one event at a time *********
def show_event():
    global current_event, current_file
    global start, end, secs, row, count

    end = timer()
    if (end - start) >= secs:
        start = timer()
        ev = list(rec_dict.items())[current_event][0]
        secs = list(rec_dict.items())[current_event][1]
        row = 0

        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%m-%d %H_%M_%S.%f")

        ev = list(rec_dict.items())[current_event][0]
        current_file = filePath2 + ev + '.' + timestampStr + '.csv'
        evf = open(current_file, 'a+')
        evf.write(header)

        print(f"Think:\t {ev}   \t\t{secs}  seconds")
        print(count)
        count = count + 1

        dict_length = len(rec_dict)
        if current_event < dict_length - 1:
            current_event += 1
        else:
            current_event = 0
    else:
        if current_file != '':
            evf = open(current_file, 'a+')

            evf.write(str(row) + ',')
            row += 1
            for i in range(0, 19):
                evf.write(str(all_waves[i]) + ",")
            evf.write(str(all_waves[19]))
            evf.write("\n")


def marker_handler(address: str, i):
    global recording, record_many, start, end

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    markerNum = address[-1]
    f.write(timestampStr + ",,,,/Marker/" + markerNum + "\n")
    start = timer()
    if (markerNum == "1"):
        recording = True
        print("Recording Started.")
    if (markerNum == "2"):
        f.close()
        server.shutdown()
        print("Recording Stopped.")

    if (markerNum == "3"):
        start = timer()

        for i in range(len(rec_dict)):
            ev = list(rec_dict.items())[i][0]
            evf = open(filePath2 + ev + '.csv', 'a+')
            evf.write(header)

        if record_many == False:
            record_many = True
            show_event()
        else:
            record_many = False


if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()

    dispatcher.map("/Marker/*", marker_handler)
    dispatcher.map("/muse/elements/delta_absolute", delta_handler, 0)
    dispatcher.map("/muse/elements/theta_absolute", theta_handler, 1)
    dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, 2)
    dispatcher.map("/muse/elements/beta_absolute", beta_handler, 3)
    dispatcher.map("/muse/elements/gamma_absolute", gamma_handler, 4)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on MUSE monitor at port " + str(port) + "\n")
    print()
    server.serve_forever()