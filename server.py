import os
from flask import Flask, send_from_directory, safe_join
from flask.ext.basicauth import BasicAuth

DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = '%s/_site' % DIR

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

def serve_page(page):
	if os.path.isdir(safe_join(SITE_DIR, page)):
		# Serve the index page
		page_file = safe_join(page, "index.html")
	else:
		# Serve the specific page
		page_file = "%s.html" % page
	return send_from_directory(SITE_DIR, page_file)

@app.route('/', defaults={'page': ''})
@app.route('/<path:page>')
def public(page):
	return serve_page(page)

@app.route('/internal', defaults={'page': ''})
@app.route('/internal/<path:page>')
@basic_auth.required
def internal(page):
	return serve_page('internal/%s' % page)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
