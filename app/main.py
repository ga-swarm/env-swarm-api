
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.main import router

from dbconnector import token_dispatcher
from swarm import swarm

app = FastAPI()
app.include_router(router)

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

# @router.get("/tx/{tx_hash}")
# async def get_tx_status(tx_hash: str, response: Response):
#     """
#     Returns transaction state from blockchain
#     """
#     return {
#         "tx_hash": 0,
#         "tx_status": -1 ,
#         'tokenId': 1
#     }

