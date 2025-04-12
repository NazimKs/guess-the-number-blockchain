// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DevineNombreV2 {
    uint private secretNumber;
    uint private maxAttempts;
    uint private attemptsLeft;
    bool private gameActive;
    
    address payable public joueurA;
    address payable public joueurB;
    uint public miseA;
    uint public miseB;
    bool public aMise;
    bool public bMise;

    event GuessResult(string result, uint attemptsRemaining);

    constructor(uint _secretNumber, uint _maxAttempts) payable {
        require(_secretNumber >= 1 && _secretNumber <= 100, "The number must be between 1 and 100");
        require(msg.value > 0, "A stake is required");
        
        secretNumber = _secretNumber;
        maxAttempts = _maxAttempts;
        attemptsLeft = _maxAttempts;
        gameActive = true;
        joueurA = payable(msg.sender);
        miseA = msg.value;
        aMise = true;
    }

    function miser() external payable {
        require(!bMise, "Player B has already placed a stake");
        require(msg.value > 0, "A stake is required");
        require(msg.sender != joueurA, "Player A cannot stake twice");
        
        joueurB = payable(msg.sender);
        miseB = msg.value;
        bMise = true;
    }

    function deviner(uint _nombre) external returns (string memory) {
        require(gameActive, "The game is over");
        require(bMise, "Player B must stake first");
        require(_nombre >= 1 && _nombre <= 100, "The number must be between 1 and 100");
        require(msg.sender == joueurB, "Only player B can guess");
        
        attemptsLeft--;
        
        if (_nombre == secretNumber) {
            gameActive = false;
            joueurB.transfer(miseA + miseB);
            emit GuessResult("Correct", attemptsLeft);
            return "Correct";
        } else if (_nombre < secretNumber) {
            if (attemptsLeft == 0) {
                gameActive = false;
                joueurA.transfer(miseA + miseB);
            }
            emit GuessResult("Higher", attemptsLeft);
            return "Higher";
        } else {
            if (attemptsLeft == 0) {
                gameActive = false;
                joueurA.transfer(miseA + miseB);
            }
            emit GuessResult("Lower", attemptsLeft);
            return "Lower";
        }
    }

    function getTentativesRestantes() external view returns (uint) {
        return attemptsLeft;
    }
    
    function getMises() external view returns (uint, uint) {
        return (miseA, miseB);
    }
}