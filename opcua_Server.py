from opcua import Server #pip install opcua
from datetime import datetime
import time
import random #pip install random

def start_opcua_server():
    #Set up servers
    server = Server()

    server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_server_name("Basic communication server")


    namespace = server.register_namespace("OPCUA_Simulation")

    #Object node to put custom stuff / data
    objects = server.get_objects_node()

    #Variable, because clients can write onto it with .set_writable()
    temperature = objects.add_variable(namespace, "Temperature", 21)
    temperature.set_writable()

    humidity = objects.add_variable(namespace, "Humidity", 45.0)
    humidity.set_writable()

    pressure = objects.add_variable(namespace, "Pressure", 101.3)
    pressure.set_writable()

    server.start()
    print("OPC-UA Server started at opc.tcp://localhost:4840/freeopcua/server/")

    #loop until stopped manually
    try:
        while True:
            temp_value = temperature.get_value() + random.uniform(-1, 1)
            humidity_value = humidity.get_value() + random.uniform(-2, 2)
            pressure_value = pressure.get_value() + random.uniform(-0.5, 0.5)

    

            temperature.set_value(temp_value)
            humidity.set_value(humidity_value)
            pressure.set_value(pressure_value)
            

            print(f"Temperature updated to: {temp_value}")
            print(f"Humidity updated to: {humidity_value}")
            print(f"Pressure updated to: {pressure_value}")
            
            time.sleep(2)
    finally:
        server.stop()
        print("Server stopped")

if __name__ == "__main__":
    start_opcua_server()



