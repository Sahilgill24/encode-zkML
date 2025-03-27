import ezkl 
import asyncio

async def main():
    await ezkl.verify("./proof.json","./settings.json","./vk.key")
    print("verified")


asyncio.run(main())

abi_path = "./test.abi"
sol_code_path= "./test.sol"
addr_verifier = "addr.txt"

async def contract():
    await ezkl.create_evm_verifier("./vk.key","./settings.json",sol_code_path,abi_path)
    print("evm verifier created")
    await ezkl.deploy_evm(addr_verifier,sol_code_path,"https://localhost:3030")
    print("contract deployed")

asyncio.run(contract())