import os
import random
from telebot import TeleBot
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.transaction import Transaction, TransactionInstruction
from solana.rpc.types import TxOpts
from solana.rpc.core import RPCException
from solana.keypair import Keypair
from base64 import b64decode

# Initialize the Telegram bot
bot_token = "7258742988:AAEexTVF1LbiE9-GUl5azOctuWiHutp5n6I"  # Replace with your bot token
bot = TeleBot(bot_token)

# Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Set up Phantom wallet private key and owner's wallet address
phantom_private_key = b64decode("3nL2SyHyRFESjkzhRD2NMD8yTjxPsbjiJ8yDgsEKQ4wmCC4EQMHQGxD3TLMsJefYb8fvDMamGtUpN1PL3r4cR7gS")  # Replace with your private key
owner_wallet = Pubkey.from_string("F6ZxJ5KnYwzvzBMoVtakRrVRLhtpWVFLyQ9WZWnr494a")  # Your wallet address

keypair = Keypair.from_secret_key(phantom_private_key)

HELP_TEXT = """
Flip a coin with your crypto! You can deposit crypto, flip it 50/50, and potentially double it.
A percentage of your earnings will go to the owner's wallet.

Use the following commands:
/start - Start bot
/help - Help text
/deposit - Deposit crypto to play
/coin - Flip a coin with crypto
"""

START_TEXT = """
Welcome to the Crypto Coin Flip bot!
Deposit your crypto, flip a coin, and double your deposit if you win!
"""

# Handle deposits (simulated)
async def deposit_crypto(user_wallet_address: Pubkey, amount: float) -> bool:
    print(f"Simulating deposit of {amount} SOL from {user_wallet_address} to {owner_wallet}")
    return True

# Flip the coin and handle payouts
async def flip_crypto(user_wallet_address: Pubkey, deposit_amount: float, user_choice: str) -> str:
    outcome = "Heads" if random.randint(0, 1) == 1 else "Tails"
    payout = deposit_amount * 2
    commission = payout * 0.05  # 5% commission

    if outcome == user_choice:
        await send_sol(user_wallet_address, payout - commission)
        await send_sol(owner_wallet, commission)
        return f"You won! Transferring {payout - commission} SOL to your wallet and {commission} SOL to the owner's wallet."
    else:
        return "You lost. Better luck next time!"

# Function to send SOL
async def send_sol(recipient: Pubkey, amount: float):
    lamports = int(amount * 1e9)  # Convert SOL to lamports
    transaction = Transaction()
    transaction.add(
        TransactionInstruction(
            program_id=Pubkey(0),  # Dummy program_id, replace with actual when real transaction
            keys=[
                {"pubkey": keypair.public_key, "is_signer": True, "is_writable": True},
                {"pubkey": recipient, "is_signer": False, "is_writable": True},
            ],
            data=lamports.to_bytes(8, "little"),  # Amount in lamports
        )
    )
    try:
        response = await solana_client.send_transaction(transaction, keypair, opts=TxOpts(skip_preflight=True))
        print(f"Transaction successful: {response['result']}")
    except RPCException as e:
        print(f"Transaction failed: {e}")

# /help command
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, HELP_TEXT)

# /start command
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, START_TEXT)

# /deposit command
@bot.message_handler(commands=["deposit"])
def deposit_message(message):
    bot.send_message(message.chat.id, "Please enter your wallet address to deposit:")
    bot.register_next_step_handler(message, handle_deposit)

def handle_deposit(message):
    try:
        user_wallet_address_str = message.text.strip()  # Get user wallet address as string
        user_wallet_address = Pubkey.from_string(user_wallet_address_str)  # Convert to Pubkey
        bot.send_message(message.chat.id, "Enter the amount of SOL you want to deposit:")
        bot.register_next_step_handler(message, lambda msg: handle_deposit_amount(msg, user_wallet_address))
    except ValueError:
        bot.send_message(message.chat.id, "Invalid wallet address. Please enter a valid Solana wallet address.")

def handle_deposit_amount(message, user_wallet_address):
    try:
        deposit_amount = float(message.text)
        success = deposit_crypto(user_wallet_address, deposit_amount)
        if success:
            bot.send_message(message.chat.id, f"Deposited {deposit_amount} SOL successfully! You can now flip a coin.")
        else:
            bot.send_message(message.chat.id, "Deposit failed, please try again.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid amount, please enter a valid number.")

# /coin command
@bot.message_handler(commands=["coin"])
def flip_coin(message):
    bot.send_message(message.chat.id, "How much would you like to flip?")
    bot.register_next_step_handler(message, handle_coin_flip)

def handle_coin_flip(message):
    try:
        deposit_amount = float(message.text)
        bot.send_message(message.chat.id, "Enter your wallet address to receive payouts:")
        bot.register_next_step_handler(message, lambda msg: handle_user_wallet(msg, deposit_amount))
    except ValueError:
        bot.send_message(message.chat.id, "Invalid amount, please enter a valid number.")

def handle_user_wallet(message, deposit_amount):
    try:
        user_wallet_address_str = message.text.strip()
        user_wallet_address = Pubkey.from_string(user_wallet_address_str)  # Convert to Pubkey
        bot.send_message(message.chat.id, "Choose your side: Type 'Heads' or 'Tails'")
        bot.register_next_step_handler(message, lambda msg: handle_user_choice(msg, deposit_amount, user_wallet_address))
    except ValueError:
        bot.send_message(message.chat.id, "Invalid wallet address. Please enter a valid Solana wallet address.")

def handle_user_choice(message, deposit_amount, user_wallet_address):
    user_choice = message.text.strip().capitalize()
    if user_choice not in ["Heads", "Tails"]:
        bot.send_message(message.chat.id, "Invalid choice. Please choose either Heads or Tails.")
        return

    result = flip_crypto(user_wallet_address, deposit_amount, user_choice)
    bot.send_message(message.chat.id, result)

# Main loop to start bot polling
def main():
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Error: {e}")
            pass

if __name__ == "__main__":
    main()
