import os
from flask import Flask, send_from_directory
from flask.ext.basicauth import BasicAuth

DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = '%s/site' % DIR

app = Flask(__name__)

app.config.update(
	DEBUG=DIR.startswith('/User'),
	BASIC_AUTH_USERNAME='user',
	BASIC_AUTH_PASSWORD='password',
)

class CustomBasicAuth(BasicAuth):
	def challenge(self):
		response = super(CustomBasicAuth, self).challenge()
		response.data = "Login required"
		return response

basic_auth = CustomBasicAuth(app)

@app.route('/<path:filename>')
def hello(filename):
	return send_from_directory(STATIC_DIR, filename)

@app.route('/internal/<path:filename>')
@basic_auth.required
def hello(filename):
	return send_from_directory('%s/internal' % STATIC_DIR, filename)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
