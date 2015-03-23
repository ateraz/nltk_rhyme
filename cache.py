from riak import RiakClient

client = RiakClient(pb_port=10017, protocol='pbc')
bucket = client.bucket('words')


def cached_rhyme(f):
	def rhyme(self):
		cached_word = bucket.get(self.word)
		if cached_word.exists:
			return cached_word.data
		data = str(f(self))
		bucket.new(self.word, data=data).store()
		return data
	return rhyme
