
import logging
from router.main import router
from dbconnector.dbconnector import dbconnector

from fastapi import Depends
from fastapi.security.api_key import APIKey
from router.auth import get_app_id

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

logger = logging.getLogger(__name__)

# ---------- 721 NFT ----------
@router.get("/discover/721/user/{chain_id}/{user_address}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
            'contract_address': contract_address,
        }
        resp = dbconnector.get_tokens_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp

@router.get("/discover/721/user/{chain_id}/{user_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
        }
        resp = dbconnector.get_tokens_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/discover/721/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str = None,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'token_id': token_id,
        }
        resp = dbconnector.get_tokens_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/discover/721/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
        }
        resp = dbconnector.get_tokens_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
# ---------- END 721 NFT ----------

# ---------- 1155 NFT ----------
@router.get("/discover/1155/user/{chain_id}/{user_address}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
            'contract_address': contract_address,
        }
        resp = dbconnector.get_tokens_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp

@router.get("/discover/1155/user/{chain_id}/{user_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
        }
        resp = dbconnector.get_tokens_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp

@router.get("/discover/1155/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str = None,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'token_id': token_id,
        }
        resp = dbconnector.get_tokens_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/discover/1155/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
        }
        resp = dbconnector.get_tokens_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
# ---------- END 1155 NFT ----------

# ---------- 721 wNFT ----------
@router.get("/wnft_collateral/721/user/{chain_id}/{user_address}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_721_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft_collateral/721/user/{chain_id}/{user_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_721_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/721/user/{chain_id}/{user_address}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/721/user/{chain_id}/{user_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft_collateral/721/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'token_id': token_id,
        }
        resp = dbconnector.get_wnfts_721_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft_collateral/721/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
        }
        resp = dbconnector.get_wnfts_721_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/721/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'token_id': token_id,
        }
        resp = dbconnector.get_wnfts_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/721/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
        }
        resp = dbconnector.get_wnfts_721(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
# ---------- END 721 wNFT ----------

# ---------- 1155 wNFT ----------
@router.get("/wnft_collateral/1155/user/{chain_id}/{user_address}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_1155_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft_collateral/1155/user/{chain_id}/{user_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_1155_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/1155/user/{chain_id}/{user_address}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/1155/user/{chain_id}/{user_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'owner': user_address,
        }
        resp = dbconnector.get_wnfts_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft_collateral/1155/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'token_id': token_id,
        }
        resp = dbconnector.get_wnfts_1155_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft_collateral/1155/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
        }
        resp = dbconnector.get_wnfts_1155_with_collaterals(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/1155/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'token_id': token_id,
        }
        resp = dbconnector.get_wnfts_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/wnft/1155/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
        }
        resp = dbconnector.get_wnfts_1155(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
# ---------- END 1155 wNFT ----------

@router.get("/royalty/user/{chain_id}/{user_address}")
async def get_token_uri(
    chain_id: int,
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'chain_id': chain_id,
            'royalty_for': user_address,
        }
        resp = dbconnector.get_royalties(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp


@router.get("/collateral/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str,
    api_id: APIKey = Depends(get_app_id)
):

    resp = {}
    try:
        resp = dbconnector.get_wnft_collaterals(chain_id, contract_address, token_id)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/original/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
            'token_id': token_id,
        }

        resp = dbconnector.get_wnft_by_nft(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/original/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        query = {
            'contract_address': contract_address,
        }

        resp = dbconnector.get_wnft_by_nft(chain_id, query, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/crossings/user/{user_address}")
async def get_token_uri(
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        resp = dbconnector.get_crossings(user_address, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/burns/user/{user_address}")
async def get_token_uri(
    user_address: str,
    page: int = 1, size: int = 10,
    api_id: APIKey = Depends(get_app_id)
):

    if size < 1:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=f"Size cannot be less than 1"
        )

    resp = {}
    try:
        resp = dbconnector.get_burns(user_address, (page - 1) * size, size,)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/token/{chain_id}")
async def get_token_uri(
    chain_id: int,
    api_id: APIKey = Depends(get_app_id)
):

    resp = {}
    try:
        query = {
            'chain_id': chain_id,
        }

        resp = dbconnector.get_token(query)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp
@router.get("/token/{chain_id}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    api_id: APIKey = Depends(get_app_id)
):

    resp = {}
    try:
        query = {
            'chain_id': chain_id,
            'contract_address': contract_address,
        }

        resp = dbconnector.get_token(query)
    except Exception as e:
        # logger.warning('Error:', e, 'Params:', chain_id, user_address)
        return { 'error': e.args[0] }

    return resp

@router.get("/update/{chain_id}/{contract_address}/{token_id}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    token_id: str,
    api_id: APIKey = Depends(get_app_id)
):
    try:
        dbconnector.request_update(chain_id, contract_address, token_id)
        return True
    except Exception as e:
        return False
@router.get("/update_token/{chain_id}/{asset_type}/{contract_address}")
async def get_token_uri(
    chain_id: int,
    contract_address: str,
    asset_type: int,
    api_id: APIKey = Depends(get_app_id)
):
    try:
        dbconnector.request_update_token(chain_id, asset_type, contract_address)
        return True
    except Exception as e:
        return False
# ---------- END wNFT ----------