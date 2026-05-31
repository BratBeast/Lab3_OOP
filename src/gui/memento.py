class ArrayMemento:
    """
    Патерн Memento.
    Зберігає знімок стану масиву (наприклад, до сортування),
    щоб його неможливо було випадково змінити ззовні.
    """

    def __init__(self, state: list):
        # Обов'язково робимо копію, щоб уникнути проблем із посиланнями
        self._state = state.copy()

    def get_state(self) -> list:
        return self._state.copy()


class Caretaker:
    """
    Опікун (Caretaker) для керування історією знімків.
    Зберігає знімки і повертає їх для реалізації функції 'Undo'.
    """

    def __init__(self):
        self._history = []

    def backup(self, state: list):
        self._history.append(ArrayMemento(state))

    def undo(self) -> list:
        if not self._history:
            return None
        memento = self._history.pop()
        return memento.get_state()