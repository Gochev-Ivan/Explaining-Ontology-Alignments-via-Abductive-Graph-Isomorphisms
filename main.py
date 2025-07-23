from Explanations import generate_explanations
from BioML import generate_subsumption_matches
from TheoreticalExample import theoretical_example
from experiments import experiments


def help_input():
    print("-" * 60)
    print(f"1) Obtain subsumption mappings from Bio-ML alignment tool.")
    print(f"2) Generate explanations for a set of correspondences.")
    print(f"3) Perform experimental evaluation.")
    print(f"4) Run theoretical example.")
    print(f"5) Help.")
    print(f"6) Exit.")
    print("-" * 60)


if __name__ == '__main__':
    while True:
        help_input()
        user_input = input("Input: ")
        if user_input == "1":
            generate_subsumption_matches()
        elif user_input == "2":
            generate_explanations()
        elif user_input == "3":
            experiments()
        elif user_input == "4":
            theoretical_example()
        elif user_input == "5":
            help_input()
        elif user_input == "6":
            break
        else:
            print("Wrong input.")

