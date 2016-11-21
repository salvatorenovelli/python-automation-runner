import datetime

from cx_Freeze import setup, Executable

dt = datetime.datetime.now()

main_executable = Executable("main.py", base=None, targetName="runner.exe")
setup(name="Automation Runner",
      version="0.1." + dt.strftime('%m%d.%H%m'),
      description="Automation Runner",
      options={
          'build_exe': {
              'packages': ['flask', 'PIL', 'user_interaction', 'system_hotkey', 'external_script_runner'],
              'include_msvcr': True}},
      executables=[main_executable],
      requires=['flask', 'PIL'])
