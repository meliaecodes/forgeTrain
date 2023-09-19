from contextlib import asynccontextmanager

import asyncio
from bleak import BleakScanner, BleakClient

from fastapi import FastAPI

HUB_NAME = "Pytrain"
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

def hub_filter(device, ad):
    return device.name and device.name.lower() == HUB_NAME.lower()

def handle_disconnect(_):
    print("Hub was disconnected.")

def handle_rx(_, data: bytearray):
    print("Received:", data)

class LegoHubClient:
    def __init__(self):
        self.lights = False
        pass

    async def connect(self):
        device = await BleakScanner.find_device_by_filter(hub_filter)
        self.client = BleakClient(device, disconnected_callback=handle_disconnect)
        await self.client.connect()
        await self.client.start_notify(UART_TX_CHAR_UUID, handle_rx)
        self.nus = self.client.services.get_service(UART_SERVICE_UUID)
        self.rx_char = self.nus.get_characteristic(UART_RX_CHAR_UUID)
        # Tell user to start program on the hub.
        print("Start the program on the hub now with the button.")

    async def send(self, data):
        try:
            await self.client.write_gatt_char(self.rx_char, data)
        except Exception as e:
            # Handle exceptions.
            print(e)

    async def toggle_lights(self):
        if(self.lights == True):
            self.lights = False
            await self.send(b"d")
        else:
            self.lights = True
            await self.send(b"n")
        return (self.lights)

    async def disconnect(self):
        await self.send(b"d")
        await self.send(b"b")
        await self.client.disconnect()

trainClient = LegoHubClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await trainClient.connect()
    yield
    await trainClient.disconnect()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/disconnect")
async def root():
    await trainClient.disconnect()
    return {"message": "Disconnected"}

@app.get("/forward")
async def root():
    await trainClient.send(b"f")
    await asyncio.sleep(8)
    await trainClient.send(b"s")
    return {"message": "Go forward"}


@app.get("/reverse")
async def root():
    await trainClient.send(b"r")
    await asyncio.sleep(9)
    await trainClient.send(b"s")
    return {"message": "Go in reverse"}

@app.get("/lights")
async def root():
    lights = await trainClient.toggle_lights()
    return {"message": "lights on: " + str(lights)}

