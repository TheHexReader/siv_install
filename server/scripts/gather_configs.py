import json
import os

class GatherConfigs:
    _configs = {}

    def __init__(self):
        for file in os.listdir('./configs'):
            self._configs[file[:-5]] = json.load(open(f'./configs/{file}', 'r'))

    def get_configs(self):
        return self._configs


if __name__ == "__main__":
    print(GatherConfigs().get_configs())