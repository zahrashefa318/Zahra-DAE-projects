# DAE Projects
This repository contains multiple sub-projects and folders, each addressing a different task, demo, or feature.
## Semester1
# python_1 

- **Project1** – A Python-based tool for analizing the odd and even numbers.
- ** This is my code for the Project1:**
- <pre>'''print("This is a program that evauates your  input number whether it is an odd or even!")
condition=True
num=0
try:
    while condition:
        num=int(input("Enter a valid , positive and integer number:"))
        if num > 0 :
            condition=False
            
            if num % 2 == 0:
                print("This is an even number.") 
            else :
                print("This is an odd number.")   

            more=input("Do you want to enter more numbers? y for 'yes' and n for 'no':")    
            more=more.lower()
            if more == "y":
                condition=True
            elif more =="n":
                condition=False
            else:
                print("Just enter y or n !")

except Exception :
    print("Enter a number please!")


''' </pre>

---
## Installation and Setup
### 🔹 Prerequisites
Make sure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js & npm](https://nodejs.org/)
- Git (optional)

---

### 🐍 Python Projects (prjc1)

```bash
# Navigate to the project directory
cd python_1

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
