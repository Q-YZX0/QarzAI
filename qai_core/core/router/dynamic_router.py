import os

dynamic_commands = []

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
modules_path = os.path.join(project_root, "modules")


def load_all_modules():
    import os
    import importlib.util

    print(f"[Router] 🔍 Explorando carpeta de módulos: {modules_path}")

    for folder in os.listdir(modules_path):
        mod_file = os.path.join(modules_path, folder, "module.py")
        if os.path.exists(mod_file):
            print(f"[Router] 📦 Cargando módulo: {folder}")
            try:
                spec = importlib.util.spec_from_file_location(
                    f"{folder}_module", mod_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "get_commands"):
                    cmds = module.get_commands()
                    if isinstance(cmds, list):
                        dynamic_commands.extend(cmds)
                        print(
                            f"[Router] ✅ Módulo '{folder}' cargado con {len(cmds)} comandos."
                        )
                    else:
                        print(
                            f"[Router] ⚠️ 'get_commands' en {folder} no retornó una lista."
                        )
                else:
                    print(f"[Router] ⚠️ El módulo '{folder}' no tiene 'get_commands()'.")
            except Exception as e:
                print(f"[Router] ❌ Error al cargar módulo '{folder}': {e}")
