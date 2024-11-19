# OPC-UA Based Sensor Data Simulation

## Project Overview

This is a basic simulation project designed to emulate an OPC-UA server that generates sensor data, such as temperature, humidity, and pressure, which can be consumed by an OPC-UA client. The server updates the sensor data periodically and provides it to any connected client in real-time.

The project is structured into two main components:
1. **OPC-UA Server**: Simulates sensor data and allows external clients to connect and read the data.
2. **OPC-UA Client**: Consumes data from the OPC-UA server, processes it, and manages a message queue based on priorities.

## Features

- **OPC-UA Server**: 
  - Provides simulated temperature, humidity, and pressure data.
  - Updates the data values every 2 seconds using random fluctuations.
  - Exposes the data through OPC-UA protocol, allowing clients to read the values.
  
- **OPC-UA Client**: 
  - Connects to the OPC-UA server to fetch the sensor data.
  - Uses a producer-consumer model where the producer reads data from the server and adds it to a priority queue, and the consumer processes the messages from the queue.
  - Implements basic message prioritization, with critical temperature values being given the highest priority.
  - Processes messages and prints them to the console.

## Technologies Used

- **Python**: The project is implemented using Python 3.x.
- **OPC-UA**: The `opcua` Python library is used for both the server and client components.
- **Threading**: Python’s threading module is used to run the producer and consumer in parallel.
- **Randomization**: Simulated data values are generated using the `random` library.

## How It Works

### Server:
1. The server starts by initializing the OPC-UA server and creating three variables: Temperature, Humidity, and Pressure.
2. The values for these variables are updated every 2 seconds with random variations to simulate real sensor data.
3. Client(s) can connect to the server and read these values.

### Client:
1. The client connects to the server and reads the Temperature, Humidity, and Pressure values.
2. A producer thread fetches the data from the server and adds it to a priority queue, where each message has a priority level.
3. A consumer thread processes the messages from the queue, printing them to the console with timestamps.

