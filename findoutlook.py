import winreg

def get_outlook_email():
    try:
        registry_path = r"Software\Microsoft\Office\Outlook\OMI Account Manager\Accounts"
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path)

        index = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(registry_key, index)
                subkey_path = f"{registry_path}\\{subkey_name}"
                subkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey_path)

                email, _ = winreg.QueryValueEx(subkey, "SMTP Address")
                return email
            except OSError:
                break  # No more registry keys
            index += 1

    except Exception as e:
        return f"Error accessing Outlook email: {e}"

email = get_outlook_email()
if email:
    print(f"Outlook Email ID: {email}")
else:
    print("No email ID found in Outlook settings.")