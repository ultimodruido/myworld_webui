import json

from browser import document, ajax

from .deps import server_address
from .lib_check_server import check_server
from .control_center_deps import TrainCard


def load_trains(reply):
    #print('loading trains')
    card_field = document['cards_container']
    config = json.loads(reply.text)
    #print(config)

    for train_id, item in enumerate(config['data']['train_list']):
        tc = TrainCard(train_id, item['name'], item['box'])
        card_field <= tc.element


def control_center_main():
    check_server()
    if server_address is not None:
        #print(f"host true in: {server_address}/train_list")
        ajax.get(f"{server_address}/train_list", oncomplete=load_trains)
        #print("host true out")
