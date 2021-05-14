from configparser import ConfigParser


class ConfigStorage:
    def __init__(self, file: str):
        self.parser = ConfigParser()
        self.parser.read(file)

    def get_config_section(self, section: str) -> dict:
        """Get section of config as dict"""
        db = {}
        if self.parser.has_section(section):
            for param in self.parser.items(section):
                db[param[0]] = param[1]

        return db

