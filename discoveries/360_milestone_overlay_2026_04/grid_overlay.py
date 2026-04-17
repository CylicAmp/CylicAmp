def print_360_grid():
    grid = [
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ]
    print("360 MILESTONE OVERLAY ON 9×9 GRID\n")
    for i, row in enumerate(grid):
        line = []
        for j, num in enumerate(row):
            if (i == 2 and j == 5):
                line.append("★9")
            elif (i == 5 and j == 2):
                line.append("★9")
            elif (i == 3 and j == 3):
                line.append("◆8")
            else:
                line.append(f"{num:2}")
        print(" ".join(line))

if __name__ == "__main__":
    print_360_grid()
