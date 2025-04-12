# Guess the Number Blockchain Game

A decentralized number guessing game built on Ethereum blockchain with Python and Solidity.

## Game Overview

"Guess the Number" is a two-player game where:
- Player A selects a secret number
- Player B tries to guess that number within a limited number of attempts
- After each guess, Player B receives feedback on whether their guess was too high, too low, or correct

This implementation uses blockchain technology to ensure fairness and prevent cheating. The game logic is implemented as smart contracts on the Ethereum blockchain, with different versions offering varying levels of security, privacy, and gameplay features.

## Project Structure

```
guess-the-number-blockchain/
├── .gitignore
├── .env                 # Global environment variables
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── main.py              # Main entry point to select game version
├── common/
│   ├── __init__.py
│   └── blockchain.py    # Common blockchain utilities
├── contracts/
│   ├── version1.sol     # Basic game smart contract
│   ├── version2.sol     # Game with rewards smart contract
│   ├── version3.sol     # Generic contract smart contract
│   └── version4.sol     # Confidential number smart contract
└── versions/
    ├── v1/              # Basic game implementation
    │   ├── __init__.py
    │   ├── client.py
    │   ├── config.env   # Version-specific contract data
    │   └── README.md
    ├── v2/              # Game with rewards implementation
    │   ├── __init__.py
    │   ├── client.py
    │   ├── config.env   # Version-specific contract data
    │   └── README.md
    ├── v3/              # Generic contract implementation
    │   ├── __init__.py
    │   ├── client.py
    │   ├── config.env   # Version-specific contract data
    │   └── README.md
    └── v4/              # Game with number confidentiality
        ├── __init__.py
        ├── client.py
        ├── config.env   # Version-specific contract data
        └── README.md
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Ethereum provider and private keys in the global `.env` file:
```
PROVIDER_URL=your_ethereum_provider_url
PRIVATE_KEY_JOUEUR_A=your_player_a_private_key
PRIVATE_KEY_JOUEUR_B=your_player_b_private_key
```

## Usage

Run the main application:
```bash
python main.py
```

Then select which version of the game you want to play.

## Game Versions

### Version 1: Basic Game

The basic version is a simple implementation of the number guessing game:

- **Player A**: Chooses a secret number between 1 and 100 and deploys a dedicated smart contract.
- **Player B**: Tries to guess the secret number by proposing numbers each turn.
- **Smart Contract Response**: For each guess, the contract returns whether the proposed number is "too small", "too large", or "correct".
- **Limited Attempts**: The number of attempts is limited (e.g., 10 tries).
- **Game End**: The game ends when Player B correctly guesses the number or runs out of attempts.

### Version 2: Game with Rewards

This version adds an economic dimension with ETH staking:

- **Player A**: Chooses a secret number and deploys a contract with an ETH stake.
- **Player B**: Guesses the number and also places an ETH stake to participate.
- **Smart Contract Response**: Same as Version 1, but with stakes at risk.
- **Rewards**: If Player B finds the correct number, they win both stakes. If not, Player A keeps both stakes.
- **Limited Attempts**: Same as Version 1, with a limited number of guesses.

### Version 3: Generic Contract

This version improves on the previous ones by using a single generic contract:

- Allows multiple pairs of players (A, B) to initiate and play games.
- Supports both staking and non-staking modes.
- More efficient as it doesn't require deploying a new contract for each game.
- Maintains the same gameplay mechanics as previous versions.

### Version 4: Game with Number Confidentiality

This version adds privacy protection for the secret number:

- **Player A**: Chooses a secret number, but it's "masked" (hashed) before being submitted to the smart contract.
- **Player B**: Guesses are also hashed before comparison.
- **Privacy Protection**: The secret number remains confidential and cannot be discovered from public blockchain data.
- **Verification**: The contract can still verify guesses without revealing the actual number.
- **Supports Staking**: Like Version 3, this version can be played with or without ETH stakes.

## Environment Files

The project uses two types of environment files:
- Global `.env` file: Contains provider URL and private keys
- Version-specific `config.env` files: Contain contract bytecode and ABI for each version

## Development

Each version is self-contained and can be run independently. The main.py file provides a menu to select which version to run.

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please see the CONTRIBUTING.md file for guidelines.

## Security Warning

**WARNING**: Never commit real private keys to version control! The private keys in this repository are for demonstration purposes only.