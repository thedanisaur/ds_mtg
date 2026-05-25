settings = '''
[Settings]
{
    "layouts": {
        "LCK": {
            "weight": 1,
            "slots": [
                {
                    "name": "Land",
                    "count": 1,
                    "sheets": [
                        {"name": "LandRare",  "weight": 1},
                        {"name": "LandUncommon",  "weight": 7}
                    ]
                },
                {
                    "name": "RareOrMythic",
                    "count": 1,
                    "sheets": [
                        {"name": "Mythic", "weight": 1},
                        {"name": "Rare",   "weight": 7}
                    ]
                },
                {
                    "name": "UncommonOrLand",
                    "count": 3,
                    "sheets": [
                        {"name": "Uncommon", "weight": 3},
                        {"name": "LandUncommon",  "weight": 1}
                    ]
                },
                {
                    "name": "Common",
                    "count": 11,
                    "sheets": [
                        {"name": "Common", "weight": 1}
                    ]
                }
            ]
        }
    }
}'''