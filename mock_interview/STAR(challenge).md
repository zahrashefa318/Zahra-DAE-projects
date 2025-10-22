## Example: Overcoming a Technical Challenge (STAR Format)

### Situation  
I was developing a **Tkinter (Python)** application for patient registration. The interface collected patient details and included a “View” button that should display all patients as a table.

### Task  
Because **Tkinter lacks a built-in table widget**, I needed a way to present structured, tabular data in the UI.

### Action  
1. I converted the patient records into a list-of-lists (or similar structure) and saved them to a file.  
2. In a loop over that list, for each element, I dynamically created Tkinter widgets (e.g. `Entry`) and placed them in the interface in rows and columns, thus simulating a table.  
3. I wrapped this logic into a **reusable class**, making it modular and usable in other projects.

### Result  
- The application successfully displayed patient data in a table-like format.  
- I now have a flexible class-based solution ready for reuse.  
- Inspired by that challenge, I am now building a **Table Maker API** to provide table-rendering capabilities across web platforms.
