import chess as ch
import random as rd

class Engine:

    def __init__(self, board, maxDepth, color):
        self.board=board
        self.color=color
        self.maxDepth=maxDepth
    
    def getBestMove(self):
        return self.engine(None, 1)

    def evalFunct(self):
        compt = 0
        #Resume los valores del material
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001 * rd.random()
        return compt

    def mateOpportunity(self):
        if (self.board.legal_moves.count() == 0):
            if (self.board.turn == self.color):
                return -999
            else:
                return 999
        else:
            return 0

    # Función para hacer que la IA tenga un mejor desarrollo en la apertura
    def openning(self):
        if (self.board.fullmove_number < 10):
            if (self.board.turn == self.color):
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

    # Toma el cuadrado como entrada y devuelve el valor del sistema Hans Berliner correspondiente a su residencia
    def squareResPoints(self, square):
        pieceValue = 0
        if (self.board.piece_type_at(square) == ch.PAWN):
            pieceValue = 1
        elif (self.board.piece_type_at(square) == ch.ROOK):
            pieceValue = 5.1
        elif (self.board.piece_type_at(square) == ch.BISHOP):
            pieceValue = 3.33
        elif (self.board.piece_type_at(square) == ch.KNIGHT):
            pieceValue = 3.2
        elif (self.board.piece_type_at(square) == ch.QUEEN):
            pieceValue = 8.8

        if (self.board.color_at(square) != self.color):
            return -pieceValue
        else:
            return pieceValue

        
    def engine(self, candidate, depth):
        
        # Se alcanza la profundidad máxima o no hay más movimientos posibles
        if (depth == self.maxDepth or self.board.legal_moves.count() == 0):
            return self.evalFunct()
        
        else:
            # Obtiene la lista de movimientos legales para la posición actual
            moveListe = list(self.board.legal_moves)
            
            # Inicia newCandidate
            newCandidate = None
            # El valor de profundidad non indica que es el turno de la computadora
            if (depth % 2 != 0):
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            
            # Analiza el tablero para movimientos más avanzados
            for i in moveListe:

                # Realiza el movimiento i
                self.board.push(i)

                # Obtiene el valor del movimiento i analizando sus repercusiones
                value = self.engine(newCandidate, depth + 1) 

                # Algoritmo minimax básico
                # Si es el turno de la IA (maximización)
                if (value > newCandidate and depth % 2 != 0):
                    # Guarda el movimiento de la IA
                    if (depth == 1):
                        move = i
                    newCandidate = value
                # Si es el turno del jugador (minimización)
                elif (value < newCandidate and depth % 2 == 0):
                    newCandidate = value

                # Poda alfa-beta:
                # Si el movimiento anterior lo hizo la IA y el valor es menor que el candidato (maximización)
                if (candidate != None and value < candidate and depth % 2 == 0):
                    self.board.pop()
                    break
                # Si el movimiento anterior lo hizo el jugador y el valor es mayor que el candidato (minimización)
                elif (candidate != None and value > candidate and depth % 2 != 0):
                    self.board.pop()
                    break
                
                # Deshace el último movimiento
                self.board.pop()

            # Entrega resultado
            if (depth > 1):
                # Entrega el valor del movimiento en el árbol
                return newCandidate
            else:
                # Regresa el movimiento
                return move
