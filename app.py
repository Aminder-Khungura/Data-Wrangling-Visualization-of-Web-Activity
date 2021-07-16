from tkinter import *
from main import main

# Create root widget
root = Tk()
root.title('Productivity Tracker')

# Set root widget size
root.geometry('500x200')

# Change icon of root widget
photo = PhotoImage(file=r'C:\Users\amind\PycharmProjects\Productivity_Tracker\icon.png')
root.iconphoto(False, photo)

# Create label widgets
start_label = Label(root, text='Enter Start Date:')
end_label = Label(root, text='Enter End Date:')

# Create widgets to input Start and End dates
start_input = Entry(root, width=10, borderwidth=5)
start_input.insert(0, '2021-07-01')
end_input = Entry(root, width=10, borderwidth=5)
end_input.insert(1, '2021-07-08')

# Get dates entered and store into variables
start = start_input.get()
end = end_input.get()

# Create button widget that runs main.py
run_button = Button(root, text='Run', command=lambda: main(start, end))

# Place widgets onto root
start_label.grid(row=0, column=0)
start_input.grid(row=0, column=1)
end_label.grid(row=1, column=0)
end_input.grid(row=1, column=1)
run_button.grid(row=2, column=1)

root.mainloop()