import importlib
import sys
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    print("Devine Nombre Blockchain Game")
    print("=============================")

    while True:
        try:
            print("Select version to run:")
            print("1. Basic Game")
            print("2. Game with Stakings")
            print("3. Game with Optional Stakings")
            print("4. Game with Hashing The Secret Number")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ")
            if choice == '5':
                print("Goodbye!")
                return
            
            version = int(choice)
            if 1 <= version <= 4:
                # Import the module
                module_name = f"versions.v{version}.client"
                print(f"\nRunning Version {version}...\n")
                
                # Run the module as a script
                os.system(f"python -m {module_name}")
            else:
                print("Please enter a number between 1 and 5")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except ImportError as e:
            print(f"Error loading version: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()