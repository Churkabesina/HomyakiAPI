from sqlalchemy import create_engine, insert
from . import models

engine = create_engine('sqlite+pysqlite:///wallets.db', echo=True)


def __create_db():
    models.metadata.create_all(engine)


def __drop_db():
    models.metadata.drop_all(engine)


def insert_wallet(address: str, private_key: str):
    stmt = insert(models.wallet).values({'address': address, 'key': private_key, 'balance': 0})
    with engine.connect() as conn:
        res = conn.execute(stmt)
        conn.commit()
        return res.lastrowid
