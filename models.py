import aiomysql
from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

Advertisement = Table(
	'advertisements',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('title', String(255)),
	Column('description', String(1000)),
	Column('owner', String(255))
)


async def init_db():
	pool = await aiomysql.create_pool(
		host='localhost',
		port=3306,
		user='user',
		password='password',
		db='aiohttp_db',
		autocommit=True
	)

	async with pool.acquire() as conn:
		await conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS advertisements (
				id SERIAL PRIMARY KEY,
				title VARCHAR(255) NOT NULL,
				description VARCHAR(1000) NOT NULL,
				owner VARCHAR(255) NOT NULL
			)
			"""
		)

	return pool