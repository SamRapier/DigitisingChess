

def updateFEN(position, piece, FEN_code='8/8/8/8/8/8/8/8'):

    ranks = FEN_code.split('/')
    fileMap = { 'a': 0, 
                'b': 1,
                'c': 2,
                'd': 3, 
                'e': 4,
                'f': 5,
                'g': 6, 
                'h': 7}

    rankMap = { '1': 7,
                '2': 6,
                '3': 5,
                '4': 4,
                '5': 3,
                '6': 2,
                '7': 1,
                '8': 0}



    filePos = fileMap[position[0]]
    rankPos = rankMap[position[1]]

    rank = ranks[rankPos]

    fileCounter = 0
    newRank = ""
    for i in range(len(rank)):

        if rank[i].isnumeric():
            # blank squares
            if int(rank[i]) + fileCounter > (filePos):
                # replace the number with a smaller number such that we can place the piece in between the blank squares
                # piecePos = fileCounter + (filePos)

                spaceBefore = filePos - fileCounter
                remainingSpace = int(rank[i]) - spaceBefore - 1
                

                if spaceBefore == 0:
                    if piece == "_":
                        # treat empty square differently
                        newRank += str(1 + remainingSpace) + rank[i+1:]
                    else :
                        if remainingSpace == 0:
                            remainingSpace = ""
                        newRank += piece + str(remainingSpace) + rank[i+1:]
                    break
                    # fileCounter += (1 + remainingSpace)
                else:
                    if piece == "_":
                        # treat empty square differently
                        newRank += str(spaceBefore + 1 + remainingSpace) + rank[i+1:]
                    else:
                        if remainingSpace == 0:
                            remainingSpace = ""
                        newRank += str(spaceBefore) + piece + str(remainingSpace) + rank[i+1:]
                    break
                    # fileCounter += (spaceBefore + 1 + remainingSpace)
            else:
                newRank += rank[i]
                # increase fileCounter
                fileCounter += int(rank[i])
            
        # currently a piece there
        else:
            if fileCounter == filePos:
                if piece == "_":
                    # check if the values before or after are numeric, and combine them
                    if rank[i-1].isnumeric():
                        newRank[-1] = newRank[-1] + 1 + rank[i+1:]
                    else:
                        newRank += "1" + rank[i+1:]

                else:
                    newRank += piece + rank[i+1:]
                break
            else:
                newRank += rank[i]
                fileCounter += 1



    # rebuild FEN_code
    ranks[rankPos] = newRank
    newFEN = '/'.join(ranks)

    return newFEN

if __name__ == "__main__":
    print(updateFEN("d3", "_", 'r1bqkb1r/2pp1ppp/p1n2n2/1p2p3/3PP3/B6N/PPP2PPP/RNBQK2R'))