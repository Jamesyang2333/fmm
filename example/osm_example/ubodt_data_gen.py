from fmm import FastMapMatch,Network,NetworkGraph,UBODTGenAlgorithm,UBODT,FastMapMatchConfig

network = Network("../data/chengdu.tmp/edges.shp","fid", "u", "v")
print(network.get_node_count())
print(network.get_edge_count())
graph = NetworkGraph(network)


# Can be skipped if you already generated an ubodt file
ubodt_gen = UBODTGenAlgorithm(network,graph)
# The delta is defined as 3 km approximately. 0.03 degrees. 
status = ubodt_gen.generate_ubodt("../data/chengdu.tmp/ubodt-chengdu.txt", 0.03, binary=False, use_omp=True)
# Binary is faster for both IO and precomputation
# status = ubodt_gen.generate_ubodt("stockholm/ubodt.bin", 0.03, binary=True, use_omp=True)
print(status)