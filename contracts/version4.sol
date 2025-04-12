// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DevineNombreHache {
    bytes32 private secretHash;
    uint private maxAttempts;
    uint private attemptsLeft;
    bool private gameActive;
    bool public hasStaking;
    
    // Staking-related variables
    address payable public joueurA;
    address payable public joueurB;
    uint public miseA;
    uint public miseB;
    bool public aMise;
    bool public bMise;

    event GuessResult(string result, uint attemptsRemaining);

    constructor(bytes32 _secretHash, uint _maxAttempts, bool _hasStaking) payable {
        require(_maxAttempts > 0, "Le nombre de tentatives doit etre superieur a 0");
        secretHash = _secretHash;
        maxAttempts = _maxAttempts;
        attemptsLeft = _maxAttempts;
        gameActive = true;
        hasStaking = _hasStaking;
        
        if (hasStaking) {
            require(msg.value > 0, "Une mise est requise");
            joueurA = payable(msg.sender);
            miseA = msg.value;
            aMise = true;
        }
    }

    function miser() external payable {
        require(hasStaking, "Ce contrat n'a pas de fonctionnalite de mise");
        require(!bMise, "Le joueur B a deja mise");
        require(msg.value > 0, "Une mise est requise");
        require(msg.sender != joueurA, "Le joueur A ne peut pas miser deux fois");
        
        joueurB = payable(msg.sender);
        miseB = msg.value;
        bMise = true;
    }

    function deviner(bytes32 _proposition) external returns (string memory) {
        require(gameActive, "La partie est terminee");
        
        if (hasStaking) {
            require(bMise, "Le joueur B doit miser d'abord");
            require(msg.sender == joueurB, "Seul le joueur B peut deviner");
        }
        
        attemptsLeft--;
        
        if (_proposition == secretHash) {
            gameActive = false;
            if (hasStaking) {
                joueurB.transfer(miseA + miseB);
            }
            emit GuessResult("Correct", attemptsLeft);
            return "Correct";
        } else if (attemptsLeft == 0) {
            gameActive = false;
            if (hasStaking) {
                joueurA.transfer(miseA + miseB);
            }
            emit GuessResult("Perdu", attemptsLeft);
            return "Perdu";
        } else {
            emit GuessResult("Incorrect", attemptsLeft);
            return "Incorrect";
        }
    }

    function getTentativesRestantes() external view returns (uint) {
        return attemptsLeft;
    }
    
    function getMises() external view returns (uint, uint) {
        require(hasStaking, "Ce contrat n'a pas de fonctionnalite de mise");
        return (miseA, miseB);
    }
}