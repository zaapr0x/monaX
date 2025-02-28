from web3 import Web3
from .config import *
import json
import time
from eth_account import Account

class Monadex:
    def __init__(self, pk):
        self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
        self.ABI = json.loads(open("abi/monadex.json").read())
        self.SIGNER = Account.from_key(pk)
     
        self.swapFrom = "0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701"
        self.pair = [
            {"ticker": "MDX", "CA": "0xD8C603A0Fe45c77f13FAF626C04fE69EEB628196"},
            {"ticker": "MLDK", "CA": "0xe9f4c0093B4e94800487cad93FBBF7C3729ccf5c"},
            {"ticker": "CHOG", "CA": "0xE0590015A873bF326bd645c3E1266d4db41C4E6B"},
            {"ticker": "USDC", "CA": "0xf817257fed379853cDe0fa4F97AB987181B1E5Ea"}
        ]
        self.contract = self.w3.eth.contract(
            address="0xCBcd292c9DAE11875E090Bb963aA4C74ccCE6a23",
            abi=self.ABI
        )

    def getEstimation(self, amount, path):
        try:
            result = self.contract.functions.getAmountsOut(amount, path).call()
            return result
        except Exception as e:
            print(f"Error getting estimation: {e}")
            return None

    def Swap(self,pair):
        try:
            amount_out_min = self.getEstimation(
                self.w3.to_wei(0.001, "ether"),
                [self.swapFrom, pair]
            )

            if not amount_out_min:
                print("Failed to fetch estimation.")
                return None

            amount_out_min = amount_out_min[1]
            deadline = int(time.time()) + 60

            tx = self.contract.functions.swapExactNativeForTokens(
                amount_out_min,
                [self.swapFrom, pair],
                self.SIGNER.address,
                deadline,
                (False, (0, 0), "0x0000000000000000000000000000000000000000")
            ).build_transaction({
                "value": self.w3.to_wei(0.001, "ether"),
                "nonce": self.w3.eth.get_transaction_count(self.SIGNER.address),
                "gas": 250000,  
                "gasPrice": self.w3.eth.gas_price
            })

            signed_tx = self.SIGNER.sign_transaction(tx)
            print(f"{'~' * 40}\nSwaping 0.001 MONAD for {self.w3.from_wei(amount_out_min, 'ether')} {pair}")
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f"Transaction Link: https://testnet.monadexplorer.com/tx/0x{tx_hash.hex()}\n{'~' * 40}")
            return tx_hash.hex()

        except Exception as e:
            print(f"Error executing swap: {e}")
            return None

    def executeSwap(self):
        for i in self.pair:
            self.Swap(i["CA"])
        print("Swapping completed.Do You Want Repeat Swap?")
        print("1. Yes\n2. Back To Menu\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            for i in self.pair:
                print(f"Swapping MONAD for {i['ticker']}...")
                self.Swap(i["CA"])
        elif choice == "2":
            from . import StartApp 
            app = StartApp()
            app.menu("0x" + self.SIGNER.key.hex())
        elif choice == "3":
            print("Exiting...")
        else:
            print("Invalid choice. Please try again.")