from pybricksdev.connections import PybricksHub
from pybricksdev.ble import find_device
import numpy
import asyncio

async def main():
    data_receive = False
    data = b""
    hub = PybricksHub()
    await hub.connect(await find_device())
    await hub.run("cityhub_measurement.py", wait=False, print_output=False)
    while not hub.program_running:
        await asyncio.sleep(0.1)
    while hub.program_running:
        await asyncio.sleep(0.05)

        if hub.output:
            line = hub.output.pop(0)
            print(len(line))
            if len(line)>500:
                data = line
                dataarr = numpy.frombuffer(data, dtype=numpy.dtype(">i2"))
                fil = input("filename:")
                numpy.save(fil, dataarr)
            else:
                print(line.decode())

    await asyncio.sleep(1)
    await hub.disconnect()


if __name__ == "__main__":
    asyncio.run(main())