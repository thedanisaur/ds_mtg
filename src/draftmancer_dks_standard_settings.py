settings = '''
[Settings]
{
    "layouts": {
        "Default": {
            "weight": 1,
            "slots": [
                {
                    "name": "LandOrBasic",
                    "count": 1,
                    "sheets": [
                        {"name": "LandMythic",  "weight": 1},
                        {"name": "LandRare",  "weight": 4},
                        {"name": "LandUncommon",  "weight": 8},
                        {"name": "Basic", "weight": 32},
                    ]
                },
                {
                    "name": "RareOrMythic",
                    "count": 1,
                    "sheets": [
                        {"name": "LandRare",  "weight": 16},
                        {"name": "Rare",   "weight": 344},
                        {"name": "LandMythic",  "weight": 2},
                        {"name": "Mythic", "weight": 16}
                    ]
                },
                {
                    "name": "UncommonOrLand1",
                    "count": 1,
                    "sheets": [
                        {"name": "Uncommon", "weight": 10},
                        {"name": "LandUncommon",  "weight": 1}
                    ]
                },
                {
                    "name": "UncommonOrLand2",
                    "count": 1,
                    "sheets": [
                        {"name": "Uncommon", "weight": 10},
                        {"name": "LandUncommon",  "weight": 1}
                    ]
                },
                {
                    "name": "UncommonOrLand3",
                    "count": 1,
                    "sheets": [
                        {"name": "Uncommon", "weight": 10},
                        {"name": "LandUncommon",  "weight": 1}
                    ]
                },
                {"name": "Common",   "count": 11},
            ]
        }
    }
}'''