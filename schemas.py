from pydantic import BaseModel, Field


class Wallet(BaseModel):
    id: int
    address: str = Field(examples=['0x0000000000000000000000000000000000000000'])
    balance: int


class WalletPrivate(Wallet):
    key: str = Field(examples=['0x0000000000000000000000000000000000000000000000000000000000000000'])


class NftData(BaseModel):
    data: str
