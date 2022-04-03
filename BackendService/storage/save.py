import json


def _main():
    obj = {
        "objects": [
            {
                "reduction": "CEO",
                "full_text": "Chief Executive Officer",
                "translation": "Генеральный директор корпорации"
            }
        ]
    }

    with open('abbreviation.json', 'w', encoding='utf-8') as file:
        json.dump(obj, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    _main()
