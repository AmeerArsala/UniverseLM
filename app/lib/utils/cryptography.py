from typing import List, Dict
import hashlib
import uuid
import secrets
import base64
import numpy as np


def uuid_to_hashed_bigint(uuid_str: str) -> int:
    # Convert the UUID string to bytes
    uuid_bytes = uuid.UUID(uuid_str).bytes

    # Hash the UUID bytes using SHA256
    hashed_bytes = hashlib.sha256(uuid_bytes).digest()

    # Convert the hash to a bigint
    hashed_bigint = int.from_bytes(hashed_bytes, byteorder="big")

    return hashed_bigint


def uuid_hashed_bigint() -> int:
    return uuid_to_hashed_bigint(str(uuid.uuid4()))


def small_uid(num_digits: int = 15) -> int:
    big_uid: int = uuid_hashed_bigint()

    # Choose num_digits random numbers (sample without replacement)
    random_digits: List[str] = np.random.choice(
        list(str(big_uid)), num_digits, replace=False
    ).tolist()

    small_uid_num_str: str = "".join(random_digits)

    return int(small_uid_num_str)


def generate_api_key(prefix: str = "UNIVERSELM") -> str:
    # Generate 32 random bytes
    random_bytes = secrets.token_bytes(32)

    # Convert those bytes into a URL-safe base64 string
    # And remove the '=' since they're only used for padding purposes (not our use-case)
    api_key: str = base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")

    if len(prefix) > 0:
        api_key = f"{prefix}_{api_key}"

    return api_key
