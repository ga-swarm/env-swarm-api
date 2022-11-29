
import logging
import requests
import base64
import json
import os
from router.main import router
from pydantic import BaseModel
from typing import List
logging.basicConfig(
   format='%(asctime)s->%(levelname)s:[in %(filename)s:%(lineno)d]:%(message)s', 
   level= int(os.environ.get('APP_LOGLEVEL', 20))
)
logger = logging.getLogger(__name__)

SWARM_GET_STAMPS_URL = os.environ.get('SWARM_GET_STAMPS_URL')
SWARM_POST_TAGS_URL  = os.environ.get('SWARM_POST_TAGS_URL')
SWARM_POST_FILE_URL  = os.environ.get('SWARM_POST_FILE_URL')

if SWARM_GET_STAMPS_URL is None or SWARM_GET_STAMPS_URL == '':
    print('No SWARM_GET_STAMPS_URL variable in .env')
if SWARM_POST_TAGS_URL is None or SWARM_POST_TAGS_URL == '':
    print('No SWARM_POST_TAGS_URL variable in .env')
if SWARM_POST_FILE_URL is None or SWARM_POST_FILE_URL == '':
    print('No SWARM_POST_FILE_URL variable in .env')

class Nftprop(BaseModel):
    type: str
    name: str

class Nftdata(BaseModel):
    name: str
    desc: str
    image: str
    mime: str
    props: List[Nftprop]

def get_swarm_batchid():
    r = ""
    try:
        res = requests.get(SWARM_GET_STAMPS_URL, timeout=3)
        get_res = res.json()
        r = get_res["stamps"][0]["batchID"]
    except Exception as e:
        print(e)
    return r

def get_swarm_tag():
    r = ""
    try:
        res = requests.post(SWARM_POST_TAGS_URL, timeout=3)
        get_res = res.json()
        r = get_res["uid"]
    except Exception as e:
        print(e)
    return r

def prepare_nft_json(data,refid):
    r = {}
    if refid:
        r.update({ "image": '{}/{}'.format(SWARM_POST_FILE_URL,refid) })
    if data.name:
        r.update({ "name": data.name })
    if data.desc:
        r.update({ "description": data.desc })
    if data.props:
        attributes = []
        for attr in data.props:
            attributes.append({ "trait_type": attr.type, "value": attr.name })
        r.update({ "attributes": attributes })
    return r

@router.post("/mint/new")
async def post_swarm_data(data: Nftdata):
    print('lol')
    r = {}

    # prepare headers from data:image/png;base64
    image_type,image_base64 = data.image.split(';')
    image_type = image_type.replace("data:", "")
    image_base64 = image_base64.replace("base64,", "")
    content_type = data.mime if image_type != data.mime else image_type
    logger.debug('===post_swarm_data data:{}'.format(data))
    try:
        # get swarm batch id and tag id
        batchid = get_swarm_batchid()
        tagid = get_swarm_tag()

        if len(str(batchid)) and len(str(tagid)):
            try:
                headers = {
                    'Swarm-Postage-Batch-Id': str(batchid),
                    'Swarm-Pin': 'true',
                    'Swarm-Tag': str(tagid),
                    'Content-Type': content_type,
                }
                body = base64.b64decode(image_base64)
                post = requests.post(SWARM_POST_FILE_URL, data=body, headers=headers, timeout=5)
                post_res = post.json()
                reference_id = post_res.get('reference')
                if reference_id != "None":
                    logger.debug(f'Image Reference ID: {reference_id}')
                    ret_json = prepare_nft_json(data,reference_id)
                    if ret_json:
                        loaded_json = json.dumps(ret_json)
                        try:
                            headers_json = {
                                'Swarm-Postage-Batch-Id': str(batchid),
                                'Swarm-Pin': 'true',
                                'Content-Type': 'application/json',
                            }
                            post_json = requests.post(SWARM_POST_FILE_URL, data=loaded_json, headers=headers_json, timeout=5)
                            post_json_res = post_json.json()
                            reference_id_json = post_json_res.get('reference')
                            if reference_id_json != "None":
                                logger.debug(f'Json Reference ID: {reference_id_json}')
                                r.update({ "json": reference_id_json })
                        except Exception as e:
                            print(e)
                        r.update(ret_json)
                else:
                    logger.debug(f'Error: no Swarm reference ID')
            except Exception as e:
                print(e)
                logger.debug(f'Error when posting to Swarm')
            logger.debug(f'Batch ID: {batchid}')
        else:
            logger.debug(f'Error: no batch ID or tag ID')
    except Exception as e:
        print(e)

    return r
