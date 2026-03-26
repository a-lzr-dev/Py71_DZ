import os
from src.scripts.database import create_tables, create_data
from src.view.menu import Menu

def main():
    create_tables()
    create_data()

    menu = Menu()

    while True:
        try:
            menu.run()
            os.system('cls' if os.name == 'nt' else 'clear') # очистка экрана
        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    main()