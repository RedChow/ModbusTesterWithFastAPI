"""
    uvicorn main:app --reload
"""
from fastapi import FastAPI, HTTPException
import threading
import json_models
import modbus_server

modbus_async_server = modbus_server.AsyncModbusServer()
app = FastAPI()


@app.post("/write")
async def write_registers(modbus_request: json_models.ModbusWriteRequest):
    register_type = modbus_request.register_type
    print(modbus_request)
    if register_type not in modbus_server.FUNCTION_MAP:
        raise HTTPException(status_code=404, detail="Register type not found")
    modbus_async_server.write_values(register_type, modbus_request)


@app.post("/get")
async def get_registers(modbus_request: json_models.ModbusReadRequest):
    register_type = modbus_request.register_type
    if register_type not in modbus_server.FUNCTION_MAP:
        raise HTTPException(status_code=404, detail="Register type not found")
    return modbus_async_server.get_values(register_type, modbus_request)

server_thread = threading.Thread(target=modbus_async_server.start_server, daemon=True)
server_thread.start()
