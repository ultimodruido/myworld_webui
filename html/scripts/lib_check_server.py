from browser import ajax

from ui.labels import IconLabel

from .deps import server_address

connection_status_label = IconLabel("connection_status_label")


def check_server_reply(reply):
    print("check server reply\n---------------")
    print(reply.read())
    print("end check server reply\n---------------")
    if reply.text == '"Maerklin MyWorld universal remote API"':
        connection_status_label.set_text(f"Running on {server_address}")
        #connection_status_label.set_classes(['ui', 'bottom', 'right', 'attached', 'label'])
        connection_status_label.set_icon(['checkmark', 'icon'])
        return True
    else:
        connection_status_label.set_text(f"Host {server_address} unreachable")
        connection_status_label.set_color('red')
        connection_status_label.set_icon(['exclamation', 'triangle', 'icon'])
        return False


def check_server(full_width=False):
    if full_width:
        connection_status_label.set_classes(['ui', 'bottom', 'attached', 'label'])
    else:
        connection_status_label.set_classes(['ui', 'bottom', 'right', 'attached', 'label'])

    if server_address is not None:
        # check if server exists at the address
        ajax.get(server_address, oncomplete=check_server_reply)
        print(f"checking server on host: {server_address}")
    else:
        # update connection_status_label
        connection_status_label.set_text("Host not set")
        connection_status_label.set_color('red')
        connection_status_label.set_icon(['exclamation', 'triangle', 'icon'])
