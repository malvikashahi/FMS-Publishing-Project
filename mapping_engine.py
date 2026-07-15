import json


class MappingEngine:

    def __init__(self, mapping_file):
        self.mapping_file = mapping_file
        self.mapping = self.load()

    def load(self):

        with open(
            self.mapping_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def get_objects(self):

        return self.mapping["objects"]

    def get_object(
        self,
        slide,
        object_name
    ):

        for obj in self.mapping["objects"]:

            if (
                obj["slide"] == slide
                and
                obj["object_name"]
                == object_name
            ):
                return obj

        return None