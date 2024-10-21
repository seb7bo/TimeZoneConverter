import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Time zone offsets relative to each other
time_zones = {
    "Mexico": 0,       # Mexico City is the reference
    "Romania": 9,      # Romania is 9 hours ahead of Mexico City
    "Germany": 8,      # Germany is 8 hours ahead of Mexico City
    "India": 10.5      # India is 10.5 hours ahead of Mexico City
}

def convert_time():
    try:
        # Get selected time zone and input time from entry
        selected_zone = selected_timezone.get()
        base_time_str = entry.get()
        
        # Parse the input time
        base_time = datetime.strptime(base_time_str, "%H:%M")
        
        # Get the offset of the selected timezone
        base_zone_offset = time_zones[selected_zone]
        
        # Calculate the time for each other zone
        results = {}
        for zone, offset in time_zones.items():
            if zone != selected_zone:
                # Calculate time relative to the selected time zone
                zone_offset = offset - base_zone_offset
                zone_time = base_time + timedelta(hours=zone_offset)

                # Get the hour difference between the selected time and the zone time
                hour_difference = (zone_time - base_time).total_seconds() / 3600
                
                # Determine if the time is previous, current, or next day
                if zone_time.hour < base_time.hour or (zone_time.hour == base_time.hour and zone_time.minute < base_time.minute):
                    if hour_difference < -12:  # Handles cross-day boundaries correctly (e.g., when wrapping from 23:00 to 00:00)
                        day_status = "Next Day"
                    else:
                        day_status = "Previous Day"
                elif zone_time.hour == base_time.hour and zone_time.minute == base_time.minute:
                    day_status = "Current Day"
                else:
                    if hour_difference > 12:
                        day_status = "Previous Day"
                    else:
                        day_status = "Next Day"
                    
                zone_time_str = zone_time.strftime("%H:%M")
                results[zone] = (zone_time_str, day_status)
        
        # Update labels with the converted times and day status
        update_labels(results)
        
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter time in HH:MM format")

def update_labels(results):
    label1.config(text=f"{list(results.keys())[0]} Time: {list(results.values())[0][0]}")
    label1_status.config(text=f"({list(results.values())[0][1]})", fg="blue")
    
    label2.config(text=f"{list(results.keys())[1]} Time: {list(results.values())[1][0]}")
    label2_status.config(text=f"({list(results.values())[1][1]})", fg="blue")
    
    label3.config(text=f"{list(results.keys())[2]} Time: {list(results.values())[2][0]}")
    label3_status.config(text=f"({list(results.values())[2][1]})", fg="blue")

# Create the main window
root = tk.Tk()
root.title("Time Converter")
root.geometry("400x450")

# Create dropdown menu for selecting the time zone
selected_timezone = tk.StringVar(root)
selected_timezone.set("Mexico")  # Default value

dropdown = tk.OptionMenu(root, selected_timezone, *time_zones.keys())
dropdown.pack(pady=10)

# Create input label and entry for the base time
label = tk.Label(root, text="Enter Time (24-hour format):")
label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=5)

# Button to trigger time conversion
button = tk.Button(root, text="Convert", command=convert_time)
button.pack(pady=10)

# Labels to display the converted times with day information
label1 = tk.Label(root, text="", font=("Arial", 18))
label1.pack(pady=5)

label1_status = tk.Label(root, text="", font=("Arial", 12), fg="blue")
label1_status.pack()

label2 = tk.Label(root, text="", font=("Arial", 18))
label2.pack(pady=5)

label2_status = tk.Label(root, text="", font=("Arial", 12), fg="blue")
label2_status.pack()

label3 = tk.Label(root, text="", font=("Arial", 18))
label3.pack(pady=5)

label3_status = tk.Label(root, text="", font=("Arial", 12), fg="blue")
label3_status.pack()

# Start the GUI event loop
root.mainloop()
