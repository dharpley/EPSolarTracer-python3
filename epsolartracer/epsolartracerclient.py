from pymodbus.client import ModbusBaseClient
# from pymodbus.pdu import ExceptionResponse
# from pymodbus.register_read_message import ReadInputRegistersResponse, ReadHoldingRegistersResponse
# from pymodbus.register_write_message import WriteSingleRegisterResponse
from pymodbus.exceptions import ModbusException

# from pymodbus.register_read_message import *
# from pymodbus.transaction import ModbusRtuFramer

import epsolartracer.registers as registers

class Response:
    def __init__(self, success, data):
        self.success = success
        self.data = data


class DataResponse:
    def __init__(self, value, raw_value, unit):
        # type: (float, float, str) -> None
        self.unit = unit
        self.value = value
        self.raw_value = raw_value

    def __str__(self):
        return str(self.value) + self.unit


class EPSolarTracerClient:
    def __init__(self, modbusclient: ModbusBaseClient, unit : int=1):
        # type: (ModbusBaseClient, int) -> None

        # Type validation
        if not isinstance(modbusclient, ModbusBaseClient):
            raise TypeError("1st argument must be a valid ModbusClient")

        if not isinstance(unit, int):
            raise TypeError("2nd argument must be a integer")

        # # Check if framer is RTU framer
        # if not isinstance(modbusclient.framer, ModbusRtuFramer):
        #     raise RuntimeError("The ModbusClient's framer must be ModbusRtuFramer.")
        self.modbusclient = modbusclient
        self.unit = unit

    def read_input_register(self, input_register : registers.InputRegister) -> Response:
        """
        Reads an input register from the device.
        """
        try:
            # Send the Modbus request to read input registers
            raw_response = self.modbusclient.read_input_registers(
                address=input_register.address,
                count=1,  # Assuming single register read
                unit=self.unit
            )

            # Check if the response is an error
            if raw_response.isError():
                return Response(False, f"Error: {raw_response}")

            # Process the valid response
            raw_value = raw_response.registers[0]  # Access the first register value
            value = float(raw_value) / input_register.multiplier  # Apply multiplier
            return Response(True, DataResponse(value, raw_value, self.unit))

        except ModbusException as e:
            # Handle Modbus-specific exceptions
            return Response(False, f"Modbus exception: {e}")

        except Exception as e:
            # Handle general exceptions
            return Response(False, f"Unexpected error: {e}")


    def read_holding_register(self, holding_register : registers.HoldingRegister) -> Response:
        """
        Reads a holding register from the device.
        """
        try:
            # Validate input
            if not isinstance(holding_register, registers.HoldingRegister):
                raise TypeError("1st argument must be a HoldingRegister")

            # Send the Modbus request to read holding registers
            raw_response = self.modbusclient.read_holding_registers(
                address=holding_register.address,
                count=1,  # Assuming single register read
                unit=self.unit
            )

            # Check if the response is an error
            if raw_response.isError():
                return Response(False, f"Error: {raw_response}")

            # Process the valid response
            raw_value = raw_response.registers[0]  # Access the first register value
            value = float(raw_value) / holding_register.multiplier  # Apply multiplier
            return Response(True, DataResponse(value, raw_value, self.unit))

        except ModbusException as e:
            # Handle Modbus-specific exceptions
            return Response(False, f"Modbus exception: {e}")

        except Exception as e:
            # Handle general exceptions
            return Response(False, f"Unexpected error: {e}")


    def write_holding_register(self, holding_register : registers.HoldingRegister, value : int) -> None:
        if not isinstance(holding_register, registers.HoldingRegister):
            raise TypeError("1st argument must be a holding register")

        self.modbusclient.write_register(holding_register, value, unit=self.unit)
