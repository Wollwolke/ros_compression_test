#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE
import resource
import filecmp
import json

sizes = {}
times = {}
samples = {}
algorithms = ["lzmh", "zlib", "bzip2", "lzma", "zstd", "lzo", "brotli"]

ROUNDS = 20

def init():
    global sizes
    global times

    with open("data/temperature.bin", "rb") as file:
        samples["temperature"] = file.read()
    with open("data/battery.bin", "rb") as file:
        samples["battery"] = file.read()
    with open("data/humidity.bin", "rb") as file:
        samples["humidity"] = file.read()
    with open("data/image.bin", "rb") as file:
        samples["image"] = file.read()
    with open("data/position.bin", "rb") as file:
        samples["position"] = file.read()
    with open("data/tempSensor.bin", "rb") as file:
        samples["tempSensor"] = file.read()

    for sample, data in samples.items():
        if sample not in sizes.keys():
            sizes[sample] = {}
            times[sample] = {}
        sizes[sample]["raw"] = len(data)
        for algo in algorithms:
            sizes[sample][algo] = {}
            times[sample][algo] = {}

def zlib():
    global sizes
    global times
    for sample, data in samples.items():
        for lvl in range(1,10):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"zlib {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen(["zlib-flate", f"-compress={lvl}"], stdout=PIPE, stdin=PIPE)
                compressedData = process.communicate(input=data)[0]
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen(["zlib-flate", "-uncompress"], stdout=PIPE, stdin=PIPE)
                if process.communicate(input=compressedData)[0] != data:
                    raise ValueError(f"Error uncompressing zlib lvl {lvl}\t{sample}")

                # Check compressed size
                if i != 0 and compressedSize != len(compressedData):
                    raise ValueError("Error: different compressed size for same lvl!")
                else:
                    compressedSize = len(compressedData)

                # Calc used time
                utime = usageEnd.ru_utime - usageStart.ru_utime
                stime = usageEnd.ru_stime - usageStart.ru_stime
                localTimes.append(utime + stime)

            # store results
            sizes[sample]["zlib"][lvl] = compressedSize
            times[sample]["zlib"][lvl] = sum(localTimes) / ROUNDS

def brotli():
    global sizes
    global times
    for sample, data in samples.items():
        for lvl in range(12):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"brotli {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen(["brotli", "--stdout", "--force", f"--quality={lvl}"], stdout=PIPE, stdin=PIPE)
                compressedData = process.communicate(input=data)[0]
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen(["brotli", "--stdout", "--force", "--decompress"], stdout=PIPE, stdin=PIPE)
                if process.communicate(input=compressedData)[0] != data:
                    raise ValueError(f"Error uncompressing brotli lvl {lvl}\t{sample}")

                # Check compressed size
                if i != 0 and compressedSize != len(compressedData):
                    raise ValueError("Error: different compressed size for same lvl!")
                else:
                    compressedSize = len(compressedData)

                # Calc used time
                utime = usageEnd.ru_utime - usageStart.ru_utime
                stime = usageEnd.ru_stime - usageStart.ru_stime
                localTimes.append(utime + stime)

            # store results
            sizes[sample]["brotli"][lvl] = compressedSize
            times[sample]["brotli"][lvl] = sum(localTimes) / ROUNDS

def lzo():
    global sizes
    global times
    for sample, data in samples.items():
        for lvl in range(1, 10):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"lzo {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen(["lzop", "-c", f"-{lvl}"], stdout=PIPE, stdin=PIPE)
                compressedData = process.communicate(input=data)[0]
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen(["lzop", "-c", "-d"], stdout=PIPE, stdin=PIPE)
                if process.communicate(input=compressedData)[0] != data:
                    raise ValueError(f"Error uncompressing lzo lvl {lvl}\t{sample}")

                # Check compressed size
                if i != 0 and compressedSize != len(compressedData):
                    raise ValueError("Error: different compressed size for same lvl!")
                else:
                    compressedSize = len(compressedData)

                # Calc used time
                utime = usageEnd.ru_utime - usageStart.ru_utime
                stime = usageEnd.ru_stime - usageStart.ru_stime
                localTimes.append(utime + stime)

            # store results
            sizes[sample]["lzo"][lvl] = compressedSize
            times[sample]["lzo"][lvl] = sum(localTimes) / ROUNDS

def zstd():
    global sizes
    global times
    for sample, data in samples.items():
        for lvl in range(1, 20):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"zstd {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen(["zstd", "--stdout", "--force", f"-{lvl}"], stdout=PIPE, stdin=PIPE)
                compressedData = process.communicate(input=data)[0]
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen(["zstd", "--stdout", "--force", "--decompress"], stdout=PIPE, stdin=PIPE)
                if process.communicate(input=compressedData)[0] != data:
                    raise ValueError(f"Error uncompressing zstd lvl {lvl}\t{sample}")

                # Check compressed size
                if i != 0 and compressedSize != len(compressedData):
                    raise ValueError("Error: different compressed size for same lvl!")
                else:
                    compressedSize = len(compressedData)

                # Calc used time
                utime = usageEnd.ru_utime - usageStart.ru_utime
                stime = usageEnd.ru_stime - usageStart.ru_stime
                localTimes.append(utime + stime)

            # store results
            sizes[sample]["zstd"][lvl] = compressedSize
            times[sample]["zstd"][lvl] = sum(localTimes) / ROUNDS

def lzma():
    global sizes
    global times
    for sample, data in samples.items():
        for lvl in range(10):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"lzma {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen(["xz", "--format=lzma", "--stdout", f"-{lvl}"], stdout=PIPE, stdin=PIPE)
                compressedData = process.communicate(input=data)[0]
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen(["xz", "--stdout", "--decompress"], stdout=PIPE, stdin=PIPE)
                if process.communicate(input=compressedData)[0] != data:
                    raise ValueError(f"Error uncompressing lzma lvl {lvl}\t{sample}")

                # Check compressed size
                if i != 0 and compressedSize != len(compressedData):
                    raise ValueError("Error: different compressed size for same lvl!")
                else:
                    compressedSize = len(compressedData)

                # Calc used time
                utime = usageEnd.ru_utime - usageStart.ru_utime
                stime = usageEnd.ru_stime - usageStart.ru_stime
                localTimes.append(utime + stime)

            # store results
            sizes[sample]["lzma"][lvl] = compressedSize
            times[sample]["lzma"][lvl] = sum(localTimes) / ROUNDS

def bzip2():
    global sizes
    global times
    for sample, data in samples.items():
        for lvl in range(1, 10):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"bzip2 {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen(["bzip2", "--compress", "--stdout", f"-{lvl}"], stdout=PIPE, stdin=PIPE)
                compressedData = process.communicate(input=data)[0]
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen(["bzip2", "--stdout", "--decompress"], stdout=PIPE, stdin=PIPE)
                if process.communicate(input=compressedData)[0] != data:
                    raise ValueError(f"Error uncompressing bzip2 lvl {lvl}\t{sample}")

                # Check compressed size
                if i != 0 and compressedSize != len(compressedData):
                    raise ValueError("Error: different compressed size for same lvl!")
                else:
                    compressedSize = len(compressedData)

                # Calc used time
                utime = usageEnd.ru_utime - usageStart.ru_utime
                stime = usageEnd.ru_stime - usageStart.ru_stime
                localTimes.append(utime + stime)

            # store results
            sizes[sample]["bzip2"][lvl] = compressedSize
            times[sample]["bzip2"][lvl] = sum(localTimes) / ROUNDS

def lzmh(useReportedTime=False):
    global sizes
    global times
    binPath = "./data-compressor/DataCompressor/build/gcc/"
    for sample, data in samples.items():
        for lvl in range(1):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"lzmh {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen([f"{binPath}DCCLI", f"data/{sample}.bin", "compressed.tmp", "encode", "lzmh"], stdout=PIPE)
                result = process.communicate()[0].decode("utf-8")
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen([f"{binPath}DCCLI", "compressed.tmp", "uncompressed.tmp", "decode", "lzmh"], stdout=PIPE)
                process.wait()
                if not filecmp.cmp(f"data/{sample}.bin", "uncompressed.tmp", False):
                    raise ValueError(f"Error uncompressing lzmh lvl {lvl}\t{sample}")

                # Check compressed size
                actualSize = os.path.getsize("compressed.tmp")
                if i != 0 and compressedSize != actualSize:
                    raise ValueError("Error: different compressed size for same lvl!")
                else:
                    compressedSize = actualSize

                # Delete tmp files
                os.remove("compressed.tmp")
                os.remove("uncompressed.tmp")

                # Calc used time
                if not useReportedTime:
                    utime = usageEnd.ru_utime - usageStart.ru_utime
                    stime = usageEnd.ru_stime - usageStart.ru_stime
                    localTimes.append(utime + stime)
                else:
                    textContainingTime = result.splitlines()[5]
                    elapsedTime = float(textContainingTime.split(" ")[4]) / 1000000
                    localTimes.append(elapsedTime)

            # store results
            sizes[sample]["lzmh"][lvl] = compressedSize
            times[sample]["lzmh"][lvl] = sum(localTimes) / ROUNDS


def main():
    init()

    zlib()
    brotli()
    lzo()
    zstd()
    lzma()
    bzip2()
    lzmh()
    
    j = {}
    j["times"] = times
    j["sizes"] = sizes

    with open("results.json","w") as file:
        json.dump(j, file)


if __name__ == "__main__":
    main()
