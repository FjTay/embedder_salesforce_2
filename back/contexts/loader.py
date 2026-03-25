from pathlib import Path


def load_business_objects():
    base = Path(__file__).parent
    business_path = base / "business.ini"
    result = set()
    with open(business_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, _, value = line.partition(": ")
            if key.strip():
                result.add(key.strip())
    return result


def load_business_descriptions():
    base = Path(__file__).parent
    business_path = base / "business.ini"
    result = {}
    with open(business_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, _, value = line.partition(": ")
            if key.strip():
                result[key.strip()] = value.strip()
    return result


def load_contexts():
    base = Path(__file__).parent
    business_path = base / "business.ini"
    model_path = base / "model.ini"

    business = {}
    with open(business_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, _, value = line.partition(": ")
            business[key.strip()] = value.strip()

    objects = []
    with open(model_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                objects.append(line)

    result = {obj: business.get(obj) for obj in objects}
    return result
