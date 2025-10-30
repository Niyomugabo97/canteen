import base64
import json
import urllib.request
from typing import Tuple, Optional

from django.conf import settings


def get_access_token() -> Tuple[Optional[str], Optional[str]]:
    """
    Returns (access_token, error). If error is not None, token will be None.
    Uses MTN MoMo Collections sandbox by default.
    """
    api_user = settings.MTN_MOMO.get('API_USER')
    api_key = settings.MTN_MOMO.get('API_KEY')
    subscription_key = settings.MTN_MOMO.get('SUBSCRIPTION_KEY')
    base_url = settings.MTN_MOMO.get('BASE_URL', 'https://sandbox.momodeveloper.mtn.com')

    if not (api_user and api_key and subscription_key):
        return None, 'Missing MTN MoMo credentials (API_USER/API_KEY/SUBSCRIPTION_KEY)'

    url = f"{base_url}/collection/token/"

    credentials = f"{api_user}:{api_key}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    req = urllib.request.Request(url, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                return None, f"Token request failed with status {resp.status}"
            body = resp.read().decode('utf-8')
            token_info = json.loads(body)
            return token_info.get('access_token'), None
    except Exception as e:
        return None, str(e)
