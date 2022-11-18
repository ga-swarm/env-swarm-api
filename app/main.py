
from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from router.main import router

from swarm import swarm

app = FastAPI()

origins = [
    '*',
    'https://192.168.0.4:3002',
    'https://192.168.0.4:3005',
    'https://stage.app.envelop.is/',
    'https://app.envelop.is/',
    'https://stage.dao.envelop.is/',
    'https://dao.envelop.is/',
    'https://stage.appv1.envelop.is/',
    'https://appv1.envelop.is/',
    'https://api.envelop.is/',
    'https://stage.api.envelop.is/',
    'https://envelop.is/',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/mint/health")
async def health():
    return { "health": "ok" }

app.include_router(router)
