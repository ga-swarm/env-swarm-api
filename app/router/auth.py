
import hashlib
import datetime
import logging

from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from dbconnector.dbconnector import dbconnector

logger = logging.getLogger(__name__)

auth_header = APIKeyHeader(name='Authorization', auto_error=False)

async def get_app_id(
    auth_header: str = Security(auth_header)
):

    # Key updates every KEY_ACTIVE_TIME seconds
    KEY_ACTIVE_TIME = 300 # s
    # Key shoud be checked for now, now + KEY_CHECK_OFFSET, now - KEY_CHECK_OFFSET
    KEY_CHECK_OFFSET = 30 # s

    logger.debug(f'Trying to auth client with auth data {auth_header}')

    if auth_header is None:
        logger.debug(f'Client with empty app_id or app_key')
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"Put Authorization header to request: <APP_ID>.<APP_KEY>"
        )
    try:
        auth_app_id  = auth_header.split('.')[0]
        auth_key     = auth_header.split('.')[1]
    except Exception:
        logger.debug(f'Client with bad app_id or app_key')
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"Put Authorization header to request: <APP_ID>.<APP_KEY>"
        )

    if auth_app_id is None or auth_app_id is None:
        logger.debug(f'Client with empty app_id or app_key')
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"Put Authorization header to request: <APP_ID>.<APP_KEY>"
        )

    client = dbconnector.get_app_key(auth_app_id)
    if not len(client):
        logger.debug(f'Client with app_id {auth_app_id} not found')
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"APP_ID not found"
        )
    client = client[0]

    now = int(datetime.datetime.timestamp(datetime.datetime.now()))

    if client['expires_when'] is not None:
        logger.debug(f'Client with app_id {auth_app_id} expires {client["expires_when"]}')
        expires_when = int(datetime.datetime.timestamp(client['expires_when']))
        if now > expires_when:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail=f"Client permission has expired"
            )

    app_key  = client['app_key']
    app_name = client['app_name']
    possible_keys = [
        hashlib.sha256(f'{app_name}{app_key}{int((now - KEY_CHECK_OFFSET) / KEY_ACTIVE_TIME)}'.encode('UTF-8')).hexdigest(),
        hashlib.sha256(f'{app_name}{app_key}{int((now)                    / KEY_ACTIVE_TIME)}'.encode('UTF-8')).hexdigest(),
        hashlib.sha256(f'{app_name}{app_key}{int((now + KEY_CHECK_OFFSET) / KEY_ACTIVE_TIME)}'.encode('UTF-8')).hexdigest(),
    ]
    logger.debug(f'Client with app_id {auth_app_id} sends key: {auth_key}. Possible keys {possible_keys}')

    if auth_key not in possible_keys:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"APP_KEY is invalid"
        )

    return auth_app_id