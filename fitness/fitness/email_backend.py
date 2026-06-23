"""
Custom email backend that disables SSL certificate verification.
Required on Windows where Python 3.13 cannot verify Gmail's cert chain.
"""
import ssl
from django.core.mail.backends.smtp import EmailBackend


class UnverifiedSMTPBackend(EmailBackend):
    """SMTP backend with SSL certificate verification disabled (Windows fix)."""

    def open(self):
        if self.connection:
            return False

        import smtplib
        self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
        self.connection.ehlo()
        if self.use_tls:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self.connection.starttls(context=ctx)
            self.connection.ehlo()
        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return True
