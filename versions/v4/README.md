# Guess The Number - Version 4

This is an enhanced version of the blockchain-based "Guess the Number" game, now with an additional security feature where Player A provides an encoded number using the keccak256 hash.

## How It Works

1. **Player A**:
    - Decides whether the game will be played with a stake or not.
    - Provides the keccak256 hash of the number to guess, the maximum number of attempts, and optionally a stake (amount of cryptocurrency).
    - Deploys a smart contract with these inputs.

2. **Player B**:
    - Enters the smart contract address.
    - If Player A has chosen to play with a stake, Player B must place an equal stake to start guessing the number.
    - If no stake is required, Player B can start guessing without placing any stake.

3. **Revealing the Number**:
    - Once the game ends, Player A must reveal the original number to verify the hash and determine the winner.

## Winning Conditions
- If Player B guesses the number correctly within the allowed attempts, they win and receive both stakes (if applicable).
- If Player B fails to guess the number, Player A wins and takes both stakes (if applicable).

Enjoy the game with enhanced security and fairness!  