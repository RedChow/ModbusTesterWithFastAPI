from pydantic import BaseModel


class ModbusWriteRequest(BaseModel):
    register_type: str
    address: int
    unit_id: int
    values: list


class ModbusReadRequest(BaseModel):
    register_type: str
    starting_address: int
    unit_id: int
    quantity: int


class ModbusReturnReadRequest(BaseModel):
    register_type: str
    starting_address: int
    unit_id: int
    quantity: int
    values: list
