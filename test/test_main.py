import pytest
import os
from utils import Variable
from utils import runTestAndGetBytesOut


def interpretOneDataInfo(bytesArr, dataType):
    if (dataType == "char"):
        assert(len(bytesArr) == 1)
        return chr(int.from_bytes(bytesArr[0], "little"))
    elif(dataType == "int"):
        assert(len(bytesArr) == 4)
        return int.from_bytes(bytesArr[0], "little")
    else:
        print("Unknown data type!")
        assert(False)
    return 'x'


def interpretOutBytes(byteArr, dataInfos):
    res = []
    i = 0
    for dataInfo in dataInfos:
        sizeInBytes = dataInfo[0]
        dataType = dataInfo[1]
        res.append(interpretOneDataInfo(byteArr[i : i + sizeInBytes], dataType))
        i += sizeInBytes

    assert(i == len(byteArr))
    return res


def checkOutput(out, expected):
    lenOut = len(out)
    assert(lenOut == len(expected))
    i = 0
    for el in out:
        assert(el == expected[i])
        i += 1
    return


@pytest.mark.parametrize(
    "dataIn, expected",
    [
        (
            [
                Variable("greeting", ".asciz \"Hello world!\"", 12, 2),
                Variable("intVar", ".word 42", 4, 2)
            ],
            [
                ((1, "char"), 'H'),
                ((1, "char"), 'e'),
                ((1, "char"), 'l'),
                ((1, "char"), 'l'),
                ((1, "char"), 'o'),
                ((1, "char"), ' '),
                ((1, "char"), 'w'),
                ((1, "char"), 'o'),
                ((1, "char"), 'r'),
                ((1, "char"), 'l'),
                ((1, "char"), 'd'),
                ((1, "char"), '!'),
                ((4, "int"), 42)
            ]
        )
    ]
)


def test_main(dataIn, expected):
    outRoot = os.path.join("test", "out")
    srcFileName = os.path.join("src", "helloWorld.s")
    name = "HelloWorldTest"

    testName = name + str(test_main.counter)
    testDir = os.path.join(outRoot, testName)
    test_main.counter += 1
    if not os.path.exists(testDir):
        os.makedirs(testDir)

    expectedSize = 0
    dataInfos = []
    expectedVals = []
    for el in expected:
        expectedSize += el[0][0]
        dataInfos.append(el[0])
        expectedVals.append(el[1])
    bytesOut = runTestAndGetBytesOut(srcFileName, dataIn, expectedSize, testDir)
    outVals = interpretOutBytes(bytesOut, dataInfos)
    checkOutput(outVals, expectedVals)
    return


test_main.counter = 0
