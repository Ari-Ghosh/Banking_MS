from datetime import datetime
from bank import db
from time import sleep
from flask import flash, session
from bank.model import Account, TransactionControl

def get_formatted_date():
    """
    Get the current date and time in a formatted string.
    """
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

def account_type_list():
    """
    Return a dictionary of account types.
    """
    return {
        '1': 'Current',
        '2': 'Saving'
    }

def add_transaction(transaction_type, amount, source_account_id, destination_account_id=None):
    """
    Add a transaction to the Transaction Control.

    Args:
        transaction_type (int): Type of transaction (1: Withdraw, 2: Deposit, 3: Transfer).
        amount (int): The transaction amount.
        source_account_id (int): The source account ID.
        destination_account_id (int): The destination account ID for transfers.

    Returns:
        bool: True if the transaction was successful, False otherwise.
    """
    if not transaction_type or (transaction_type == 3 and not destination_account_id):
        return False

    # Wait if accounts are locked
    while check_locked([source_account_id, destination_account_id]):

        sleep(0.5)

    locked_account([source_account_id, destination_account_id])

    account_obj = Account.query.get(source_account_id)

    if transaction_type == 1:
        # Withdraw Money
        if account_obj.amount < amount:
            flash('Withdraw not allowed, please choose a smaller amount')
            return False
        account_obj.amount -= amount
        save_transaction_entry(source_account_id, "Withdraw", amount)
    elif transaction_type == 2:
        # Deposit Money
        account_obj.amount += amount
        save_transaction_entry(source_account_id, "Deposit", amount)
    elif transaction_type == 3:
        if account_obj.amount < amount:
            flash('Withdraw not allowed, please choose a smaller amount')
            return False

        destination_account_obj = Account.query.get(destination_account_id)
        account_obj.amount -= amount
        destination_account_obj.amount += amount

        save_transaction_entry(source_account_id, "Withdraw", amount)
        save_transaction_entry(destination_account_id, "Deposit", amount)

    db.session.add(account_obj)
    db.session.commit()

    unlocked_account([source_account_id, destination_account_id])
    flash("Transaction completed successfully")
    return True

def locked_account(accounts=[]):
    """
    Lock the specified accounts.

    Args:
        accounts (list): List of account IDs to lock.
    """
    for account in accounts:
        account_obj = Account.query.get(account)
        account_obj.is_locked = True
        db.session.add(account_obj)
        db.session.commit()

def unlocked_account(accounts=[]):
    """
    Unlock the specified accounts.

    Args:
        accounts (list): List of account IDs to unlock.
    """
    for account in accounts:
        account_obj = Account.query.get(account)
        account_obj.is_locked = False
        db.session.add(account_obj)
        db.session.commit()

def check_locked(accounts=[]):
    """
    Check if any of the specified accounts are locked.

    Args:
        accounts (list): List of account IDs to check.

    Returns:
        bool: True if any account is locked, False otherwise.
    """
    return any(Account.query.get(account).is_locked for account in accounts)

def save_transaction_entry(account_id, description, amount):
    """
    Save a transaction entry in the Transaction Control.

    Args:
        account_id (int): The account ID.
        description (str): Description of the transaction.
        amount (int): The transaction amount.
    """
    transaction_obj = TransactionControl(account_id, description, amount, get_formatted_date())
    db.session.add(transaction_obj)
    db.session.commit()

def flash_set(message):
    """
    Set a flash message in the session.

    Args:
        message (str): The flash message to set.
    """
    if 'flash' in session:
        session['flash'].append(message)
    else:
        session['flash'] = [message]

def flash_retrieve():
    """
    Retrieve and clear flash messages from the session.

    Returns:
        list: List of flash messages.
    """
    messages = session.pop('flash', [])
    for message in messages:
        flash(message)
