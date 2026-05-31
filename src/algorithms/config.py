class SettingsManager:
    """
    Патерн Singleton.
    Менеджер конфігурацій, який гарантує єдину точку доступу до налаштувань програми.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            # Базові налаштування за замовчуванням
            cls._instance.animation_speed = 0.5
            cls._instance.array_size = 50
            cls._instance.theme = "light"
        return cls._instance

    def update_speed(self, new_speed: float):
        self.animation_speed = new_speed

    def update_size(self, new_size: int):
        self.array_size = new_size