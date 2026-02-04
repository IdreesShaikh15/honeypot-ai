def should_terminate(session: dict) -> bool:

    intelligence = session["intelligence"]

    # If strong intelligence collected
    if (
        intelligence["upiIds"] or
        intelligence["phoneNumbers"] or
        intelligence["phishingLinks"]
    ):
        return True

    # Allow deeper engagement
    if session["total_messages"] >= 12:
        return True

    return False
