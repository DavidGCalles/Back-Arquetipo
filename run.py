from app import create_app
from os import urandom, environ

app = create_app()
app.secret_key = urandom(24)
GPIOCONTROLLER = None

if __name__ == "__main__":
    if environ.get("RPI_MODULE"):
        from app.services.rpi_gpio_controller import GPIOController
        GPIOCONTROLLER = GPIOController()
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port , debug= True)
