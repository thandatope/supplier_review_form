from subprocess import call

import pkg_resources


def update_packages():
    packages = [dist.project_name for dist in pkg_resources.working_set]
    call("pip install --upgrade " + ' '.join(packages), shell=True)


def update_reqs():
    call("pipreqs --use-local --mode compat --force --ignore _TESTING", shell=True)


if __name__ == "__main__":
    print("1 - Update installed packages")
    print("2 - Update requirements.txt")
    c = input("Choice: ")
    if c == "1":
        update_packages()
    elif c == "2":
        update_reqs()
    else:
        print("Invalid choice")
