#!/usr/bin/env python
"""Quick and dirty script to log the power etc from the EP Solar MPPT Tracker.

Outputs the data to the console, since we are gpl3 and don't want to pollute our
actual codebase with the GPL3 license.
"""

from pymodbus.client import ModbusSerialClient

# import epsolartracer

from epsolartracer.epsolartracerclient import EPSolarTracerClient
from epsolartracer.registers import RealtimeDatum

import argparse
import time
from pathlib import Path

def getargs():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        default=None,
        required = True,
        help="Serial port to connect to the USB-RS485 adapter",
    )
    parser.add_argument(
        "-u",
        "--unit",
        type=int,
        default=None,
        help="Modbus Unit to connect to",
    )
    parser.add_argument(
        "-r",
        "--output-rated",
        dest="outputrated",
        type=bool,
        default=False,
        help="Output the Solar regulator ratings prior to logging",
    )
    parser.add_argument(
        "-t",
        "--time-interval",
        dest="interval",
        type=float,
        default=5.0,
        help="Interval between reads of the data, in seconds",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        default=None,
        help="File to output the data to, instead of the console",
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const="DEBUG",
        default="INFO",
    )
    verbosity.add_argument(
        "-q", "--quiet", dest="verbose", action="store_const", const="WARNING"
    )
    return parser


def main():
    parser = getargs()
    args = parser.parse_args()

    print(f"{args=}")
    
    # Create a Modbus client using a serial connection
    modbus_client = ModbusSerialClient(
        # method="rtu",       # RTU mode for serial communication
        port=args.port,  # Replace with your serial port
        baudrate=9600,       # Replace with your baud rate
        parity="N",          # Parity (N: None, E: Even, O: Odd)
        stopbits=1,
        bytesize=8,
        timeout=3            # Communication timeout in seconds
    )
    
    # Create an EPSolarTracerClient
    epsolar_client = EPSolarTracerClient(modbus_client)

    try:
        while True:
            #FIXME: @Dale change the register you want to read here:
            # In this example, we'll retrieve the battery SOC
            print(f"Retrieving battery SOC ({RealtimeDatum.BatterySOC.description})")

            # Call read_input_register
            response = epsolar_client.read_input_register(RealtimeDatum.BatterySOC)

            # Check the response for success
            if response.success:
                print("Battery SOC: " + response.data.value)
                print("Raw value: " + str(response.data.raw_value.registers[0].value))
            else:
                print("An error occurred while retrieving battery SOC ({response.data})")
            time.sleep(args.)
    except KeyboardInterrupt:
        pass
        
    finally:
        # Close the client connection
        modbus_client.close()
  
    
if __name__ == "__main__":
    main()
