import tkinter as tk
from tkinter import messagebox
from db import get_available_rooms, add_booking, cancel_booking, get_user_bookings

class UserDashboard:
    def __init__(self, user_id):
        self.user_id = user_id
        self.window = tk.Tk()
        self.window.title("User Dashboard")
        self.window.geometry("600x400")

        tk.Label(self.window, text="User Dashboard", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.window, text="View Available Rooms", command=self.view_available_rooms).pack(pady=10)
        tk.Button(self.window, text="Book a Room", command=self.book_room).pack(pady=10)
        tk.Button(self.window, text="View My Bookings", command=self.view_my_bookings).pack(pady=10)
        tk.Button(self.window, text="Cancel a Booking", command=self.cancel_booking).pack(pady=10)

    def view_available_rooms(self):
        rooms = get_available_rooms()
        if rooms:
            room_details = "\n".join([f"Room {room[0]}: ${room[1]}" for room in rooms])
            messagebox.showinfo("Available Rooms", room_details)
        else:
            messagebox.showinfo("Available Rooms", "No available rooms at the moment.")

    def book_room(self):
        room_number = tk.simpledialog.askstring("Book Room", "Enter the room number you want to book:")
        if room_number:
            success = add_booking(self.user_id, room_number)
            if success:
                messagebox.showinfo("Success", f"Room {room_number} has been booked successfully.")
            else:
                messagebox.showerror("Error", "Room booking failed. Please ensure the room is available.")

    def view_my_bookings(self):
        bookings = get_user_bookings(self.user_id)
        if bookings:
            booking_details = "\n".join([f"Booking ID {b[0]} - Room {b[1]} (Check-in: {b[2]}, Check-out: {b[3]})" for b in bookings])
            messagebox.showinfo("My Bookings", booking_details)
        else:
            messagebox.showinfo("My Bookings", "You have no bookings.")

    def cancel_booking(self):
        booking_id = tk.simpledialog.askinteger("Cancel Booking", "Enter the booking ID to cancel:")
        if booking_id:
            success = cancel_booking(booking_id, self.user_id)
            if success:
                messagebox.showinfo("Success", f"Booking ID {booking_id} has been canceled.")
            else:
                messagebox.showerror("Error", "Cancellation failed. Please check your booking ID.")

    def run(self):
        self.window.mainloop()

