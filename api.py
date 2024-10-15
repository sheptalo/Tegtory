from sinAPI import SinApi
from dotenv import load_dotenv
import os

load_dotenv('.env')
api = SinApi(os.environ['DB_API_KEY'])
