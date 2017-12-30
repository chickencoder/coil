import requests
import hashlib
import datetime

def doubleHash(input):
    return hashlib.sha256(hashlib.sha256(input).digest()).hexdigest()

def doubleHashEncode(input):
    return doubleHash(input.encode("utf-8"))

started = datetime.datetime.now()
total = 0

print("welcome to hacky miner")
print("we be mining all t'day")
print("Ctrl-C to quit m'deer")

s = requests.Session()
url = "http://localhost:1337"

s.get(url + "/wallet/new/mine")
address = s.get(url + "/wallet/mine").json()["address"]

last_hash = s.get(url + "/block/hash").json()["message"]

nonce = 0

try:
	while True:
		if doubleHashEncode(str(last_hash) + str(nonce))[:5] == "00000":
			payload = {
				'minerAddress': address,
				'previousBlockHash': last_hash,
				'nonce': str(nonce),
				'transactionHashes': ''
			}

			r = s.post(url + "/mine", payload)
			total += 1

			print("New block mined")
			elapsed = (datetime.datetime.now() - started).total_seconds()
			print("Time Elapsed: ", elapsed , "s")
			print("Average Speed:", (total / elapsed), " blocks per second")

			# print("Node says:", r.text)
			print()

			last_hash = s.get(url + "/block/hash").json()["message"]

		nonce += 1


except KeyboardInterrupt:
	print()