import asyncio
from intcode_computer import IntCodeComputerMk2


class Computer:
    def __init__(self, netaddr, program, router_channel):
        self.input = asyncio.Queue()
        self.output = asyncio.Queue()
        self.netaddr = netaddr
        self.router_channel = router_channel
        self.nic = IntCodeComputerMk2(program, self.input, self.output)
    
    async def send_to(self):
        while True:
            addr = await self.output.get()
            self.output.task_done()
            if addr is None: break
            x = await self.output.get()
            self.output.task_done()
            y = await self.output.get()
            self.output.task_done()
            await self.router_channel.put((addr, x, y))
    
    async def run(self):
        # register network address
        await self.input.put(self.netaddr)
        await self.input.put(-1)
        await asyncio.gather(self.send_to(), self.nic.execute())


async def router(router_channel, nat_channel, computers):
    # all messages are put on the channel
    # router will send these to the correct computer
    while True:
        addr, x, y = await router_channel.get()
        router_channel.task_done()
        if addr == 255:
            await nat_channel.put(x)
            await nat_channel.put(y)
        else:
            # send in order x, y
            for data in (x, y):
                await computers[addr].input.put(data)


def is_network_idle(computers):
    for computer in computers:
        if computer.input.qsize() != 0 and computer.output.qsize() != 0:
            return False
    return True


async def nat(nat_channel, computers):
    last_y = None

    while True:
        x = await nat_channel.get()
        nat_channel.task_done()
        y = await nat_channel.get()
        nat_channel.task_done()

        #print(f'NAT received {x},{y}')

        if is_network_idle(computers):
            if last_y == y:
                print(f'NAT sent {y} earlier')

            last_y = y
            
            #print(f'NAT sending {x} {y}')
            await computers[0].input.put(x)
            await computers[0].input.put(y)


async def run_network(program):
    router_channel = asyncio.Queue()
    nat_channel = asyncio.Queue()
    computers = [Computer(i, program, router_channel) for i in range(50)]

    tasks = [computer.run() for computer in computers]
    tasks.append(router(router_channel, nat_channel, computers))
    tasks.append(nat(nat_channel, computers))

    await asyncio.gather(*tasks)
    await router_channel.join()
    await nat_channel.join()
    print('after')


async def main():
    with open('d23.txt') as fin:
        program = [int(x) for x in fin.readline().split(',') if x]
    
    ret = await run_network(program)
    print(ret)


asyncio.run(main())
