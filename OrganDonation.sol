// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OrganDonation {
    struct Match {
        string donorId;
        string recipientId;
        string organType;
        uint timestamp;
    }

    Match[] public matches;

    event MatchSaved(string donorId, string recipientId, string organType, uint timestamp);

    function saveMatch(string memory _donorId, string memory _recipientId, string memory _organType) public {
        matches.push(Match(_donorId, _recipientId, _organType, block.timestamp));
        emit MatchSaved(_donorId, _recipientId, _organType, block.timestamp);
    }

    function getMatches() public view returns (Match[] memory) {
        return matches;
    }
}
