import mysql.connector
import tkinter as tk
from mysql.connector import Error

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='rolex_transports',
        user='root',
        password='pragi93613'
    )
    if connection.is_connected():
        print('Connected to MySQL database')

except Error as e:
    print(f'Error connecting to MySQL database: {e}')


# Define the functions for each button
def show_trucks():
    truck_list.delete(0, tk.END)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM trucks')
    for truck_data in cursor.fetchall():
        truck_list.insert(tk.END, f"{truck_data[0]}. {truck_data[1]} - {truck_data[2]} - {truck_data[3]}")

def show_drivers():
    driver_list.delete(0, tk.END)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM drivers')
    for driver_data in cursor.fetchall():
        driver_list.insert(tk.END, driver_data[1])

def enter_order():
    order_id = order_id_entry.get()
    source = source_entry.get()
    destination = destination_entry.get()
    order_type = order_type_var.get()
    if order_type == 1:
        price = 125
    elif order_type == 2:
        price = 100
    elif order_type == 3:
        price = 50
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO orders (order_id, source, destination, order_type, cost_per_km) VALUES ('{order_id}', '{source}', '{destination}', '{order_type}', '{price}')")
    connection.commit()

def calculate_cost():
    order_id = order_id_entry2.get()
    distance = int(distance_entry.get())
    cursor = connection.cursor()
    cursor.execute(f"SELECT cost_per_km FROM orders WHERE order_id = '{order_id}'")
    result = cursor.fetchone()
    if result:
        cost_per_km = int(result[0])
        total_cost = distance * cost_per_km
        cost_label.config(text=f"Total cost for the order: {total_cost}")
    else:
        cost_label.config(text="Order ID not found")

def add_truck():
    truck_id = truck_id_entry.get()
    truck_name = truck_name_entry.get()
    truck_capacity = truck_capacity_entry.get()
    truck_availability = truck_availability_var.get()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO trucks (truck_id, name, capacity, availability) VALUES ('{truck_id}', '{truck_name}', '{truck_capacity}', '{truck_availability}')")
    connection.commit()
    truck_id_entry.delete(0, tk.END)
    truck_name_entry.delete(0, tk.END)
    truck_capacity_entry.delete(0, tk.END)
    print("Truck added successfully.")
    show_trucks()

def delete_truck():
    truck_id = truck_id_entry.get()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM trucks WHERE truck_id = '{truck_id}'")
    connection.commit()
    truck_id_entry.delete(0, tk.END)
    print("Truck deleted successfully.")
    show_trucks()

def add_driver():
    driver_id = driver_id_entry.get()
    driver_name = driver_name_entry.get()
    driver_license = driver_license_entry.get()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO drivers (driver_id, name, license_number) VALUES ('{driver_id}', '{driver_name}', '{driver_license}')")
    connection.commit()
    driver_id_entry.delete(0, tk.END)
    driver_name_entry.delete(0, tk.END)
    driver_license_entry.delete(0, tk.END)
    print("Driver added successfully.")
    show_drivers()

def delete_driver():
    driver_id = driver_id_entry.get()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM drivers WHERE driver_id = '{driver_id}'")
    connection.commit()
    driver_id_entry.delete(0, tk.END)
    print("Driver deleted successfully.")
    show_drivers()

# Create the main window
root = tk.Tk()
root.title("Rolex Transports")

# Create the frames
frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, padx=10, pady=10)

frame2 = tk.Frame(root)
frame2.pack(side=tk.LEFT, padx=10, pady=10)

frame3 = tk.Frame(root)
frame3.pack(side=tk.LEFT, padx=10, pady=10)

# Create the widgets for frame1
trucks_label = tk.Label(frame1, text="Available Trucks")
trucks_label.pack()

truck_list = tk.Listbox(frame1, width=50)
truck_list.pack()

show_trucks_button = tk.Button(frame1, text="Show Available Trucks", command=show_trucks)
show_trucks_button.pack(pady=10)

add_truck_label = tk.Label(frame1, text="Add Truck Details")
add_truck_label.pack()

truck_id_label = tk.Label(frame1, text="Truck ID:")
truck_id_label.pack()

truck_id_entry = tk.Entry(frame1)
truck_id_entry.pack()

truck_name_label = tk.Label(frame1, text="Truck Name:")
truck_name_label.pack()

truck_name_entry = tk.Entry(frame1)
truck_name_entry.pack()

truck_capacity_label = tk.Label(frame1, text="Truck Capacity:")
truck_capacity_label.pack()

truck_capacity_entry = tk.Entry(frame1)
truck_capacity_entry.pack()

truck_availability_label = tk.Label(frame1, text="Truck Availability:")
truck_availability_label.pack()

truck_availability_var = tk.StringVar()
truck_availability_var.set("Available")

available_radio = tk.Radiobutton(frame1, text="Available", variable=truck_availability_var, value="Available")
available_radio.pack()

not_available_radio = tk.Radiobutton(frame1, text="Not Available", variable=truck_availability_var, value="Not available")
not_available_radio.pack()

add_truck_button = tk.Button(frame1, text="Add Truck", command=add_truck)
add_truck_button.pack(pady=10)

delete_truck_label = tk.Label(frame1, text="Delete Truck Details")
delete_truck_label.pack()

delete_truck_id_label = tk.Label(frame1, text="Truck ID:")
delete_truck_id_label.pack()

delete_truck_id_entry = tk.Entry(frame1)
delete_truck_id_entry.pack()

delete_truck_button = tk.Button(frame1, text="Delete Truck", command=delete_truck)
delete_truck_button.pack(pady=10)

# Create the widgets for frame2
drivers_label = tk.Label(frame2, text="Available Drivers")
drivers_label.pack()

driver_list = tk.Listbox(frame2, width=50)
driver_list.pack()

show_drivers_button = tk.Button(frame2, text="Show Available Drivers", command=show_drivers)
show_drivers_button.pack(pady=10)

add_driver_label = tk.Label(frame2, text="Add Driver Details")
add_driver_label.pack()

driver_id_label = tk.Label(frame2, text="Driver ID:")
driver_id_label.pack()

driver_id_entry = tk.Entry(frame2)
driver_id_entry.pack()

driver_name_label = tk.Label(frame2, text="Driver Name:")
driver_name_label.pack()

driver_name_entry = tk.Entry(frame2)
driver_name_entry.pack()

driver_license_label = tk.Label(frame2, text="Driver License Number:")
driver_license_label.pack()

driver_license_entry = tk.Entry(frame2)
driver_license_entry.pack()

add_driver_button = tk.Button(frame2, text="Add Driver", command=add_driver)
add_driver_button.pack(pady=10)

delete_driver_label = tk.Label(frame2, text="Delete Driver Details")
delete_driver_label.pack()

delete_driver_id_label = tk.Label(frame2, text="Driver ID:")
delete_driver_id_label.pack()

delete_driver_id_entry = tk.Entry(frame2)
delete_driver_id_entry.pack()

delete_driver_button = tk.Button(frame2, text="Delete Driver", command=delete_driver)
delete_driver_button.pack(pady=10)

# Create the widgets for frame3
order_label = tk.Label(frame3, text="Enter Order Details")
order_label.pack()

order_id_label = tk.Label(frame3, text="Order ID:")
order_id_label.pack()

order_id_entry = tk.Entry(frame3)
order_id_entry.pack()

source_label = tk.Label(frame3, text="Source:")
source_label.pack()

source_entry = tk.Entry(frame3)
source_entry.pack()

destination_label = tk.Label(frame3, text="Destination:")
destination_label.pack()

destination_entry = tk.Entry(frame3)
destination_entry.pack()

order_type_label = tk.Label(frame3, text="Order Type:")
order_type_label.pack()

order_type_var = tk.IntVar()
order_type_var.set(1)

superfast_radio = tk.Radiobutton(frame3, text="Superfast", variable=order_type_var, value=1)
superfast_radio.pack()

fast_radio = tk.Radiobutton(frame3, text="Fast", variable=order_type_var, value=2)
fast_radio.pack()

normal_radio = tk.Radiobutton(frame3, text="Normal", variable=order_type_var, value=3)
normal_radio.pack()

enter_order_button = tk.Button(frame3, text="Enter Order Details", command=enter_order)
enter_order_button.pack(pady=10)

calculate_label = tk.Label(frame3, text="Calculate Order Cost")
calculate_label.pack()

order_id_label2 = tk.Label(frame3, text="Order ID:")
order_id_label2.pack()

order_id_entry2 = tk.Entry(frame3)
order_id_entry2.pack()

distance_label = tk.Label(frame3, text="Distance (km):")
distance_label.pack()

distance_entry = tk.Entry(frame3)
distance_entry.pack()

calculate_button = tk.Button(frame3, text="Calculate Cost", command=calculate_cost)
calculate_button.pack(pady=10)

cost_label = tk.Label(frame3, text="")
cost_label.pack()

# Start the main loop
root.mainloop()
