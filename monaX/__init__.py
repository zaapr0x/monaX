from .config import *  # Mengimpor konfigurasi jika diperlukan
from web3 import Web3
from eth_account import Account
from .monadex import Monadex

class StartApp:  # Menggunakan PascalCase
    def __init__(self):
        pass

    def run(self):  # Nama metode lebih deskriptif
        print(BANNER)
        try:
            print("Checking private key...")
            with open("pk.txt", "r") as f:
                pk = f.read()
            print("Private key found. Validating...")
            w3 = Web3(Web3.HTTPProvider(RPC_URL))
            acc = Account.from_key(pk)
            print(f"{'~' * 40}\nAccount: {acc.address}\nBalance: {w3.from_wei(w3.eth.get_balance(acc.address), 'ether')} MON\n{'~' * 40}")
            self.menu(pk)
        except FileNotFoundError:
            print("Private key not found.")
            pk = input("Please enter your private key: ")
            with open("pk.txt", "w") as f:
                f.write(pk)
    
    def menu(self,pk):
        print(f"""[Num | Category | Site Name | URL ]\n|1.  | DEX      | Monadex   | https://monadex.monad.xyz/
              """)
        choice = input("Enter your choice: ")
        if choice == "1":
            app = Monadex(pk)
            app.executeSwap()
        elif choice == "2":
            print("Exiting...")