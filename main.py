import customtkinter
from customtkinter import *
from tkinter import *
import requests
import datetime
from win10toast import ToastNotifier

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")
root.title("Launcher")

toast = ToastNotifier()

webhook_url = "YOUR-WEBHOOK-HERE"

def submit_license():
    license_key = entry2.get()
    username = entry1.get()
    # Die Daten für die eingebettete Nachricht definieren und dabei die Variable license_key verwenden
    data = {
        "embeds": [
            {
                "title": "User Authenticated",
                "description": "A User has logged in to the launcher via a license key! \n```User: {0}```".format(username) + "\n ```License: {0}```".format(license_key),
                "color": 0x00FF00
            }
        ]
    }
    # Die Anfrage an den Webhook senden
    response = requests.post(webhook_url, json=data)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 204:
        print("Used License:", license_key)
    else:
        print("Fehler beim Senden der Nachricht:", response.text)
      

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        frameChecker = customtkinter.CTkFrame(master=self)
        frameChecker.pack(pady=20, padx=60, fill="both", expand=True)

        self.labelCheck = customtkinter.CTkLabel(master=frameChecker, text="License Checker", font=("Roboto", 24))
        self.labelCheck.pack(pady=12, padx=10)

        self.licenseCheck = customtkinter.CTkEntry(master=frameChecker ,placeholder_text="License")
        self.licenseCheck.pack(padx=20, pady=20)

        self.checkLicenseButton = customtkinter.CTkButton(master=frameChecker, text="Check License", command=self.check_license)
        self.checkLicenseButton.pack(pady=12, padx=10)

    def check_license(self):
        check_license_key_input = self.licenseCheck.get()
        with open("lizenzen.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                license_data = line.strip()
                if license_data:
                    license_data = eval(license_data)  # parse license data from string to dictionary
                    if license_data["License"] == check_license_key_input:
                        expiration_date = datetime.datetime.strptime(license_data["Expiration_Date"], "%Y-%m-%d")
                        if expiration_date > datetime.datetime.now():
                            print("License gültig bis " + expiration_date.strftime("%d.%m.%Y"))
                            toast.show_toast("License Checker", "Your license is valid until" + expiration_date.strftime("%d.%m.%Y"))
                            return
                        else:
                            print("License abgelaufen")
                            toast.show_toast("License Checker", "Your license is expired. If you want to use this tool you have to buy another license")
                            return
        print("Ungültige License")
        toast.show_toast("License Chcker", "The license you have entered is not known in our database. Please check your license and try again!")

def open_license_checker():
            root.toplevel_window = ToplevelWindow(root)  # create window if its None or destroyed
            root.toplevel_window.focus()  # if window exists focus it
 


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="License", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Login", command=submit_license)
button.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="Check your License", command=open_license_checker)
button2.pack(pady=12, padx=10)
button2.configure(state="disabled", text="Check your License")

root.mainloop()