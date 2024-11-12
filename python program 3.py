import tkinter as tk
from tkinter import messagebox, simpledialog
from db import add_room, update_room_price, get_available_rooms, get_booking_details

class AdminDashboard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Admin Dashboard")
        self.window.geometry("600x400")

        
        tk.Label(self.window, text="Admin Dashboard", font=("Arial", 18)).pack(pady=20)

        
        tk.Button(self.window, text="Add Room", command=self.add_room).pack(pady=10)
        tk.Button(self.window, text="Update Room Price", command=self.update_room_price).pack(pady=10)
        tk.Button(self.window, text="View Available Rooms", command=self.view_available_rooms).pack(pady=10)
        tk.Button(self.window, text="View Booking Details", command=self.view_booking_details).pack(pady=10)

    def add_room(self):
        room_number = simpledialog.askstring("Room Number", "Enter the new room number:")
        room_price = simpledialog.askstring("Room Price", "Enter the price for the new room:")
        
        if room_number and room_price:
            if add_room(room_number, float(room_price)):
                messagebox.showinfo("Success", f"Room {room_number} added successfully!")
            else:
                messagebox.showerror("Error", "Room number already exists or invalid data.")
        else:
            messagebox.showerror("Error", "Both room number and price are required.")

    def update_room_price(self):
        room_number = simpledialog.askstring("Room Number", "Enter the room number to update:")
        new_price = simpledialog.askstring("New Price", "Enter the new price for the room:")
        
        if room_number and new_price:
            update_room_price(room_number, float(new_price))
            messagebox.showinfo("Success", f"Room {room_number} price updated to ${new_price}")
        else:
            messagebox.showerror("Error", "Both room number and new price are required.")

    def view_available_rooms(self):
        rooms = get_available_rooms()
        if rooms:
            room_details = "\n".join([f"Room {room[0]}: ${room[1]}" for room in rooms])
            messagebox.showinfo("Available Rooms", room_details)
        else:
            messagebox.showinfo("Available Rooms", "No available rooms at the moment.")

    def view_booking_details(self):
        bookings = get_booking_details()
        if bookings:
            booking_details = "\n".join([f"Booking ID {b[0]} - User {b[1]} - Room {b[2]} (Check-in: {b[3]}, Check-out: {b[4]})" for b in bookings])
            messagebox.showinfo("Booking Details", booking_details)
        else:
            messagebox.showinfo("Booking Details", "No bookings available.")

    def run(self):
        self.window.mainloop()

