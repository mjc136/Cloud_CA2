import os
import webbrowser
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import *
from textual.events import *
from textual.widgets.option_list import *
from textual.screen import *

from swim_utils import *; """created by Paul Barry"""
from hfpy_utils import *; """created by Paul Barry"""
from my_utils import *

FOLDER = r"swimdata/"

NAMES = getNames(FOLDER)
SORTED_NAMES = sorted(NAMES)

optionlist = OptionList()

class ExitScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Would you like to exit?")
        yield Button("Yes", id="Exit", variant="success")
        yield Button("No", id="Continue", variant="error")

    @on(Button.Pressed, "#Exit")
    def button_pressed_Yes(self) -> None:
        """Event handler called when a button is pressed."""
        self.app.exit()

    @on(Button.Pressed, "#Continue")
    def button_pressed_No(self) -> None:
        """Event handler called when a button is pressed."""
        self.app.pop_screen()

 
class SwimmerApp(App):
    """Main application."""

    CSS_PATH = "Swimmers.tcss"

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Select([(name, name) for name in SORTED_NAMES])
        yield Footer()
        self.install_screen(ExitScreen(), "start")

    
    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if event.value is not None:
            """Handle the select changed event."""
            self.title = str(event.value)
            self.swimmer_name = event.value
            optionlist.clear_options()
            self.show_swimmer_events()
    
            

    def show_swimmer_events(self):
        """Create option list for events."""
        swimmer_events_list = list_swimmer_events(FOLDER, self.swimmer_name)
        for i in range(len(swimmer_events_list)):
            optionlist.add_option(Option(str(swimmer_events_list[i])))
        self.mount(optionlist) 

       
    @on(OptionList.OptionSelected)
    def select_event(self, event:OptionList.OptionSelected) -> None:
        index = event.option_index
        self.swimmer_event = optionlist.get_option_at_index(index).prompt
        html_content = self.create_html()
        with open(self.swimmer_name + ".html", "w") as df:
            print(html_content, file=df)  
            webbrowser.open_new_tab(self.swimmer_name + ".html")
        self.push_screen(ExitScreen())
        
            
    def get_swimmer_file(self):
        """Get swimmer data."""
        for filename in os.listdir(FOLDER):
            result = get_swimmers_data(filename)
            if self.swimmer_name in result and self.swimmer_event.split()[0] in result[2] and self.swimmer_event.split()[1] in result[3]:
                return result

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark 


    def create_html(self) -> None:
        """Create the HTML file."""
        """inspired from BarChart.ipynb created by Paul Barry"""

        data = self.get_swimmer_file()
        name, age, distance, stroke, times, values, average = data 
        title = f"{name} (Under {age}) {distance} - {stroke}"

        converts = []
        for n in values:
            converts.append(convert2range(n, 0, max(values)+50, 0, 400))

        times.reverse()
        converts.reverse()

        body = ""
        for t, c in zip(times, converts):
            svg = f""" 
                        <svg height="30" width="400">
                                <rect height="30" width="{c}" style="fill:rgb(0,0,255);" />
                        </svg>{t}<br />
                    """
            body = body + svg

        header = f"""
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>
                            {title}
                        </title>
                    </head>
                    <body>
                        <h3>{title}</h3>
                """

        footer = f""" 
                        <p>Average: {average}</p>
                    </body>
                </html>
                """
        
        html = header + body + footer
        return html
            

if __name__ == "__main__":
    app = SwimmerApp()
    app.run()