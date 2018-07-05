var OracleCore = artifacts.require("./OracleCore");

module.exports = function(deployer) {
    deployer.deploy(OracleCore).then(function(inst) {
    });
 }
