from __future__ import annotations

import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import peewee

from .logger import logger
from models import Message, User
from exceptions import SMTPConnectException, DatabaseConnectException
import settings


class SendMail:

    __slots__ = (
        "password",
        "login",
        "host",
        "port_ssl",
        "port_tls",
        "message_from",
        "recipients",
        "user_id",
        "subject",
        "message",
        "result_status",
        "result_msg",
    )

    def __call__(self, subject: str, message: str):
        """
        param: subject - subject for message
        param: message - body message
        """
        self.subject = subject
        self.message = message
        self.__send_mail()
        self.__record_db()
        return {"status": self.result_status, "message": self.result_msg}

    def __init__(self, recipients: str | list, user_id: int = None):
        """
        param: recipients: str or list -user/users from message
        """
        self.password = settings.EMAIL_HOST_PASSWORD
        self.login = settings.EMAIL_HOST_USER
        self.host = settings.EMAIL_HOST
        self.port_ssl = settings.EMAIL_PORT_SSL
        self.port_tls = settings.EMAIL_PORT_TLS
        self.message_from = self.login
        self.recipients = recipients
        self.user_id = user_id
        self.subject = None
        self.message = None
        self.result_status = False
        self.result_msg = ""
        if not isinstance(self.recipients, list):
            self.recipients = [self.recipients]

    def __get_server_ssl(self):
        # Создание безопасного контекста SSL
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(self.host, self.port_ssl, context=context)
        server.login(self.login, self.password)
        return server
    
    def __get_dsn(self):
        return ": ".join([self.host, self.port_tls])

    def __get_server_tls(self):
        server = smtplib.SMTP(self.__get_dsn())
        server.starttls()
        return server

    def __get_server(self):
        try:
            return self.__get_server_ssl()            
        except Exception as e:
            logger("error", f"""Ошибка подключения к почтовому серверу по SSL.
            Error: {e}
            Попытка подлкючения по TLS...""")            
            try:
                return self.__get_server_tls()
            except Exception as e:
                raise SMTPConnectException(
                f"""Ошибка соеднинения с почтовым сервером.
                host: {self.host}
                port_ssl: {self.port_ssl}
                port_tls: {self.port_ssl}  
                Error: {e} """)

    def __get_msg(self, subject: str, message: str):
        msg = MIMEMultipart()
        msg["From"] = self.message_from
        msg["Subject"] = subject
        msg.attach(MIMEText(message))
        return msg
    
    def __record_db(self):
        try:
            user = User.get(User.id == self.user_id)
        except peewee.OperationalError as e: 
            raise DatabaseConnectException(
                f"""Ошибка соеднинения с БД.
                host: {settings.POSTGRES_HOST}
                port: {settings.POSTGRES_PORT}
                db: {settings.POSTGRES_DB}
                Error: {e}""" 
            )
        except peewee.DoesNotExist:
            user = None
            logger("error", f"""Пользователь с id {self.user_id} не найден, 
                   сообщение не будет привязано к определенному пользователю.""")        
        for message_to in self.recipients:
            msg = Message(
                user=user,
                subject=self.subject,
                message=self.message,
                email_to=message_to,
                email_from=self.login,
                is_send=self.result_status,
                status_msg=self.result_msg,
            )
            msg.save()
        return msg

    def __send_mail(self):
        if not self.message:
            self.result_msg = "Cообщение пусто."
            return
        if not self.subject:
            self.result_msg = "Заголовок пуст."
            return
        msg = self.__get_msg(self.subject, self.message)
        server = self.__get_server()
        if server:
            try:
                [
                    server.sendmail(self.message_from, message_to, msg.as_string())
                    for message_to in self.recipients
                ]
            except smtplib.SMTPException as e:
                self.result_msg = str(e)
            self.result_msg = (
                "Письмо было успешно отправлено."
            )
            self.result_status = True
