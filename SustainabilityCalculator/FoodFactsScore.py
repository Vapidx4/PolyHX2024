import sys
import os
import DistanceCalculator as dstCal
import json

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.append(parent_directory)

from EcoScan import OpenFoodFactsScrapper

def calculateResult(image):

    imageDirectory = parent_directory + "\\res\\" + image

    dictData = OpenFoodFactsScrapper.getBarecodeData(imageDirectory)

    result = 0
    maxResult = 0

    if "Scores" in dictData.keys():
        for score in dictData["Scores"]:
            components = score.split()
            if (components[0] == "Nutri-Score" and components[1] != "unknown"):
                result += 4 - (ord(components[1]) - 65)
                maxResult += 4
            elif (components[0] == "NOVA" and components[1] != "not"):
                result += 3 - (int(components[1])-1)
                maxResult += 3
            elif(components[0] == "Eco-Score" and components[1] != "not"):
                result += 4 - (ord(components[1]) - 65)
                maxResult += 4

    if "Carbon Footprint" in dictData.keys():
        value = int(dictData["Carbon Footprint"].split()[0])

        if value < 50:
            result += 2

        elif value < 100:
            result += 1   

        maxResult += 2

    if "Packaging Impact" in dictData.keys() and dictData["Packaging Impact"].split()[0] != "Missing":
        value = dictData["Packaging Impact"].split()[3]

        if value == "low":
            result += 2
        elif value == "medium":
            result += 1

        maxResult += 2

    if "Ingredients Impact" in dictData.keys() and dictData["Ingredients Impact"].split()[0] != "Missing":
        value = dictData["Ingredients Impact"].split()[5]

        if value == "low":
            result += 2
        elif value == "medium":
            result += 1

        maxResult += 2

    if "Manufacturer" in dictData.keys():
        distance = dstCal.findDistance("x", dictData["Manufacturer"])

        if distance < 1000:
            result += 4
        elif distance < 3000:
            result += 3
        elif distance < 5000:
            result += 2
        elif distance < 7000:
            result += 1

        maxResult += 4

    if "Origin of Ingredients" in dictData.keys():
        distance = dstCal.findDistance("x", dictData["Origin of Ingredients"])

        if distance < 1000:
            result += 4
        elif distance < 3000:
            result += 3
        elif distance < 5000:
            result += 2
        elif distance < 7000:
            result += 1

        maxResult += 4

    if (maxResult < 10):
        resultDict = {}
        resultDict["score"] = "Not enough information to calculate the score"
        return json.dumps(resultDict)

    percentage = (result/maxResult) * 100

    if percentage >= 80:
        finalResult = "Good"
    elif percentage >= 60:
        finalResult = "Okay" 
    elif percentage >= 40:
        finalResult = "Mediocre"
    else:
        finalResult = "Unsustainable"

    finalDict = {}
    finalDict["data"] = dictData
    finalDict["score"] = finalResult

    return json.dumps(finalDict)

print(calculateResult("barcode.png"))