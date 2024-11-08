from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
engine = create_engine('sqlite:///expenses.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Expense model
class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Expense(name='{self.name}', category='{self.category}', amount={self.amount})>"

# Create the database
Base.metadata.create_all(engine)

def add_expense(name, category, amount):
    expense = Expense(name=name, category=category, amount=amount)
    session.add(expense)
    session.commit()
    print(f"Added expense: {expense}")

def view_expenses():
    expenses = session.query(Expense).all()
    if not expenses:
        print("No expenses recorded.")
    for expense in expenses:
        print(expense)

def delete_expense(expense_id):
    expense = session.query(Expense).get(expense_id)
    if expense:
        session.delete(expense)
        session.commit()
        print(f"Deleted expense: {expense}")
    else:
        print(f"No expense found with ID {expense_id}")

def summarize_expenses():
    total = session.query(Expense).with_entities(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).all()
    if not total:
        print("No expenses to summarize.")
    for category, amount in total:
        print(f"{category}: ${amount:.2f}")

def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Summarize Expenses")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter expense name: ")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            add_expense(name, category, amount)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id)
        elif choice == '4':
            summarize_expenses()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()