from random import randint
import tkinter as tk

class Grid: 
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k
        self.table = self.generate_table(m, n, k)
        self.cell_labels = []
        self.game_won = False
        self.game_over = False
        self.game_over_label = None
        self.score = 0

    def generate_table(self, m, n, k):
        table = []
        for x in range(m):
            cols = []
            for y in range(n):
                cols.append(randint(1, k - 1))
            table.append(cols)

        return table

    def print_table(self):
        table = self.table
        
        for rows in table:
            print(rows)
   
    def check_coordinates_are_valid(self, x, y, m, n):
        return 0 <= x < m and 0 <= y < n
    
    def find_matching_adjacents(self, x, y):
        visited = set()
        stack = [(x, y)]
        match_adjacent = {}

        while stack:
            x, y = stack.pop()
            visited.add((x, y))
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    if not(a == b == 0) and not(a == b == -1) and not(a == -1 and b == 1) and not(a == 1 and b == -1) and not (a == b == 1) and self.check_coordinates_are_valid(x + a, y + b, m, n): # top, left, right, bottom                              
                        adjacent_x, adjacent_y = x + a, y + b
                        if (adjacent_x, adjacent_y) not in visited and self.table[x][y] == self.table[adjacent_x][adjacent_y]:
                            stack.append((adjacent_x, adjacent_y))
                            match_adjacent[(adjacent_x, adjacent_y)] = self.table[adjacent_x][adjacent_y]   
  
        return match_adjacent
    
    def replace_adjacent_with_blank(self, x, y):
        replaced_match_coordinates = self.find_matching_adjacents(x, y)

        for key in replaced_match_coordinates:
            x0, y0 = key[0], key[1]

            if len(replaced_match_coordinates) >= 2: # must pick coordinates with more than 2 adjacents
                self.table[x0][y0] = 0
                self.table[x][y] = 0

            else:
                print("Matching adjacents must be greater than 1.")

        if len(replaced_match_coordinates) >= 2:
            self.score += (len(replaced_match_coordinates) - 2)**2
            print(self.score)

        else: print("Matching adjacents must be greater than 1.")

        return replaced_match_coordinates
        
    def falling_characters(self, x, y):
        self.replace_adjacent_with_blank(x, y)
        coordinates_list = []
        sorted_coordinates_list = []

        for i in range(0, n):
            for j in range(0, m):
                if self.table[j][i] != 0: # if every row in that column is NOT "0" or blank
                    coordinates_list.append(self.table[j][i]) # append those

            for _ in range(0, (m - len(coordinates_list))): # append zero deficiency depending on the difference of m and length of coordinates list
                coordinates_list.insert(0, 0)

            for coordinate in coordinates_list:
                sorted_coordinates_list.append(coordinate)

            coordinates_list.clear()

        return sorted_coordinates_list

    def sort_column(self, cols):
        return sum(cols) == 0

    def table_updater(self, x, y):
        sorted_coordinates_list = self.falling_characters(x, y) 
        
        # columns
        column = []
        for i in range(0, len(sorted_coordinates_list), m):
            subcol = sorted_coordinates_list[i:i + m]
            column.append(subcol) 

        # sorted columns
        sorted_column = sorted(column, key=self.sort_column) # values in "key" that return False (nonzero lists) comes first before values that return True (zero lists)
        converted_sorted_column = []
        for subcol in sorted_column:
            for merged_subcol in subcol:
                converted_sorted_column.append(merged_subcol) # flatten out the lists of list into just 1 list

        # rows
        rows = [[] for _ in range(m)]
        for index, col in enumerate(converted_sorted_column): # https://stackoverflow.com/questions/26945277/how-to-split-python-list-every-nth-element
            rows[index % m].append(col)
         
        # actual table updater
        for i in range(m):
           self.table[i] = rows[i]

        self.game_over_and_win_notification(x, y, converted_sorted_column)

    def game_over_and_win_notification(self, x, y, converted_sorted_column):
        tracker = []
        no_more = 0
        zero = 0

        # check every cell if they still have adjacents
        for i in range(0, m):
            for j in range(0, n):
                if len(self.find_matching_adjacents(i, j)) > 1 and self.table[i][j] != 0:
                    tracker.append((key[0], key[1]) for key in self.find_matching_adjacents(i, j))
                                  
                    if len(tracker) > 1:
                        tracker.clear()
            
                else:
                    no_more += 1

        for i in range(0, len(converted_sorted_column)):
            if converted_sorted_column[i] == 0: 
                zero += 1

        if no_more == m * n: # win or game over system
            if zero == m * n:
                self.game_over_label.config(text=f"You won! Congratulations! Your score is {self.score}.", font=("Helvetica", 20))
                self.game_won = True
            else: 
                self.game_over_label.config(text=f"Game Over! Try again next time! Your score is {self.score}.", font=("Helvetica", 20))
                self.game_over = True
        
    def cell_click(self, x, y): # gui
        self.print_table()
        value = self.table[x][y]
        print(f"Clicked on cell at row {x}, column {y}, value: {value}")

        if self.check_coordinates_are_valid(x, y, m, n):
            if self.table[x][y] != 0:
                print(f"({x}, {y}): {self.table[x][y]}")

                self.table_updater(x, y)
                self.update_gui()
                self.update_score(self.score_label)

            else:
                print("That is blank. Pick another coordinate.")
        else:
            print("Coordinates are invalid.")

    def update_gui(self): # gui
        for i in range(self.m):
            for j in range(self.n):
                self.cell_labels[i][j].config(text=str(self.table[i][j]))

    def update_score(self, score_label):
        score_label.config(text=f"Current Score: {self.score}")

    def main(self):
        self.running = True  # flag to control the game loop

        def stop_game():
            self.running = False
            root.destroy()  # close the main window

        def try_again():
            # reset the game to its initial state
            self.table = self.generate_table(self.m, self.n, self.k)
            self.update_gui()
            if self.game_over_label:
                self.game_over_label.config(text="")  # clear the game-over message
            self.game_won = False
            self.game_over = False
            self.score = 0
            self.update_score(self.score_label)
            

        # create the main window
        root = tk.Tk()
        root.title("Matching Number Game")
        root.geometry("700x700")

        # frame for stop and try again buttons
        button_frame = tk.Frame(root)
        button_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # stop button
        stop_button = tk.Button(button_frame, text="Stop", command=stop_game)
        stop_button.grid(row=0, column=0)

        # try again button
        try_again_button = tk.Button(button_frame, text="Try Again", command=try_again)
        try_again_button.grid(row=0, column=1)

        # score
        self.score_label = tk.Label(root, text=f"Current Score: {self.score}", font=("Helvetica", 15))
        self.score_label.grid(row=0, column=0, padx=20, pady=20, sticky="ne")

        # create a frame to hold the table and center it
        table_frame = tk.Frame(root)
        table_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        max_font_size = 20  # maximum font size (you can adjust this value)
        cell_width = int(700 / self.n)  # calculate cell width
        cell_height = int(700 / self.m)  # calculate cell height

        for i in range(self.m):
            row_labels = []  # list to store labels in each row
            for j in range(self.n):
                cell_value = self.table[i][j]
                cell_label = tk.Label(table_frame, text=str(cell_value), borderwidth=1, relief="solid", width=cell_width, height=cell_height)
                
                # Calculate font size based on cell dimensions and maximum font size
                font_size = min(max_font_size, int(min(cell_height / 2, cell_width / 5)))
                font = ("Helvetica", font_size)
                cell_label.config(font=font)

                cell_label.grid(row=i, column=j)
                cell_label.bind("<Button-1>", lambda event, x=i, y=j: self.cell_click(x, y))
                row_labels.append(cell_label)
            self.cell_labels.append(row_labels)

        if not self.game_over_label:
            self.game_over_label = tk.Label(root, text="", padx=20, pady=10)
            self.game_over_label.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # make the table frame expand to fill the window
        root.grid_rowconfigure(1, weight=1)  # allow the table frame to expand vertically
        root.grid_columnconfigure(0, weight=1)  # allow the table frame to expand horizontally

        # Configure the rows and columns of table_frame
        for i in range(self.m):
            table_frame.grid_rowconfigure(i, weight=1)
        for j in range(self.n):
            table_frame.grid_columnconfigure(j, weight=1)

        root.mainloop()

# input section
m, n, k = list(map(int, input("Enter your table size: ").split()))
table = Grid(m, n, k) 
table.main()