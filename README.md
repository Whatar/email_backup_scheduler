# Email Backup Scheduler

This script fetches and backs up emails from an IMAP server and saves them to a local file. It is scheduled to run periodically to ensure that new emails are backed up regularly.

## Prerequisites

- Python 3.x
- `imaplib` and `email` modules (included in the Python standard library)
- `schedule` module
- `configparser` module

## Installation

1. Clone the repository or download the script.
2. Install the required Python modules using pip:
    ```sh
    pip install schedule configparser
    ```

## Configuration

1. Create a [.env](http://_vscodecontentref_/0) file in the root directory with the following content:
    ```ini
    [DEFAULT]
    EMAIL_USER=your_email@example.com
    EMAIL_PASSWORD=your_password
    ```

2. Ensure that the [.gitignore](http://_vscodecontentref_/1) file includes the [.env](http://_vscodecontentref_/2) file to prevent sensitive information from being committed to version control:
    ```gitignore
    .env
    out/*
    ```

## Usage

1. Run the script:
    ```sh
    python schedule_backup_register_emails.py
    ```

2. The script will fetch and back up emails from the IMAP server and save them to [emails_backup.mbox](http://_vscodecontentref_/3). It will also log the backup process in [backup.log](http://_vscodecontentref_/4).

3. The script is scheduled to run every Sunday at 01:00. You can modify the schedule by uncommenting and adjusting the following line in the script:
    ```python
    schedule.every().sunday.at("01:00").do(fetch_and_backup_emails)
    ```

## Script Details

- The script reads email credentials from the [.env](http://_vscodecontentref_/5) file.
- It connects to the IMAP server and logs in using the provided credentials.
- It fetches new emails since the last backup and appends them to the backup file.
- It logs the backup process, including the last saved email ID, to a log file.
- The script runs continuously, checking for scheduled tasks every second.

## License

This project is licensed under the MIT License.