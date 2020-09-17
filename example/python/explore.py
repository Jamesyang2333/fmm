from fmm import Network,NetworkGraph,FastMapMatch,FastMapMatchConfig,UBODT

network = Network("../data/harbin.tmp/edges.shp", "fid", "u", "v")
print "Nodes {} edges {}".format(network.get_node_count(),network.get_edge_count())
graph = NetworkGraph(network)

# from fmm import UBODTGenAlgorithm
# ubodt_gen = UBODTGenAlgorithm(network,graph)
# status = ubodt_gen.generate_ubodt("../data/ubodt.txt", 4, binary=False, use_omp=True)
# print status

ubodt = UBODT.read_ubodt_csv("../data/harbin.tmp/ubodt-harbin.txt")
model = FastMapMatch(network,graph,ubodt)
k = 4
radius = 0.4
gps_error = 0.5
fmm_config = FastMapMatchConfig(k,radius,gps_error)

wkt = "LINESTRING(126.60311000000002 45.742172,126.60328 45.742348,126.60574 45.744152,126.60761 45.746216,126.60878999999998 45.74774,126.60878 45.74777,126.60883 45.747696000000005,126.60884 45.7477,126.60725 45.74565,126.60481 45.74328,126.60404 45.74251,126.60352 45.742764,126.60663 45.740715,126.61026 45.73876,126.61136 45.738293,126.614 45.736755,126.617516 45.73877,126.619125 45.739956,126.62125 45.739075,126.622284 45.73876,126.62337 45.738537,126.62215 45.736294,126.620705 45.73475,126.61933 45.733807,126.614494 45.73659,126.61197 45.738026,126.60894 45.73976,126.6061 45.741264,126.607025 45.74259,126.60714 45.742744,126.60595 45.7412,126.61218999999998 45.73778,126.6141 45.736694)"
result = model.match_wkt(wkt,fmm_config)
print "Matched path: ", list(result.cpath)
print "Matched edge for each point: ", list(result.opath)
print "Matched edge index ",list(result.indices)
print "Matched geometry: ",result.mgeom.export_wkt()
print "Matched point ", result.pgeom.export_wkt()
print "number of links", len(result.cpath)
print "number of points", len(result.opath)
# print "offset", result.offset
#
# print "length", result.length
offset = [c.offset for c in result.candidates]
spdist = [c.spdist for c in result.candidates]
print dir(result)
print(len(result.candidates))
print(offset)
print(spdist)


from fmm import GPSConfig,ResultConfig
input_config = GPSConfig()
input_config.file = "../data/trips.csv"
input_config.id = "id"
print input_config.to_string()

result_config = ResultConfig()
result_config.file = "../data/mr.txt"
result_config.output_config.write_opath = True
print result_config.to_string()

status = model.match_gps_file(input_config, result_config, fmm_config)

print(status)