import sqlite3
import datetime

# اتصال به دیتابیس
conn = sqlite3.connect('google_calendar.db')
cursor = conn.cursor()

# ایجاد جدول برای رویدادها
cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    location TEXT,
                    status TEXT,
                    reminder_time TEXT,
                    attendees TEXT)''')

# تابع برای نمایش رویدادها
def view_events():
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    if events:
        for event in events:
            print(f"ID: {event[0]}, Title: {event[1]}, Start: {event[3]}, End: {event[4]}, Status: {event[6]}, Reminder: {event[7]}")
    else:
        print("No events found.")

# تابع برای افزودن رویداد
def add_event(title, description, start_time, end_time, location, status='Pending', reminder_time=None, attendees=None):
    cursor.execute('''INSERT INTO events (title, description, start_time, end_time, location, status, reminder_time, attendees)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (title, description, start_time, end_time, location, status, reminder_time, attendees))
    conn.commit()
    print("Event added successfully.")

# تابع برای حذف رویداد
def delete_event(event_id):
    cursor.execute('''DELETE FROM events WHERE id = ?''', (event_id,))
    conn.commit()
    print(f"Event with ID {event_id} deleted successfully.")

# تابع برای ویرایش وضعیت رویداد
def update_event_status(event_id, new_status):
    cursor.execute('''UPDATE events SET status = ? WHERE id = ?''', (new_status, event_id))
    conn.commit()
    print(f"Event with ID {event_id} updated to {new_status}.")

# تابع برای ارسال یادآوری
def send_reminder(event_id):
    cursor.execute("SELECT reminder_time, title FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    if event and event[0]:
        print(f"Reminder: Your event '{event[1]}' is coming up at {event[0]}")
    else:
        print(f"No reminder set for this event.")

# نمایش منو
def show_menu():
    print("\n--- Google Calendar Menu ---")
    print("1. View Events")
    print("2. Add Event")
    print("3. Delete Event")
    print("4. Update Event Status")
    print("5. Set Reminder")
    print("6. Exit")

# اجرای برنامه
def main():
    while True:
        show_menu()
        choice = input("Select an option (1-6): ")
        if choice == '1':
            view_events()
        elif choice == '2':
            title = input("Enter event title: ")
            description = input("Enter event description: ")
            start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
            end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
            location = input("Enter event location: ")
            reminder_time = input("Enter reminder time (YYYY-MM-DD HH:MM:SS) or leave blank: ")
            attendees = input("Enter attendees (comma separated): ")
            add_event(title, description, start_time, end_time, location, reminder_time=reminder_time, attendees=attendees)
        elif choice == '3':
            event_id = int(input("Enter event ID to delete: "))
            delete_event(event_id)
        elif choice == '4':
            event_id = int(input("Enter event ID to update status: "))
            new_status = input("Enter new status (Pending/Done): ")
            update_event_status(event_id, new_status)
        elif choice == '5':
            event_id = int(input("Enter event ID to set reminder: "))
            send_reminder(event_id)
        elif choice == '6':
            print("Exiting Google Calendar App.")
            break
        else:
            print("Invalid choice. Please select between 1 and 6.")

if __name__ == "__main__":
    main()

# بستن اتصال دیتابیس پس از اتمام برنامه
conn.close()
