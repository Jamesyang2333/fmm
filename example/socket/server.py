import SocketServer
from mapmatcher import MapMatcher
import os
import time
import optparse
import logging
import json

class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        wkt = self.rfile.readline().strip()
        # print "{} wrote:".format(self.client_address[0])
        # print wkt
        # logging.info('WKT get in python: %s', wkt)
        starttime = time.time()
        result = self.server.mapmatcher.match_wkt(wkt)
        mgeom_wkt = ""
        if (result.mgeom.get_num_points() > 0):
            mgeom_wkt = result.mgeom.export_wkt()
        pgeom_wkt = ""
        if (result.pgeom.get_num_points() > 0):
            pgeom_wkt = result.pgeom.export_wkt()
        offset = [c.offset for c in result.candidates]
        spdist = [c.spdist for c in result.candidates]
        # logging.info('Probs %s',probs)
        endtime = time.time()
        # logging.info('%s', result)
        # logging.info('Time cost: %s', result[2])
        # print "Result is ",result
        # print "Result geom is ",result.mgeom
        if (mgeom_wkt != ""):
            # print "Matched"
            response_json = {"mgeom_wkt": mgeom_wkt, "opath": list(result.opath), "cpath": list(result.cpath), "pgeom_wkt": pgeom_wkt, "indices": list(result.indices), "offset": offset, "spdist": spdist, "state": 1}
            self.request.sendall(json.dumps(response_json))
        else:
            # print "Not matched"
            self.request.sendall(json.dumps({"state": 0}))

if __name__ == "__main__":

    parser = optparse.OptionParser()
    # Store the file argument into the filename attr
    # parser.add_option("-f", "--file", action="store", type="string", dest="filename")
    parser.add_option(
        '-d', '--debug',
        help="enable debug mode",
        action="store_true", default=False)
    parser.add_option(
        '-p', '--port',
        help="which port to serve content on", action="store", dest="port", type='int', default=1235)
    parser.add_option(
        '-c', '--config',
        help="the model configuration file", action="store", dest="config_file",
        type='string', default="config.json")
    opts, args = parser.parse_args()

    HOST, PORT = "0.0.0.0", opts.port
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    server.mapmatcher = MapMatcher(opts.config_file)


    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()