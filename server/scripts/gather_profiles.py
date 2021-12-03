import json

class GatherProfiles:
    _default_profile = {}
    _user_profiles = {}

    def __init__(self):
        self._default_profile = json.load(open("./profiles/default_profile.json", 'r'))
        self._user_profiles = json.load(open("./profiles/profiles.json", 'r'))

    def get_default_profile(self):
        return self._default_profile

    def get_user_profiles(self):
        return self._user_profiles


if __name__ == "__main__":
    print(GatherProfiles().get_default_profile())
    print(GatherProfiles().get_user_profiles())