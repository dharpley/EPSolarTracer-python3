import asyncio
from pymodbus.client import AsyncModbusSerialClient
import logging

# Enable detailed logging (optional)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

async def read_data():
    # Create the AsyncModbusSerialClient for Windows
    client = AsyncModbusSerialClient(
        port="COM17",  # Replace with your serial port
        baudrate=115200,
        stopbits=1,
        bytesize=8,
        parity="N",
    )

    # Connect to the client
    connection = await client.connect()
    if connection:
        print("Connection successful!")
        try:
            # Read the battery voltage register (example: 0x3100)
            result = await client.read_input_registers(address=0x3100, count=2, slave=1)  # Use 'slave' to specify the Modbus address
            if result.isError():
                print("Error reading register")
            else:
                # Combine the two registers and scale if necessary
                battery_voltage = result.registers[0] / 100.0  # Adjust scaling as needed
                print(f"Battery Voltage: {battery_voltage} V")
        except Exception as e:
            print(f"Error during read: {e}")
    else:
        print("Failed to connect to the device.")

    # Close the client
    await client.close()

# Run the asynchronous function
asyncio.run(read_data())
