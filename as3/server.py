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
        flare = {}
        read = open('cereal.csv', 'r+')
        for line in read:
            sep = line.rstrip("\n").split(" ")
            data.append(sep)
        for item in data:
            cereal_name = item[0].replace("_", " ")
            cereal_man = item[1]
            cereal_type = item[2]

            if cereal_man is "A": cereal_man = "AAHF Products"
            elif cereal_man is "G": cereal_man = "General Mill"
            elif cereal_man is "K": cereal_man = "Kellogs"
            elif cereal_man is "N": cereal_man = "Nabisco"
            elif cereal_man is "P": cereal_man = "Post"
            elif cereal_man is "Q": cereal_man = "Quaker Oats"
            elif cereal_man is "R": cereal_man = "Ralston Purina"

            if cereal_type is "H": cereal_type = "Hot Cereal"
            elif cereal_type is "C": cereal_type = "Cold Cereal"

            flare.setdefault(cereal_man, {}).setdefault(cereal_type, {})[cereal_name] = 8000 

        self.write(tornado.escape.json_encode(flare))

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
