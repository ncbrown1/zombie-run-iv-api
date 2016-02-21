from flask import Blueprint


api = Blueprint('api', __name__)


# Import any endpoints here to make them available
#from . import dis_endpoint, dat_endpoint
from . import player
from . import score

@api.route('/', methods=['GET'])
def index():
	return "Hello, world!"