import asyncio
import logging
import socket
import json
import threading
import sys
import signal

from opcua import Server
from inverter_run_mode import InverterMode, generate_cyclical_values

logging.basicConfig(level=logging.INFO)

SERVER_ENDPOINT = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
NAMESPACE_URI = "http://examples.freeopcua.github.io"
OBJECT_NAME = "InverterObject"

stop_flag = False
current_recipe = InverterMode.NORMAL
time_step = 0
temporary_variable_updates = {}

def get_enum_by_value(value):
    for recipe in InverterMode:
        if recipe.value == value:
            return recipe
    return None

def handle_client(client_socket, variables):
    global current_recipe, time_step, temporary_variable_updates
    try:
        data = client_socket.recv(1024)
        data_json = json.loads(data)
        if 'recipe' in data_json:
            new_recipe = get_enum_by_value(data_json['recipe'])
            if new_recipe:
                current_recipe = new_recipe
                time_step = 0  # Reset time_step on recipe change
                print(f"Recipe changed to: {current_recipe.name}")
        elif 'variable' in data_json and 'value' in data_json and 'duration' in data_json:
            variable_name = data_json['variable']
            new_value = data_json['value']
            duration = int(data_json['duration'])
            temporary_variable_updates[variable_name] = (new_value, duration)
            print(f"Temporary update for {variable_name} to {new_value} for {duration} seconds")
    finally:
        client_socket.close()

def update_variables(variables):
    global current_recipe, time_step, temporary_variable_updates
    recipe_values = generate_cyclical_values(current_recipe, time_step)
    # recipe_values['OperatingMode'] = current_recipe.value  # Reflect the current recipe in operating_mode
    # Apply temporary variable updates
    for var_name, (value, duration) in list(temporary_variable_updates.items()):
        if var_name in variables:
            variables[var_name].set_value(value)
            temporary_variable_updates[var_name] = (value, duration - 1)
            if duration <= 1:
                del temporary_variable_updates[var_name]
    # Apply regular updates
    for key, value in recipe_values.items():
        if key not in temporary_variable_updates:
            variables[key].set_value(value)
    print(f"Updated variables for recipe {current_recipe.name}, Time Step: {time_step}")
    time_step += 1

def start_tcp_server(variables):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen(5)
    print("Listening on localhost:9999")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client, variables))
        client_handler.start()

async def update_loop(variables):
    global stop_flag
    while not stop_flag:
        update_variables(variables)
        await asyncio.sleep(1)

def main():
    server = Server()
    server.set_endpoint(SERVER_ENDPOINT)
    uri = NAMESPACE_URI
    idx = server.register_namespace(uri)
    objects = server.get_objects_node()
    myobject = objects.add_object(idx, OBJECT_NAME)

    variables = {
        'PvCurrent': myobject.add_variable(idx, "PvCurrent", 0.0),
        'PvAmperage': myobject.add_variable(idx, "PvAmperage", 0.0),
        'PvVoltage': myobject.add_variable(idx, "PvVoltage", 0.0),
        'Load': myobject.add_variable(idx, "Load", 0.0),
        'PvACPower': myobject.add_variable(idx, "PvACPower", 0.0),
        'PvDCPower': myobject.add_variable(idx, "PvDCPower", 0.0),
        'PvPower': myobject.add_variable(idx, "PvPower", 0.0),
        'OperatingMode': myobject.add_variable(idx, "OperatingMode", "NORMAL"),
        'Firmware': myobject.add_variable(idx, "Firmware", "1.1.2"),
        'PvTemperature': myobject.add_variable(idx, "PvTemperature", 0.0),
        'StatusCode': myobject.add_variable(idx, "StatusCode", 1),
        'BatteryTemp': myobject.add_variable(idx, "BatteryTemperature", 0.0),
        'BatteryHealth': myobject.add_variable(idx, "BatteryHealth", 0.0),
        'BatteryCharge': myobject.add_variable(idx, "BatteryCharge", 0.0)
    }

    for var in variables.values():
        var.set_writable()

    tcp_server_thread = threading.Thread(target=start_tcp_server, args=(variables,))
    tcp_server_thread.start()

    server.start()
    logging.info("Server started")

    loop = asyncio.get_event_loop()
    loop.create_task(update_loop(variables))
    loop.run_forever()


if __name__ == "__main__":
    main()
