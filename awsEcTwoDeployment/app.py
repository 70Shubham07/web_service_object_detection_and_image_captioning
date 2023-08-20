
from flask_script import Manager



from flask import Flask
from flask_restful import Resource, Api

from rest_apis import app

from rest_apis.api_file_one import HelloWorld
api = Api(app)


class Vocabulary(object):
    """Simple vocabulary wrapper."""
    def __init__(self):
        self.word2idx = {}
        self.idx2word = {}
        self.idx = 0

    def add_word(self, word):
        if not word in self.word2idx:
            self.word2idx[word] = self.idx
            self.idx2word[self.idx] = word
            self.idx += 1

    def __call__(self, word):
        if not word in self.word2idx:
            return self.word2idx['<unk>']
        return self.word2idx[word]

    def __len__(self):
        return len(self.word2idx)


api.add_resource(HelloWorld, '/')

print('apis added')

if __name__ == "__main__":
    #cli()
    # manager.run(  )
	app.run( host="127.0.0.1", port = 5000 )


