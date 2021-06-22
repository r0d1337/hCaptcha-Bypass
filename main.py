import os
import time
import json
import gzip
from seleniumwire.undetected_chromedriver import Chrome

# Note: You should also change the site key in html file
host = "discord.com"

def request_interceptor(request):
	if "https://hcaptcha.com/checksiteconfig" in request.url:
		request.url = f"https://hcaptcha.com/checksiteconfig?host={host}&sitekey=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34&sc=1&swa=1"
	elif "https://hcaptcha.com/getcaptcha" in request.url:
		modify = request.body.decode('utf-8').split("&")
		modify[2] = f"host={host}" 
		request.body = bytes("&".join(modify), 'utf-8')
		del request.headers['Content-Length']
		request.headers['Content-Length'] = str(len(request.body))

def response_interceptor(request, response):
	if "https://hcaptcha.com/getcaptcha" in request.url:
		try:
			body = gzip.decompress(response.body).decode('utf-8')
			data = json.loads(body)
			print(data['generated_pass_UUID'])
		except:
			...

driver = Chrome(executable_path="./chromedriver")
driver.request_interceptor = request_interceptor
driver.response_interceptor = response_interceptor
driver.get(f'file://{os.getcwd()}/hcaptcha.html')

driver.switch_to.frame(0)
while True:
	try:
		driver.find_element_by_id("checkbox").send_keys(Keys.ENTER)
	except:
		...
	time.sleep(0.2)