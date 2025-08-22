from email.message import EmailMessage

import aiosmtplib
from babel.support import Translations
from jinja2 import Environment, FileSystemLoader

from app.schemas.user import RegisteredPayload, PassChangedPayload, PassResetPayload


def _normalize_locale(loc: str | None, default: str) -> list[str]:
    if not loc:
        return [default]
    loc2 = loc.replace("-", "_")
    parts = loc2.split("_")
    chain = []
    if len(parts) == 2:
        chain = [f"{parts[0]}_{parts[1]}", parts[0]]
    else:
        chain = [parts[0]]
    if default not in chain:
        chain.append(default)
    return chain


class EmailService:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        from_email: str,
        start_tls: bool = True,
        smtp_timeout: float = 15.0,
        templates_dir: str = "app/templates",
        translations_dir: str = "app/locale",
        default_locale: str = "en",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.start_tls = start_tls
        self.smtp_timeout = smtp_timeout

        self.default_locale = default_locale
        self.translations_dir = translations_dir

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            extensions=["jinja2.ext.i18n"],
            enable_async=False,
            autoescape=True,
        )

    def _get_template(self, template_name: str, language: str):
        env = self.env.overlay()
        locales = _normalize_locale(language, self.default_locale)
        translations = Translations.load(
            dirname=self.translations_dir,
            locales=locales,
            domain="messages",
        )
        env.install_gettext_translations(translations)
        return env.get_template(template_name)

    async def send_registration_credentials(self, u: RegisteredPayload):
        html_tpl = self._get_template("registered.html", u.language)
        txt_tpl  = self._get_template("registered.txt.html", u.language)  # можно держать .txt.j2

        ctx = u.model_dump()
        html = html_tpl.render(**ctx)
        text = txt_tpl.render(**ctx) if txt_tpl else None

        msg = EmailMessage()
        msg["From"] = self.from_email
        msg["To"] = u.email
        msg["Subject"] = "FJC_RS Registration Confirmation"
        if text:
            msg.set_content(text, subtype="plain", charset="utf-8")
            msg.add_alternative(html, subtype="html", charset="utf-8")
        else:
            msg.set_content(html, subtype="html", charset="utf-8")
        await self.__send_email(msg)

    async def send_reset_password(self, u: PassResetPayload):
        html_tpl = self._get_template("reset_password.html", u.language)
        txt_tpl  = self._get_template("reset_password.txt.html", u.language)

        ctx = u.model_dump()
        html = html_tpl.render(**ctx)
        text = txt_tpl.render(**ctx) if txt_tpl else None

        msg = EmailMessage()
        msg["From"] = self.from_email
        msg["To"] = u.email
        msg["Subject"] = "FJC_RS Reset Password"
        if text:
            msg.set_content(text, subtype="plain", charset="utf-8")
            msg.add_alternative(html, subtype="html", charset="utf-8")
        else:
            msg.set_content(html, subtype="html", charset="utf-8")
        await self.__send_email(msg)

    async def send_password_changed_success(self, u: PassChangedPayload):
        html_tpl = self._get_template("password_changed.html", u.language)
        txt_tpl  = self._get_template("password_changed.txt.html", u.language)

        ctx = u.model_dump()
        html = html_tpl.render(**ctx)
        text = txt_tpl.render(**ctx) if txt_tpl else None

        msg = EmailMessage()
        msg["From"] = self.from_email
        msg["To"] = u.email
        msg["Subject"] = "FJC_RS Password Changed"
        if text:
            msg.set_content(text, subtype="plain", charset="utf-8")
            msg.add_alternative(html, subtype="html", charset="utf-8")
        else:
            msg.set_content(html, subtype="html", charset="utf-8")
        await self.__send_email(msg)

    async def __send_email(self, msg: EmailMessage) -> str:
        await aiosmtplib.send(
            msg,
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            start_tls=self.start_tls,
            timeout=self.smtp_timeout,
        )
        return msg.get("Message-Id") or ""
