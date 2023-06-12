import subprocess
import sys
import os

def check_dependencies():
    print("Checking Docker and Docker Compose...")
    try:
        subprocess.check_output(["docker", "--version"])
        subprocess.check_output(["docker-compose", "--version"])
    except subprocess.CalledProcessError:
        print("Docker and/or Docker Compose not found. Installing...")
        install_docker()
        install_docker_compose()

def install_docker():
    subprocess.call(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"])
    subprocess.call(["sudo", "sh", "get-docker.sh"])
    os.remove("get-docker.sh")

def install_docker_compose():
    subprocess.call(["sudo", "curl", "-L", "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)", "-o", "/usr/local/bin/docker-compose"])
    subprocess.call(["sudo", "chmod", "+x", "/usr/local/bin/docker-compose"])

def create_wordpress_site(site_name):
    print("Creating WordPress site...")
    subprocess.call(["docker-compose", "-f", "docker-compose.yml", "up", "-d"])
    add_etc_hosts_entry(site_name)

def add_etc_hosts_entry(site_name):
    with open("/etc/hosts", "a") as hosts_file:
        hosts_file.write(f"127.0.0.1 {site_name}\n")

def open_browser(site_name):
    print(f"Open {site_name} in your browser to access the site.")

def enable_site():
    subprocess.call(["docker-compose", "-f", "docker-compose.yml", "start"])

def disable_site():
    subprocess.call(["docker-compose", "-f", "docker-compose.yml", "stop"])

def delete_site():
    subprocess.call(["docker-compose", "-f", "docker-compose.yml", "down"])
    site_name = sys.argv[2] if len(sys.argv) > 2 else ""
    if site_name:
        with open("/etc/hosts", "r") as hosts_file:
            lines = hosts_file.readlines()
        with open("/etc/hosts", "w") as hosts_file:
            for line in lines:
                if site_name not in line:
                    hosts_file.write(line)

def main():
    if len(sys.argv) < 2:
        print("Please provide a command.")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Please provide a site name.")
            sys.exit(1)
        site_name = sys.argv[2]
        check_dependencies()
        create_wordpress_site(site_name)
        open_browser(site_name)
    elif command == "enable":
        enable_site()
    elif command == "disable":
        disable_site()
    elif command == "delete":
        delete_site()
    else:
        print("Invalid command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
