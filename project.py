from pathlib import Path
import csv
import datetime
import tabulate



def main():
    '''
    Main function to run the application.
    '''
    print()
    print("Welcome to Expense Tracker")
    while True:
        print("\n--- Main Menu ---")
        print("a: Add expense")
        print("s: Show stats")
        print("q: Quit")
        user_choice = input("Select an option: ").lower().strip()

        if user_choice == 'q':
            print("Bye, Have a good day!")
            break

        if user_choice in ['a', 's']:   
            year, month = get_valid_period()
            csv_path = get_file(year, month)

            if user_choice == 'a':
                user_input(csv_path, year, month)
                user_choice = input("s:Show stats! / q:Quit: ")
                if user_choice == 's':
                    print_summary(csv_path, month)
                else:
                    pass
            elif user_choice == 's':
                print_summary(csv_path, month)


def parse_year_month(user_input):
    '''
    Parse a "YYYY, MM" string into year and month intergers.
    '''
    try:
        if "," not in user_input:
            raise ValueError("Missing Comma")
        y_str, m_str = user_input.strip().split(",")
        year, month = int(y_str), int(m_str)

        if not(1 <= month <= 12):
            raise ValueError("Invalid Month")
        return year, month
    except ValueError:
        raise ValueError("Invalid Format")
    
def get_file(year, month):
    '''
    Create the folder and file, if it does not exist.
    return the Path object to the csv file.
    '''
    folder = Path(str(year))
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder/f"{month:02d}.csv"

    if not file_path.exists():
        with file_path.open("w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Year", "Month", "Day", "Amount", "Category"])
    return file_path

def add_entry_to_csv(file_path, year, month, day, amount, category):
    '''
    Append a new list of expense data to the csv file.
    '''
    with open(file_path, 'a', newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([year, month, day, amount, category])

def calculate_stats(file_path):
    '''
    Read csv file and calculate total expenses and the categories.
    '''
    total = 0.0
    categories = {}

    with open(file_path, 'r', newline="", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            amount_str = row.get("Amount", "").strip()
            category = row.get("Category", "").strip().title()

            if not amount_str:
                continue
            try:
                amount = float(amount_str)
                total += amount

                if category in categories:
                    categories[category] += amount
                else:
                    categories[category] = amount
            except ValueError:
                continue
    return total, categories

def user_input(file_path, year, month):
    '''
    Prompt user for expese details and save them.
    '''
    while True:
        day = input("Enter day: ")
        if not valid_date(year, month, day):
            print(f"Invalid date: {year}/{month}/{day}")
            continue

        while True:
            try:
                amount = float(input("Amount: "))
                break
            except ValueError:
                print("Enter a valid number!")

        category = input("Category: ").title()

        add_entry_to_csv(file_path, year, month, day, amount, category)

        add_more = input("Do you want to add more? y or n: ").lower()
        if add_more == 'y':
            continue
        else:
            break

#convert integer month to Jan-Dec format
def print_month(month):
    months = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    return f"{months[month]}"

def valid_date(year, month, day):
    '''
    Check uf the given year, month, and day from a valid date.
    '''
    try:
        year, month, day = int(year), int(month), int(day)
        datetime.date(year, month, day)
        return True
    except ValueError:
        return False
    
# check validity of year and month
def get_valid_period():
    while True:
        print(f"\nCurrent year, month: {datetime.datetime.now().strftime('%Y,%m')}")
        year_month = input("Enter 'year, month' (or just press Enter for current Year/month): ")

        #if user does not enter anything
        if not year_month.strip():
            today = datetime.date.today()
            return today.year, today.month
        
        try:
            year, month = parse_year_month(year_month)
            return year, month
        except ValueError:
            print()
            print("Error: Enter in 'YYYY, MM' format (e.g., 2025, 12)")

#print summary of the stats for that month
def print_summary(csv_path, month):
    total, cats = calculate_stats(csv_path)

    if total == 0:
        print(f"\nNo expenses found for {print_month(month)}.")
        return
    print("\n--- Monthly Breakdown ---")
    print(f"Monthly expsense for {print_month(month)}")
    table_data = [[c, f"{a:.2f} JPY"] for c, a in cats.items()]
    print(tabulate.tabulate(table_data, headers=["Category", "Amount"], tablefmt="grid"))                            
    print(f"\nTotal spend in {print_month(month)}: {total:.2f} JPY\n")


if __name__ == "__main__":
    main()
