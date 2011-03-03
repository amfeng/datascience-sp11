import tornado.ioloop
import tornado.web, tornado.escape

import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("index.html", title="Cereal Data Visualization")

class GraphHandler(tornado.web.RequestHandler):
    def get(self, graph_id):
        self.render(graph_id + ".html", title="")

class DataHandler(tornado.web.RequestHandler):
    def get(self, data_id):
        #Parse and package data
        raw = []
        data = None
        read = open('cereal.csv', 'r+')
        def toFloat(x):
            return float(x)
        for line in read:
            sep = line.rstrip("\n").split(" ")
            sep[3:] = map(toFloat, sep[3:])
            raw.append(sep)
        
        if data_id == "flare":
            data = {}
            for item in raw:
                cereal_name = item[0].replace("_", " ")
                cereal_man = item[1]
                cereal_type = item[2]

                if cereal_man == "A": cereal_man = "AAHF Products"
                elif cereal_man == "G": cereal_man = "General Mill"
                elif cereal_man == "K": cereal_man = "Kellogs"
                elif cereal_man == "N": cereal_man = "Nabisco"
                elif cereal_man == "P": cereal_man = "Post"
                elif cereal_man == "Q": cereal_man = "Quaker Oats"
                elif cereal_man == "R": cereal_man = "Ralston Purina"

                if cereal_type == "H": cereal_type = "Hot Cereal"
                elif cereal_type == "C": cereal_type = "Cold Cereal"

                data.setdefault(cereal_man, {}).setdefault(cereal_type, {})[cereal_name] = 0
        elif data_id == "stackedcal":
            data = []
            data_calc = {}
            for item in raw:
                man = item[1]
                protein = float(item[4])
                fat = item[5]
                cal = item[3]
                carb = item[8]
                
                bucket = data_calc.setdefault(man, ([],[],[],[]))
                bucket[0].append(protein)
                bucket[1].append(fat)
                bucket[2].append(carb)
                bucket[3].append(cal)
            
            protein = []
            fat = []
            carb = []
            cal = []
            man = []

            print data_calc
            for key in data_calc:
                man.append(key)

            def average(values):
                return sum(values, 0.0)/len(values)
            
            for key, value in data_calc.iteritems():
                protein.append(average(value[0]))
                fat.append(average(value[1]))
                carb.append(average(value[2]))
                cal.append(average(value[3]))

            data.append(protein)
            data.append(fat)
            data.append(carb)
        elif data_id == "heat":
            def shift(x):
                d = [x[0]]
                d.extend(x[3:])
                return d
            data = map(shift, raw)
            data.insert(0, ["NAME", "CAL", "PROTEIN", "FAT", "SODIUM", "FIBER", "CARB", "SUGAR", "SHELF", "POTAS", "VITA", "WEIGHT", "CUP/S"])
        else:

            data = []
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
