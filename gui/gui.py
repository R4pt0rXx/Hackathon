import tkinter as tk

window = tk.TK()
test = tk.Label(text= "Placeholder Name")
test.pack()
window.mainloop()

datalabel = tk.label(text = "Data:")

devicelabel = tk.label(text = "Device Name:")
deviceentry = tk.entry()
device = deviceentry.get()

samplelabel = tk.label(text = "Samplesize:")
sampleentry = tk.entry()

blocklabel = tk.label(text = "Blocksize:")
blockentry = tk.entry()

steplabel = tk.label(text = "Stepsize:")
stepentry = tk.entry()

durationlabel = tk.label(text = "Duration:")
durationentry = tk.entry()

generatebtn = tk.Button(
    text = "Start Recording"
)

output = tk.label(text = input())