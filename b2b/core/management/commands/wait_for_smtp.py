"""Wait for SMTP availability."""
import time

from django.core.mail import get_connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to make Django wait for the SMTP server."""

    def handle(self, *args, **options):
        """Entry point for command."""
        self.stdout.write("Waiting for SMTP server...")
        smtp_ready = False
        while not smtp_ready:
            try:
                # Check if the SMTP server is ready
                connection = get_connection(fail_silently=False)
                connection.open()
                connection.close()
                smtp_ready = True
            except ConnectionRefusedError:
                self.stdout.write("SMTP server unavailable, retrying...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("SMTP server connection SUCCESS!"))
