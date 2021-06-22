import os
import time
import json
import gzip
from seleniumwire.undetected_chromedriver import Chrome

# Note: You should also change the site key in html file
host = "discord.com"
driver = Chrome(executable_path="./chromedriver")

def request_interceptor(request):
	if "https://hcaptcha.com/checksiteconfig" in request.url:
		request.url = f"https://hcaptcha.com/checksiteconfig?host={host}&sitekey=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34&sc=1&swa=1"
	elif "https://hcaptcha.com/getcaptcha" in request.url:
		modify = request.body.decode('utf-8').split("&")
		modify[2] = f"host={host}" 
		request.body = bytes("&".join(modify), 'utf-8')
		del request.headers['Content-Length']
		request.headers['Content-Length'] = str(len(request.body))
		request.headers['Cookie'] = "hc_accessibility=4tU0ZNSIjbdY8m5mgY+bE90Wq5XwAcBoWew3/h7A3bq2zDl3jkQcaSx/F0bji1ph6x3Ct1VVtJJX66CPpD+enEpFknXYmyfwXF9+HLnxYwKRQy4bqssblcWzE9xIoDzikoC0tu5Vfie3dKpVgCzI1tsepz8Ps0yU3+hjho66GTE79nSo09qqSEJtvbxKfiyud0hSxfg+8ADuOGcHDr269GVBT2w6rbSIRlYFNEm1kwySOtt8TBC926EcDOsMyM6pDLoBdtmF7xQudqFmxPMOfaPZPPVrIO9yKOcTV5fJ2p2brhUtUIEbaqY7YEyBu/E7Pb07Ou+fuPqxDt5yPWXtBaVWlyJitMQ4DUcwTdgfdCvVpmZXeuRfb65jMgIdWw9vFCti8TtbfXauGtaOdjevCYyXAfImEfBOwKtdKEno752vyNG0+5HBfEXUVJUE+eywCxKSvMmL7o2QCyuKs6B2GaslJIiKByVSXiBcm1e5YwaC+74RGzLwls+fYfoEuvBfAs1dXFDoNq5Q+BFQ"

def response_interceptor(request, response):
	if "https://hcaptcha.com/getcaptcha" in request.url:
		try:
			body = gzip.decompress(response.body).decode('utf-8')
			data = json.loads(body)
			print(data['generated_pass_UUID'])
			driver.close()
		except:
			...
			#print(e)

driver.request_interceptor = request_interceptor
driver.response_interceptor = response_interceptor
driver.get(f'file://{os.getcwd()}/hcaptcha.html')

while True:
	try:
		driver.switch_to.frame(0)
		driver.find_element_by_id("checkbox").click()
		break
	except Exception as e:
		#print(e)
		driver.switch_to.default_content()
		time.sleep(0.2)

time.sleep(120)