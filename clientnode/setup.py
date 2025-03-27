import ezkl

ezkl.gen_settings("./network.onnx")
print("settings generated")
ezkl.compile_circuit("./network.onnx","network.ezkl","settings.json")
print("circuit compiled")

#ezkl.setup("./network.ezkl","vk.key","pk.key","../../.ezkl/srs/kzg17.srs")
print("setup done ,keys generated")
