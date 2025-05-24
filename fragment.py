import requests
import json
url = "https://tg.parssms.info/v1/premium/testnet/payment"
payload = json.dumps({
 "query": "jailbroken",
 "months": "3"
})
headers = {
 'Content-Type': 'application/json',
 'api-key': 'db14f2bb-aa03-4d45-8269-3a0254ab0fb1'
}
response = requests.post(url, headers=headers, data=payload)
print(response.text)