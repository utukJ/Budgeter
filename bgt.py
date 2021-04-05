import os
from prettytable import PrettyTable

# Budget class for manipulating budget data


class Budget:
    def __init__(self, initial_amount=None, spent=None, name=None):
        self.name = name
        if initial_amount is None:
            # if no value supplied for initial obtain budget info from filename
            with open(base_dir + str(name) + ".txt", mode= "r") as f:
                self.initial_amount = float(f.readline())
                self.spent = float(f.readline())
                # obtain budget allocation
                self.allocs = f.readline()[:-1].split(" ")
                # create dict mapping allocation to list of expenditures
                # obtain amount planned for each allocation
                self.alloc_amounts = [float(k) for k in f.readline().split(" ")]
                # obtain amount spent for each allocation
                self.alloc_spent = [float(k) for k in f.readline().split(" ")]
                self.expenditures = f.readlines()
        else:
            self.initial_amount = initial_amount
            self.spent = spent
            # obtain categories and starting amount
            self.allocs = []
            self.alloc_amounts = []
            self.alloc_spent = []
            self.expenditures = []
            while True:
                user_input = input("Enter category and starting amount: ")
                if user_input == "":
                    break
                else:
                    alloc, amount = user_input.split()
                    self.allocs.append(alloc)
                    self.alloc_amounts.append(int(amount))
                    self.alloc_spent.append(0)
            with open(base_dir + str(name) + ".txt", mode="w") as f:
                f.writelines([str(initial_amount)+'\n', str(spent)+'\n', " ".join(self.allocs)+'\n'])
                f.write(" ".join([str(k) for k in self.alloc_amounts]) + "\n")
                f.write(" ".join([str(k) for k in self.alloc_spent]) + "\n")

        print("self.allocs: ", self.allocs)
        print("self.alloc_amounts: ", self.alloc_amounts)
        print("self.alloc_spent: ", self.alloc_spent)

    def report(self):
        """display budget info"""
        print("\n================================================================")
        print("Initial amount: ", self.initial_amount)
        print("Total spent: ", self.spent)
        print("You have {} left to spend".format(self.initial_amount - self.spent))
        # create dict of tables for each category
        print("==================================================================\n")
        tables = {}
        alloc_spents = {}
        for alloc in self.allocs:
            tables[alloc] = PrettyTable()
            tables[alloc].field_names = ['Amount spent', 'Description']
            alloc_spents[alloc] = 0
        for exp in self.expenditures:
            e_list = exp.split(" ")
            tables[e_list[0]].add_row([e_list[1], " ".join(e_list[2:])])
            alloc_spents[e_list[0]] += float(e_list[1])
        for alloc, table in tables.items():
            # fix this later
            # summary = PrettyTable()
            # summary.field_names = [''] + self.allocs
            # summary.add_row(["Initial", self.allocs[0]])
            # summary.add_row(["Spent", alloc_spents[alloc]])
            # summary.add_row(["Left",self.allocs[]])
            i = self.allocs.index(alloc)
            print(f"Details for {alloc} transactions::")
            print(f"Initial amount: {self.alloc_amounts[i]}, Spent: {self.alloc_spent[i]}, Remaining: {self.alloc_amounts[i] - self.alloc_spent[i]}")
            print(table)
            print()

    def expend(self, detail):
        """
        detail: string of the form <category> <amount> <description>
        update expenditure and budget file with info contained in string detail"""
        category, amount = detail.split(" ")[:2]
        self.spent += float(amount)
        a_indx = self.allocs.index(category) # assuming valid category is inputted by user... should modify later
        self.alloc_spent[a_indx] += float(amount)
        self.expenditures.append(detail + '\n')

    def increment(self, amount):
        """to be updated later"""
        pass

    def save_changes(self):
        """update file according to changes made"""
        with open(base_dir + str(self.name) + ".txt", mode="w") as f:
            f.writelines([str(self.initial_amount)+'\n', str(self.spent)+'\n', " ".join(self.allocs)+'\n'])
            f.write(" ".join([str(k) for k in self.alloc_amounts]) + "\n")
            f.write(" ".join([str(k) for k in self.alloc_spent]) + "\n")
            f.writelines(self.expenditures)
        self.report()




base_dir = "C:/Users/PC AI/Desktop/budgeter/"


print("Keep track of your spending here!!")
bname = input("Enter new or existing budget name: ")

if os.path.exists(base_dir + bname + ".txt"):
    bgt = Budget(name=bname)
    bgt.report()
else:
    start_amount = float(input("Enter the starting amount for {} budget: ".format(bname)))
    bgt = Budget(initial_amount=start_amount, spent=0, name=bname)

# print("Input expenditure in format, Category <space> Amount <space> Description") not yet implemented!

user_input = input("Expenditure: \n")

while user_input != "":
    bgt.expend(user_input)
    try:
        user_input = input("Expenditure: \n")
    except ValueError:
        print("Category - {} does not exist. Try again!".format(user_input))

bgt.save_changes()
print("\n{} budget updated successfully!".format(bname))

