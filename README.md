# SudokuGameProject
The game uses backtracking to both generate a board with only 1 solution as well as solve any solvable game board and check if user answers are correct

to play the game download the exe file and run it.
can also play by downloading SudokuSolverGUI.py and SudokuSolverProject.py placing both in the same folder then running SudokuSolverGUI

basic controls:
spacebar: Solves the board while showing each step to visualize the backtracking algorithm
H: gives hint by filling in the first empty square with the correct answer
right/left Mouse Click: selects square or press the button
1-9: sketch in number in the selected square as long as the number is in the range of possibilities
0: empties selected square of a sketched in number
enter: Submites sketched in num as the final answer if it's wrong it counts as a mistake
4x4 Button: generates new random puzzle board 4x4 large and resets mistake counter
9x9 Button: generates new random puzzle board 9x9 large and resets mistake counter
Solve: solves puzzle using backtracking with no pauses so appears to solve instantly
Mistakes: clicking it will hide the defeat or victory screen so you can see the puzzle

Rules
5 mistakes = Defeat
Solving the final square in the puzzle with enter = victory
If the board is solved with the solve button or spacebar then selecting any square and pressing enter will bring up the victory screen
