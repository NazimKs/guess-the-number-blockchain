// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DevineNombre {
    uint private secretNumber;
    uint private maxAttempts;
    uint private attemptsLeft;
    bool private gameActive;

    event GuessResult(string result, uint attemptsRemaining);

    constructor(uint _secretNumber, uint _maxAttempts) {
        require(_secretNumber >= 1 && _secretNumber <= 100, "The number must be between 1 and 100");
        secretNumber = _secretNumber;
        maxAttempts = _maxAttempts;
        attemptsLeft = _maxAttempts;
        gameActive = true;
    }

    function deviner(uint _nombre) external returns (string memory) {
        require(gameActive, "The game is over");
        require(_nombre >= 1 && _nombre <= 100, "The number must be between 1 and 100");
        
        attemptsLeft--;
        
        if (_nombre == secretNumber) {
            gameActive = false;
            emit GuessResult("Correct", attemptsLeft);
            return "Correct";
        } else if (_nombre < secretNumber) {
            if (attemptsLeft == 0) gameActive = false;
            emit GuessResult("Higher", attemptsLeft);
            return "Higher";
        } else {
            if (attemptsLeft == 0) gameActive = false;
            emit GuessResult("Lower", attemptsLeft);
            return "Lower";
        }
    }

    function getTentativesRestantes() external view returns (uint) {
        return attemptsLeft;
    }
}