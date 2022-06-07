from browser import html

from ui.classes import Element
from ui.lists import ListContainer, ListItem
from ui.dropdown import DropdownItem


class TrainPropertyItem(ListItem):
    def __init__(self, header, value, icon):
        super().__init__()

        tmp_el_1 = Element(None, html.I,
                           ['large', 'blue', icon, 'middle', 'aligned', 'icon']
                           )
        self <= tmp_el_1

        tmp_el_1 = Element(None, html.DIV, ['content'])
        self <= tmp_el_1

        tmp_el_2 = Element(None, html.DIV, ['header'])
        tmp_el_2.set_text(header)
        tmp_el_1 <= tmp_el_2

        tmp_el_2 = Element(None, html.DIV, ['description'])
        tmp_el_2.set_text(str(value))
        tmp_el_1 <= tmp_el_2


class TrainSettingsCard(Element):
    def __init__(self, train_id, train_name, frequency, box_code):
        super().__init__(None, html.DIV, ['ui', 'card'])
        # self.card = Element(None, html.DIV, ['ui', 'card'])
        self.element.id = f"train_{train_id}"
        self.train_id = train_id

        # create name DIV
        tmp_el_1 = Element(None, html.DIV, ['content'])
        tmp_el_2 = Element(None, html.DIV, ['header'])
        tmp_el_2.set_text(train_name)

        # add to the Card
        tmp_el_1 <= tmp_el_2.element
        self <= tmp_el_1.element

        # create properties DIV
        tmp_el_1 = Element(None, html.DIV, ['content'])
        self.train_list = ListContainer(None, TrainPropertyItem)

        # add the list to the Card
        tmp_el_1 <= self.train_list
        self <= tmp_el_1

        # fill the list
        train_properties = [
            ('Remote frequency:', frequency, 'wifi'),
            ('Box code:', box_code, 'barcode'),
            ('Unique ID:', train_id, 'terminal'),
        ]

        for header, value, icon in train_properties:
            self.train_list.add_element(TrainPropertyItem(header, value, icon))


class BoxCard(Element):
    def __init__(self, box_code):
        super().__init__(None, html.DIV, ['ui', 'card'])

        # create name DIV
        tmp_el_1 = Element(None, html.DIV, ['content'])
        tmp_el_2 = Element(None, html.DIV, ['header'])
        tmp_el_2.set_text(box_code)

        # add to the Card
        tmp_el_1 <= tmp_el_2.element
        self <= tmp_el_1.element

        # create image
        tmp_el_1 = Element(None, html.DIV, ['image'])
        tmp_el_2 = Element(None, html.IMG, [''])
        tmp_el_2.element.src = f"./data/{box_code}.jpg"

        # add the list to the Card
        tmp_el_1 <= tmp_el_2.element
        self <= tmp_el_1.element


class TrainDropdownItem(DropdownItem):
    def __init__(self, train_id, train_name):
        super().__init__(None)
        self.set_text(f"{train_name} [ID:{train_id}]")
        self.element.attrs["data-value"] = str(train_id)

        self.refresh()