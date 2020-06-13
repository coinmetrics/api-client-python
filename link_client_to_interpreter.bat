FOR /F "tokens=* USEBACKQ" %%F IN (`python -c "import site;print(site.getsitepackages()[1])"`) DO (SET package_target_path=%%F\coinmetrics)
rmdir %package_target_path%
rmdir /s /q %package_target_path%
mklink /J %package_target_path% .\coinmetrics
