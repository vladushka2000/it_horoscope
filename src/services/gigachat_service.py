import datetime
import logging
import uuid
from http import HTTPStatus

from dependency_injector.wiring import inject, Provide

from bases import base_http_client, base_llm_client
from bases.services import gigachat_llm_service
from config import llm_config
from dto import http_dto, user_dto
from tools import const
from tools.di_containers import integration_container, llm_container

logger = logging.getLogger(__name__)


class GigaChatService(gigachat_llm_service.GigaChatLLMService):
    _PROMPT = """
        Input Rules:
        1. Гороскоп на английском языке
        2. Знак зодиака пользователя
        3. Роль в компании (должность)
        4. Любимое emoji пользователя
        5. Имя пользователя (может быть пустой строкой)
        User Input:
        АНГЛИЙСКИЙ ГОРОСКОП - {english_horoscope}
        ЗНАК - {sign}
        ТЕКУЩАЯ ДАТА - {current_date}
        ЛЮБИМОЕ EMOJI - {emoji}
        РОЛЬ В КОМПАНИИ - {role}
        ИМЯ ПОЛЬЗОВАТЕЛЯ - {user_name}
        Instructions:
        1. Креативно переведи гороскоп с английского на русский, сохраняя смысл, но адаптируя под стиль "Дирекции Вайба"
        2. Учти роль пользователя в компании — вплети соответствующие профессиональные детали (для разработчиков — про код, для менеджеров — про проекты, для дизайнеров — про интерфейсы)
        3. Органично интегрируй любимое emoji пользователя в текст (2-3 раза в разных разделах)
        4. Используй персональное обращение
        5. Строго соблюдай структуру форматирования
        6. Нельзя использовать разметку markdown в ответе
        7. В пункте "Чек-лист для классного вайба" используй предложения в инфинитиве
        8. Обязательно убери квадратные скобки из ответа
        9. В пункте "Чек-лист для классного вайба" emoji должны быть разными и подходящими к тексту чек-листа по смыслу
        10. Не допускай орфографических ошибок
        11. Строго следуй шаблону Message
        12. Нельзя генерировать сообщение оскорбительного характера или вредящее психологическому здоровью
        13. Современная лексика (вайб, хайп, краш, кринж, сиять и т.д.)
        14. Персонализированное обращение через имя/должность/любимое emoji
        15. Генерируй текст в пунтке "Вайб дня" с учетом характера любимого emoji
        16. Соблюдай ограничения по длине для каждого пункта
        Message:
        Хей, {user_name}, держи вайбовый гороскоп для {sign} на {current_date}
        💫 Вайб дня: [2-3 предложения, от 30 до 50 слов, используй любимый emoji 1 раз]
        🎯 Чек-лист для классного вайба:
        · [ПОДХОДЯЩИЙ EMOJI] [1 предложение (что необходимо сделать) до 12 слов, активность, связанная с работой в целом]
        · [ПОДХОДЯЩИЙ EMOJI] [1 предложение (что необходимо сделать) до 12 слов, активность, связанная с ролью в компании]
        · [ПОДХОДЯЩИЙ EMOJI] [1 предложение (что необходимо сделать) до 12 слов, активность, не связанная с работой]
        💎 Девиз дня: [1 короткая фраза на основе пункта "Вайб дня", до 8 слов]

        С любовью и заботой, твоя Дирекция Вайба 🚀
        Requirements:
        Output: Только готовый гороскоп на основе шаблона Message на русском с правильным форматированием, без дополнительных комментариев.
    """
    _SYSTEM_MESSAGE = """
        Ты — астролог из "Дирекции Вайба". Твоя задача — творчески перевести гороскоп с английского на русский, адаптируя его под конкретного пользователя. Твой стиль — вдохновляющий, мотивирующий и немного ироничный, в современном стиле для IT-специалистов.
    """

    @inject
    async def generate_horoscope(
        self,
        user: user_dto.UserDTO,
        english_horoscope: str,
        date: datetime.date,
        http_client: base_http_client.BaseHTTPClient = Provide[
            integration_container.IntegrationContainer.http_client
        ],  # noqa
        llm_client: base_llm_client.BaseLLMClient = Provide[
            llm_container.LLMContainer.gigachat_client
        ],  # noqa
    ) -> str:
        logger.info("Генерация гороскопа по формату")

        async with http_client as client:
            response = await client.post(
                http_dto.HTTPRequestDTO(
                    url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                    headers={
                        "Authorization": f"Basic {llm_config.llm_config.gigachat_auth_key}",
                        "RqUID": str(uuid.uuid4()),
                        "Accept": "application/json"
                    },
                    form_data={
                        "scope": "GIGACHAT_API_PERS"
                    }
                )
            )

        if response.status != HTTPStatus.OK:
            raise ValueError("Ошибка доступа к LLM")

        llm_client.set_api_key(response.payload["access_token"])

        async with llm_client:
            prompt = self._PROMPT.format(
                english_horoscope=english_horoscope,
                current_date=f"{date.day} {const.russian_months[date.month]}",
                emoji=user.emoji,
                role=user.company_role.value,
                user_name=user.full_name,
                sign=user.sign.value
            )

            return await llm_client.chat(prompt, self._SYSTEM_MESSAGE)
