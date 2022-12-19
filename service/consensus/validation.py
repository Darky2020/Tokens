from . import checks

async def validate_create(decoded, inputs, height):
    if len(inputs) != 1:
        return False

    send_address = list(inputs)[0]

    # Check if transaction has been sent from admin address
    if not checks.admin(send_address, height):
        return False

    # Check value for new token
    if not checks.value(decoded["value"]):
        return False

    # Check decimal points for new token
    if not checks.decimals(decoded["decimals"]):
        return False

    # Check if new token supply within constraints
    if not await checks.supply_create(
        decoded["value"], decoded["decimals"]
    ):
        return False

    # Check ticker length and if it's available
    if not await checks.ticker(decoded["ticker"]):
        return False

    return True

async def validate_issue(decoded, inputs, height):
    if len(inputs) != 1:
        return False

    send_address = list(inputs)[0]

    # Check if transaction has been sent from admin address
    if not checks.admin(send_address, height):
        return False

    # Check value for new tokens issued
    if not checks.value(decoded["value"]):
        return False

    # Check if token reissuable
    if not await checks.reissuable(decoded["ticker"]):
        return False

    # Check if token exists
    if not await checks.token(decoded["ticker"]):
        return False

    # Check if token owner
    if not await checks.owner(decoded["ticker"], send_address):
        return False

    # Check if issued amount within supply constraints
    if not await checks.supply_issue(decoded["ticker"], decoded["value"]):
        return False

    return True

async def validate_transfer(decoded, inputs, outputs):
    if len(inputs) != 1:
        return False

    if len(outputs) != 2:
        return False

    send_address = list(inputs)[0]

    # Check transfer value
    if not checks.value(decoded["value"]):
        return False

    # Check if token exists
    if not await checks.token(decoded["ticker"]):
        return False

    # Check if address has enough balance
    if not await checks.balance(
        decoded["ticker"], send_address, decoded["value"]
    ):
        return False

    return True