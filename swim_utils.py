from statistics import mean


FOLDER = "swimdata/"


def convert2hundreths(timestring):
    """Given a string which represents a time, this function converts the string
    to a number (int) representing the string's hundredths of seconds value, which is
    returned.
    """
    if ":" in timestring:
        mins, rest = timestring.split(":")
        secs, hundredths = rest.split(".")
    else:
        mins = 0
        secs, hundredths = timestring.split(".")

    return int(hundredths) + (int(secs) * 100) + ((int(mins) * 60) * 100) 


def build_time_string(num_time):
    """ """
    secs, hundredths = str(round(num_time / 100, 2)).split(".")
    mins = int(secs) // 60
    seconds = int(secs) - mins*60
    return f"{mins}:{seconds}.{hundredths}"  


def get_swimmers_data(filename):
    """ """
    name, age, distance, stroke = filename.removesuffix(".txt").split("-")
    with open(FOLDER + filename) as fh:
        data = fh.read()    
    times = data.strip().split(",")
    converts = []  # empty list
    for t in times:
        converts.append(convert2hundreths(t))
    average = build_time_string(mean(converts))

    return name, age, distance, stroke, times, converts, average




