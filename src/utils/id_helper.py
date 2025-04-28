import uuid

def generate_cow_id():
    return "cow_" + str(uuid.uuid4())[:8]