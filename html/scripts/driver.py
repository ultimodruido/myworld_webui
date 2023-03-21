import json

from browser import document, ajax
from collections import namedtuple

from .deps import server_address
from .lib_check_server import check_server
from .driver_deps import TrainCard, CardTitle


def load_trains(reply):
    #print('loading trains')
    #train_choice_menu = document['train_choice']
    config = json.loads(reply.text)
    #print(config)

    train_list = dict()

    Train = namedtuple('Train', ['id', 'name', 'box'])

    for train_id, item in enumerate(config['data']['train_list']):
        train_list[train_id] = Train(train_id, item['name'], item['box'])

    #tc = CardTitle(train_list, update_callback)
    tc = TrainCard(train_list)
    #print(tc)
    #card_field <= tc.element
    main_container = document["main_container"]
    main_container <= tc.element


def update_callback(train_id):
    print(f"callback train id {train_id}")


def driver_main():
    check_server(full_width=True)
    print('check server stopped')
    if server_address is not None:
        print(f"host true in: {server_address}/train_list")
        ajax.get(f"{server_address}/train_list", oncomplete=load_trains)
        #print("host true out")
