def is_valid_username(value: str) -> bool:
    return bool(value and len(value) >= 3)


def is_valid_password(value: str) -> bool:
    return (
        len(value) >= 8
        and any(character.islower() for character in value)
        and any(character.isupper() for character in value)
        and any(character.isdigit() for character in value)
    )
