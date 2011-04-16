import tornado.ioloop
import tornado.web, tornado.escape

import os, json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Stack Overflow Visualizations")

class GraphHandler(tornado.web.RequestHandler):
    def get(self, graph_id):
        self.render(graph_id + ".html", title="")

class DataHandler(tornado.web.RequestHandler):
    def get(self, data_id):
        jsonDecoder = json.JSONDecoder()
        #Parse and package data
        raw = []
        data = {} 
        #read = open('cereal.csv', 'r+')
        #for line in read:
            #raw.append(sep)
        if data_id == "toptags" or data_id == "toptagsn":
            input = open("etl/toptags_20.json").read()
            if data_id == "toptags": 
                self.write(input)
                return
            elif data_id == "toptagsn":
                count = {}
                input = jsonDecoder.decode(input)
                input = input["data"]
                
                for row in input:
                    key = str(row["month"]) + "-" + str(row["year"])
                    if key in count: count[key] += row["count"]
                    else: count[key] = row["count"]
                
                data["count"] = count
                data["data"] = input
                
        self.write(tornado.escape.json_encode(data))


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/data/([a-z]+)", DataHandler),
    (r"/graph/([a-z]+)", GraphHandler)
], **settings)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
