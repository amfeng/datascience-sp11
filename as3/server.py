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
        def removeUnderscore(x):
            return x.replace("_", " ")
        for line in read:
            sep = line.rstrip("\n").split(" ")
            sep[0:3] = map(removeUnderscore, sep[0:3])
            sep[3:] = map(toFloat, sep[3:])
            raw.append(sep)
        
        if data_id in ["flare", "pie"]:
            data = {}
            total = 0
            for item in raw:
                total = total + 1
                cereal_name = item[0]
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

                if data_id == "flare": data.setdefault(cereal_man, {}).setdefault(cereal_type, {})[cereal_name] = 0
                if data_id == "pie": data[cereal_man] = data.setdefault(cereal_man, 0) + 1
            
            if data_id == "pie":
                temp = []
                for key in ["AAHF Products", "General Mill", "Kellogs", "Nabisco", "Post", "Quaker Oats", "Ralston Purina"]:
                    temp.append(float(data[key])/float(total) * 100)
                data = temp


        elif data_id in ["calories", "protein", "fat", "carb"]:
            data = []
            data_indv = []
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
            
            man = []

            for key in data_calc:
                man.append(key)

            def average(values):
                return sum(values, 0.0)/len(values)
            
            for key in ["A", "G", "K", "N", "P", "Q", "R"]:
                value = data_calc[key]
                if data_id == "protein": data_indv.append(average(value[0]))
                elif data_id == "fat": data_indv.append(average(value[1]))
                elif data_id == "carb": data_indv.append(average(value[2]))
                elif data_id == "calories": data_indv.append(average(value[3]))

            data.append(data_indv)
            data.append(man)
        elif data_id in ["a", "g", "k", "n", "p", "q", "r"]:
            data_id = data_id.upper()
            data = []
            data_calc = {}
            for item in raw:
                man = item[1]
                fiber = float(item[7])
                sugar = item[9]
                protein = item[4]
                sodium = item[6]
                
                bucket = data_calc.setdefault(man, ([],[],[],[]))
                bucket[0].append(fiber)
                bucket[1].append(sugar)
                bucket[2].append(protein)
                bucket[3].append(sodium)
            
            man = []

            for key in data_calc:
                man.append(key)

            def average(values):
                return sum(values, 0.0)/len(values)
            
            fiber = ["Fiber", [20/5, 35/5, 40/5], [], "grams"]
            sugar = ["Sugar", [2200*0.1/4, 2900*0.1/4, 3500*0.1/4], [], "grams"]
            protein = ["Protein", [50/5, 63/5, 70/5], [], "grams"]
            sodium = ["Sodium", [1800/5, 2400/5, 3000/5], [], "milligrams"]

            value = data_calc[data_id]
           
            fiber[2].append((average(value[0])))
            sugar[2].append((average(value[1])))
            protein[2].append((average(value[2])))
            sodium[2].append((average(value[3])))
            
            data.append(fiber)
            data.append(sugar)
            data.append(protein)
            data.append(sodium)
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
