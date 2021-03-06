ui_string = """
#:import Factory kivy.factory.Factory
<Menu@FloatLayout>:
    FloatLayout:
        id: layout
        size: root.size
        Button:
            size_hint: (0.16, 0.06)
            pos_hint: {"x": 0.5, "y": 0.9}
            text: "Test"
            color: 0, 0, 0, 1
            font_size: 16
            on_release: Factory.Menu.run()
        Button:
            size_hint: (0.16, 0.06)
            pos_hint: {"x": 0.3, "y": 0.9}
            text: "Options"
            color: 0, 0, 0, 1
            font_size: 16
            on_release: Factory.OptionsPopup().open()

<OptionsPopup@ModalView>:
    size_hint: (0.7, 0.7)
    auto_dismiss: False
    title: "Options"
    FloatLayout:
        Label:
            size_hint: (0.2, 0.13)
            pos_hint: {"x": 0.05, "y": 0.75}
            text: "Arguments: "
            color: 0, 0, 0, 1
            font_size: 20
        TextInput:
            id: args_input
            size_hint: (0.6, 0.2)
            pos_hint: {"x": 0.3, "y": 0.75}
        Button:
            size_hint: (0.4, 0.1)
            pos_hint: {"x": 0.0725, "y": 0.05}
            text: "Save and Close"
            on_release: root.save_options()
        Button:
            size_hint: (0.4, 0.1)
            pos_hint: {"x": 0.525, "y": 0.05}
            text: "Close Without Saving"
            on_release: root.dismiss()

<AddPopup@ModalView>:
    size_hint: (0.7, 0.7)
    auto_dismiss: False
    title: "Add a Login"
    FloatLayout:
        Label:
            size_hint: (0.2, 0.13)
            pos_hint: {"x": 0.05, "y": 0.8}
            text: "Website: "
            color: 0, 0, 0, 1
            font_size: 20
        TextInput:
            id: website_input
            size_hint: (0.6, 0.13)
            pos_hint: {"x": 0.3, "y": 0.8}
        Label:
            size_hint: (0.2, 0.13)
            pos_hint: {"x": 0.05, "y": 0.65}
            text: "Username: "
            color: 0, 0, 0, 1
            font_size: 20
        TextInput:
            id: user_input
            size_hint: (0.6, 0.07)
            pos_hint: {"x": 0.3, "y": 0.675}
        Label:
            size_hint: (0.2, 0.13)
            pos_hint: {"x": 0.05, "y": 0.525}
            text: "Password: "
            color: 0, 0, 0, 1
            font_size: 20
        TextInput:
            id: password_input
            password: True
            size_hint: (0.6, 0.07)
            pos_hint: {"x": 0.3, "y": 0.55}
        Button:
            size_hint: (0.4, 0.1)
            pos_hint: {"x": 0.0725, "y": 0.05}
            text: "Save and Close"
            on_release: root.save_input()
        Button:
            size_hint: (0.4, 0.1)
            pos_hint: {"x": 0.525, "y": 0.05}
            text: "Close Without Saving"
            on_release: root.dismiss()

<ModifyPopup@ModalView>:
    size_hint: (0.7, 0.7)
    auto_dismiss: False
    title: "Modify a Login"
    FloatLayout:
        Label:
            size_hint: (0.2, 0.13)
            pos_hint: {"x": 0.05, "y": 0.8}
            text: "Website: "
            color: 0, 0, 0, 1
            font_size: 20
        TextInput:
            id: website_input
            size_hint: (0.6, 0.13)
            pos_hint: {"x": 0.3, "y": 0.8}
        Label:
            size_hint: (0.2, 0.13)
            pos_hint: {"x": 0.05, "y": 0.65}
            text: "Username: "
            color: 0, 0, 0, 1
            font_size: 20
        TextInput:
            id: user_input
            size_hint: (0.6, 0.07)
            pos_hint: {"x": 0.3, "y": 0.675}
        Label:
            size_hint: (0.2, 0.13)
            pos_hint: {"x": 0.05, "y": 0.525}
            text: "Password: "
            color: 0, 0, 0, 1
            font_size: 20
        TextInput:
            id: password_input
            password: True
            size_hint: (0.6, 0.07)
            pos_hint: {"x": 0.3, "y": 0.55}
        Button:
            size_hint: (0.4, 0.1)
            pos_hint: {"x": 0.0725, "y": 0.05}
            text: "Save and Close"
            on_release: root.save_input()
        Button:
            size_hint: (0.4, 0.1)
            pos_hint: {"x": 0.525, "y": 0.05}
            text: "Close Without Saving"
            on_release: root.dismiss()

<DeletePopup@ModalView>:
    size_hint: (0.4, 0.4)
    auto_dismiss: False
    title: "Confirm Delete"

    FloatLayout:
        Label:
            size_hint: (0.6, 0.6)
            pos_hint: {"x": 0.2, "y": 0.35}
            markup: True
            text: "[b]Are you sure you\\n want to delete\\n this login?[/b]"
            color: 0, 0, 0, 1
            font_size: 36
        Button:
            size_hint: (0.4, 0.15)
            pos_hint: {"x": 0.0725, "y": 0.05}
            text: "Yes"
            on_release: root.delete_info_btn()
        Button:
            size_hint: (0.4, 0.15)
            pos_hint: {"x": 0.525, "y": 0.05}
            text: "No"
            on_release: root.dismiss()
"""
