import os
import subprocess


class Variable:
    def __init__(self, name, valStr, size, p2align):
        self.name = name
        self.valStr = valStr
        self.size = size
        self.p2align = p2align
        return


def writeDataInFile(dataIn, outDir):
    outFile = open(os.path.join(outDir, "dataIn.s"), "w")
    for var in dataIn:
        outFile.write(
            (
                ".type  {name}, @object\n" +
                ".section  .data\n" +
                ".globl  {name}\n" +
                ".p2align  {p2alignStr}\n" +
                "{name}:\n" +
                "  {valStr}\n" +
                "  .size  {name}, {sizeStr}\n\n"
            )
            .format(
                name=var.name,
                valStr=str(var.valStr),
                sizeStr=str(var.size),
                p2alignStr=str(var.p2align)
            )
        )
    outFile.close()
    return


def writeGdbRunFile(outSizeInBytes, outDir):
    outFile = open(os.path.join(outDir, "gdbRun.gdb"), "w")
    outFile.write(
        "target remote:1234\n" +
        "break _end\n" +
        "continue\n"
    )
    outFile.write("echo OUTPUT_START\\n\n")
    outFile.write(
        "x/{sizeStr}xb &__dataOutTop\n"
        .format(sizeStr=str(outSizeInBytes))
    )
    outFile.write("echo OUTPUT_END\\n\n")
    outFile.close()
    return


def writeFiles(srcFileName, dataIn, expectedSize, outDir):
    writeDataInFile(dataIn, outDir)

    writeGdbRunFile(expectedSize, outDir)
    os.system(
        "cp {srcFileName} {outDir}/main.s"
        .format(
            srcFileName=srcFileName,
            outDir=outDir
        )
    )

    for fileName in [
        "startup.s",
        "riscv32.lds",
        "Makefile",
        "gdbDebug.gdb"
    ]:
        os.system(
            "cp test/{fileName} {outDir}/{fileName}"
            .format(
                fileName=fileName,
                outDir=outDir
            )
        )
    return


def extractBytes(out):
    out = out.decode("utf-8")
    out = out.split("\n")
    outStartIdx = out.index("OUTPUT_START") + 1
    outEndIdx = out.index("OUTPUT_END")
    out = out[outStartIdx : outEndIdx]
    outBytesStr = []
    for line in out:
        splitted = line.split("\t")
        for i in range(1, len(splitted)):
            outBytesStr.append(int(splitted[i], 16).to_bytes(1, byteorder="little"))
    
    return outBytesStr


def runTestAndGetBytesOut(srcFileName, dataIn, expectedSize, outDir):
    writeFiles(srcFileName, dataIn, expectedSize, outDir)

    p = subprocess.Popen(
        ["make", "gdbRun"],
        stdout=subprocess.PIPE,
        cwd = outDir
    )
    out, err = p.communicate()

    return extractBytes(out)
