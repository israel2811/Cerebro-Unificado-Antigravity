# 🚀 Guía de Despliegue: Nodo Ráfaga (Codespaces)

El procesamiento de millones de palabras satura tu laptop local de 2GB de RAM. A partir de ahora, toda la **extracción forense** (Omni-Scanner) y el **volcado a Docs** (Docs Injector) se harán en el **Nodo Ráfaga**.

## ¿Qué es el Nodo Ráfaga?
Es una Máquina Virtual gratuita de Microsoft (GitHub Codespaces) que te regalará **8GB o 16GB de RAM** bajo demanda para devorar toda tu memoria de Obsidian y JSONs sin pestañear.

## Instrucciones de Activación (Desde Chrome Local):

1. **Abre Chrome** en tu PC local.
2. Navega a tu repositorio en GitHub donde hemos alojado este ecosistema (`Antigravity_Cloud_Project`).
3. Presiona el atajo de teclado: `.` (Punto)
   *(O alternativamente, dale click al botón verde `<> Code` -> Pestaña `Codespaces` -> `+ Create codespace on main`)*.
4. Magia Pura: GitHub leerá el archivo `.devcontainer.json` que forjamos, e instalará Python, Playwright y todo lo necesario en una VM en un servidor Linux.
5. Verás Visual Studio Code abrirse dentro del propio Chrome.

## Comandos a Ejecutar en la Terminal de Codespaces:

Una vez que la terminal web esté lista, clava la recolección masiva ahí:

```bash
cd scripts_leviathan
# Activa el extractor masivo (ya no hay límite de RAM para nosotros)
python 01_nexus_deep_scanner.py

# Envía todo a la nube (Inyección de Docs)
python 02_docs_prep_injector.py
```

Al terminar, toda tu base mental estará inyectada y formateada para el *Redactor Jefe (Claude)*. Puedes cerrar la pestaña, Codespaces hibernará y no gastará horas de tu cuota mensual.
