import asyncio
from pymodbus.client import AsyncModbusSerialClient
import logging

# Set up logging to file and console
logging.basicConfig(
    filename="epsolar_test.log",  # Log file name
    filemode="w",                # Overwrite the log file each time
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,         # Log all levels (DEBUG and above)
)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set console log level
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the console handler to the root logger
logging.getLogger().addHandler(console_handler)

# Async function to communicate with the MPPT controller
async def read_data():
    client = AsyncModbusSerialClient(
        port="COM17",  # Replace with your serial port
        baudrate=115200,  # Default is 115200 for EPEVER IT6415ND
        stopbits=1,
        bytesize=8,
        parity="N",
    )

    # Connect to the client
    connection = await client.connect()
    if connection:
        logging.info("Connection successful!")
        try:
            # Read the battery voltage register (example: 0x3100)
            result = await client.read_input_registers(address=0x3100, count=2, slave=1)
            if result.isError():
                logging.error("Error reading register")
            else:
                # Combine the two registers and scale if necessary
                battery_voltage = result.registers[0] / 100.0  # Adjust scaling as needed
                logging.info(f"Battery Voltage: {battery_voltage} V")
                print(f"Battery Voltage: {battery_voltage} V")  # Print to console
        except Exception as e:
            logging.error(f"Error during read: {e}")
            print(f"Error during read: {e}")  # Print to console
    else:
        logging.error("Failed to connect to the device.")
        print("Failed to connect to the device.")  # Print to console

    await client.close()

# Run the asynchronous function
asyncio.run(read_data())
