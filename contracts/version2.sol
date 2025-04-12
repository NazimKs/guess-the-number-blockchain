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
        require(_secretNumber >= 1 && _secretNumber <= 100, "Le nombre doit etre entre 1 et 100");
        require(msg.value > 0, "Une mise est requise");
        
        secretNumber = _secretNumber;
        maxAttempts = _maxAttempts;
        attemptsLeft = _maxAttempts;
        gameActive = true;
        joueurA = payable(msg.sender);
        miseA = msg.value;
        aMise = true;
    }

    function miser() external payable {
        require(!bMise, "Le joueur B a deja mise");
        require(msg.value > 0, "Une mise est requise");
        require(msg.sender != joueurA, "Le joueur A ne peut pas miser deux fois");
        
        joueurB = payable(msg.sender);
        miseB = msg.value;
        bMise = true;
    }

    function deviner(uint _nombre) external returns (string memory) {
        require(gameActive, "La partie est terminee");
        require(bMise, "Le joueur B doit miser d'abord");
        require(_nombre >= 1 && _nombre <= 100, "Le nombre doit etre entre 1 et 100");
        require(msg.sender == joueurB, "Seul le joueur B peut deviner");
        
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
            emit GuessResult("Plus grand", attemptsLeft);
            return "Plus grand";
        } else {
            if (attemptsLeft == 0) {
                gameActive = false;
                joueurA.transfer(miseA + miseB);
            }
            emit GuessResult("Plus petit", attemptsLeft);
            return "Plus petit";
        }
    }

    function getTentativesRestantes() external view returns (uint) {
        return attemptsLeft;
    }
    
    function getMises() external view returns (uint, uint) {
        return (miseA, miseB);
    }
}