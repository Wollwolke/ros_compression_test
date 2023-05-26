#!/usr/bin/env python3
import os
from collections import defaultdict
from subprocess import Popen, PIPE
import resource
import filecmp
import json

sizes = {}
times = {}
samples = defaultdict(list)
algorithms = ["zlib", "bzip2", "lzma", "zstd", "lzo", "brotli", "lzmh"]
filenames = ["battery", "detectedImages", "image", "humidity", "position", "temperature", "tempSensor"]

ROUNDS = 5

def init():
    global sizes
    global times
    global samples

    for filename in filenames:
        for cnt in range(10):
            with open(f"data/new/{filename}{cnt}.bin", "rb") as file:
                samples[filename].append(file.read())

    for sampleType, dataList in samples.items():
        if sampleType not in sizes.keys():
            sizes[sampleType] = {}
            times[sampleType] = {}
        size = 0
        for sample in dataList:
            size += len(sample)
        sizes[sampleType]["raw"] = size / len(dataList)
        for algo in algorithms:
            sizes[sampleType][algo] = {}
            times[sampleType][algo] = {}

class Algos:
    def zlib(self, data):
        sizes = {}
        times = {}
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
                    raise ValueError(f"Error uncompressing zlib lvl {lvl}")

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
            sizes[lvl] = compressedSize
            times[lvl] = sum(localTimes) / ROUNDS
        return sizes, times

    def brotli(self, data):
        sizes = {}
        times = {}
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
                    raise ValueError(f"Error uncompressing brotli lvl {lvl}")

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
            sizes[lvl] = compressedSize
            times[lvl] = sum(localTimes) / ROUNDS
        return sizes, times

    def lzo(self, data):
        sizes = {}
        times = {}
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
            sizes[lvl] = compressedSize
            times[lvl] = sum(localTimes) / ROUNDS
        return sizes, times

    def zstd(self, data):
        sizes = {}
        times = {}
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
            sizes[lvl] = compressedSize
            times[lvl] = sum(localTimes) / ROUNDS
        return sizes, times

    def lzma(self, data):
        sizes = {}
        times = {}
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
            sizes[lvl] = compressedSize
            times[lvl] = sum(localTimes) / ROUNDS
        return sizes, times

    def bzip2(self, data):
        sizes = {}
        times = {}
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
            sizes[lvl] = compressedSize
            times[lvl] = sum(localTimes) / ROUNDS
        return sizes, times

    def lzmh(self, data, useReportedTime=False):
        sizes = {}
        times = {}
        binPath = "./data-compressor/DataCompressor/build/gcc/"
        for lvl in range(1):
            localTimes = []
            compressedSize = 0
            for i in range(ROUNDS):
                print(f"lzmh {lvl}")
                usageStart = resource.getrusage(resource.RUSAGE_CHILDREN)
                process = Popen([f"{binPath}DCCLI", data, "compressed.tmp", "encode", "lzmh"], stdout=PIPE)
                result = process.communicate()[0].decode("utf-8")
                usageEnd = resource.getrusage(resource.RUSAGE_CHILDREN)

                # check decompression
                process = Popen([f"{binPath}DCCLI", "compressed.tmp", "uncompressed.tmp", "decode", "lzmh"], stdout=PIPE)
                process.wait()
                if not filecmp.cmp(data, "uncompressed.tmp", False):
                    raise ValueError(f"Error uncompressing lzmh lvl {lvl}")

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
            sizes[lvl] = compressedSize
            times[lvl] = sum(localTimes) / ROUNDS
        return sizes, times

def getMeanDict(dictList):
    resultDict = defaultdict(lambda: 0)
    for entry in dictList:
        for lvl, data in entry.items():
            resultDict[lvl] += data
    
    for lvl, entry in resultDict.items():
        resultDict[lvl] = entry / len(dictList)
    return resultDict

def main():
    global sizes, times

    init()

    for algo in algorithms:
        compressionAlgo = getattr(Algos(), algo)
        for sampleType, sampleList in samples.items():
            sizeList = []
            timeList = []
            cnt = 0
            for sample in sampleList:
                if algo == "lzmh":
                    resultSizes, resultTimes = compressionAlgo(f"data/new/{sampleType}{cnt}.bin")
                    cnt += 1
                else:
                    resultSizes, resultTimes = compressionAlgo(sample)
                sizeList.append(resultSizes)
                timeList.append(resultTimes)
            meanSizes = getMeanDict(sizeList)
            meanTimes = getMeanDict(timeList)
            sizes[sampleType][algo] = meanSizes
            times[sampleType][algo] = meanTimes
    
    j = {}
    j["times"] = times
    j["sizes"] = sizes

    with open("results/resultsImages.json","w") as file:
        json.dump(j, file)


if __name__ == "__main__":
    main()
