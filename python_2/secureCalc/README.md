# Secure Web Calculator (Flask)

## Overview  
This project is a secure, web-based calculator built using Flask. It emphasizes modular, object-oriented design, making it easy to extend with new operations without rewriting the core logic.

## Features  

### Core Functionality  
- **User Authentication:** Only authorized users can access the calculator interface  
- **Action Logging:** Every calculation is recorded for auditing and review  
- **Arithmetic Operations:**  
  - Percentages  
  - Multiplication tables  
  - Sum, average  
  - Minimum / maximum  
  - Remainder  
- **Seamless UI Flow:**  
  - Operations are triggered through modal pop-ups (no page refresh)  
  - Results displayed on a separate page with “Back” navigation  
  - Prevents browser back-button reuse after logout  
- **Robust Input Handling:**  
  - Input fields accept only valid entries  
  - Exceptions handled prior to submission  

## Architecture & Extensibility  
- Built following object-oriented principles with a modular structure  
- New mathematical functions can be added by implementing just the function logic — no changes needed to routing, UI templates, or core modules  
- Clear separation of concerns ensures maintainability and scalability  

## Technologies Used  
- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Design Patterns:** OOP, session control, modularization  
- **UX/UX Enhancements:** Flash messages, modal dialogs  
- **Additional:** Input validation, exception management  

## Installation & Usage  
1. Clone the repository  
2. Install dependencies (e.g. via `pip install -r requirements.txt`)  
3. Configure and launch the Flask app  
4. Register / log in, and begin using the calculator  
5. Future enhancements: simply add a new operation function into the designated module, and wire it into the UI  

## Impact  
- Enhanced security and accountability by enforcing authenticated access and audit trails  
- Delivered fluid user experience with modal pop-ups and controlled navigation  
- Ensured ease of future expansion by isolating core logic from new operation code  
- Promoted maintainability and clarity with modular, well-documented code  

