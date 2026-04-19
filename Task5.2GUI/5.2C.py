from tkinter import *
from gpiozero import PWMLED, LED

living_led = PWMLED(18)
bathroom_led = LED(27)
closet_led = LED(22)

def update_living():
    if living_var.get() == 1:
        brightness = brightness_slider.get() / 100
        living_led.value = brightness
    else:
        living_led.off()

def update_bathroom():
    if bathroom_var.get() == 1:
        bathroom_led.on()
    else:
        bathroom_led.off()

def update_closet():
    if closet_var.get() == 1:
        closet_led.on()
    else:
        closet_led.off()

def update_brightness(value):
    if living_var.get() == 1:
        living_led.value = float(value) / 100

def all_off():
    living_var.set(0)
    bathroom_var.set(0)
    closet_var.set(0)
    living_led.off()
    bathroom_led.off()
    closet_led.off()
    brightness_slider.set(0)

def exit_program():
    all_off()
    win.destroy()

win = Tk()
win.title("Home Light Control")
win.geometry("750x420")
win.configure(bg="lightblue")

title = Label(
    win,
    text="Linda's Light Control Panel",
    font=("Helvetica", 18, "bold"),
    bg="lightblue"
)
title.grid(row=0, column=0, columnspan=3, pady=20)

Label(win, text="Room", font=("Helvetica", 14, "bold"), bg="lightblue").grid(row=1, column=0, padx=20, pady=10)
Label(win, text="ON", font=("Helvetica", 14, "bold"), bg="lightblue").grid(row=1, column=1, padx=20, pady=10)
Label(win, text="OFF", font=("Helvetica", 14, "bold"), bg="lightblue").grid(row=1, column=2, padx=20, pady=10)

living_var = IntVar(value=0)
bathroom_var = IntVar(value=0)
closet_var = IntVar(value=0)

Label(win, text="Living Room", font=("Helvetica", 13), bg="lightblue").grid(row=2, column=0, padx=20, pady=10)
Radiobutton(win, text="ON", variable=living_var, value=1, command=update_living, bg="lightblue", activebackground="lightblue").grid(row=2, column=1)
Radiobutton(win, text="OFF", variable=living_var, value=0, command=update_living, bg="lightblue", activebackground="lightblue").grid(row=2, column=2)

Label(win, text="Living Room Brightness", font=("Helvetica", 13, "bold"), bg="lightblue").grid(row=3, column=0, columnspan=3, pady=(20, 5))
brightness_slider = Scale(
    win,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    length=400,
    command=update_brightness,
    bg="lightblue",
    highlightthickness=0
)
brightness_slider.set(50)
brightness_slider.grid(row=4, column=0, columnspan=3, pady=10)

Label(win, text="Bathroom", font=("Helvetica", 13), bg="lightblue").grid(row=5, column=0, padx=20, pady=10)
Radiobutton(win, text="ON", variable=bathroom_var, value=1, command=update_bathroom, bg="lightblue", activebackground="lightblue").grid(row=5, column=1)
Radiobutton(win, text="OFF", variable=bathroom_var, value=0, command=update_bathroom, bg="lightblue", activebackground="lightblue").grid(row=5, column=2)

Label(win, text="Closet", font=("Helvetica", 13), bg="lightblue").grid(row=6, column=0, padx=20, pady=10)
Radiobutton(win, text="ON", variable=closet_var, value=1, command=update_closet, bg="lightblue", activebackground="lightblue").grid(row=6, column=1)
Radiobutton(win, text="OFF", variable=closet_var, value=0, command=update_closet, bg="lightblue", activebackground="lightblue").grid(row=6, column=2)

Button(win, text="ALL OFF", width=12, command=all_off, bg="orange").grid(row=7, column=0, pady=30)
Button(win, text="EXIT", width=12, command=exit_program, bg="gray", fg="white").grid(row=7, column=2, pady=30)

win.mainloop()
