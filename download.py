import GetPoolData

# Create config.py in this directory and enter your own Bitquery API Token
from config import BITQUERY_API_TOKEN


def get_data(pair, download=False):
    """
    """

    if pair == 'RAI/ETH':
        '''
        SELECT
        	block_id,
        	block_timestamp,
        	pool_address,
        	pool_name,
        	price_0_1,
        	price_1_0,
        	tick,
          	virtual_liquidity_adjusted
        	from uniswapv3.pool_stats
        	where pool_address = '0x14de8287adc90f0f95bf567c0707670de52e3813' and BLOCK_ID > 12300000
        	order by block_id asc
        '''

        # Pool contract RAI-ETH
        pool_address = '0x14de8287adc90f0f95bf567c0707670de52e3813'
        # RAI
        token_0_address = '0x03ab458634910aad20ef5f1c8ee96f1d6ac54919'
        # ETH
        token_1_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
        flipside_queries = ['https://api.flipsidecrypto.com/api/v2/queries/ccb631f8-f0f6-44e4-ac85-8f6f040b7088/data/latest']

        file_name = 'RAI-ETH/rai_eth'

    elif pair == 'FLX/ETH':

        # Pool contract FLX/ETH
        pool_address = '0x8e5778ded8a7dd4000561a119b65f973158c277f'
        # FLX
        token_0_address = '0x6243d8cea23066d098a15582d81a598b4e8391f4'
        # ETH
        token_1_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

        """
        SELECT
        	block_id,
        	block_timestamp,
        	pool_address,
        	pool_name,
        	price_0_1,
        	price_1_0,
        	tick,
          	virtual_liquidity_adjusted
        	from uniswapv3.pool_stats
        	where pool_address = '0x8e5778ded8a7dd4000561a119b65f973158c277f' and BLOCK_ID > 12300000
        	order by block_id asc
        """
        flipside_queries = ['https://api.flipsidecrypto.com/api/v2/queries/b46086b6-8c22-4f0d-9ce8-f9f44d052410/data/latest']

        file_name = 'FLX-ETH/flx_eth'

    elif pair == 'DAI/MKR':

        # Pool contract DAI/MKR
        pool_address = '0x2a84e2bd2e961b1557d6e516ca647268b432cba4'
        # DAI
        token_0_address = '0x6b175474e89094c44da98b954eedeac495271d0f'
        # MKR
        token_1_address = '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2'

        '''
        SELECT
        	block_id,
        	block_timestamp,
        	pool_address,
        	pool_name,
        	price_0_1,
        	price_1_0,
        	tick,
          	virtual_liquidity_adjusted
        	from uniswapv3.pool_stats
        	where pool_address = '0x2a84e2bd2e961b1557d6e516ca647268b432cba4' and BLOCK_ID > 12300000
        	order by block_id asc
        '''
        flipside_queries = ['https://api.flipsidecrypto.com/api/v2/queries/a10c44cf-6db6-4e45-be92-70d1f35a11c6/data/latest']

        file_name = 'DAI-MKR/dai_mkr'

    elif pair == 'MKR/ETH':

        # Pool contract MKR/ETH
        pool_address = '0xe8c6c9227491c0a8156a0106a0204d881bb7e531'
        eth_usdc_poo_address = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'
        # MKR
        token_0_address = '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2'
        # ETH
        token_1_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

        '''
        SELECT
        	block_id,
        	block_timestamp,
        	pool_address,
        	pool_name,
        	price_0_1,
        	price_1_0,
        	tick,
          	virtual_liquidity_adjusted
        	from uniswapv3.pool_stats
        	where pool_address = '0xe8c6c9227491c0a8156a0106a0204d881bb7e531' and BLOCK_ID > 12363860
        	order by block_id asc
        '''
        flipside_queries = ['https://api.flipsidecrypto.com/api/v2/queries/e86d28f2-cad4-42f4-a497-c844e64c17f8/data/latest']

        file_name = 'MKR-ETH/mkr_eth'

    elif pair == 'DAI/ETH':

        # Pool contract DAI/ETH
        pool_address = '0x60594a405d53811d3bc4766596efd80fd545a270'
        # DAI
        token_0_address = '0x6b175474e89094c44da98b954eedeac495271d0f'
        # ETH
        token_1_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

        '''
        SELECT
        	block_id,
        	block_timestamp,
        	pool_address,
        	pool_name,
        	price_0_1,
        	price_1_0,
        	tick,
          	virtual_liquidity_adjusted
        	from uniswapv3.pool_stats
        	where pool_address = '0x60594a405d53811d3bc4766596efd80fd545a270' and BLOCK_ID > 12363860
        	order by block_id asc
        '''
        flipside_queries = ['https://api.flipsidecrypto.com/api/v2/queries/2fc92f27-a017-4b72-a73d-398800edc21d/data/latest']

        file_name = 'DAI-ETH/dai_eth'

    price_data_begin = '2021-12-31'
    price_data_end = '2022-12-31'
    swap_data = GetPoolData.get_pool_data_flipside(pool_address,
                                                   flipside_queries,
                                                   file_name,
                                                   download)
    price_data = GetPoolData.get_price_data_bitquery(token_0_address,
                                                     token_1_address,
                                                     price_data_begin,
                                                     price_data_end,
                                                     BITQUERY_API_TOKEN,
                                                     file_name,
                                                     download)

    return price_data, swap_data
