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
        require(_maxAttempts > 0, "The number of attempts must be greater than 0");
        secretHash = _secretHash;
        maxAttempts = _maxAttempts;
        attemptsLeft = _maxAttempts;
        gameActive = true;
        hasStaking = _hasStaking;
        
        if (hasStaking) {
            require(msg.value > 0, "A stake is required");
            joueurA = payable(msg.sender);
            miseA = msg.value;
            aMise = true;
        }
    }

    function miser() external payable {
        require(hasStaking, "This contract does not have staking functionality");
        require(!bMise, "Player B has already placed a stake");
        require(msg.value > 0, "A stake is required");
        require(msg.sender != joueurA, "Player A cannot stake twice");
        
        joueurB = payable(msg.sender);
        miseB = msg.value;
        bMise = true;
    }

    function deviner(bytes32 _proposition) external returns (string memory) {
        require(gameActive, "The game is over");
        
        if (hasStaking) {
            require(bMise, "Player B must stake first");
            require(msg.sender == joueurB, "Only player B can guess");
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
            emit GuessResult("Lost", attemptsLeft);
            return "Lost";
        } else {
            emit GuessResult("Incorrect", attemptsLeft);
            return "Incorrect";
        }
    }

    function getTentativesRestantes() external view returns (uint) {
        return attemptsLeft;
    }
    
    function getMises() external view returns (uint, uint) {
        require(hasStaking, "This contract does not have staking functionality");
        return (miseA, miseB);
    }
}