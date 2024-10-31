from my_sin_api import SinApi
from dotenv import load_dotenv
import os

load_dotenv('.env')
api = SinApi(os.environ['DB_API_KEY'], os.environ['API_URL'])
