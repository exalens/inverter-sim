from opcua import Client
import socket
import json

SERVER_ENDPOINT = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
TCP_SERVER_IP = "localhost"
TCP_SERVER_PORT = 9999

def send_recipe_data(recipe):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_SERVER_IP, TCP_SERVER_PORT))
    data = {'recipe': recipe}
    client.send(json.dumps(data).encode())
    client.close()

def send_variable_update(variable_name, new_value, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_SERVER_IP, TCP_SERVER_PORT))
    data = {'variable': variable_name, 'value': new_value, 'duration': duration}
    client.send(json.dumps(data).encode())
    client.close()

def main():
    client = Client(SERVER_ENDPOINT)
    try:
        client.connect()
        root = client.get_root_node()
        print("Root node is: ", root)
        uri = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index(uri)
        myobject = root.get_child(["0:Objects", f"{idx}:InverterObject"])

        while True:
            print("Choose an action:")
            print("1. Set the Operating Mode of the Inverter")
            print("2. Modify a Inverter Process Variable")
            print("3. Exit")
            choice = input("Enter choice (1, 2, or 3): ")

            if choice == '1':
                recipe_choice = input("Enter Inverter Operating Mode: NORMAL, MAINTENANCE, ERROR (case sensitive): ")
                send_recipe_data(recipe_choice)
                print(f"Inverter Operating Mode has been set to {recipe_choice}")
            elif choice == '2':
                print("Inverter Process Variables")
                print("=================================")
                print(f"PvCurrent")
                print(f"PvVoltage")
                print(f"PvAmperage")
                print(f"PvPower")
                print(f"PvACPower")
                print(f"PvDCPower")
                print(f"PvTemperature")
                print(f"StatusCode")
                print(f"BatteryHealth")
                print(f"BatteryTemp")
                print(f"BatteryCharge")
                print(f"OperatingMode")
                print("=================================")
                variable_name = input("Enter the  name of the Inverter process variable you wish to modify: ")
                new_value = input(f"Enter the new value for {variable_name}: ")
                duration = input("Enter the duration (in seconds) for this value: ")
                send_variable_update(variable_name, new_value, duration)
                print(f"Variable {variable_name} has been set to {new_value} for {duration} seconds.")
            elif choice == '3':
                break
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
