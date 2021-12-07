input_ = "./data.txt"


class Board:
    def __init__(self):
        self.board = None
        self.checked = None
        self.bingo = 0
        self.won = False

    @classmethod
    def from_string(cls, string):
        board = cls()
        board.board = [[int(x) for x in l.split()] for l in string.strip().split("\n")]
        board.checked = [[False] * len(board.board[0]) for _ in board.board]

        board.bingo = len(board.board)

        return board

    def traverse(self):
        for i, line in enumerate(self.board):
            for j, val in enumerate(line):
                yield i, j, val

    def __repr__(self):
        lines = [[] for _ in self.board]
        for i, j, val in self.traverse():
            if self.checked[i][j]:
                lines[i].append(f"({val})")
            else:
                lines[i].append(str(val))
        return "\n".join("\t".join(l) for l in lines)

    def process_draw(self, draw):
        for i, j, val in self.traverse():
            if draw == val:
                self.checked[i][j] = True
                return 1
        return 0

    def check_win(self):
        lineScores = [0 for _ in self.board]
        colScores = [0 for _ in self.board[0]]
        for i, j, val in self.traverse():
            lineScores[i] += self.checked[i][j]
            colScores[j] += self.checked[i][j]
        if self.bingo in lineScores or self.bingo in colScores:
            self.won = True
            return True
        return False

    def compute_score(self):
        score = 0
        for i, j, val in self.traverse():
            if not self.checked[i][j]:
                score += val
        return score


def main():
    boards = []
    with open(input_, "r") as lines:
        draws = [int(x) for x in lines.__next__().split(",")]
        curr_board = ""
        for line in lines:
            if line.strip() != "":
                curr_board += line
            else:
                if curr_board != "":
                    boards.append(Board.from_string(curr_board))
                    curr_board = ""
    boards.append(Board.from_string(curr_board))

    won = []
    last = None
    for val in draws:
        for i, b in enumerate(boards):
            if b.won:
                continue
            b.process_draw(val)
            w = b.check_win()
            if w:
                if len(won) < len(boards) - 1:
                    won.append(i)
                else:
                    last = b
                    break
            if last is not None:
                break
        if last is not None:
            break

    print(last)
    score = last.compute_score()
    print(score, score * val)


if __name__ == "__main__":
    main()
