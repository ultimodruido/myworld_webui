from browser import html, ajax, window

from ui.classes import Element
from ui.slider import Slider
from ui.buttons import Button

from .deps import server_address


jq = window.jQuery


class TrainCard(Element):
    def __init__(self, train_id, train_name, box_code=""):
        super().__init__(None, html.DIV, ['ui', 'card'])
        # self.card = Element(None, html.DIV, ['ui', 'card'])
        self.element.id = f"train_{train_id}"
        self.direction = "F"
        self.train_id = train_id

        # create image DIV
        tmp_el_1 = Element(None, html.DIV, ['image'])
        tmp_el_2 = Element(None, html.IMG, [])
        tmp_el_2.element.attrs['src'] = f"./data/{box_code}.jpg"

        tmp_el_1 <= tmp_el_2.element
        self <= tmp_el_1.element

        # content section
        tmp_el_1 = Element(None, html.DIV, ['content'])
        self <= tmp_el_1.element

        tmp_el_2 = Element(None, html.H2, ['ui', 'dividing', 'blue', 'header'])
        tmp_el_2.set_text(train_name)

        tmp_el_1 <= tmp_el_2.element

        # description section
        description_el = Element(None, html.DIV, ['description'])
        tmp_el_1 <= description_el.element

        # menu function with 4 buttons
        menu_el = Element(None, html.DIV, ['ui', 'four', 'item', 'secondary', 'menu'])
        description_el <= menu_el.element

        tmp_el_1 = Element(None, html.DIV, ['ui', 'item'])
        tmp_el_2 = Button(has_icon=True, button_class_attr=['ui', 'yellow', 'icon', 'big', 'button'],
                          icon_class_attr=['lightbulb', 'icon'])
        tmp_el_2.element.id = f"btn_{train_id}_light"
        tmp_el_2.set_clicked_callback(btn_function_clicked)
        tmp_el_2.refresh()
        tmp_el_1 <= tmp_el_2.element
        menu_el <= tmp_el_1.element

        tmp_el_1 = Element(None, html.DIV, ['ui', 'item'])
        tmp_el_2 = Button(has_icon=True, button_class_attr=['ui', 'olive', 'icon', 'big', 'button'],
                          icon_class_attr=['bullhorn', 'icon'])
        tmp_el_2.element.id = f"btn_{train_id}_horn"
        tmp_el_2.set_clicked_callback(btn_function_clicked)
        tmp_el_2.refresh()
        tmp_el_1 <= tmp_el_2.element
        menu_el <= tmp_el_1.element

        tmp_el_1 = Element(None, html.DIV, ['ui', 'item'])
        tmp_el_2 = Button(has_icon=True, button_class_attr=['ui', 'teal', 'icon', 'big', 'button'],
                          icon_class_attr=['volume', 'up', 'icon'])
        tmp_el_2.element.id = f"btn_{train_id}_sound1"
        tmp_el_2.set_clicked_callback(btn_function_clicked)
        tmp_el_2.set_text(' 1')
        tmp_el_1 <= tmp_el_2.element
        menu_el <= tmp_el_1.element

        tmp_el_1 = Element(None, html.DIV, ['ui', 'item'])
        tmp_el_2 = Button(has_icon=True, button_class_attr=['ui', 'teal', 'icon', 'big', 'button'],
                          icon_class_attr=['volume', 'up', 'icon'])
        tmp_el_2.element.id = f"btn_{train_id}_sound2"
        tmp_el_2.set_clicked_callback(btn_function_clicked)
        tmp_el_2.set_text(' 2')
        tmp_el_1 <= tmp_el_2.element
        menu_el <= tmp_el_1.element

        # speed control segments
        tmp_el_1 = Element(None, html.DIV, ['ui', 'horizontal', 'basic', 'segments'])
        # speed direction
        tmp_el_2 = Element(None, html.DIV, ['ui', 'center', 'align', 'basic', 'segment'])
        tmp_el_2 <= html.BR()
        tmp_el_2 <= html.BR()
        self.dir = Element(None, html.I, ['arrow', 'alternate', 'circle', 'up', 'grey', 'massive', 'icon'])
        self.dir.set_clicked_callback(self.change_direction)
        self.dir.element.id = f"btn_{train_id}_dir"
        tmp_el_2 <= self.dir.element
        tmp_el_2 <= html.BR()
        tmp_el_2 <= html.BR()

        tmp_el_1 <= tmp_el_2

        # speed control
        tmp_el_2 = Element(None, html.DIV, ['ui', 'center', 'align', 'basic', 'segment'])
        # manage callback on the element for mousewheel
        tmp_el_2.set_event_callback("wheel", self.get_mousewheel)
        # self.speed = Element(None, html.DIV, ['ui', 'vertical', 'reversed', 'yellow', 'big', 'slider'])
        self.speed = Slider(None, slider_class_attr=['ui', 'vertical', 'reversed', 'yellow', 'big', 'slider'])
        self.speed.set_event_callback('click', self.slider_function_clicked)
        self.speed.element.id = f"btn_{train_id}_speed"
        tmp_el_2 <= self.speed
        tmp_el_1 <= tmp_el_2

        description_el <= tmp_el_1

        slider_settings = {
            'min': 0,
            'max': 3,
            'start': 0,
            'step': 1
        }
        # jq('.ui.slider').slider(slider_settings)
        jq(self.speed.element).slider(slider_settings)

        # emergency button
        self.sos = Button(has_icon=True, button_class_attr=['ui', 'red', 'fluid', 'button'],
               icon_class_attr=['bell', 'icon'])
        self.sos.id = f"btn_{train_id}_dir"
        self.sos.set_text('SOS')
        self.sos.set_clicked_callback(self.btn_sos_clicked)

        self <= self.sos

    def change_direction(self, event):
        if event.target.id == f"btn_{self.train_id}_dir":
            btn_classes = self.dir.get_classes()
            if 'up' in btn_classes:
                self.direction = "B"
                self.dir.replace_classes(
                    plus_classes=['arrow', 'alternate', 'circle', 'down', 'outline', 'grey', 'huge', 'icon'],
                    minus_classes=['arrow', 'alternate', 'circle', 'up', 'grey', 'huge', 'icon']
                )
            elif 'down' in btn_classes:
                self.direction = "F"
                self.dir.replace_classes(
                    plus_classes=['arrow', 'alternate', 'circle', 'up', 'grey', 'huge', 'icon'],
                    minus_classes=['arrow', 'alternate', 'circle', 'down', 'outline', 'grey', 'huge', 'icon']
                )
            # update slider to STOP
            jq(self.speed.element).slider('set value', 0)
            # send STOP signal
            self.send_speed_request(0)

    def slider_function_clicked(self, event):
        speed = jq(self.speed.element).slider('get value')
        self.send_speed_request(speed)

    def send_speed_request(self, speed):
        if speed == 0:
            cmd = "STOP"
        elif speed in [1, 2, 3]:
            cmd = f"{self.direction}{speed}"
        print(f"{server_address}/train/{self.train_id}/speed/{cmd}")
        ajax.post(f"{server_address}/train/{self.train_id}/speed/{cmd}")

    def get_mousewheel(self, event):
        # forbid mousewheel events to scroll the page if the event occurs on the slider
        event.preventDefault()
        actual_speed = jq(self.speed.element).slider('get value')
        try:
            value = int(event.deltaY)
            if value < 0:
                new_speed = min(actual_speed+1, 3)
                if new_speed != actual_speed:
                    jq(self.speed.element).slider('set value', new_speed)
                    self.send_speed_request(new_speed)
            elif value > 0:
                new_speed = max(actual_speed-1, 0)
                if new_speed != actual_speed:
                    jq(self.speed.element).slider('set value', new_speed)
                    self.send_speed_request(new_speed)
        except ValueError as e:
            print(e)

    def btn_sos_clicked(self, event):
        if self.sos.element.text == 'SOS':
            print(f"{server_address}/sos")
            ajax.get(f"{server_address}/sos")
            self.sos.set_color('green')
            self.sos.set_icon(['bell', 'slash', 'icon'])
            self.sos.set_text('back to normal')
        else:
            print(f"{server_address}/sos_release")
            ajax.get(f"{server_address}/sos_release")
            self.sos.set_color('red')
            self.sos.set_icon(['bell', 'icon'])
            self.sos.set_text('SOS')

def btn_function_clicked(event):
    elem_id = event.target.id
    if elem_id is '':
        # just need to go one level up from the image to the button
        elem_id = event.target.parentElement.id
    _, train_id, function = elem_id.split('_')
    if function == 'light':
        print(f"{server_address}/train/{train_id}/light")
        ajax.post(f"{server_address}/train/{train_id}/light")
    elif function == 'horn':
        print(f"{server_address}/train/{train_id}/horn")
        ajax.post(f"{server_address}/train/{train_id}/horn")
    elif function == 'sound1':
        print(f"{server_address}/train/{train_id}/sound1")
        ajax.post(f"{server_address}/train/{train_id}/sound1")
    elif function == 'sound2':
        print(f"{server_address}/train/{train_id}/sound2")
        ajax.post(f"{server_address}/train/{train_id}/sound2")


