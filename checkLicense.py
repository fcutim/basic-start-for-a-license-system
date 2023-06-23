import datetime

def check_license(license_code):
    with open("lizenzen.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            license_data = line.strip()
            if license_data:
                license_data = eval(license_data)  # parse license data from string to dictionary
                if license_data["License"] == license_code:
                    expiration_date = datetime.datetime.strptime(license_data["Expiration_Date"], "%Y-%m-%d")
                    if expiration_date > datetime.datetime.now():
                        return f"License gültig bis {expiration_date.strftime('%d.%m.%Y')}, \nLizenzinhaber: {license_data['Username']}"
                    else:
                        return "License abgelaufen"
        return "Ungültige License"

print()
print()

license_code = input("Geben Sie den Lizenzcode ein > ")

print()
print()

result = check_license(license_code)
print(result)

print()
print()
