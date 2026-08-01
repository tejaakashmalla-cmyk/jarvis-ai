# ExpenseTracker

## Features

- Add an expense using the `add` command
- Delete an expense using the `delete` command
- List all expenses using the `list` command

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application:**
   ```bash
   python src/main.py
   ```
   This will start the CLI application in your terminal.

3. **Commands:**
   - `add <category> <amount>`: Add an expense with category and amount.
   - `delete <id>`: Delete an expense by its ID.
   - `list`: List all expenses.

## Known Issues

- The application uses JSON for storage, which may lead to data loss if the system is restarted or corrupted. Ensure that backups are in place.

---

This documentation serves as a guide for setting up and using the ExpenseTracker CLI tool. For further customization or feature requests, please refer to the source code and make necessary changes.