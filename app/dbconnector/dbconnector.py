
from itertools import chain
import logging
import os

import psycopg
from psycopg.rows import dict_row

class DBConnector:

    def __init__(self) -> None:

        try:
            self.db_params = {
                'DB_USER': os.environ.get('DB_USER'),
                'DB_PASSWORD': os.environ.get('DB_PASSWORD'),
                'DB_HOST': os.environ.get('DB_HOST'),
                'DB_PORT': int(os.environ.get('DB_PORT')),
                'DB_DATABASE': os.environ.get('DB_DATABASE'),
            }

            self.connect()
        except Exception as e:
            logging.error('Cannot connect to db:', e)

    def connect(self):
        self.connection = psycopg.connect(f'host={ self.db_params["DB_HOST"] } port={ self.db_params["DB_PORT"] } user={ self.db_params["DB_USER"] } password={ self.db_params["DB_PASSWORD"] } dbname={ self.db_params["DB_DATABASE"] } ', options="-c search_path=chain_1,chain_4,chain_56,chain_137,dao,public")

    ########## AUTH ##########
    def get_app_key(self, app_id: str):
        if app_id is None:
            return []

        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                SELECT *
                FROM public.auth_clients
                WHERE LOWER("public"."auth_clients"."app_id") = '{app_id.lower()}'
            '''
            cur.execute(query)
            output = []
            records = cur.fetchall()
            for item in records:
                output.append(item)

            return output
    ########## END AUTH ##########

    def process_data_from_db(self, records: list, chain_id: int, asset_type: int = None):
        wnft_contracts = self.get_wnft_contracts(chain_id)

        output = []
        for item in records:
            # if asset_type is not None:
            #     item['asset_type'] = asset_type

            if 'token_id' in item and item['token_id'] is not None:
                item['token_id'] = str(item['token_id'])

            if 'in_token_id' in item and item['in_token_id'] is not None:
                item['in_token_id'] = str(item['in_token_id'])

            if 'target_token_id' in item and item['target_token_id'] is not None:
                item['target_token_id'] = str(item['target_token_id'])

            if 'unwrap_destinition' in item:
                item['unwrap_destination'] = str(item['unwrap_destinition'])
                del item['unwrap_destinition']

            if 'locks' in item and item['locks'] is not None:
                for iitem in item['locks']:
                    if 'lockType' in iitem and iitem['lockType'] is not None:
                        iitem['lockType'] = '0x{0:0{1}X}'.format(iitem['lockType'],2)

            if 'fees' in item and item['fees'] is not None:
                for iitem in item['fees']:
                    if 'feeType' in iitem and iitem['feeType'] is not None:
                        iitem['feeType'] = '0x{0:0{1}X}'.format(iitem['feeType'],2)

            if 'rules' in item and item['rules'] is not None:
                item['rules'] = '0x{0:0{1}X}'.format(int(item['rules'], 2), 4)

            # if 'contract_address' in item and item['contract_address'] is not None:
            #     if item['contract_address'].lower() in wnft_contracts:
            #         item['is_wnft'] = True
            #     else:
            #         item['is_wnft'] = False

            output.append(item)

        return output

    def get_wnft_contracts(self, chain_id: int):
        if self.connection.closed:
            self.connect()

        if chain_id == 0:
            return []

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:

            query = f'''
                SELECT *
                FROM public.wnft_contracts
                WHERE "chain_id" = {str(chain_id)}
            '''

            cur.execute(query)
            output = []
            records = cur.fetchall()

            for item in records:
                output.append(item['contract_address'].lower())

            return output

    def get_tokens_721(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query_filter = []
            if 'owner' in search_filter:
                query_filter.append(f'''n.owner = '{search_filter['owner'].lower()}' ''')

            if 'contract_address' in search_filter:
                query_filter.append(f'''n.contract_address = '{search_filter['contract_address'].lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''n.token_id = '{search_filter['token_id'].lower()}' ''')

            query = f'''
                SELECT 3 as asset_type,
                    CASE
                    WHEN w.contract_address is null THEN false
                    ELSE true
                END as is_wnft,
                    n.*, w.in_contract_address, in_token_id, in_asset_type
                FROM chain_{str(chain_id)}.token_721 n
                left join chain_4.wnft_info w
                on w.contract_address = n.contract_address and w.token_id = n.token_id
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                ORDER BY -blocknumber, -logindex LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id, 3)

    def get_tokens_1155(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query_filter = []
            if 'owner' in search_filter:
                query_filter.append(f'''N.owner = '{search_filter['owner'].lower()}' ''')

            if 'contract_address' in search_filter:
                query_filter.append(f'''N.contract_address = '{search_filter['contract_address'].lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''N.token_id = '{search_filter['token_id'].lower()}' ''')

            query = f'''
                SELECT
                    4 as asset_type,
                    CASE
                    WHEN w.contract_address is null THEN false
                        ELSE true
                    END as is_wnft,
                    n.*, w.in_contract_address, in_token_id, in_asset_type,
                    chain_{str(chain_id)}.totalsupply1155( N.contract_address, n.token_id) AS "totalSupply"
                FROM chain_{str(chain_id)}.token_1155_balances n
                left join chain_4.wnft_info w
                on w.contract_address = n.contract_address and w.token_id = n.token_id
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                ORDER BY -blocknumber, -logindex LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id, 4)

    def get_wnfts_721_with_collaterals(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query_filter = []
            if 'owner' in search_filter:
                query_filter.append(f'''N.OWNER = '{str(search_filter['owner']).lower()}' ''')

            if 'contract_address' in search_filter:
                query_filter.append(f'''N.CONTRACT_ADDRESS = '{str(search_filter['contract_address']).lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''N.TOKEN_ID = '{str(search_filter['token_id']).lower()}' ''')

            query = f'''
                SELECT
                (SELECT
                JSONB_AGG(JSONB_BUILD_OBJECT(
                    'assetType', V.COLLATERAL_TYPE,
                    'contractAddress',V.COLLATERAL_ADDRESS,
                    'tokenId', V.COLLATERAL_TOKEN_ID,
                    'amount', V.COLLATERAL_BALANCE::varchar)) AS COLLATERAL_JSON
                FROM CHAIN_{str(chain_id)}.WNFT_VAULT V
                WHERE WNFT_ADDRESS = W.contract_address
                AND WNFT_TOKEN_ID = W.token_id ),
                N.*,
                    W.contract_address,
                    W.token_id,
                    W.wnft_type as asset_type,
                    W.initial_out_balance,
                    W.in_asset_type,
                    W.in_contract_address,
                    W.in_token_id,
                    W.in_amount::varchar,
                    W.unwrap_destinition as unwrap_destination,
                    W.rules,
                    W.is_burned,
                    W.fees,
                    W.locks,
                    W.royalties,
                    W.first_owner,
                    W.create_tx,
                    W.burn_tx,
                    W.inserted,
                    W.updated,
                    W.updated_by
                FROM CHAIN_{str(chain_id)}.TOKEN_721 N
                INNER JOIN CHAIN_{str(chain_id)}.WNFT_INFO W ON W.CONTRACT_ADDRESS = N.CONTRACT_ADDRESS
                AND W.TOKEN_ID = N.TOKEN_ID
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                ORDER BY inserted DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id, 3)

    def get_wnfts_721(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query_filter = []
            if 'owner' in search_filter:
                query_filter.append(f'''N.OWNER = '{str(search_filter['owner']).lower()}' ''')

            if 'contract_address' in search_filter:
                query_filter.append(f'''N.CONTRACT_ADDRESS = '{str(search_filter['contract_address']).lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''N.TOKEN_ID = '{str(search_filter['token_id']).lower()}' ''')

            query = f'''
                SELECT
                    n.*,
                    w.contract_address,
                    w.token_id,
                    w.wnft_type as asset_type,
                    w.initial_out_balance,
                    w.in_asset_type,
                    w.in_contract_address,
                    w.in_token_id,
                    w.in_amount::varchar,
                    w.unwrap_destinition as unwrap_destination,
                    w.rules,
                    w.is_burned,
                    w.fees,
                    w.locks,
                    w.royalties,
                    w.first_owner,
                    w.create_tx,
                    w.burn_tx,
                    w.inserted,
                    w.updated,
                    w.updated_by
                FROM chain_{str(chain_id)}.token_721 n
                inner join chain_{str(chain_id)}.wnft_info w
                on w.contract_address = n.contract_address and w.token_id = n.token_id
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                ORDER BY inserted DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id, 3)

    def get_wnfts_1155_with_collaterals(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query_filter = []
            if 'owner' in search_filter:
                query_filter.append(f'''N.OWNER = '{str(search_filter['owner']).lower()}' ''')

            if 'contract_address' in search_filter:
                query_filter.append(f'''N.CONTRACT_ADDRESS = '{str(search_filter['contract_address']).lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''N.TOKEN_ID = '{str(search_filter['token_id']).lower()}' ''')

            query = f'''
                SELECT
                chain_{str(chain_id)}.totalsupply1155(n.contract_address, n.token_id) AS "totalSupply",
                (SELECT
                JSONB_AGG(JSONB_BUILD_OBJECT(
                    'assetType', V.COLLATERAL_TYPE,
                    'contractAddress',V.COLLATERAL_ADDRESS,
                    'tokenId', V.COLLATERAL_TOKEN_ID,
                    'amount', V.COLLATERAL_BALANCE::varchar)) AS COLLATERAL_JSON
                FROM CHAIN_{str(chain_id)}.WNFT_VAULT V
                WHERE WNFT_ADDRESS = W.contract_address
                AND WNFT_TOKEN_ID = W.token_id ),
                    N.*,
                    w.contract_address,
                    w.token_id,
                    w.wnft_type as asset_type,
                    w.initial_out_balance,
                    w.in_asset_type,
                    w.in_contract_address,
                    w.in_token_id,
                    w.in_amount::varchar,
                    w.unwrap_destinition as unwrap_destination,
                    w.rules,
                    w.is_burned,
                    w.fees,
                    w.locks,
                    w.royalties,
                    w.first_owner,
                    w.create_tx,
                    w.burn_tx,
                    w.inserted,
                    w.updated,
                    w.updated_by
                FROM CHAIN_{str(chain_id)}.TOKEN_1155_BALANCES N
                INNER JOIN CHAIN_{str(chain_id)}.WNFT_INFO W ON W.CONTRACT_ADDRESS = N.CONTRACT_ADDRESS
                AND W.TOKEN_ID = N.TOKEN_ID
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                AND "balance" > 0
                ORDER BY inserted DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id, 4)

    def get_wnfts_1155(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query_filter = []
            if 'owner' in search_filter:
                query_filter.append(f'''N.OWNER = '{str(search_filter['owner']).lower()}' ''')

            if 'contract_address' in search_filter:
                query_filter.append(f'''N.CONTRACT_ADDRESS = '{str(search_filter['contract_address']).lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''N.TOKEN_ID = '{str(search_filter['token_id']).lower()}' ''')

            query = f'''
                SELECT
                    n.*,
                    w.contract_address,
                    w.token_id,
                    w.wnft_type as asset_type,
                    w.initial_out_balance,
                    w.in_asset_type,
                    w.in_contract_address,
                    w.in_token_id,
                    w.in_amount::varchar,
                    w.unwrap_destinition as unwrap_destination,
                    w.rules,
                    w.is_burned,
                    w.fees,
                    w.locks,
                    w.royalties,
                    w.first_owner,
                    w.create_tx,
                    w.burn_tx,
                    w.inserted,
                    w.updated,
                    w.updated_by,
                    chain_{str(chain_id)}.totalsupply1155(n.contract_address, n.token_id) AS "totalSupply"
                FROM chain_{str(chain_id)}.token_1155_balances n
                inner join chain_{str(chain_id)}.wnft_info w
                on w.contract_address = n.contract_address and w.token_id = n.token_id
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                AND "balance" > 0
                ORDER BY inserted DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id, 4)

    def get_wnft_collaterals(self, chain_id: int, contract_address: str, token_id: str):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                SELECT *,
                chain_{str(chain_id)}.totalsupply1155('{str(contract_address)}', '{str(token_id)}') AS "totalSupply"
                FROM chain_{str(chain_id)}.wnft_vault
                where wnft_address = '{str(contract_address.lower())}'
                and wnft_token_id = '{str(token_id)}';
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id)

    def get_wnft_by_nft(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:

            query_filter = []
            if 'contract_address' in search_filter:
                query_filter.append(f'''in_contract_address = '{str(search_filter['contract_address']).lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''in_token_id = '{str(search_filter['token_id']).lower()}' ''')

            query = f'''
                SELECT
                    w.contract_address,
                    w.token_id,
                    w.wnft_type as asset_type,
                    w.initial_out_balance,
                    w.in_asset_type,
                    w.in_contract_address,
                    w.in_token_id,
                    w.in_amount::varchar,
                    w.unwrap_destinition as unwrap_destination,
                    w.rules,
                    w.is_burned,
                    w.fees,
                    w.locks,
                    w.royalties,
                    w.first_owner,
                    w.create_tx,
                    w.burn_tx,
                    w.inserted,
                    w.updated,
                    w.updated_by,
                    chain_{str(chain_id)}.totalsupply1155(w.contract_address, w.token_id) AS "totalSupply"
                FROM chain_{str(chain_id)}.wnft_info w
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                ORDER BY inserted DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id)

    def request_update(self, chain_id: int, contract_address: str, token_id: str):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                CALL public.request_notify(
                'wnft_info_update',
                '{str(chain_id)};{str(contract_address.lower())};{str(token_id)}'
                )
            '''

            try:
                cur.execute(query)
            except Exception:
                cur.execute("ROLLBACK")
                raise Exception('Cannot request update nfts')

            return []

    def request_update_token(self, chain_id: int, asset_type: int, contract_address: str):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                CALL public.upsert_dict_contract(
                    {str(chain_id)},
                    '{str(contract_address)}',
                    {str(asset_type)},
                    false
                );
            '''
            try:
                cur.execute(query)
            except Exception:
                cur.execute("ROLLBACK")
                raise Exception('Cannot request update tokens')

            return []

    def get_crossings(self, user_address: str, page: int, size: int):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                SELECT * FROM public.v_crosschains vc
                where
                    ( crossing_initiator = '{user_address.lower()}' and target_owner is null )
                    or
                    ( target_owner = '{user_address.lower()}' and target_burn_txhash is null )
                ORDER BY sortorder DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, 0)

    def get_burns(self, user_address: str, page: int, size: int):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                SELECT * FROM public.v_crosschains vc
                INNER JOIN (
                    select max(id) as id from public.v_crosschains
                    group by source_nft_address, source_nft_token_id
                ) vcm on vc.id=vcm.id
                where
                    ( target_owner  = '{user_address.lower()}' )
                    or
                    ( target_burner_address = '{user_address.lower()}' and source_nft_status = 'frozen')
                ORDER BY sortorder DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, 0)

    def get_token(self, search_filter: dict):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:

            query_filter = []
            if 'contract_address' in search_filter:
                query_filter.append(f'''v.contract_address = '{str(search_filter['contract_address']).lower()}' ''')
            if 'chain_id' in search_filter:
                query_filter.append(f'''v.chain_id = '{str(search_filter['chain_id']).lower()}' ''')

            query = f'''
                SELECT p.param_name, t.description, v.chain_id, v.contract_address, v.param_value, v.updated
                FROM public.contracts_params_values v
                    inner join public.dict_params_by_type p on p.id=v.param_id
                    inner join public.dict_contract_types t on t.id=p.contract_type_id
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                ORDER BY updated DESC
            '''

            cur.execute(query)
            records = cur.fetchall()

            def get_asset_type(name: str):
                if 'native' in name: return 1
                if '20' in name: return 2
                if '721' in name: return 3
                if '1155' in name: return 4
                return 0

            output = []
            for item in records:
                found = list(filter(lambda x: x['contract_address'] == item['contract_address'], output ))
                if len(found):
                    output = list(filter(lambda x: x['contract_address'] != item['contract_address'], output ))
                    obj = found[0]
                    obj[item['param_name']] = item['param_value']
                    output.append(obj)
                else:
                    output.append({
                        'contract_address': item['contract_address'],
                        item['param_name']: item['param_value'],
                        'asset_type': get_asset_type(item['description']),
                    })


            return output

    def get_royalties(self, chain_id: int, search_filter: dict, page: int, size: int):
        if self.connection.closed:
            self.connect()

        if chain_id not in [ 1, 4, 5, 56, 137 ]:
            raise Exception('Unsupported chain')

        with self.connection.cursor(row_factory=dict_row) as cur:
            query_filter = []
            if 'chain_id' in search_filter:
                query_filter.append(f'''chain_id = '{str(search_filter['chain_id']).lower()}' ''')

            if 'contract_address' in search_filter:
                query_filter.append(f'''contract_address = '{str(search_filter['contract_address']).lower()}' ''')

            if 'token_id' in search_filter:
                query_filter.append(f'''token_id = '{str(search_filter['token_id']).lower()}' ''')

            if 'royalty_from' in search_filter:
                query_filter.append(f'''royalty_from = '{str(search_filter['royalty_from']).lower()}' ''')

            if 'royalty_for' in search_filter:
                query_filter.append(f'''royalty_for = '{str(search_filter['royalty_for']).lower()}' ''')

            if 'royalty_token' in search_filter:
                query_filter.append(f'''royalty_token = '{str(search_filter['royalty_token']).lower()}' ''')

            query_filter.append(f'''royalty_token is not null''')

            query = f'''
                SELECT *
	            FROM public.v_royalties
                { 'WHERE ' + ' AND '.join(query_filter) if len(query_filter) else '' }
                ORDER BY blocknumber DESC LIMIT {size} OFFSET {page}
            '''

            cur.execute(query)
            records = cur.fetchall()

            return self.process_data_from_db(records, chain_id, 4)

    def get_erc20_balance_by_datetime(self, data: dict,address: str):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            # get balance
            query = f''' SELECT public.get_erc20_balance_by_datetime({int(data['chain_id'])},'{data['token'].lower()}','{address.lower()}','{data['date']}',{int(data['decimals'])}) '''
            cur.execute(query)
            records = cur.fetchall()
            output = records[0]['get_erc20_balance_by_datetime']

            return output

    def update_chain_data(self, data):

        output = []

        for d in data:
            multisig = self.get_erc20_balance_by_datetime(d,d['multisig'])
            if d['chain_id'] not in [137]:
                # get total value
                total = 500000000 - multisig
            else:
                # temporary number
                total = 3941244
            noncirculating = 0
            for c in d['contracts']:
                balance = self.get_erc20_balance_by_datetime(d,c)
                # get noncirculating value
                noncirculating += balance
            # get circulating value
            circulating = total - noncirculating
            output.append({'chain_id': d['chain_id'], 'total': total, 'emitted': circulating, 'locked': noncirculating})

        if len(output):

            if self.connection.closed:
                self.connect()

            with self.connection.cursor(row_factory=dict_row) as cur:
                # update values for every chain
                for o in output:
                    query = f''' UPDATE dao.info SET emitted = '{o.emitted}', locked = '{o.locked}') WHERE chain = {o.chain_id} '''
                    try:
                        cur.execute(query)
                        self.connection.commit()
                    except Exception as e:
                        logging.error('PostgreSQL error', e)

    def get_chain_data(self, data):
        # update values
        self.update_chain_data(data)

        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            # get summary by chain
            query = f''' SELECT chains.id, chains.title, chains.slug, chains.lockdate, SUM(info.emitted) AS emitted, SUM(info.locked) AS locked, SUM(info.longterm) AS longterm FROM dao.info AS info LEFT JOIN dao.chains AS chains ON info.chain_id = chains.id GROUP by chains.id ORDER BY chains.id '''
            cur.execute(query)
            output = []
            records = cur.fetchall()
            for item in records:
                output.append(item)

            return output

    def get_schedule_data(self, chain_id: int):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f''' SELECT date, value FROM dao.schedule WHERE chain_id = '{chain_id}' ORDER BY id '''
            cur.execute(query)
            output = []
            records = cur.fetchall()
            for item in records:
                output.append(item)

            return output

    def get_stat_data(self):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            # get summary by chain
            query = f''' SELECT id, period, total FROM dao.stat ORDER BY id '''
            cur.execute(query)
            output = []
            records = cur.fetchall()
            for item in records:
                output.append(item)

            return output

    def get_spendings_data(self, stat_id: int):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f''' SELECT spendings.category AS id, spendings."desc" AS label, spendings."value" AS value FROM dao.spendings AS spendings WHERE stat_id = '{stat_id}' ORDER BY spendings.id '''
            cur.execute(query)
            output = []
            records = cur.fetchall()
            for item in records:
                output.append(item)

            return output

    def get_widget_data(self, project_name: str):
        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                SELECT * FROM lpad_projects lp
                JOIN lpad_data ld ON lp.id = ld.project_id
                WHERE lp.description = '{str(project_name)}' and lp.is_active;
            '''
            cur.execute(query)
            records = cur.fetchall()

            return records

dbconnector = DBConnector()