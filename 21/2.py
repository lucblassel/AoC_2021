from collections import defaultdict


ROLL_COUNTS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

def get_score(roll):
    return (roll - 1) % 10 + 1

def main():
    wins = [0,0]
    # startpos = [4,8] # test start
    startpos = [4,7] # my input
    counts = {
        # player1_pos, player2_pos, player1_score, player2_score -> count
        (startpos[0], startpos[1], 0, 0): 1,
    }

    turn = 0
    while len(counts) > 0:

        if turn > 21: # Something went wrong...
            print("Reached max turns...")
            break

        new_universes = defaultdict(int)

        for (p1_pos, p2_pos, p1_score, p2_score), count in counts.items(): # iterate through universe categories

            if turn % 2 == 0:
                pos, score, player = p1_pos, p1_score, 0
            else:
                pos, score, player = p2_pos, p2_score, 1

            for roll, times in ROLL_COUNTS.items(): # iterate through all possible rolls
                new_pos = get_score(pos + roll)
                new_score = new_pos + score

                if new_score >= 21:
                    wins[player] += count * times
                else:
                    if turn % 2 == 0:
                        new_universes[(new_pos, p2_pos, new_score, p2_score)] += count * times
                    else:
                        new_universes[(p1_pos, new_pos, p1_score, new_score)] += count * times

        counts = {k:v for k,v in new_universes.items()}
        turn += 1

    
    print(f"Player 1 won in {wins[0]} universes.")
    print(f"Player 2 won in {wins[1]} universes.")
    print(f"\nMax wins: {max(wins)}")
    
    



if __name__ == "__main__":
    main()
