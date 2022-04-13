# take fen code, look through chessPieces folder and put the image into a folder based on the piece from the FEN code

def label_input_image(FEN_code, imageFolder):
    # example FEN
    # A FEN "record" defines a particular game position, all in one text line and using only the ASCII character set. A text file with only FEN data records should have the file extension ".fen".[4]

    # A FEN record contains six fields. The separator between fields is a space. The fields are:[5]

    # Piece placement (from White's perspective). Each rank is described, starting with rank 8 and ending with rank 1; within each rank, the contents of each square are described from file "a" through file "h". Following the Standard Algebraic Notation (SAN), each piece is identified by a single letter taken from the standard English names (pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q" and king = "K"). White pieces are designated using upper-case letters ("PNBRQK") while black pieces use lowercase ("pnbrqk"). Empty squares are noted using digits 1 through 8 (the number of empty squares), and "/" separates ranks.
    # Active color. "w" means White moves next, "b" means Black moves next.
    # Castling availability. If neither side can castle, this is "-". Otherwise, this has one or more letters: "K" (White can castle kingside), "Q" (White can castle queenside), "k" (Black can castle kingside), and/or "q" (Black can castle queenside). A move that temporarily prevents castling does not negate this notation.
    # En passant target square in algebraic notation. If there's no en passant target square, this is "-". If a pawn has just made a two-square move, this is the position "behind" the pawn. This is recorded regardless of whether there is a pawn in position to make an en passant capture.[6]
    # Halfmove clock: The number of halfmoves since the last capture or pawn advance, used for the fifty-move rule.[7]
    # Fullmove number: The number of the full move. It starts at 1, and is incremented after Black's move.

    # FEN for starting position
    # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

    # we shall limit the FEN input to only include piece position - no information about who's turn, castling rights, En Passant shall be included

    # loop through string until '/' is found
    # this separates each rank
    ranks = FEN_code.split('/')
    
    # go through each letter in the rank, this is the piece folder they belong to
    # if number is found, this indicates an empty square, so the value of the number indicates how many empty squares are in a row
    # lowercase letters are black pieces
    rankCounter = 7
    fileCounter = 0
    folderName = ""
    currSquare = ""

    root_dataset_folder = ""

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = [1, 2, 3, 4, 5, 6, 7, 8]
    pieceList = "RNBQKP"

    for rank in ranks:
        for i in range(len(rank)):
            currSquare = str(files[fileCounter]) + str(ranks[rankCounter])
            # check if value is numeric
            if rank[i].isnumeric():
                # put images into '_' folder
                fileCounter += rank[i]
                folderName = '_'
                # copy image from imageFolder to "root_dataset_folder + folderName"

            # check if value belongs to pieceList
            elif rank[i].toupper() in pieceList:

                # is it a black piece?
                if rank[i].islower():
                    # put image into 'b'
                    folderName = 'b' + rank[i]
                    # copy image from imageFolder to "root_dataset_folder + folderName"
                    
                else:
                    # put image into 'w'
                    folderName = 'w' + rank[i]
                    # copy image from imageFolder to "root_dataset_folder + folderName"

            else:
                print("invalid FEN code")

        fileCounter = 0
        rankCounter -= 1

# def copyImage(location1, location2):
