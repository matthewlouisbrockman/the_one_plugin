import dotenv
from os import getenv

dotenv.load_dotenv()

IS_LOCALHOST = getenv('IS_LOCALHOST', False)

print('is local? ', IS_LOCALHOST)
