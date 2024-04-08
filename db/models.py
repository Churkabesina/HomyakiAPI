from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

wallet = Table(
    'wallets',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('address', String),
    Column('key', String),
    Column('balance', Integer)
)
