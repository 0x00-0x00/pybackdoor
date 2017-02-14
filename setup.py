import cx_Freeze

script = "backdoor.py"
name = "backdoor"
version = "0.1"
packages = {
        "packages":[
            "socket",
            "multiprocessing",
            "os",
            "subprocess",
            "time",
            "threading"
            ],
        "include_files": []
        }

exe = [cx_Freeze.Executable(script)]

cx_Freeze.setup(name=name, version=version, options = {"build_exe": packages}, executables = exe)
