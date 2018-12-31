from kivy.uix.modalview import ModalView
from kivy.uix.togglebutton import ToggleButton


class OptionsPopup(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        new_file = False
        options_file = ""
        try:
            options_file = open("options.dat", "r")
        except FileNotFoundError:
            new_file = True
        # TODO fix lazy try-except
        try:
            browser = int(options_file.readline())
        except EOFError:
            browser = -1
        index = -1
        for child in self.children[0].children:
            if browser == -1:
                break
            print("child:", child)
            if type(child) != ToggleButton:
                continue
            elif child.group == "browser_selection":
                index += 1
                if index == browser:
                    child.state = "down"
                    print("newchild:", child)
        if not new_file:
            self.ids.args_input.text = options_file.readline()[:-1]
        # self.ids.firefox_input.text = options_file.readline()[:-1]
        # self.ids.edge_input.text = options_file.readline()[:-1]
            options_file.close()

    def save_options(self):
        options_file = open("options.dat", "w")
        # TODO fix lazy try-except
        try:
            browser = str([index for index, button in enumerate(ToggleButton.get_widgets("browser_selection"))
                          if button.state == "down"][0])
        except:
            browser = str(-1)
        print("browser", browser)
        args = self.ids.args_input.text
        # firefox_args = self.ids.firefox_input.text
        # edge_args = self.ids.edge_input.text
        options_file.write(browser)
        options_file.write("\n")
        options_file.write(args)
        options_file.write("\n")
        # options_file.write(firefox_args)
        # options_file.write("\n")
        # options_file.write(edge_args)
        # options_file.write("\n")
        options_file.close()
        self.dismiss()
