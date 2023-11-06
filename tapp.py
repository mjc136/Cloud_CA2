from textual import on
from textual.app import App
from textual.widgets import Header, Select


import os
import webbrowser

import swim_utils


class SelectApp(App):
    def get_swimmer_names(self):
        """Return the unique set of swimmer names."""
        self.files = os.listdir(swim_utils.FOLDER)
        self.files.remove(".DS_Store")
        self.names = set()
        for swimmer in self.files:
            self.names.add(swim_utils.get_swimmers_data(swimmer)[0])

    def compose(self):
        """From Textual: set-up UI."""
        yield Header()
        self.get_swimmer_names()
        self.s1 = Select(options=[(name, name) for name in sorted(self.names)])
        yield self.s1
        self.s2 = Select(options=[(None, None)])
        yield self.s2

    def get_event(self, filename):
        """Given a filename, return the swimming event name."""
        filename = filename.removesuffix(".txt")
        return filename.split("-")[2] + " " + filename.split("-")[3]

    def get_swimmers_events(self, name):
        """Given a swimmer's name, assign their swimming events data to 'self.events'."""
        self.events = (
            (self.get_event(file), file) for file in self.files if file.startswith(name)
        )

    @on(Select.Changed)  # When a drop-down box is changed...
    def select_changed(self, message):
        """Do the right thing (based on the Select drop-down box sending the message)."""
        if message.control == self.s1:
            self.get_swimmers_events(str(message.value))
            self.s2.set_options((name, file) for name, file in self.events)
        else:
            # The assumption here is the second drop-down box (s2) has changed.
            which_html = swim_utils.produce_bar_chart(message.value)
            webbrowser.open("file://" + os.path.realpath(which_html))


if __name__ == "__main__":
    app = SelectApp()
    app.run()
