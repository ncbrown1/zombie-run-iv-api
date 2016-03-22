from flask import Blueprint, redirect


api = Blueprint('api', __name__)


# Import any endpoints here to make them available
#from . import dis_endpoint, dat_endpoint
from . import player
from . import score

@api.route('/', methods=['GET'])
def index():
	return redirect('/index.html', code=302)