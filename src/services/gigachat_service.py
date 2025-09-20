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
        Role:
        Ты — астролог из "Дирекции Вайба". Твоя задача — творчески перевести гороскоп с английского на русский, адаптируя его под конкретного пользователя. Твой стиль — вдохновляющий, мотивирующий и немного ироничный, в современном стиле для IT-специалистов.
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
        4. Если имя пользователя указано — используй персональное обращение, если нет — обращайся на "ты"
        5. Строго соблюдай структуру форматирования
        6. Нельзя использовать разметку markdown в ответе
        <Horoscope\n\tsign={sign}\n\tdate={current_date}>
        <💫 Общий вайб /> [2-3 предложения, не более 25 слов]
        <🚀 Карьерный вайб />
        · Утром: [1 предложение, до 15 слов, профессиональный контекст]
        · Днём: [1 предложение, до 15 слов, профессиональный контекст]
        · Вечером: [1 предложение, до 15 слов, профессиональный контекст]
        <❤️ Личный вайб /> [2 предложения, не более 20 слов]
        <🎯 Вайб-активности на день />
        · [ПОДХОДЯЩИЙ EMOJI] [1 предложение, до 12 слов]
        · [ПОДХОДЯЩИЙ EMOJI] [1 предложение, до 12 слов, персональный акцент]
        · [ПОДХОДЯЩИЙ EMOJI] [1 предложение, до 12 слов]
        <🔥 Главный совет от Вселенной /> [1 предложение, до 12 слов]
        <🎵 Саундтрек дня /> [1-2 трека, исполнитель, до 5 слов]
        <💎 Девиз дня /> [1 короткая фраза, до 8 слов] [ЛЮБИМОЕ EMOJI]

        <love>твоя Дирекция Вайба 🚀</love>
        </Horoscope>
        Requirements:
        - Современная лексика (вайб, хайп, краш, кринж, сиять)
        - IT-тематика в соответствии с должностью
        - Позитивный подход даже к вызовам
        - Персонализированное обращение через имя/должность
        - Общая длина: 120-180 слов
        - Естественная интеграция любимого emoji
        - Соблюдай ограничения по длине для каждого пункта
        - Не используй Markdown
        - В квадратных скобках в шаблоне ответа находятся подсказки для генерации
        - После генерации удали квадратные скобки
        - Саундтрек дня должен быть очень популярным и существовать в реальной жизни
        - Вплети обращение по имени пользователя, если оно передается в исходных данных
        Output: Только готовый гороскоп на русском с правильным форматированием, без дополнительных комментариев.
    """
    _SYSTEM_MESSAGE = """
        Ты — астролог-художник из "Дирекции Вайба". Твои гороскопы — это вдохновляющие, мотивирующие и немного ироничные тексты в современном стиле для IT-специалистов и креативных людей. Твой тон — уверенный, творческий, позитивный и дружелюбный.
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
                role=user.company_role,
                user_name=user.full_name,
                sign=user.sign.value
            )

            return await llm_client.chat(prompt, self._SYSTEM_MESSAGE)
