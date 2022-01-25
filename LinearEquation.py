# بسم الله الرحمن الرحيم
from fractions import Fraction as Fr
from decimal import Decimal as D


class LinearEquation:
    def __init__(self, matrix=[], no_rows=0, no_colns=0):
        self._matrix = matrix
        self._no_rows = no_rows
        self._no_colns = no_colns
        self._infin_sol = False
        self.__sub_script = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    # Method For Formatting The Matrix Printing
    def print_matrix(self):
        for row in range(self._no_rows):
            print('[', end="")
            for coln in range(self._no_colns):
                if self._matrix[row][coln] == -0.0:
                    self._matrix[row][coln] = D(0.0)
                print(f"{Fr(self._matrix[row][coln]).limit_denominator(25000)}".center(
                    5, " "), end="")
                if coln < self._no_colns-2:
                    print(", ", end="")
                if coln == self._no_colns-2:
                    print(" | ", end="")
            print(']')
        print()

    # Method For Setting Up The Matrix Elements, It Can Get The Matrix As An Argument Or Get The Input From User
    def set_matrix(self, matrix=None, no_rows=0, no_colns=0):
        if matrix:
            self._matrix = matrix
            self._no_rows = no_rows
            self._no_colns = no_colns
        else:
            self._no_rows = int(input("Number Of Rows: "))
            self._no_colns = int(input("Number Of Columns: "))
            if self._no_colns > self._no_rows+1:
                self._matrix = [[0 for num in range(self._no_colns)]
                                for num in range(self._no_colns-1)]
            else:
                self._matrix = [[0 for num in range(self._no_colns)]
                                for num in range(self._no_rows)]
            for row in range(self._no_rows):
                for coln in range(self._no_colns):
                    self._matrix[row][coln] = D(
                        input(f"Enter The Element [{row+1}][{coln+1}]: "))
            print('='*50)
            # // Checking The Inputs //
            self.__check_inputs()

    # Method For Verification and Modification Of Current Matrix Elements
    def __check_inputs(self, flag=1):
        if flag == 1:
            print("Your Current Matrix Looks Like:")
            self.print_matrix()
        op = int(input("Type '1' For Editing, '2' For Elimination: "))
        if op == 1:
            row = int(input("Row Number: "))
            coln = int(input("Column Number: "))
            self._matrix[row-1][coln-1] = D(input("New Value: "))
            print('='*50)
            self.__check_inputs()
        elif op != 2:
            self.__check_inputs(2)

    # Method For Start The Elimination And Getting The Results
    def solve(self):
        choice = int(input(
            "For 'Gaussian Elimination' type '1', For 'Gauss-Jordan Elimination' type '2' : "))
        if choice == 1:
            print('='*50)
            self.eliminate()
            self.back_substitute()
            self.get_result()
            self.__exit_check()
        elif choice == 2:
            print('='*50)
            self.eliminate()
            self.gauss_jordan()
            self.get_result()
            self.__exit_check()
        else:
            print("Wrong Entry, Please Try Again")
            self.solve()

    # Method For Checking Whether To Solve Another Equation or Exit
    def __exit_check(self):
        op = int(input("Type '1' For Solving Another Equation, '2' For Exit : "))
        if op == 1:
            self._infin_sol = False
            self.set_matrix()
            self.solve()
        else:
            exit()

    # Method For Eliminating The Matrix To 'Row-Echelon' Form
    def eliminate(self):
        coln = 0
        is_lead = False
        for row in range(len(self._matrix)):
            # [1] Locate The First Leftmost Column That Does Not Consist Entirely Of Zeros.
            while(coln < self._no_colns-1):
                for i in range(row, len(self._matrix)):
                    if self._matrix[i][coln] != 0:
                        is_lead = True
                        break
                if is_lead:
                    break
                coln += 1

            if coln == self._no_colns-1:
                coln -= 1

            # // Check If No More non-zero Columns Found //
            if not is_lead:
                if self._matrix[row][self._no_colns-1] == 0 and row == coln and coln != self._no_colns-1:
                    infin_sol = True
                elif self._matrix[row][self._no_colns-1] != 0:
                    print(
                        f"0 ≠ {Fr(self._matrix[row][self._no_colns-1]).limit_denominator(25000)}\nThe System Has No Solution\n")
                    self.__exit_check()
                continue

            # [2] Interchange The First Row With Another Row, if necessary. To Bring nonzero Entry To The Top Of The Column
            if self._matrix[row][coln] == 0:
                for j in range(row+1, len(self._matrix)):
                    if self._matrix[j][coln] != 0:
                        print(
                            f"Current Operation : R{row+1} <-> R{j+1}\nResult:")
                        self._matrix[j], self._matrix[row] = self._matrix[row], self._matrix[j]
                        self.print_matrix()
                        break

            # [3] Make The Top Entry Of The Column Equal To 1
            if self._matrix[row][coln] != 1:
                temp = self._matrix[row][coln]
                print(
                    f"Current Operation : ({Fr(1/temp).limit_denominator(25000)})R{row+1} -> R{row+1}\nResult:")
                for col in range(len(self._matrix[row])):
                    self._matrix[row][col] = (self._matrix[row][col])/(temp)
                self.print_matrix()

            # [4] Make All Enetries Below The leading To 0
            for i in range(row+1, len(self._matrix)):
                if self._matrix[i][coln] != 0:
                    temp = (self._matrix[i][coln]) / (self._matrix[row][coln])
                    print(
                        f"Current Operation : ({-Fr(temp).limit_denominator(25000)})R{row+1}+R{i+1} -> R{i+1}\nResult:")
                    for j in range(self._no_colns):
                        self._matrix[i][j] -= temp * self._matrix[row][j]
                    self.print_matrix()
            coln += 1
            is_lead = False

    # Method for Applying 'Gauss-Jordan' Step
    def gauss_jordan(self):
        print('='*50)
        print("Gauss-Jordan Step:")
        for i in range(self._no_rows-2, -1, -1):
            for k in range(i+1, self._no_rows):
                if self._matrix[k][k] != 0 and self._matrix[i][k] != 0:
                    temp = self._matrix[i][k]/self._matrix[k][k]
                    print(
                        f"Current Operation : ({-Fr(temp).limit_denominator(25000)})R{k+1}+R{i+1} -> R{i+1}\nResult:")
                    for j in range(self._no_colns):
                        self._matrix[i][j] -= temp*self._matrix[k][j]
                    self.print_matrix()

    # Method for Applying Back-Substitute On The Matrix
    def back_substitute(self):
        print('='*50)
        print("Back Substitute:")
        print("Equations From The Augmented Matrix:")
        for row in range(self._no_colns-1):
            # Check if The Current Variable is Free Variable
            if self._matrix[row][row] == 0 and self._matrix[row][self._no_colns-1] == 0:
                continue
            ans = f"x{row+1} = ".translate(self.__sub_script)

            # Check If There is a Free Variables Relation
            is_rel = False
            for coln in range(row+1, self._no_colns-1):
                if self._matrix[row][coln] != 0:
                    is_rel = True

            # Check Whether To Print The '0' Or Not
            if is_rel:
                if(self._matrix[row][self._no_colns-1] != 0):
                    ans += f"{Fr(self._matrix[row][self._no_colns-1]).limit_denominator(25000)}"
            else:
                ans += f"{Fr(self._matrix[row][self._no_colns-1]).limit_denominator(25000)}"

            # Getting The Free Variables Relation
            for coln in range(row+1, self._no_colns-1):
                if(self._matrix[row][coln] != 0):
                    if ans[-1] != " ":
                        ans += (" + " if -
                                self._matrix[row][coln] > 0 else " - ")
                        ans += (f"{Fr(abs(self._matrix[row][coln])).limit_denominator(25000)}" if abs(self._matrix[row][coln]) != 1 else "") + \
                            f"x{coln+1}".translate(self.__sub_script)
                    else:
                        ans += (f"{Fr(-self._matrix[row][coln]).limit_denominator(25000)}" if abs(self._matrix[row][coln]) != 1 else "") + \
                            f"x{coln+1}".translate(self.__sub_script)
            print(ans)
        print('-'*50)
        # Printing Result After Each Susbtitution
        for i in range(len(self._matrix)-2, -1, -1):
            ans = f"x{i+1} = ".translate(
                self.__sub_script)+f"{Fr(self._matrix[i][self._no_colns-1]).limit_denominator(25000)} "
            for j in range(i+1, self._no_colns-1):
                temp = self._matrix[j][self._no_colns-1]
                ans += (" + " if -self._matrix[i][j] > 0 else " - ")
                ans += (f"{Fr(abs(self._matrix[i][j])).limit_denominator(25000)}" if abs(
                    self._matrix[i][j]) != 1 else "") + (f"({Fr(temp).limit_denominator(25000)})")
                self._matrix[i][self._no_colns-1] -= temp*self._matrix[i][j]
                self._matrix[i][j] = 0
            ans += f" = {Fr(self._matrix[i][self._no_colns-1]).limit_denominator(25000)}"
            print(ans)

    # Method for Exctracting And Printing The 'Solution Set'
    def get_result(self):
        print('='*50)
        print("Answer:")
        if self._infin_sol:
            print("Infinte Number Of Solutions")

        print("\nSolution Set:")
        for row in range(self._no_colns-1):
            # Check if The Current Variable is Free Variable
            if self._matrix[row][row] == 0 and self._matrix[row][self._no_colns-1] == 0:
                print(f"x{row+1} = Free Variable".translate(self.__sub_script))
                continue
            ans = f"x{row+1} = ".translate(self.__sub_script)

            # Check If There is a Free Variables Relation
            is_rel = False
            for coln in range(row+1, self._no_colns-1):
                if self._matrix[row][coln] != 0:
                    is_rel = True

            # Check Whether To Print The '0' Or Not
            if is_rel:
                if(self._matrix[row][self._no_colns-1] != 0):
                    ans += f"{Fr(self._matrix[row][self._no_colns-1]).limit_denominator(25000)}"
            else:
                ans += f"{Fr(self._matrix[row][self._no_colns-1]).limit_denominator(25000)}"

            # Getting The Free Variables Relation
            for coln in range(row+1, self._no_colns-1):
                if(self._matrix[row][coln] != 0):
                    if ans[-1] != " ":
                        ans += (" + " if -
                                self._matrix[row][coln] > 0 else " - ")
                        ans += (f"{Fr(abs(self._matrix[row][coln])).limit_denominator(25000)}" if abs(self._matrix[row][coln]) != 1 else "") + \
                            f"x{coln+1}".translate(self.__sub_script)
                    else:
                        ans += (f"{Fr(-self._matrix[row][coln]).limit_denominator(25000)}" if abs(self._matrix[row][coln]) != 1 else "") + \
                            f"x{coln+1}".translate(self.__sub_script)
            print(ans)
        print()


print("==== Linear Equation Elimination ====".center(50, '='))
print("==== Made By: Ahmed Mohsen (PrinceEGY) ====".center(50, '='))
le = LinearEquation()
le.set_matrix()
le.solve()
