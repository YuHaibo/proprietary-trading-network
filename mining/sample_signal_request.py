import sys
import os

import requests
import json

from vali_objects.enums.order_type_enum import OrderType
from vali_objects.vali_config import TradePair, TradePairCategory


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TradePair) or isinstance(obj, OrderType):
            return obj.__json__()  # Use the to_dict method to serialize TradePair

        if isinstance(obj, TradePairCategory):
            # Return the value of the Enum member, which is a string
            return obj.value

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def load_api_key():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'miner_secrets.json')
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('api_key', 'error_key')
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"invalid config: {e}")
        return 'error_key'


if __name__ == "__main__":
    # Set the default URL endpoint
    default_base_url = 'http://127.0.0.1:80'

    # Check if the URL argument is provided
    if len(sys.argv) == 2:
        # Extract the URL from the command line argument
        base_url = sys.argv[1]
    else:
        # Use the default URL if no argument is provided
        base_url = default_base_url

    print("base URL endpoint:", base_url)

    url = f'{base_url}/api/receive-signal'

    api_key = load_api_key()

    # Define the JSON data to be sent in the request
    data = {
        'trade_pair': TradePair.BTCUSD,
        'order_type': OrderType.LONG,
        'leverage': .1,
        'api_key': api_key
    }

    # Convert the Python dictionary to JSON format
    json_data = json.dumps(data, cls=CustomEncoder)
    print(json_data)
    # Set the headers to specify that the content is in JSON format
    headers = {
        'Content-Type': 'application/json',
    }

    # Make the POST request with JSON data
    response = requests.post(url, data=json_data, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("POST request was successful.")
        print("Response:")
        print(response.json())  # Print the response data
    else:
        print(response.__dict__)
        print("POST request failed with status code:", response.status_code)