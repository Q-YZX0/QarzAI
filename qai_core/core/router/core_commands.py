def handle(command, router):
    command = command.strip().lower()

    if command.startswith("repite esto"):
        msg = command[len("repite esto") :].strip()
        router.io.speak(msg)
        return "El mensaje ha sido leído."

    elif command.startswith("genera sobre"):
        prompt = command[len("genera sobre") :].strip()
        return router.generator.create(prompt)

    elif command == "enable voice":
        router.io.switch_mode("voz")
        router.io.start()
        return "Modo voz activado."

    elif command == "disable voice":
        router.io.switch_mode("texto")
        router.io.start()
        return "Modo texto activado."
