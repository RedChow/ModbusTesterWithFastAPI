from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.version import version
import twisted.internet.error
import socket
import json_models


FUNCTION_MAP = {
    "coils": 1,
    'discrete_inputs': 2,
    'input_registers': 4,
    'holding_registers': 3
}


class CustomDataBlock(ModbusSparseDataBlock):
    """ A datablock that stores the new value in memory
    and performs a custom action after it has been stored.
    """

    def setValues(self, address, values):
        """ Sets the requested values of the datastore
        :param address: The starting address
        :param values: The new values to be set
        """
        super(CustomDataBlock, self).setValues(address, values)


class AsyncModbusServer:
    def __init__(self):
        self.units = {}
        self.could_not_start = 0

    def start_server(self):
        self.create_units()
        context = ModbusServerContext(slaves=self.units, single=False)

        identity = ModbusDeviceIdentification()
        identity.VendorName = 'MyModbusServer'
        identity.ProductCode = 'PM'
        identity.VendorUrl = ''
        identity.ProductName = 'Ignition Modbus Tester'
        identity.ModelName = 'Modbus Server'
        identity.MajorMinorRevision = version.short()
        try:
            StartTcpServer(context, identity=identity, address=("localhost", 502))
            self.could_not_start = -1
        except (socket.gaierror, twisted.internet.error.CannotListenError):
            self.could_not_start = 1

    def create_units(self):
        for i in range(0, 256):
            self.units[i] = ModbusSlaveContext(di=CustomDataBlock([0]*100), co=CustomDataBlock([0]*100),
                                               hr=CustomDataBlock([0] * 100),
                                               ir=CustomDataBlock([0]*100))

    def write_values(self, fx, j_data: json_models.ModbusWriteRequest):
        self.units[j_data.unit_id].setValues(FUNCTION_MAP[fx], j_data.address, j_data.values)

    def get_values(self, fx, j_data: json_models.ModbusReadRequest):
        values = self.units[j_data.unit_id].getValues(FUNCTION_MAP[fx], address=j_data.starting_address,
                                                      count=j_data.quantity)
        return json_models.ModbusReturnReadRequest(starting_address=j_data.starting_address,
                                                   register_type=j_data.register_type, unit_id=j_data.unit_id,
                                                   quantity=j_data.quantity, values=values)
