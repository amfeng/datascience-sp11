from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from django.utils import simplejson

import os

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))
        #self.render("index.html", title="Stack Overflow Visualizations")

class GraphHandler(webapp.RequestHandler):
    def get(self, graph_id):
        path = os.path.join(os.path.dirname(__file__), graph_id + '.html')
        self.response.out.write(template.render(path, {}))
        #self.render(graph_id + ".html", title="")

class DataHandler(webapp.RequestHandler):
    def get(self, data_id):
        #Parse and package data
        raw = []
        data = {} 
        if data_id == "toptags" or data_id == "toptagsn":
            input = open(os.path.join(os.path.dirname(__file__), "data/toptags_20.json")).read()
            if data_id == "toptags": 
                self.response.out.write(input)
                return
            elif data_id == "toptagsn":
                count = {}
                input = simplejson.loads(input)
                input = input["data"]
                
                for row in input:
                    key = str(row["month"]) + "-" + str(row["year"])
                    if key in count: count[key] += row["count"]
                    else: count[key] = row["count"]
                
                data["count"] = count
                data["data"] = input
                
        self.response.out.write(simplejson.dumps(data))

if __name__ == "__main__":
    application = webapp.WSGIApplication([
    (r"/", MainHandler),
    (r"/data/([a-z]+)", DataHandler),
    (r"/graph/([a-z]+)", GraphHandler)
    ])

    #application.listen(8080)
    #tornado.ioloop.IOLoop.instance().start()
    #wsgiref.handlers.CGIHandler().run(application)
    util.run_wsgi_app(application)
