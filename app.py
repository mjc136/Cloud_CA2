from flask import Flask, render_template, request  # from module import Class.


import os 

import hfpy_utils # created by Paul Barry
import swim_utils # created by Paul Barry
import my_utils

FOLDER = r"swimdata/"

app = Flask(__name__)


@app.get("/")
@app.get("/getswimmers")
def get_swimmers_names():
    NAMES = my_utils.getNames(FOLDER)
    SORTED_NAMES = sorted(NAMES)
    return render_template(
        "select.html",
        title = "Select a swimmer to chart",
        data = SORTED_NAMES,
    )

@app.post("/displayevents")
def list_swimmer_events(): # get all events from a swimmer
    swimmers_event = set()
    for filename in os.listdir(FOLDER):
        result = swim_utils.get_swimmers_data(filename)
        event = result[2] + " " + result[3]
        #if name in filename:
        swimmers_event.add(event)
    return render_template(
        "select.html",
        title="Select a swimmers event to chart",
        data = swimmers_event,
    )
    

@app.get("/chart")
def display_chart():
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data("Darius-13-100m-Fly.txt")

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts ]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )






if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
