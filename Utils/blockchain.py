from email.mime import image
from random import randint
import time
from Utils.block import Block
from Utils.imageConverter import serialize_image

class Blockchain:
      def __init__(self):
            self.chain=[]
            self.create_genesis_block()

      def create_genesis_block(self):
            img = serialize_image("./images/drone1.jpeg")
            genesis_block = Block(0, img, time.time(), "0")
            genesis_block.hash = genesis_block.compute_hash()
            self.chain.append(genesis_block)

      def get_previous_block(self):
            return self.chain[-1]

      def mine_block(self):
            previous_block = self.get_previous_block()
            previous_hash = previous_block.compute_hash()
            rand_val = randint(2, 5)
            img_location = "./images/drone{}.jpg".format(rand_val)
            data = serialize_image(img_location)
            block = Block(len(self.chain), data, time.time(), previous_hash)
            return block

      def add_block(self, block):
            previous_block = self.get_previous_block()
            previous_hash = previous_block.compute_hash()

            if previous_hash != block.previous_hash:
                  return False
            else:
                  self.chain.append(block)
                  return True
      
      def validate_node(self, id):
            file = open("./Credentials/cred.txt", "r")

            for line in file:
                  curr_id = int(line)
                  if id == curr_id:
                        return True
                  
            return False