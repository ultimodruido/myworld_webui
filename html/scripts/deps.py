from browser.local_storage import storage


server_address = None
server = None
port = None

try:
    server = storage['server']
    port = storage['port']
    server_address = f"http://{server}:{port}"
    print(server_address)

except KeyError:
    pass


def set_server(address, port):
    storage['server'] = address
    storage['port'] = port
