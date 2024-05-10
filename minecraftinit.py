import os
import urllib.request
import questionary
import subprocess
import platform

def create_server_folder(server_name):
    os.makedirs(server_name)

def download_purpur_jar(version, server_name):
    version_urls = {
        "1.20": "https://api.purpurmc.org/v2/purpur/1.20/1990/download",
        "1.20.1": "https://api.purpurmc.org/v2/purpur/1.20.1/2062/download",
        "1.20.2": "https://api.purpurmc.org/v2/purpur/1.20.2/2095/download",
        "1.20.3-1.20.5": "https://api.purpurmc.org/v2/purpur/1.20.4/2176/download",
        "1.20.6": "https://api.purpurmc.org/v2/purpur/1.20.6/2193/download"
    }
    url = version_urls.get(version)
    if url:
        jar_filename = f"purpur-{version}.jar"
        urllib.request.urlretrieve(url, os.path.join(server_name, jar_filename))
        return jar_filename
    else:
        print("Invalid version specified.")
        return None

def create_start_script(jar_filename, server_name):
    system = platform.system()
    if system == "Windows":
        script_name = "start.bat"
        command = f"java -Xmx3024M -Xms3024M -jar {jar_filename}"
    else:
        script_name = "start.sh"
        command = f"#!/bin/bash\njava -Xmx3024M -Xms3024M -jar {jar_filename}"
    
    with open(os.path.join(server_name, script_name), "w") as script_file:
        script_file.write(command)

    if system != "Windows":
        os.chmod(os.path.join(server_name, script_name), 0o755)  # Set executable permissions for Unix-like systems

def run_server(server_name):
    server_path = os.path.join(os.getcwd(), server_name)
    system = platform.system()
    if system == "Windows":
        script_name = "start.bat"
    else:
        script_name = "start.sh"

    script_path = os.path.join(server_path, script_name)

    if os.path.exists(script_path):
        os.chdir(server_path)
        subprocess.run([script_path], shell=True)
    else:
        print(f"{script_name} not found. Make sure the server setup is complete.")

def main():
    server_name = input("What would you like to name your Minecraft server folder? ")
    create_server_folder(server_name)

    version = questionary.select(
        "Which Minecraft version would you like to use?",
        choices=["1.20", "1.20.1", "1.20.2", "1.20.3-1.20.5", "1.20.6"]
    ).ask()

    jar_filename = download_purpur_jar(version, server_name)

    if jar_filename:
        create_start_script(jar_filename, server_name)

        run_choice = input("Server setup completed. Do you want to run the server now? (yes/no) ").lower()
        if run_choice == "yes":
            run_server(server_name)
        else:
            print("Server setup completed. You can run the server later by executing the appropriate script in the server folder.")

if __name__ == "__main__":
    main()
