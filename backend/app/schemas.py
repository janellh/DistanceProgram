from pydantic import BaseModel, Field, constr

AddressStr = constr(strip_whitespace=True, min_length=3, max_length=255)

class DistanceRequest(BaseModel):
    source: AddressStr = Field(description="Source address")
    destination: AddressStr = Field(description="Destination address")

class DistanceResponse(BaseModel):
    km: float
    mi: float

class HistoryItem(BaseModel):
    id: int
    source: str
    destination: str
    km: float
    mi: float
    created_at: str

class HistoryResponse(BaseModel):
    items: list[HistoryItem]
