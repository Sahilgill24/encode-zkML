import ezkl
import asyncio

async def main():
    await ezkl.gen_witness("./input.json","./network.ezkl")
    print("witness generated")
    
    print("proof generated")

    


print("proof generated")
ezkl.prove("./witness.json","./network.ezkl","./pk.key","./proof.json", "single")
print("over")