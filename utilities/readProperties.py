import configparser
import os

config = configparser.RawConfigParser()
# Get absolute path to config.ini
base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of readProperties.py
config_path = os.path.join(base_dir, "..", "Configurations", "config.ini")
config.read(config_path)

class ReadConfig:

    @staticmethod
    def getApplicationUrl():
        try:
            url = config.get("login info","base_url")
            return url
        except configparser.NoSectionError:
            print("Missing section 'login info' in config file.")
        except configparser.NoOptionError:
            print("Missing 'base_url' key in 'login info' section.")

    @staticmethod
    def getUserName():
        try:
            username = config.get("login info","username")
            return username
        except configparser.NoSectionError:
            print("Missing section 'login info' in config file.")
        except configparser.NoOptionError:
            print("Missing 'username' key in 'login info' section.")

    @staticmethod
    def getPassword():
        try:
            password = config.get("login info","password")
            return password
        except configparser.NoSectionError:
            print("Missing section 'login info' in config file.")
        except configparser.NoOptionError:
            print("Missing 'password' key in 'login info' section.")