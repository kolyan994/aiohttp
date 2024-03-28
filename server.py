from aiohttp import web
from models import init_db, Advertisement


async def get_all_advertisements(request):
	async with request.app['db'].acquire() as conn:
		advertisements = await conn.execute(Advertisement.select())
		output = []
		async for ad in advertisements:
			ad_data = {'id': ad.id, 'title': ad.title, 'description': ad.description, 'owner': ad.owner}
			output.append(ad_data)
		return web.json_response({'advertisements': output})


async def get_advertisement(request):
	advertisement_id = request.match_info['id']
	async with request.app['db'].acquire() as conn:
		advertisement = await conn.execute(Advertisement.select().where(Advertisement.c.id == advertisement_id))
		ad = await advertisement.fetchone()
		if ad is None:
			return web.json_response({'error': 'Advertisement not found'}, status=404)
		return web.json_response({'id': ad.id, 'title': ad.title, 'description': ad.description, 'owner': ad.owner})


async def delete_advertisement(request):
	advertisement_id = request.match_info['id']
	async with request.app['db'].acquire() as conn:
		await conn.execute(Advertisement.delete().where(Advertisement.c.id == advertisement_id))
		return web.json_response({'message': 'Advertisement deleted successfully'})


async def update_advertisement(request):
	advertisement_id = request.match_info['id']
	data = await request.json()

	async with request.app['db'].acquire() as conn:
		await conn.execute(Advertisement.update().values(title=data.get('title'), description=data.get('description'),
														 owner=data.get('owner')).where(
			Advertisement.c.id == advertisement_id))

	return web.json_response({'message': 'Advertisement updated successfully'})


async def init_app():
	app = web.Application()
	app['db'] = await init_db()

	app.router.add_get('/advertisements', get_all_advertisements)
	app.router.add_get('/advertisements/{id}', get_advertisement)
	app.router.add_delete('/advertisements/{id}', delete_advertisement)
	app.router.add_put('/advertisements/{id}', update_advertisement)

	return app


if __name__ == '__main__':
	web.run_app(init_app())