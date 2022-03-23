#!/usr/bin/python
import os, logging
from flask import Flask, request
from datetime import datetime
import selenium.webdriver
from selenium.common.exceptions import TimeoutException


app = Flask(__name__)


options = selenium.webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage') # this arg is to prevent chrome from crashing due to not enough memory (use disk instead)

browser = selenium.webdriver.Chrome(options=options)
browser.set_page_load_timeout(4)


# this function is not threaded. only 1 request will be served at a time.
@app.route('/', methods=['POST'])
def crawlURL():
	# get url to crawl
	jsonData = request.get_json()
	url = jsonData['url']
	print('\nstarting\n' + url)
	startTime = datetime.now()
	try:
		try:
			# load page
			browser.get(url)
		except TimeoutException:
			# get whatever html is loaded after 4 seconds
			print('stopping page load')
			browser.execute_script("window.stop();")
		# return html
		html = browser.page_source
		print('success\n' + str((datetime.now() - startTime).total_seconds()) + ' seconds')
		return html
	except Exception as errorMessage:
		# catch error
		print('error\n' + str((datetime.now() - startTime).total_seconds()) + ' seconds')
		logging.error('', exc_info=errorMessage)
		if 'session deleted because of page crash' in str(errorMessage) or 'invalid session id' in str(errorMessage):
			# kill flask if chrome crashed
			shutdown_hook = request.environ.get('werkzeug.server.shutdown')
			if shutdown_hook is not None:
				print('shutting down')
				shutdown_hook()
			else:
				print('failed to shut down!')
		else:
			pass
		return "There was an error", 500


if __name__ == '__main__':
	app.run(
		debug=(os.environ['DEBUG_MODE'] == 'true'),
		host='0.0.0.0',
		threaded=False,
		port=5002
	)