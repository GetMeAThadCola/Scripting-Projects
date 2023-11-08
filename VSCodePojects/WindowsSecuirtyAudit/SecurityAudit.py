import psutil
import os

# Check if Windows Update service is running
def check_windows_update():
    wuauserv = "wuauserv"
    services = psutil.win_service_iter()
    for service in services:
        if wuauserv.lower() in service.name().lower():
            if service.status() == "running":
                print("Windows Update service is running.")
                return
    print("Windows Update service is not running. Enable it for security updates.")

# Check for antivirus software
def check_antivirus():
    # You might need to replace this placeholder with a valid check for installed antivirus software
    # For instance, querying the registry or checking installed software
    # This example assumes the presence of an "Antivirus Software"
    antivirus_installed = True  # Replace this with your check
    if antivirus_installed:
        print("Antivirus software is installed.")
    else:
        print("Antivirus software is not installed. Please install it for security reasons.")

# Check for firewall status
def check_firewall():
    firewall_status = os.system('netsh advfirewall show allprofiles')  # You can refine this check based on your specific firewall settings
    if firewall_status == 0:
        print("Firewall is active.")
    else:
        print("Firewall is not active. Please configure the firewall for security purposes.")

# Check for User Account Control (UAC)
def check_uac():
    uac_enabled = os.system('REG QUERY "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA')
    if uac_enabled == 1:  # This assumes the value is 1 when UAC is enabled, adjust as per your system
        print("User Account Control (UAC) is enabled.")
    else:
        print("User Account Control (UAC) is disabled. Enable it for better security.")

# Perform the security checks
if __name__ == "__main__":
    print("Performing security checks...\n")
    check_windows_update()
    check_antivirus()
    check_firewall()
    check_uac()

    # Additional checks and recommendations can be added as required

    # Recommendations
    print("\nRecommendations:")
    print("1. Ensure all recommended software is installed.")
    print("2. Enable services that are currently stopped for security reasons.")
    print("3. Keep Windows Update enabled for regular security updates.")
    print("4. Regularly update and maintain antivirus software.")
    print("5. Enable User Account Control (UAC) for added security.")
