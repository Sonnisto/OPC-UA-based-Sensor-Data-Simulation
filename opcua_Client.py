from opcua import Client
from datetime import datetime
import time
import queue
import threading
import random

message_queue = queue.PriorityQueue()
producer_done = threading.Event()  # Event to signal when producer is finished

# Producer: Reads from OPC-UA server and populates the queue
def producer(temperature_node, humidity_node, pressure_node):
    print("Producer function started")
    for i in range(30):
        try:
            temp_value = temperature_node.get_value()
            humidity_value = humidity_node.get_value()
            pressure_value = pressure_node.get_value()

            timestamp = datetime.now()

            if random.random() <= 0.15:
                critical_temp = temp_value * 50
                message_queue.put((0, f"CRITICAL Temperature: {critical_temp}", timestamp))
                print(f"Produced: CRITICAL Temperature={critical_temp}, Priority=0")
            else:
                message_queue.put((2, f"Temperature: {temp_value}", timestamp))

            
            
            message_queue.put((3, f"Humidity: {humidity_value}", timestamp))
            message_queue.put((4, f"Pressure: {pressure_value}", timestamp))



            print(f"Produced: Temperature={temp_value}, Humidity={humidity_value}, Pressure={pressure_value}")
            time.sleep(0.5)  # Simulate delay between reads

        except Exception as e:
            print(f"Error in producer: {e}")

    producer_done.set()  # Signal that production is done
    print("Producer finished producing messages.")

# Consumer: Processes messages from the queue
def consumer():
    print("Consumer function started")
    while not (producer_done.is_set() and message_queue.empty()):
        try:
            if not message_queue.empty():
                priority, message, timestamp = message_queue.get()
                print(f"Consumed: {message}, Priority={priority}, Time={timestamp}")
                time.sleep(1) 
            else:
                time.sleep(0.5)  
        except Exception as e:
            print(f"Error in consumer: {e}")

    print("Consumer finished consuming messages.")

# Start the OPC-UA client and threads
def start_client():
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")

    try:
        client.connect()
        print("Connected to OPC-UA Server")

        root = client.get_root_node()
        temperature_node = root.get_child(["0:Objects", "2:Temperature"])
        humidity_node = root.get_child(["0:Objects", "2:Humidity"])
        pressure_node = root.get_child(["0:Objects", "2:Pressure"])

        print("Starting producer thread...")
        producer_thread = threading.Thread(target=producer, args=(temperature_node, humidity_node, pressure_node))
        producer_thread.start()

        time.sleep(3)

        print("Starting consumer thread...")
        consumer_thread = threading.Thread(target=consumer)
        consumer_thread.start()
        

        producer_thread.join()
        consumer_thread.join()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        try:
            if client.uaclient and client.uaclient._uasocket:
                client.disconnect()
                print("Client disconnected successfully.")
        except Exception as e:
            print(f"Error during disconnect: {e}")

if __name__ == "__main__":
    start_client()
