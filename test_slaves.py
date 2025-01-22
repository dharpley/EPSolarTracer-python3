import asyncio
from pymodbus.client import AsyncModbusSerialClient
import logging

# Set up logging
logging.basicConfig(
    filename="slave_check.log",  # Log file
    filemode="w",               # Overwrite log file each time
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

# Add logging to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

async def check_slave_ids():
    try:
        client = AsyncModbusSerialClient(
            port="COM17",  # Replace with your serial port
            baudrate=115200,  # Default for EPEVER
            stopbits=1,
            bytesize=8,
            parity="N",
        )

        # Attempt to connect to the client
        connection = await client.connect()
        if not connection:
            logging.error("Failed to establish connection to the Modbus client.")
            print("Failed to establish connection to the Modbus client.")
            return  # Exit if no connection

        logging.info("Connection successful!")
        print("Checking slave IDs...")

        # Test slave IDs from 1 to 5
        for slave_id in range(1, 6):
            try:
                logging.info(f"Testing slave ID {slave_id}...")
                # Try reading a common register (e.g., 0x3100)
                result = await client.read_input_registers(address=0x3100, count=2, slave=slave_id)
                if not result.isError():
                    battery_voltage = result.registers[0] / 100.0  # Adjust scaling as needed
                    logging.info(f"Response from slave ID {slave_id}: Battery Voltage = {battery_voltage} V")
                    print(f"Response from slave ID {slave_id}: Battery Voltage = {battery_voltage} V")
                else:
                    logging.warning(f"No valid response from slave ID {slave_id}.")
            except Exception as e:
                logging.error(f"No response from slave ID {slave_id}: {e}")
                print(f"No response from slave ID {slave_id}: {e}")

        # Close the client connection
        await client.close()
        logging.info("Connection closed.")
        print("Connection closed.")

    except Exception as e:
        logging.critical(f"Unexpected error occurred: {e}")
        print(f"Unexpected error occurred: {e}")

# Run the slave ID check
asyncio.run(check_slave_ids())
