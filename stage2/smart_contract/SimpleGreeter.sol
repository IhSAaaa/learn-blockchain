// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SimpleGreeter
 * @dev A simple contract for demonstrating Solidity and blockchain interaction.
 */
contract SimpleGreeter {
    // State variables
    string public greeting;
    address public owner;
    
    // Event to log greeting updates
    event GreetingUpdated(address indexed updater, string newGreeting);
    
    /**
     * @dev Constructor - sets the initial greeting and owner.
     * @param initialGreeting The initial greeting message.
     */
    constructor(string memory initialGreeting) {
        greeting = initialGreeting;
        owner = msg.sender;
    }
    
    /**
     * @dev Updates the greeting message.
     * @param newGreeting The new greeting message.
     */
    function setGreeting(string memory newGreeting) public {
        greeting = newGreeting;
        emit GreetingUpdated(msg.sender, newGreeting);
    }
    
    /**
     * @dev Gets the current greeting (view function - no gas cost).
     * @return The current greeting message.
     */
    function getGreeting() public view returns (string memory) {
        return greeting;
    }
}
