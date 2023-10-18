from webdriver_manager.chrome import ChromeDriverManager

with open('../chrome_driver_path.txt', 'w') as f_driverPath:
    f_driverPath.write(ChromeDriverManager().install())
