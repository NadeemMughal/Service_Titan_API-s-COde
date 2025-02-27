from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI()

class Address(BaseModel):
    street: str
    unit: Optional[str]
    city: str
    state: str
    zip: str
    country: str

class Contact(BaseModel):
    type: str
    value: str
    memo: Optional[str]

class BookingRequest(BaseModel):
    source: str
    name: str
    address: Address
    contacts: List[Contact]
    customerType: Optional[str]
    start: Optional[str]
    summary: str
    campaignId: Optional[int]
    businessUnitId: Optional[int]
    jobTypeId: Optional[int]
    priority: Optional[str]
    isFirstTimeClient: bool
    uploadedImages: Optional[List[str]]
    isSendConfirmationEmail: Optional[bool]
    externalId: str

async def get_access_token(client_id: str, client_secret: str, tenant_id: str) -> str:
    url = "https://auth.servicetitan.io/connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

async def get_booking_status(booking_id: int, access_token: str) -> dict:
    url = f"https://public-api-gateway.st.dev/crm/v2/bookings/{booking_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@app.post("/create-booking")
async def create_booking(booking: BookingRequest):
    access_token = await get_access_token(
        client_id="cid.tqn91qx5m8xp3ya71s1kauztd",
        client_secret="cs1.1jof6blgkvq0k34ws1lp53kwzu8qvlvh611ksrahruaigpyvzd",
        tenant_id="1561207974",
    )
    url = f"https://public-api-gateway.st.dev/crm/v2/tenant/{tenant_id}/booking-provider/{booking_provider_id}/bookings"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await httpx.AsyncClient().post(url, json=booking.dict(), headers=headers)
    if response.status_code == 201:
        booking_data = response.json()
        booking_id = booking_data.get("id")
        # Check booking status
        booking_status = await get_booking_status(booking_id, access_token)
        if booking_status.get("status") == "Scheduled":
            return {"message": "Booking created and scheduled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Booking creation failed")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
