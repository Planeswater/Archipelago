import toml

class LocalConfig:

    def __init__(self, world):
        self.configurations = {
            "server_url": "<get_from_host>",
            "password": "<get_from_host_or_leave_as_empty_quotes>",
            "log_file_name": "lamulanamw.txt",
            "local_player_id": world.player,
            "players": [{"id": player_id, "name": world.multiworld.player_name[player_id]} for player_id in world.multiworld.player_ids],
            "item_mapping": []
        }

    def add_item(self, params):
        self.configurations["item_mapping"].append(
            {
                "flag": params["new_obtain_flag"],
                "location_id": params["location"].address,
                "player_id": params["location"].item.player,
                "obtain_value": params["obtain_value"]
            }
        )

    def write_file(self):
        return toml.dumps(self.configurations)
