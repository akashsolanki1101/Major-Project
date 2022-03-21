from Utils.imageConverter import show_image
import json
from hashlib import sha256

class Block:
	def __init__(self, index, data, timestamp, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash

	def compute_hash(self):
		"""
		A function that return the hash of the block contents.
		"""
		block_string = self.toJson()
		return sha256(block_string.encode()).hexdigest()

	def print_data(self):
		print("Index : " + str(self.index))
		print("Timestamp : " + str(self.timestamp))
		print("Prev hash : " + str(self.previous_hash) + '\n')
		show_image(self.data)

	def __str__(self):
		res = ""
		res += "Block : " + '\n'
		res += "Index : " + str(self.index) + '\n'
		res += "Timestamp : " + str(self.timestamp) + '\n'   
		res += "Data : " + str(self.data) + '\n' 
		res += "Prev hash : " + str(self.previous_hash) + '\n'

		return res 
	
	def toJson(self):
		obj = {
			"index" : self.index,
			"data" : self.data,
			"timestamp" : self.timestamp,
			"previous_hash" : self.previous_hash
		}

		return json.dumps(obj)
