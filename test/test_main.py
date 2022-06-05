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
    "mainFileName, dataIn, expected",
    [
        (
            "helloWorld",
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
        ),
        (
            "findMaxInArr",
            [
                Variable("size", ".word 1", 4, 2),
                Variable("arr", ".word 0", 4, 2)
            ],
            [
                ((4, "int"), 0)
            ]
        ),
        (
            "findMaxInArr",
            [
                Variable("size", ".word 2", 4, 2),
                Variable("arr", ".word 0\n.word 1", 4, 2)
            ],
            [
                ((4, "int"), 1)
            ]
        ),
        (
            "findMaxInArr",
            [
                Variable("size", ".word 2", 4, 2),
                Variable("arr", ".word 1\n.word 0", 4, 2)
            ],
            [
                ((4, "int"), 1)
            ]
        ),
        (
            "findMaxInArr",
            [
                Variable("size", ".word 3", 4, 2),
                Variable("arr", ".word 2\n.word 3\n.word 1", 12, 2)
            ],
            [
                ((4, "int"), 3)
            ]
        ),
        (
            "gcdEuclid",
            [
                Variable("arr", ".word 1\n.word 1\n.word 1", 8, 2)
            ],
            [
                ((4, "int"), 1)
            ]
        ),
        (
            "gcdEuclid",
            [
                Variable("arr", ".word 4\n.word 2\n.word 1", 8, 2)
            ],
            [
                ((4, "int"), 2)
            ]
        ),
        (
            "gcdEuclid",
            [
                Variable("arr", ".word 4\n.word 2\n.word 1", 8, 2)
            ],
            [
                ((4, "int"), 2)
            ]
        ),
        (
            "gcdEuclid",
            [
                Variable("arr", ".word 1071\n.word 462\n.word 1", 8, 2)
            ],
            [
                ((4, "int"), 21)
            ]
        ),
    ]
)


def test_main(mainFileName, dataIn, expected):
    outRoot = os.path.join("test", "out")
    srcFileName = os.path.join("src", mainFileName + ".s")
    name = mainFileName + "Test"

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
