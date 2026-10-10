from django.core.mail.backends.console import EmailBackend


class ReadableConsoleEmailBackend(EmailBackend):
    """Mostra o e-mail legível no terminal: acentos e link inteiros.

    O backend de console do Django imprime a mensagem MIME crua, com o corpo
    codificado (quoted-printable), o que quebra acentos e links longos.
    """

    def write_message(self, message):
        self.stream.write(f'Subject: {message.subject}\n')
        self.stream.write(f'From: {message.from_email}\n')
        self.stream.write(f'To: {", ".join(message.to)}\n\n')
        self.stream.write(f'{message.body}\n')
        self.stream.write('-' * 79)
        self.stream.write('\n')
