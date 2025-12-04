"""
WSGI entry point для продакшена.
"""

from main2 import app

if __name__ == "__main__":
    # Этот блок выполняется только при прямом запуске файла
    app.run()
