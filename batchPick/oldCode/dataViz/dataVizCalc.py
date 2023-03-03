timeToPick = 60
speed = 1.4  # m/s
response = {
    "batches": [
        {
            "number": 1,
            "dist": 250,  # in metres
            "noOfItem": 32
        },
        {
            "number": 2,
            "dist": 500,  # in metres
            "noOfItem": 37
        }
    ]
}


def getTotalDist(response):
    totalDist = 0
    batchesList = response["batches"]
    for batch in batchesList:
        totalDist += batch["dist"]
    return totalDist


def getTotalNoOfItems(response):
    totalNoOfItems = 0
    batchesList = response["batches"]
    for batch in batchesList:
        totalNoOfItems += batch["noOfItem"]
    return totalNoOfItems


def getTotalTimeTaken(totalNoOfItems, timeToPick, totalDist, speed):  # in hours
    return ((totalNoOfItems * timeToPick) + (totalDist / speed)) / 3600


totalDist = getTotalDist(response)
totalNoOfItems = getTotalNoOfItems(response)

totalTimeTaken = getTotalTimeTaken(
    totalNoOfItems, timeToPick, totalDist, speed)

print("totalDist", totalDist)
print("totalNoOfItems", totalNoOfItems)
print("totalTimeTaken", totalTimeTaken, "hours")
