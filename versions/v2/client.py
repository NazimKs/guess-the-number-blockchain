from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env files
load_dotenv('.env')  # Load global .env
load_dotenv('versions/v2/config.env')  # Load version-specific config

# Configuration
PROVIDER_URL = os.getenv('PROVIDER_URL')
PRIVATE_KEY_JOUEUR_A = os.getenv('PRIVATE_KEY_JOUEUR_A')
PRIVATE_KEY_JOUEUR_B = os.getenv('PRIVATE_KEY_JOUEUR_B')

# Load contract data from version-specific .env
CONTRACT_BYTECODE = os.getenv('CONTRACT_BYTECODE')
CONTRACT_ABI = json.loads(os.getenv('CONTRACT_ABI', '[]'))

# Initialize web3
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

def deploy_contract(joueur_a_private_key, secret_number, max_attempts, stake):
    compte = w3.eth.account.from_key(joueur_a_private_key)
    contrat = w3.eth.contract(abi=CONTRACT_ABI, bytecode=CONTRACT_BYTECODE)
    
    # Build transaction for contract deployment
    tx = contrat.constructor(secret_number, max_attempts).build_transaction({
        'from': compte.address,
        'nonce': w3.eth.get_transaction_count(compte.address),
        'value': w3.to_wei(stake, 'ether')
    })
    
    # Sign and send transaction
    tx_signe = compte.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(tx_signe.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
    
    print(f"Contract deployed at address: {receipt.contractAddress}")
    return receipt.contractAddress

def jouer_partie(joueur_b_private_key, contrat_address):
    compte = w3.eth.account.from_key(joueur_b_private_key)
    contrat = w3.eth.contract(address=contrat_address, abi=CONTRACT_ABI)
    
    # Player B must stake ETH first
    while True:
        try:
            stake = float(input("Enter your stake in ETH (must be positive): "))
            if stake > 0:
                break
            else:
                print("Error: Stake must be a positive value.")
        except ValueError:
            print("Error: Please enter a valid number.")
    
    try:
        tx_mise = contrat.functions.miser().build_transaction({
            'from': compte.address,
            'nonce': w3.eth.get_transaction_count(compte.address),
            'value': w3.to_wei(stake, 'ether')
        })
    except Exception as e:
        print(f"Error preparing stake transaction: {e}")
        return
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
                print("Congratulations! You found the secret number and won the stakes!")
                return
            
            tentatives_restantes = result_event['attemptsRemaining']
            
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print("Game over - You have used all your attempts.")
    mises = contrat.functions.getMises().call()
    print(f"Total stakes: {w3.from_wei(mises[0] + mises[1], 'ether')} ETH")


if __name__ == "__main__":
    running = True
    
    while running:
        print("\n1. Player A - Create contract with stake")
        print("2. Player B - Play with stake")
        print("3. Exit")
        choix = input("Choose (1, 2, or 3): ")
        
        if choix == "1":
            # Input validation for secret number
            while True:
                try:
                    secret_number = int(input("Enter the secret number (between 1 and 100): "))
                    if 1 <= secret_number <= 100:
                        break
                    else:
                        print("Error: The secret number must be between 1 and 100.")
                except ValueError:
                    print("Error: Please enter a valid number.")
            
            # Input validation for number of attempts
            while True:
                try:
                    max_attempts = int(input("Enter the number of attempts (between 1 and 10): "))
                    if 1 <= max_attempts <= 10:
                        break
                    else:
                        print("Error: The number of attempts must be between 1 and 10.")
                except ValueError:
                    print("Error: Please enter a valid number.")
            
            # Input validation for stake
            while True:
                try:
                    stake = float(input("Enter your stake in ETH (must be positive): "))
                    if stake > 0:
                        break
                    else:
                        print("Error: Stake must be a positive value.")
                except ValueError:
                    print("Error: Please enter a valid number.")
            
            try:
                deploy_contract(PRIVATE_KEY_JOUEUR_A, secret_number, max_attempts, stake)
            except Exception as e:
                print(f"Error deploying contract: {e}")
        elif choix == "2":
            # Input validation for contract address
            while True:
                adresse_contrat = input("Enter the contract address (0x...): ")
                if adresse_contrat.startswith('0x') and len(adresse_contrat) == 42:
                    try:
                        # Check if it's a valid address format
                        w3.to_checksum_address(adresse_contrat)
                        break
                    except ValueError:
                        print("Error: Invalid Ethereum address format.")
                else:
                    print("Error: Address must start with '0x' and be 42 characters long.")
            
            try:
                jouer_partie(PRIVATE_KEY_JOUEUR_B, adresse_contrat)
            except Exception as e:
                print(f"Error connecting to contract: {e}")
        elif choix == "3":
            print("Exiting the program...")
            running = False
        else:
            print("Invalid choice")