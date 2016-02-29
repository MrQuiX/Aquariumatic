import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class TankHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.render('tank.html', test1="100 Degrees C", test2="14.0")

    def post(self, input):
        aquarium_id = input
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        mintemp_data = self.get_argument('MinTemp', '')
        maxtemp_data = self.get_argument('MaxTemp', '')

        if WebCommand == 'Heating':
            print(WebCommand + ": " + WebValue)
            self.write(json.dumps({"msg":"heater set to " + WebValue}))
            return
        elif WebCommand == 'Light':
            print(WebCommand + ": " + WebValue)
            self.write(json.dumps({"msg":"Light " + WebValue + " toggled"}))
            return
        elif WebCommand == 'UpdateValues':
            print(WebCommand + ": " + WebValue)
            update_response = {}
            update_response['TankNo'] = aquarium_id
            update_response['msg'] = 'Update requested'
            update_response['TempValue'] = '50 Degrees C'
            update_response['pHValue'] = '7.0'
            #print(json.dumps(update_response))
            self.write(json.dumps(update_response))
            return
        else:
            self.write('parameter not defined for heating')
            


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        example_response = {}
        example_response['name'] = 'example'
        example_response['width'] = 1020

        self.write(json.dumps(example_response))


    def post(self):
        json_obj = json_decode(self.request.body)
        print('Post data received')

        for key in list(json_obj.keys()):
            print('key: %s , value: %s' % (key, json_obj[key]))

        # new dictionary
        response_to_send = {}
        response_to_send['newkey'] = json_obj['key1']

        print('Response to return')

        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/test", TestHandler),
            (r"/aquarium(\d+)", TankHandler)],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"))

    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    tornado.ioloop.IOLoop.instance().start()
