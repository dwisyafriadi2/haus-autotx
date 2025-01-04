import os
from web3 import Web3
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich import box

# Load environment variables
load_dotenv()

# Initialize console for better output
console = Console()

# Haust Testnet Configuration
RPC_URL = "https://rpc-test.haust.network"
CHAIN_ID = 1570754601
CURRENCY_SYMBOL = "HAUST"

# Connect to Blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    console.print("[bold red]❌ Failed to connect to Haust Testnet![/bold red]")
    raise ConnectionError("Failed to connect to Haust Testnet!")

console.print(f"[bold green]✅ Connected to Haust Testnet ({RPC_URL})[/bold green]")

# Read private keys from .env file
with open(".env", "r") as file:
    PRIVATE_KEYS = [line.strip() for line in file if line.strip()]  # Read all private keys line by line

if not PRIVATE_KEYS:
    raise ValueError("No private keys found in .env file!")

# Function to get balance for a given address
def get_balance(address):
    try:
        balance_wei = web3.eth.get_balance(address)
        balance_haust = web3.from_wei(balance_wei, 'ether')
        return balance_haust
    except Exception as e:
        console.print(f"[bold red]❌ Failed to fetch balance for {address}: {e}[/bold red]")
        return 0

# Get addresses from private keys
def get_addresses_from_private_keys(keys):
    addresses = []
    for key in keys:
        address = web3.eth.account.from_key(key).address
        addresses.append(address)
    return addresses

# Main checker logic
def main():
    total_balance = 0
    table = Table(title="Token Balance Summary", box=box.DOUBLE_EDGE)
    table.add_column("Private Key", style="cyan", justify="center")
    table.add_column("Address", style="magenta", justify="center")
    table.add_column("Balance (HAUST)", style="green", justify="center")

    addresses = get_addresses_from_private_keys(PRIVATE_KEYS)

    for i, private_key in enumerate(PRIVATE_KEYS):
        address = addresses[i]
        balance = get_balance(address)
        total_balance += balance

        table.add_row(private_key[:6] + "..." + private_key[-4:], address, f"{balance:.6f}")

    console.print(table)
    console.print(f"[bold yellow]Total Balance Across All Accounts: {total_balance:.6f} {CURRENCY_SYMBOL}[/bold yellow]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[bold red]\n🚪 Script terminated by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected Error: {e}[/bold red]")
