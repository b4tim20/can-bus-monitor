import tkinter as tk
from tkinter import ttk, scrolledtext
import serial
import threading
import queue
from tkinter.simpledialog import askstring

# Serial configuration (adjust these dynamically in the GUI)
SERIAL_PORT = 'com5'
BAUD_RATE = 115200

# Thread-safe queue for incoming Serial data

data_queue = queue.Queue()
ser = None  # Serial connection object
ser_lock = threading.Lock()  # Lock for thread safety


def select_com_port():
    """Prompt the user to enter the COM port dynamically."""
    global SERIAL_PORT
    port = askstring("Select COM Port", "Enter COM Port (e.g., COM3):")
    if port:
        SERIAL_PORT = port
        status_bar.config(text=f"Status: Selected {SERIAL_PORT}")


def connect_serial():
    """Establish Serial connection."""
    global ser
    if SERIAL_PORT is None:
        status_bar.config(text="Status: Please select a COM port first!")
        return

    try:
        with ser_lock:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        status_bar.config(text=f"Status: Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
    except Exception as e:
        status_bar.config(text=f"Status: Connection Failed ({e})")


def read_serial():
    """Read Serial data in a background thread."""
    global ser
    try:
        while True:
            with ser_lock:
                if ser and ser.in_waiting:
                    try:
                        data = ser.readline().decode("utf-8").strip()
                        data_queue.put(data)  # Add data to queue for thread-safe handling
                    except Exception as e:
                        data_queue.put(f"Error: {e}")
                        break
    finally:
        with ser_lock:
            if ser:
                ser.close()
                ser = None


def update_output():
    """Update the GUI with Serial data from the queue."""
    while not data_queue.empty():
        data = data_queue.get()
        if "Error" in data:
            output.insert(tk.END, f"{data}\n", "error")
        else:
            output.insert(tk.END, f"{data}\n", "normal")
        output.see(tk.END)
    root.after(100, update_output)


def start_reading():
    """Start the Serial monitoring in a separate thread."""
    if SERIAL_PORT is None:
        status_bar.config(text="Status: Please select a COM port first!")
        return

    threading.Thread(target=read_serial, daemon=True).start()
    status_bar.config(text="Status: Monitoring CAN Bus")


def save_to_file():
    """Save the CAN Bus data to a log file."""
    with open("can_bus_log.txt", "w") as file:
        log = output.get("1.0", tk.END)
        file.write(log)
    status_bar.config(text="Status: Log saved to can_bus_log.txt")


def send_to_arduino():
    """Send the CAN Bus data to the Arduino to save to the SD card."""
    if ser is None:
        status_bar.config(text="Status: Not connected to serial port!")
        return

    log = output.get("1.0", tk.END).strip()
    lines = log.split("\n")
    for line in lines:
        ser.write((line + "\n").encode("utf-8"))
    status_bar.config(text="Status: Data sent to Arduino")


def convert_data():
    """Convert raw CAN Bus data to a readable format."""
    raw_data = output.get("1.0", tk.END).strip().split("\n")
    readable_data = []

    for line in raw_data:
        try:
            # Example conversion: Convert hex to ASCII
            readable_line = bytes.fromhex(line).decode('utf-8')
            readable_data.append(readable_line)
        except Exception as e:
            readable_data.append(f"Conversion Error: {e}")

    # Display the converted data in a new window
    converted_window = tk.Toplevel(root)
    converted_window.title("Converted Data")
    converted_output = scrolledtext.ScrolledText(converted_window, wrap=tk.WORD)
    converted_output.pack(fill="both", expand=True)
    converted_output.insert(tk.END, "\n".join(readable_data))


def setup_gui():
    """Setup the GUI components."""
    global root, status_bar, output

    # Create the main GUI window
    root = tk.Tk()
    root.title("CAN Bus Monitor")
    root.geometry("600x400")
    root.resizable(True, True)

    # Define frames for layout
    control_frame = tk.Frame(root)
    control_frame.pack(fill="x", padx=10, pady=5)

    output_frame = tk.Frame(root)
    output_frame.pack(fill="both", expand=True, padx=10)

    # Add widgets to the frames
    ttk.Button(control_frame, text="Select COM Port", command=select_com_port).pack(side="left")
    ttk.Button(control_frame, text="Connect", command=connect_serial).pack(side="left")
    ttk.Button(control_frame, text="Start Reading", command=start_reading).pack(side="left")
    ttk.Button(control_frame, text="Save Log", command=save_to_file).pack(side="left")
    ttk.Button(control_frame, text="Send to Arduino", command=send_to_arduino).pack(side="left")
    ttk.Button(control_frame, text="Convert Data", command=convert_data).pack(side="left")

    output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
    output.pack(fill="both", expand=True)

    status_bar = ttk.Label(root, text="Status: Ready", relief=tk.SUNKEN, anchor="w")
    status_bar.pack(side="bottom", fill="x")

    # Start the update loop
    root.after(100, update_output)

    # Start the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    setup_gui()