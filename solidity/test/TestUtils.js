/* global assert */

function WaitContractEventGet(myevent) {
    return new Promise((resolve, reject) => {
        myevent.get((error, resp) => {
            if (error !== null) {
                reject(error);
            }
            resolve(resp);
        });
    });
}

function CheckObjectEqual(ol, or) {
    const olKeys = Object.keys(ol).sort();
    const orKeys = Object.keys(or).sort();

    if (olKeys.length !== orKeys.length) {
        console.log(`show me compare result: ${olKeys} v.s. ${orKeys}`);
        return false;
    }

    for (let i = 0; i < olKeys.length; i += 1) {
        const olKey = olKeys[i];
        const orKey = orKeys[i];
        if (olKey !== orKey || ol[olKey] !== or[orKey]) {
            console.log(`show me compare result ${olKey}: ${ol[olKey]} v.s. ${orKey}: ${or[orKey]}`);
            return false;
        }
    }
    return true;
}

async function AssertRevert(promise) {
    try {
        await promise;
        assert.fail('Expected revert not received');
    } catch (error) {
        const revertFound = error.message.search('revert') >= 0;
        assert(revertFound, `Expected "revert", got ${error} instead`);
    }
}

async function AssertPass(promise) {
    try {
        await promise;
    } catch (error) {
        console.log(`Expected error received, got ${error}`);
        assert.fail(`Expected error received, got ${error}`);
    }
}

module.exports = {
    WaitContractEventGet,
    CheckObjectEqual,
    AssertRevert,
    AssertPass,
};
