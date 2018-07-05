var OracleCore = artifacts.require("./OracleCore");
var TestOracleExample = artifacts.require("./TestOracleExample");

module.exports = function(deployer) {
    deployer.deploy(OracleCore).then(function(inst) {
        return deployer.deploy(TestOracleExample);
    }).then(function(inst) {
        // do nothing right now
    });
 }
