from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env files
load_dotenv('.env')  # Load global .env
load_dotenv('versions/v3/config.env')  # Load version-specific config

# Configuration
PROVIDER_URL = os.getenv('PROVIDER_URL')
PRIVATE_KEY_JOUEUR_A = os.getenv('PRIVATE_KEY_JOUEUR_A')
PRIVATE_KEY_JOUEUR_B = os.getenv('PRIVATE_KEY_JOUEUR_B')

# Load contract data from version-specific .env
CONTRACT_BYTECODE = os.getenv('CONTRACT_BYTECODE')
CONTRACT_ABI = json.loads(os.getenv('CONTRACT_ABI', '[]'))
# Initialize web3
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

def deploy_contract(joueur_a_private_key, secret_number, max_attempts, stake=None):
    compte = w3.eth.account.from_key(joueur_a_private_key)
    contrat = w3.eth.contract(abi=CONTRACT_ABI, bytecode=CONTRACT_BYTECODE)
    
    # Determine if we're using staking mode
    has_staking = stake is not None
    
    # Build transaction for contract deployment
    tx_params = {
        'from': compte.address,
        'nonce': w3.eth.get_transaction_count(compte.address)
    }
    
    if has_staking:
        tx_params['value'] = w3.to_wei(stake, 'ether')
    
    tx = contrat.constructor(secret_number, max_attempts, has_staking).build_transaction(tx_params)
    
    # Sign and send transaction
    tx_signe = compte.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(tx_signe.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
    
    print(f"Contract deployed at address: {receipt.contractAddress}")
    return receipt.contractAddress

def jouer_partie(joueur_b_private_key, contrat_address):
    compte = w3.eth.account.from_key(joueur_b_private_key)
    contrat = w3.eth.contract(address=contrat_address, abi=CONTRACT_ABI)
    
    # Check if contract has staking
    has_staking = contrat.functions.hasStaking().call()
    
    if has_staking:
        # Player B must stake ETH first
        stake = float(input("Enter your stake in ETH: "))
        tx_mise = contrat.functions.miser().build_transaction({
            'from': compte.address,
            'nonce': w3.eth.get_transaction_count(compte.address),
            'value': w3.to_wei(stake, 'ether')
        })
        tx_mise_signe = compte.sign_transaction(tx_mise)
        tx_mise_hash = w3.eth.send_raw_transaction(tx_mise_signe.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_mise_hash, timeout=30)
        print("Stake placed successfully!")
    
    tentatives_restantes = contrat.functions.getTentativesRestantes().call()
    print(f"Game started. Remaining attempts: {tentatives_restantes}")
    
    while tentatives_restantes > 0:
        try:
            proposition = int(input("Guess a number between 1 and 100: "))
            if proposition < 1 or proposition > 100:
                print("The number must be between 1 and 100")
                continue
            
            # Prepare the transaction
            tx = contrat.functions.deviner(proposition).build_transaction({
                'from': compte.address,
                'nonce': w3.eth.get_transaction_count(compte.address)
            })
            
            # Sign and send
            tx_signe = compte.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(tx_signe.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            
            # Get the result
            result_event = contrat.events.GuessResult().process_receipt(receipt)[0]['args']
            print(f"Result: {result_event['result']}, Remaining attempts: {result_event['attemptsRemaining']}")
            
            if result_event['result'] == "Correct":
                if has_staking:
                    print("Congratulations! You found the secret number and won the stakes!")
                else:
                    print("Congratulations! You found the secret number!")
                return
            
            tentatives_restantes = result_event['attemptsRemaining']
            
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print("Game over - You have used all your attempts.")
    if has_staking:
        mises = contrat.functions.getMises().call()
        print(f"Total stakes: {w3.from_wei(mises[0] + mises[1], 'ether')} ETH")

if __name__ == "__main__":
    print("1. Player A - Create the contract")
    print("2. Player B - Play the game")
    choix = input("Choose (1 or 2): ")
    
    if choix == "1":
        secret_number = int(input("Enter the secret number: "))
        max_attempts = int(input("Enter the number of attempts: "))
        use_staking = input("Do you want to use staking? (y/n): ").lower() == 'y'
        
        if use_staking:
            stake = float(input("Enter your stake in ETH: "))
            deploy_contract(PRIVATE_KEY_JOUEUR_A, secret_number, max_attempts, stake)
        else:
            deploy_contract(PRIVATE_KEY_JOUEUR_A, secret_number, max_attempts)
    elif choix == "2":
        adresse_contrat = input("Enter the contract address: ")
        jouer_partie(PRIVATE_KEY_JOUEUR_B, adresse_contrat)
    else:
        print("Invalid choice")