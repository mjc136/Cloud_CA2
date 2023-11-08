from flask import Flask, render_template, request, session  # from module import Class.


import os

import hfpy_utils  # created by Paul Barry
import swim_utils  # created by Paul Barry
import my_utils

FOLDER = r"swimdata/"

app = Flask(__name__)
app.secret_key = "SecretKey"


@app.get("/")
@app.get("/getswimmers")
def get_swimmers_names():
    NAMES = my_utils.getNames(FOLDER)  # List all names in the folder
    SORTED_NAMES = sorted(NAMES)  # sort names alphabetically

    return render_template(
        "selectSwimmer.html",
        title="Select a swimmer to chart",
        data=SORTED_NAMES,
    )


@app.post("/displayevents")
def list_swimmer_events():  # get all events from a swimmer
    session["SwimmerName"] = request.form["swimmer"]  # get result of select swimmer
    swimmers_event = set()

    for filename in os.listdir(FOLDER):
        result = swim_utils.get_swimmers_data(filename)
        event = result[2] + " " + result[3]  # split event and stroke

        if session["SwimmerName"] == result[0]:
            swimmers_event.add(event)

    return render_template(
        "selectEvent.html",
        title="Select a swimmers event to chart",
        data=swimmers_event,
    )


@app.post("/chart")
def display_chart():
    event = request.form["event"]  # get result of select event
    event = event.split(" ")
    event = event[0] + "-" + event[1]  # format event to match filename

    for filename in os.listdir(FOLDER):
        result = swim_utils.get_swimmers_data(filename)

        if (
            session["SwimmerName"] == result[0]
            and session["SwimmerName"] + "-"
            and event in filename
        ):
            (
                name,
                age,
                distance,
                stroke,
                the_times,
                converts,
                the_average,
            ) = swim_utils.get_swimmers_data(
                f"{session['SwimmerName']}-{result[1]}-{result[2]}-{result[3]}.txt"
            )

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
