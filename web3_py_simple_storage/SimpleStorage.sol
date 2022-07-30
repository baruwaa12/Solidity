// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;  // Always define at the beginning of a program

contract SimpleStorage {
    
    // initalized to 0
    uint256 favouriteNumber;
    bool favouriteBool;

    struct People {
        uint256 favouriteNumber;
        string name;
    }
    
    // How to create a struct
    People[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;

    function store(uint256 _favoriteNumber) public {
        favouriteNumber = _favoriteNumber;
    }

    
    // view functions allow a state to be read on the function
    function retrieve() public view returns(uint256) {
        return favouriteNumber;
    }       

    function addPerson(string memory _name, uint256 _favoriteNumber) public{
        people.push(People(favouriteNumber, _name));      
    }
}