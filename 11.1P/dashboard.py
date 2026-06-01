import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

# ---------------- LOGIN DETAILS ----------------
VALID_USERNAME = "carer"
VALID_PASSWORD = "1234"

# ---------------- CUSTOM TEMP THRESHOLDS ----------------
TEMP_THRESHOLDS = {
    "patient1": {"cold": 18, "hot": 30},
    "patient2": {"cold": 20, "hot": 28},
    "patient3": {"cold": 19, "hot": 29}
}

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Carer Login")
root.geometry("420x280")
root.configure(bg="#f2f2f2")

patient_widgets = {}
dashboard_window = None

def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_password_button.config(text="Hide Password")
    else:
        password_entry.config(show="*")
        show_password_button.config(text="Show Password")

def logout():
    global dashboard_window
    if dashboard_window is not None:
        dashboard_window.destroy()
        dashboard_window = None
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    password_entry.config(show="*")
    show_password_button.config(text="Show Password")
    root.deiconify()

def create_dashboard():
    global dashboard_window
    patient_widgets.clear()

    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Smart Assisted Living Dashboard")
    dashboard_window.geometry("950x820")
    dashboard_window.configure(bg="#f2f2f2")
    dashboard_window.protocol("WM_DELETE_WINDOW", logout)

    title_label = tk.Label(
        dashboard_window,
        text="SMART ASSISTED LIVING DASHBOARD",
        font=("Arial", 18, "bold"),
        bg="#f2f2f2"
    )
    title_label.pack(pady=10)

    logout_button = tk.Button(
        dashboard_window,
        text="Logout",
        font=("Arial", 11, "bold"),
        bg="#d9534f",
        fg="white",
        command=logout
    )
    logout_button.pack(pady=5)

    main_frame = tk.Frame(dashboard_window, bg="#f2f2f2")
    main_frame.pack(fill="both", expand=1)

    canvas = tk.Canvas(main_frame, bg="#f2f2f2", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=1)

    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    content_frame = tk.Frame(canvas, bg="#f2f2f2")
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def create_patient_frame(patient_id):
        frame = tk.LabelFrame(
            content_frame,
            text=patient_id.upper(),
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
            bg="white"
        )
        frame.pack(fill="x", padx=15, pady=10)

        button_label = tk.Label(frame, text="Emergency Button: No device connected", font=("Arial", 11), bg="white")
        button_label.pack(anchor="w")

        motion_label = tk.Label(frame, text="Motion: No device connected", font=("Arial", 11), bg="white")
        motion_label.pack(anchor="w")

        led_label = tk.Label(frame, text="LED: No device connected", font=("Arial", 11), bg="white")
        led_label.pack(anchor="w")

        light_label = tk.Label(frame, text="Light Status: No device connected", font=("Arial", 11), bg="white")
        light_label.pack(anchor="w")

        lux_label = tk.Label(frame, text="Light Level: No device connected", font=("Arial", 11), bg="white")
        lux_label.pack(anchor="w")

        temp_label = tk.Label(frame, text="Temperature: No device connected", font=("Arial", 11), bg="white")
        temp_label.pack(anchor="w")

        hum_label = tk.Label(frame, text="Humidity: No device connected", font=("Arial", 11), bg="white")
        hum_label.pack(anchor="w")

        threshold_label = tk.Label(
            frame,
            text=f"Thresholds: Cold < {TEMP_THRESHOLDS[patient_id]['cold']}°C | Hot > {TEMP_THRESHOLDS[patient_id]['hot']}°C",
            font=("Arial", 11),
            bg="white"
        )
        threshold_label.pack(anchor="w")

        update_label = tk.Label(frame, text="Last Update: N/A", font=("Arial", 11), bg="white")
        update_label.pack(anchor="w")

        status_label = tk.Label(frame, text="Status: Waiting for patient data...", font=("Arial", 11, "bold"), bg="white")
        status_label.pack(anchor="w", pady=5)

        patient_widgets[patient_id] = {
            "frame": frame,
            "button": button_label,
            "motion": motion_label,
            "led": led_label,
            "light": light_label,
            "lux": lux_label,
            "temp": temp_label,
            "hum": hum_label,
            "threshold": threshold_label,
            "update": update_label,
            "status": status_label
        }

    create_patient_frame("patient1")
    create_patient_frame("patient2")
    create_patient_frame("patient3")

    def set_status(patient_id, text, color):
        patient_widgets[patient_id]["status"].config(text=text, fg=color)

    def update_dashboard():
        try:
            response = requests.get("http://127.0.0.1:5000/latest", timeout=1)
            data = response.json()

            now = datetime.now()

            for patient_id, values in data.items():
                widgets = patient_widgets.get(patient_id)
                if not widgets:
                    continue

                button = values.get("button", 0)
                motion = values.get("motion", 0)
                led = values.get("led", 0)
                light_status = values.get("light_status", None)
                lux = values.get("lux", None)
                temp = values.get("temp", None)
                hum = values.get("hum", None)
                last_update = values.get("last_update", None)

                has_real_data = (
                    button != 0 or motion != 0 or led != 0 or
                    temp is not None or hum is not None or
                    lux is not None or light_status is not None or
                    last_update is not None
                )

                if not has_real_data and patient_id != "patient1":
                    widgets["button"].config(text="Emergency Button: No device connected")
                    widgets["motion"].config(text="Motion: No device connected")
                    widgets["led"].config(text="LED: No device connected")
                    widgets["light"].config(text="Light Status: No device connected")
                    widgets["lux"].config(text="Light Level: No device connected")
                    widgets["temp"].config(text="Temperature: No device connected")
                    widgets["hum"].config(text="Humidity: No device connected")
                    widgets["update"].config(text="Last Update: N/A")
                    set_status(patient_id, "Status: Waiting for patient data...", "gray")
                    continue

                widgets["button"].config(text=f"Emergency Button: {'Pressed' if button == 1 else 'Not pressed'}")
                widgets["motion"].config(text=f"Motion: {'Detected' if motion == 1 else 'No motion'}")
                widgets["led"].config(text=f"LED: {'ON' if led == 1 else 'OFF'}")
                widgets["light"].config(text=f"Light Status: {light_status if light_status is not None else 'N/A'}")
                widgets["lux"].config(text=f"Light Level: {lux} lux" if lux is not None else "Light Level: N/A")
                widgets["temp"].config(text=f"Temperature: {temp} C" if temp is not None else "Temperature: N/A")
                widgets["hum"].config(text=f"Humidity: {hum} %" if hum is not None else "Humidity: N/A")
                widgets["update"].config(text=f"Last Update: {last_update if last_update else 'N/A'}")

                if last_update:
                    try:
                        update_time = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
                        seconds_since_update = (now - update_time).total_seconds()
                        if seconds_since_update > 5:
                            set_status(patient_id, "Status: Connection lost", "darkred")
                            continue
                    except:
                        pass

                cold_limit = TEMP_THRESHOLDS[patient_id]["cold"]
                hot_limit = TEMP_THRESHOLDS[patient_id]["hot"]

                if button == 1:
                    set_status(patient_id, "Status: EMERGENCY BUTTON PRESSED", "red")
                elif temp is not None and temp < cold_limit:
                    set_status(patient_id, "Status: Too cold", "blue")
                elif temp is not None and temp > hot_limit:
                    set_status(patient_id, "Status: Too hot", "orange")
                elif motion == 1 and light_status == "dark":
                    set_status(patient_id, "Status: Motion detected in darkness", "purple")
                elif motion == 1:
                    set_status(patient_id, "Status: Motion detected", "purple")
                else:
                    set_status(patient_id, "Status: System normal", "green")

        except Exception:
            for patient_id in patient_widgets:
                set_status(patient_id, "Status: Server not reachable", "darkred")

        if dashboard_window is not None and dashboard_window.winfo_exists():
            dashboard_window.after(1000, update_dashboard)

    update_dashboard()

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        messagebox.showinfo("Login", "Login successful")
        root.withdraw()
        create_dashboard()
    else:
        messagebox.showerror("Login", "Invalid username or password")

# ---------------- LOGIN UI ----------------
title = tk.Label(root, text="Carer Login", font=("Arial", 18, "bold"), bg="#f2f2f2")
title.pack(pady=15)

username_label = tk.Label(root, text="Username", font=("Arial", 12), bg="#f2f2f2")
username_label.pack()
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack(pady=5)

password_label = tk.Label(root, text="Password", font=("Arial", 12), bg="#f2f2f2")
password_label.pack()
password_entry = tk.Entry(root, font=("Arial", 12), show="*")
password_entry.pack(pady=5)

show_password_button = tk.Button(root, text="Show Password", font=("Arial", 10), command=toggle_password)
show_password_button.pack(pady=5)

login_button = tk.Button(root, text="Login", font=("Arial", 12, "bold"), command=login)
login_button.pack(pady=15)

root.mainloop()