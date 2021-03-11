import cx_Freeze

executables = [cx_Freeze.Executable(script="flappybir.py", icon="assets/flappy.ico")]

cx_Freeze.setup(
    name= "Flappy Bird - Patrick Piccini",
    options={"build_exe": {"packages":["pygame"],
    "include_files":["assets"]    
    }}, executables=executables
    )