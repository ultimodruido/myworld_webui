import json

from browser import document, html, ajax, alert

from ui.classes import Element
from ui.dropdown import SelectionDropdown
from ui.buttons import Button

from .deps import server_address, server, port, set_server
from .lib_check_server import check_server
from .settings_deps import TrainSettingsCard, TrainDropdownItem, BoxCard
from .boxes import box_list

# DOM elements
card_field = Element('train_list_container', html.DIV)
remove_train_selection = SelectionDropdown("remove_train_selection", "remove_train",
                                           default_text="Select train",
                                           icon_class_attr=["subway", "icon"])
manage_train_selection = SelectionDropdown("manage_train_selection", "manage_train",
                                           default_text="Select train",
                                           icon_class_attr=["subway", "icon"])
boxes_art_field = Element('box_list_container', html.DIV)


def fake_callback(reply):
    print(reply.text)
    reply_data = json.loads(reply.text)
    try:
        if reply_data['result'] is False:
            alert(reply_data['data']['error'])
    except KeyError:
        alert("Command not performed correctly")


def remove_train(event):
    train_id = str(remove_train_selection.get_value())
    ajax.post(f"{server_address}/remove/train/{train_id}", oncomplete=fake_callback)
    ajax.get(f"{server_address}/train_list", oncomplete=load_trains)


def new_train(event):
    el = Element("ipt_train_name", html.INPUT)
    train_name = el.element.value
    el = Element("ipt_train_freq", html.INPUT)
    train_freq = el.element.value
    ajax.post(f"{server_address}/register/newtrain/{train_name}/{train_freq}", oncomplete=fake_callback)
    ajax.get(f"{server_address}/train_list", oncomplete=load_trains)


def load_trains(reply):
    # get train list from server
    config = json.loads(reply.text)

    # fill fleet overview section
    global card_field
    card_field.clear()
    for train_id, item in enumerate(config['data']['train_list']):
        # print(f"ID: {train_id} - item: {item}")
        tc = TrainSettingsCard(train_id, item['name'], item['frequency'], item['box'])
        card_field <= tc

    # fill remove train dropdown list
    global remove_train_selection
    remove_train_selection.empty()
    for train_id, item in enumerate(config['data']['train_list']):
        tc = TrainDropdownItem(train_id, item['name'])
        remove_train_selection.add_element(tc)
    remove_train_selection.clear_value()

    # fill remove train dropdown list
    global manage_train_selection
    manage_train_selection.empty()
    for train_id, item in enumerate(config['data']['train_list']):
        tc = TrainDropdownItem(train_id, item['name'])
        manage_train_selection.add_element(tc)
    manage_train_selection.clear_value()


def show_stored_server_address():
    el = Element("ipt_server_address", html.INPUT)
    el.element.value = server
    el = Element("ipt_server_port", html.INPUT)
    el.element.value = port


def save_stored_server_address(event):
    el = Element("ipt_server_address", html.INPUT)
    new_server = el.element.value
    el = Element("ipt_server_port", html.INPUT)
    new_port = el.element.value
    set_server(new_server, new_port)
    document.location.reload()
    #check_server()


def configure_remote_port(event):
    el = Element("ipt_remote_port", html.INPUT)
    remote_port = el.element.value
    ajax.post(f"{server_address}/register/remote/{remote_port}", oncomplete=fake_callback)


def change_train_management(event):
    src_element = event.srcElement.id
    if src_element not in ("btn_change_train_name", "btn_change_train_frequency", "btn_change_train_box"):
        src_element = event.srcElement.parent.id

    # get train_id
    train_id = str(manage_train_selection.get_value())
    if train_id == "":
        alert("Select a train to be modified!")
        return

    if src_element == "btn_change_train_name":
        el = Element("ipt_change_train_name", html.INPUT)
        new_name = el.element.value
        ajax.post(f"{server_address}/register/train/{train_id}/name/{new_name}", oncomplete=fake_callback)
    elif src_element == "btn_change_train_frequency":
        el = Element("ipt_change_train_frequency", html.INPUT)
        new_freq = el.element.value
        ajax.post(f"{server_address}/register/train/{train_id}/frequency/{new_freq}", oncomplete=fake_callback)
    elif src_element == "btn_change_train_box":
        el = Element("ipt_change_train_box", html.INPUT)
        new_box = el.element.value
        ajax.post(f"{server_address}/register/train/{train_id}/box/{new_box}", oncomplete=fake_callback)

    ajax.get(f"{server_address}/train_list", oncomplete=load_trains)


def settings_main():
    check_server()
    show_stored_server_address()

    if server_address is not None:
        ajax.get(f"{server_address}/train_list", oncomplete=load_trains)

    # configure buttons
    # server address
    btn_server_address = Button("btn_server_address", has_icon=True,
                                button_class_attr=["ui", "icon", "primary", "button"],
                                icon_class_attr=["save", "icon"])
    btn_server_address.set_clicked_callback(save_stored_server_address)

    # remote port
    btn_remote_port = Button("btn_remote_port", has_icon=True,
                                button_class_attr=["ui", "icon", "primary", "button"],
                                icon_class_attr=["save", "icon"])
    btn_remote_port.set_clicked_callback(configure_remote_port)

    # add/remove trains
    btn_remove_train = Button("btn_remove_train", has_icon=True,
                              button_class_attr=["ui", "icon", "orange", "button"],
                              icon_class_attr=["trash", "alternate", "icon"])
    btn_remove_train.set_clicked_callback(remove_train)

    btn_new_train = Button("btn_new_train", has_icon=True,
                           button_class_attr=["ui", "icon", "primary", "button"],
                           icon_class_attr=["save", "icon"])
    btn_new_train.set_clicked_callback(new_train)

    # setting buttons for train management
    btn_train_change = Button("btn_change_train_name", has_icon=True,
                              button_class_attr=["ui", "icon", "primary", "button"],
                              icon_class_attr=["save", "icon"])
    btn_train_change.set_clicked_callback(change_train_management)

    btn_train_change = Button("btn_change_train_frequency", has_icon=True,
                              button_class_attr=["ui", "icon", "primary", "button"],
                              icon_class_attr=["save", "icon"])
    btn_train_change.set_clicked_callback(change_train_management)

    btn_train_change = Button("btn_change_train_box", has_icon=True,
                              button_class_attr=["ui", "icon", "primary", "button"],
                              icon_class_attr=["save", "icon"])
    btn_train_change.set_clicked_callback(change_train_management)

    # box art gallery
    global boxes_art_field
    boxes_art_field.clear()
    for box in box_list:
        box_card = BoxCard(box)
        boxes_art_field <= box_card
