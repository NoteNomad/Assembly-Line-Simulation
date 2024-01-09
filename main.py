import sys
import os
import tkinter
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import datetime

#Install customtkinter, pandas and import it
try:
    import pandas as pd
    import customtkinter
except ImportError or ModuleNotFoundError:
    os.system("pip install customtkinter pandas &")
    import customtkinter
    import pandas as pd
    # print("", end="")

# Install pandas and import it
# try:
#     os.system("pip install pandas")
#     import pandas as pd
# except ImportError:
#     print("", end="")

# Create the first production frame
def production_frame():
    # Hides all other frames and brings the first on to the top
    frame.tkraise()
    
    # Create the first subframe to list all available products
    product_frame = tkinter.LabelFrame(frame, text = "Produkte")
    product_frame.grid(row = 0, column= 0,rowspan=3, padx=20, pady=20,sticky="nswe")
    
    # Create an enumerated listing of all available products
    all_products_label = tkinter.Label(product_frame, text = "Folgende Produkte stehen für die Produktion zur Verfügung:")
    all_products_label.grid(row=0,column=0)

    for index, product in enumerate(total_products, start=1):
        product_label = tkinter.Label(product_frame, text=f"{index}. {product}")
        product_label.grid(row=index, column=0)
    
    # Create second subframe to realise product entries
    produce_frame = tkinter.LabelFrame(frame, text = "Produkt")
    produce_frame.grid(row=0,column=1, sticky="news",padx=20,pady=20)
    produce_label = tkinter.Label(produce_frame, text = "Produkt zum Produzieren:")
    produce_label.grid(row=0,column=0,sticky="nswe")
    product_entry = tkinter.Entry(produce_frame)
    product_entry.grid(row=1, column=0, padx=10,pady=10,sticky="nswe")
    
    # Third subframe to feed in cycle times
    cycle_frame = tkinter.LabelFrame(frame,text="Zykluszeit")
    cycle_frame.grid(row=1,column=1,padx=20,pady=20,sticky="nswe")
    cycle_label = tkinter.Label(cycle_frame, text="Zykluszeit des Produktes:")
    cycle_label.grid(row=0,column=0,sticky="nswe")
    cycle_entry = tkinter.Entry(cycle_frame)
    cycle_entry.grid(row=1, column=0, padx=10,pady=10,sticky="nswe")

    # Button to enter the data into dict
    prod_btn = customtkinter.CTkButton(frame,
                                       text = "Daten eingeben",
                                       command = lambda: entry_data(product_entry, cycle_entry),
                                       fg_color = "slategray",
                                       hover_color = "dimgray")
    prod_btn.grid(row=2, column=1, sticky="news", padx=20, pady=10)
    
    # Button to submit entered data and continue
    finish_btn = customtkinter.CTkButton(frame,
                                         text="Nächste Seite",
                                         command=lambda: next_page(produce_products),
                                         fg_color = "steelblue")
    finish_btn.grid(row=3, columnspan=2, sticky="news", padx=20, pady=20)

# Function to be called when entering data
def entry_data(product_entry, cycle_entry):
    
    # Get the entered product
    product = product_entry.get()
    
    # Get the cycle time, respectively
    try:
        cycletime = int(cycle_entry.get())
    except ValueError:  
        tkinter.messagebox.showwarning(title="Error",message="Das war keine gültige Zykluszeit. Bitte versuchen Sie es erneut")
        return

    # Make sure all entries are available
    if product and cycletime:
        
        # Allocate product entry to key and cycle time to value of dict
        if product in total_products:
            
            # Avoid double entries
            if product not in produce_products:
                produce_products[product] = product
                produce_products[product] = cycletime
            else:
                tkinter.messagebox.showwarning(title="Error",message="Das Produkt wird bereits produziert!")
        
        # Avoid inadequate entries
        else:
            tkinter.messagebox.showwarning(title="Error",message="Dieses Produkt gibt es nicht!")
    
    else:
        tkinter.messagebox.showwarning(title="Error",message="Produkt und Zykluszeit müssen eingegeben werden!")
    
    # Reset the input fields
    product_entry.delete(0, 'end')
    cycle_entry.delete(0, 'end')
    return produce_products

# Function to switch between the first and second frame (necessary to avoid no entries)
# If entries not empty, switch to second frame, otherwise repeat
def next_page(produce_products):
    if not produce_products:
        tkinter.messagebox.showwarning(title="Error",message="Sie haben keine Daten eingegeben. Bitte versuchen Sie es erneut")
        return
    switch_frames(frame, frame2)
    sequence_frame()
 
# Function to switch between frames
def switch_frames(frame_to_hide, frame_to_show):
    
    # Destroy widgets in the frame to hide
    for widget in frame_to_hide.winfo_children():
        widget.destroy()
    
    # Resizing frames to original size
    frame_to_hide.grid_forget()
    frame_to_show.grid(row=0, column = 0)
    
    # Make the frame to show appear
    frame_to_show.tkraise()

# Second frame to input lead time, the sequence to be produced, sequence repetition
def sequence_frame():
    
    # Show frame
    frame2.tkraise()
    
    # First subframe to show all produced products
    product_frame2 = tkinter.LabelFrame(frame2, text = "",borderwidth=0, highlightthickness=0)
    product_frame2.grid(row=0, column= 0,rowspan=3, padx=20, pady=20, sticky="nsew")
    
    # Creating a table overview for all products to be produced
    tree = ttk.Treeview(product_frame2, columns=("Column 1", "Column 2"), show="headings")
    tree.heading("Column 1", text="Produkt")
    tree.heading("Column 2", text="Zykluszeit [in min]")
    for i, (key, value) in enumerate(produce_products.items(), start=1):
        tree.insert("",str(i), values=(str(key),str(value)))
        tree.pack(expand=True, fill='y')
    
    # Subframe to enter lead time
    lead_frame = tkinter.LabelFrame(frame2, text="Bearbeitungszeit")
    lead_frame.grid(row=0,column=1,padx=20,pady=20,sticky="news")
    lead_label = tkinter.Label(lead_frame,text="Die jeweilige Bearbeitungszeit der Stationen:")
    lead_label.grid(row=0,column=0,sticky="news")
    lead_entry = tkinter.Entry(lead_frame)
    lead_entry.grid(row=1,column=0, padx=10,pady=10,sticky="news")

    # Subframe to enter sequence
    sequence_frame = tkinter.LabelFrame(frame2, text="Sequenz")
    sequence_frame.grid(row=1,column=1,padx=20,pady=20,sticky="news")
    sequence_label = tkinter.Label(sequence_frame,text="Die jeweilige Produktionssequenz:")
    sequence_label.grid(row=0,column=0,sticky="news")
    sequence_entry = tkinter.Entry(sequence_frame)
    sequence_entry.grid(row=1,column=0, padx=10,pady=10,sticky="news")

    # Subframe to enter amount of sequence repetition
    sequence_rep_frame = tkinter.LabelFrame(frame2, text="Sequenz Wiederholen")
    sequence_rep_frame.grid(row=2,column=1,padx=20,pady=20,sticky="news")
    sequence_rep_label = tkinter.Label(sequence_rep_frame,text="Die jeweilige Anzahl an Sequenzwiederholungen:")
    sequence_rep_label.grid(row=0,column=0,sticky="news")
    sequence_rep_entry = tkinter.Entry(sequence_rep_frame)
    sequence_rep_entry.grid(row=1,column=0, padx=10,pady=10,sticky="news")

    # Button to produce and create assembly table
    prod_btn = customtkinter.CTkButton(frame2,
                                       text="Produktion starten",
                                       command = lambda: create_table(lead_entry,sequence_entry,sequence_rep_entry),
                                       fg_color = "steelblue")
    prod_btn.grid(row=3, column=1, sticky="news", padx=20, pady=10)
    
    # Button to go back and deleting entries
    back_btn = customtkinter.CTkButton(frame2,
                                   text="Zurück",
                                   command= lambda: [switch_frames(frame2, frame),clear_dictionary(produce_products),production_frame()],
                                   fg_color="slategray")
    back_btn.grid(row=3, column=0, sticky="news", padx=20, pady=10)    

# Function to reset the dict
def clear_dictionary(my_dict):
    my_dict.clear()

# Creating the assembly table
def create_table(lead_entry,sequence_entry,sequence_rep_entry):
    
    # Get lead time value
    try:
        lead_time = int(lead_entry.get())
        
        # Lead time smaller than cycle time not allowed
        for cyc_time in produce_products.values():
            if lead_time < cyc_time:
                tkinter.messagebox.showwarning(title="Error",message="Die Bearbeitungszeit ist kleiner als eine Zykluszeit und würde in der Produktion zu Fehlern führen. Bitte versuchen Sie es erneut")
                return
    except ValueError:  
        tkinter.messagebox.showwarning(title="Error",message="Das war keine gültige Bearbeitungszeit. Bitte versuchen Sie es erneut")
        return
    
    # Get sequence 
    sequence = sequence_entry.get()
    
    # Get value of sequence repitions
    try:
        sequence_rep = int(sequence_rep_entry.get())
    except ValueError: 
        tkinter.messagebox.showwarning(title="Error",message="Das war keine gültige Anzahl an Sequenzwiederholungen. Bitte versuchen Sie es erneut")
        return
    
    # Make sure all values are entered
    if lead_time and sequence and sequence_rep:

        # Multiply sequence with the amount of repetitions
        sequence = str(sequence)*int(sequence_rep)
        
        # Intialising variables
        sequence_parts = []
        part = ""
        current_sum = 0
        idle = lead_time
        idle_time = []

        # Make sure sequence doesn't contain wrong products
        for element in sequence:
            if element not in produce_products:
                tkinter.messagebox.showwarning(title="Error", message="Die Sequenz enthält ein oder mehrere Produkte, die nicht zur Produktion ausgewählt wurde. Bitte versuchen Sie es erneut")
                return
            
            current_sum += produce_products[element]
            part += element

            if current_sum > lead_time:
                idle_time.append(idle)
                append_string = part[:-1] + " (Leerlauf: {} Minuten)".format(idle)
                idle = lead_time
                sequence_parts.append(append_string)  # Das letzte Element aus dem aktuellen Teil entfernen
                part = element  # Das aktuelle Element in den nächsten Teil übernehmen
                current_sum = produce_products[element]

            idle = idle - produce_products[element]
            
        # Add the last part if the sequence doesn't end exactly on the entered lead time
        if part:
            idle_time.append(idle)
            append_string = part + " (Leerlauf: {} Minuten)".format(idle)
            sequence_parts.append(append_string)
            
        # Number of stations
        num_columns = 8
        
        # Create empty dataframe
        columns = [f'Station {i}' for i in range(1, num_columns + 1)]
        df = pd.DataFrame(columns=columns)

        # Values of entered sequence
        values = sequence_parts

        # Schleife zum Hinzufügen von Zeilen
        # Add rows to columns
        for i, value in enumerate(values):
            row_values = [None] * num_columns

            # Create index from list and add it to row
            start_index = max(0, i - num_columns + 1)

            # Put Values into the rows, respectively
            for j in range(start_index, i + 1):
                row_values[j - start_index] = values[i - (j - start_index)]

            # Add rows to dataframe
            df.loc[len(df)] = row_values

        # Get index of the last row after first production cycle
        row_name = int(df.iloc[-1].name)
        
        # Calculate the number of runs necessary to finish producing products
        number_runs = len(sequence_parts) + 8

        # Loop for the additional sequence rows after the first repetition is done and append it to the dataframe
        for i in range(row_name,number_runs-1):
            new_df = pd.DataFrame(columns=df.columns)
            new_df = pd.concat([new_df, df.iloc[[-1]]], axis=0)
            new_df = new_df.shift(1, axis = 1)
            new_df.rename(index={i-1: i}, inplace=True)
            df = pd.concat([df,new_df],axis = 0)

        # Initialising start time of production day
        # strptime realises conversion of string to datetime object
        start_time = datetime.datetime.strptime("8:00", "%H:%M")

        # Calculate the start and end times for each period and put into list
        time_periods = [(start_time + datetime.timedelta(minutes=lead_time * i),
                        start_time + datetime.timedelta(minutes=lead_time * (i + 1) - 1))
                        for i in range(len(df))]

        # strftime formats the periods into strings again
        time_column_formatted = [f"{start.strftime('%H:%M')}Uhr - {end.strftime('%H:%M')}Uhr" for start, end in time_periods]

        # Insert the formatted time periods into dataframe
        df.insert(0, 'Zeitplan', time_column_formatted)
            
        # Calculate produced times
        produce_time = (num_columns+len(sequence_parts)-1)*lead_time

        # Create text summaries
        production_summary_txt = "Insgesamt wurden in <b>{} Minuten</b>, mit einer jeweiligen Bearbeitungszeit von <b>{} Minuten</b>, " \
                                 "die folgende Menge an Produkten produziert:".format(produce_time, lead_time)
        
        product_a_txt= "0  mal Produkt A"
        product_b_txt= "0  mal Produkt B"
        product_c_txt= "0  mal Produkt C"
        product_d_txt= "0  mal Produkt D"
        product_e_txt= "0  mal Produkt E"
        if sequence.count('A')>0 : product_a_txt = str("{} mal Produkt A".format(sequence.count('A')))
        if sequence.count('B')>0 : product_b_txt = str("{} mal Produkt B".format(sequence.count('B')))
        if sequence.count('C')>0 : product_c_txt = str("{} mal Produkt C".format(sequence.count('C')))
        if sequence.count('D')>0 : product_d_txt = str("{} mal Produkt D".format(sequence.count('D')))
        if sequence.count('E')>0 : product_e_txt = str("{} mal Produkt E".format(sequence.count('E')))
        
        # Replace all empty cell values with "-"
        df = df.replace({None: '-'})
        sequence_entry.delete(0, 'end')
        
        # Calculate cycle time
        cycle_time = daily_hours / len(sequence)
        
        # Calculate the task times of products, respectively
        task_time = sum(produce_products.values())
        idle_time_cycle = sum(idle_time)
        percent_idle_time = idle_time_cycle/(8*cycle_time)
        print(cycle_time)
        print(idle_time_cycle)
        print(percent_idle_time)
        # Calculate efficiency
        efficiency = str(round(100 - ((task_time / (num_columns * cycle_time)) * 100), 3)) + "%"

        # Display results
        display_dataframe(df,efficiency,production_summary_txt, product_a_txt, product_b_txt, 
                          product_c_txt, product_d_txt, product_e_txt)

# Function to display results in html
def display_dataframe(dataframe, val, production_summary_txt, product_a_txt=None, product_b_txt=None,
                      product_c_txt=None, product_d_txt=None, product_e_txt=None):
    
    # Abbreviate dataframe
    df = dataframe
    
    # Title
    table_title = "<h1 style='text-align: center;'> Produktionsliniensimulation </h1>"
    
    # Production amount
    a_txt = "<br /> " + str(product_a_txt) + ""
    b_txt = "<br /> " + str(product_b_txt) + ""
    c_txt = "<br /> " + str(product_c_txt) + ""
    d_txt = "<br /> " + str(product_d_txt) + ""
    e_txt = "<br /> " + str(product_e_txt) + ""
    
    
    # Leerlaufzeit
    idle_time_txt = "<br /> <br /> "
    
        
    # Bearbeitungszeit
    lead_time_txt = "<br /> <br /> "
    # Efficiency text
    efficiency_txt = "<br /> <br /> <b> Effizienz</b> der Produktion: " + val + ""
    html_string = table_title + df.to_html(index=False) + production_summary_txt + a_txt + b_txt + c_txt + d_txt + e_txt + efficiency_txt
    
    # Create temporary path to access table (private path)
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assembly_table.html'), 'w') as f:
        f.write(html_string)
   
    # Open path in default webbrowser
    filename = "file:///" + os.path.abspath(os.path.dirname(__file__)) + "/assembly_table.html"
    webbrowser.open_new_tab(filename)

# Function to quit the program
def on_closing():
    if messagebox.askokcancel("Quit", "Wollen Sie das Programm beenden?"):
        sys.exit()

# Initialising products dict
produce_products = {}

# Available products
total_products = ['A','B','C','D','E']

# Production time
daily_hours = 8*60

# Initialising tkinter frames
window = tkinter.Tk()
window.title("Assembly Production Line")
welcome_fr = tkinter.Frame(window)
welcome_fr.grid(row=0,column=0)
frame = tkinter.Frame(window)
frame.grid(row=0,column=0)
frame2 = tkinter.Frame(window)
frame2.grid(row=0,column=0)
frame.tkraise()

# Call first function
production_frame()

# Call function to close window
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
