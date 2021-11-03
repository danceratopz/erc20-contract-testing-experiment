var XyzCoin = artifacts.require("./XyzCoin.sol");

module.exports = function(deployer) {
    deployer.deploy(XyzCoin, 1e3);
};
