from sqlalchemy import create_engine, insert, update, select
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


def update_account_balance(address: str, new_balance: int):
    stmt = update(models.wallet).where(models.wallet.c.address == address).values({'balance': new_balance})
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


def get_id_by_address(address: str):
    stmt = select(models.wallet.c.id).where(models.wallet.c.address == address)
    with engine.connect() as conn:
        res = conn.execute(stmt).first()
        return res


def get_private_by_address(address: str):
    stmt = select(models.wallet.c.key).where(models.wallet.c.address == address)
    with engine.connect() as conn:
        res = conn.execute(stmt).first()
        return res
