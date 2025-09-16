import enum


class Stage(enum.Enum):
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Sign(enum.Enum):
    ARIES = "♈️ Овен"
    TAURUS = "♉️ Телец"
    GEMINI = "♊️ Близнецы"
    CANCE = "♋️ Рак"
    LEO = "♌️ Лев"
    VIRGO = "♍️ Дева"
    LIBRA = "♎️ Весы"
    SCORPIO = "♏️ Скорпион"
    SAGITTARIUS = "♐️ Стрелец"
    CAPRICORN = "♑️ Козерог"
    AQUARIUS = "♒️ Водолей"
    PISCES = "♓️ Рыбы"


horoscope_integration_signs = {
    Sign.ARIES: "Aries",
    Sign.TAURUS: "Taurus",
    Sign.GEMINI: "Gemini",
    Sign.CANCE: "Cancer",
    Sign.LEO: "Leo",
    Sign.VIRGO: "Virgo",
    Sign.LIBRA: "Libra",
    Sign.SCORPIO: "Scorpio",
    Sign.SAGITTARIUS: "Sagittarius",
    Sign.CAPRICORN: "Capricorn",
    Sign.AQUARIUS: "Aquarius",
    Sign.PISCES: "Pisces"
}


class CompanyRole(enum.Enum):
    SYS_ANALYST = "Аналитик"
    BUSINESS_ANALYST = "Бизнесс-аналитик"
    ARCHITECT = "Архитектор"
    BACKEND = "Разработчик backend"
    FRONTEND = "Разработчик frontend"
    DESIGNER = "Дизайнер"
    QA_ENGINEER = "Тестировщик"
    DEVOPS_ENGINEER = "Инженер DevOps"


class LLMProvider(enum.Enum):
    GIGACHAT = "GIGACHAT"


russian_months = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря"
}
