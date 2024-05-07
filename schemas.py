from pydantic import BaseModel, Field


class Wallet(BaseModel):
    id: int
    address: str = Field(examples=['0x0000000000000000000000000000000000000000'])
    balance: int


class WalletTemp(BaseModel):  # Temp, временный потому, что не могу отдать пока баланс во время, не успеваю за чейном
    id: int
    address: str = Field(examples=['0x0000000000000000000000000000000000000000'])


class WalletPrivate(Wallet):
    key: str = Field(examples=['0x0000000000000000000000000000000000000000000000000000000000000000'])


class YEplayNftData(BaseModel):
    data: str


class ResultNftData(BaseModel):
    data: int


class NftStorage(BaseModel):
    account: str = Field(examples=['0x0000000000000000000000000000000000000000000000000000000000000000'])
    storage: list[int]


class TxnStatus(BaseModel):
    txn_hash: str = Field(examples=['0x0000000000000000000000000000000000000000000000000000000000000000'])
    status: bool


class MetaDataJson(BaseModel):
    meta_data_uuid: str
    is_played: bool = Field(examples=[False])


class MintYePlayResponse(MetaDataJson):
    txn_hash: str = Field(examples=['0x0000000000000000000000000000000000000000000000000000000000000000'])


class BuyYePlayResponse(MintYePlayResponse):
    pay_txn_hash: str = Field(examples=['0x0000000000000000000000000000000000000000000000000000000000000000'])
