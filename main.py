import xows
import asyncio

async def start():
	async with xows.XoWSClient('170.2.245.212', username='admin', password='Trucks08!') as client:
		def callback(data, id_):
			print(f'Feedback (Id {id_}): {data}')

		print('Status Query:',
			await client.xQuery(['Status', '**', 'DisplayName']))

#		print('Command:',
#			  await client.xCommand(['SystemUnit', 'Boot']))

#		await client.wait_until_closed() 

asyncio.run(start())