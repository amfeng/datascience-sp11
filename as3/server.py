import tornado.ioloop
import tornado.web, tornado.escape

import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("index.html", title="Cereal Data Visualization")

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        #Parse and package data
        data = []
        read = open('cereal.csv', 'r+')
        for line in read:
            sep = line.rstrip("\n").split(" ")
            data.append(sep)
        self.write(tornado.escape.json_encode(data))

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/data", DataHandler)
], **settings)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
