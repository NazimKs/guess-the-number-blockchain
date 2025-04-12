// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DevineNombre {
    uint private secretNumber;
    uint private maxAttempts;
    uint private attemptsLeft;
    bool private gameActive;

    event GuessResult(string result, uint attemptsRemaining);

    constructor(uint _secretNumber, uint _maxAttempts) {
        require(_secretNumber >= 1 && _secretNumber <= 100, "Le nombre doit etre entre 1 et 100");
        secretNumber = _secretNumber;
        maxAttempts = _maxAttempts;
        attemptsLeft = _maxAttempts;
        gameActive = true;
    }

    function deviner(uint _nombre) external returns (string memory) {
        require(gameActive, "La partie est terminee");
        require(_nombre >= 1 && _nombre <= 100, "Le nombre doit etre entre 1 et 100");
        
        attemptsLeft--;
        
        if (_nombre == secretNumber) {
            gameActive = false;
            emit GuessResult("Correct", attemptsLeft);
            return "Correct";
        } else if (_nombre < secretNumber) {
            if (attemptsLeft == 0) gameActive = false;
            emit GuessResult("Plus grand", attemptsLeft);
            return "Plus grand";
        } else {
            if (attemptsLeft == 0) gameActive = false;
            emit GuessResult("Plus petit", attemptsLeft);
            return "Plus petit";
        }
    }

    function getTentativesRestantes() external view returns (uint) {
        return attemptsLeft;
    }
}