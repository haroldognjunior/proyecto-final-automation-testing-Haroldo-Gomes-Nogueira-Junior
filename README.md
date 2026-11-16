# Proyecto Final – Automation Testing – Haroldo Nogueira

Framework de pruebas automatizadas en Python para:

- **UI** de [saucedemo.com](https://www.saucedemo.com) con Selenium WebDriver y Page Object Model.
- **API** de [JSONPlaceholder](https://jsonplaceholder.typicode.com) con Requests.

Genera un reporte HTML (con captura de pantalla en cada test de UI que falla) y un log de ejecución. Corre solo en GitHub Actions con cada push a `main`.

## De la pre-entrega al proyecto final

Tomé como base la pre-entrega (login, catálogo y carrito con funciones en `utils/helpers.py`) y la fui extendiendo:

| Pre-entrega                                                       | Proyecto final                                                                     |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Acciones y selectores en `utils/helpers.py` y `utils/locators.py` | Una clase por página en `pages/` (Page Object Model)                               |
| Un solo usuario (`datos/usuarios.json`)                           | Login parametrizado desde `datos/login_users.csv`, con casos negativos             |
| Login, catálogo y carrito                                         | + orden de productos, quitar del carrito, checkout completo y validación de campos |
| Solo UI                                                           | + pruebas de API (GET, POST, DELETE, error 404 y peticiones encadenadas)           |
| Captura en fallos guardada en carpeta                             | Además se adjunta al reporte HTML                                                  |
| Ejecución manual                                                  | GitHub Actions con los reportes como artefacto                                     |

`utils/helpers.py` se quedó con lo que no pertenece a ninguna página: crear el navegador, leer los datos y guardar capturas.

## Tecnologías

| Herramienta          | Uso                               |
| -------------------- | --------------------------------- |
| Python 3.10+         | Lenguaje                          |
| Pytest               | Tests, fixtures y parametrización |
| Selenium WebDriver 4 | Pruebas de UI                     |
| Requests             | Pruebas de API                    |
| pytest-html          | Reporte HTML                      |
| GitHub Actions       | Ejecución automática (CI)         |

## Estructura

```
├── .github/workflows/tests.yml   # pipeline de CI
├── conftest.py                   # fixture del navegador + captura automática en fallos
├── pytest.ini                    # reporte HTML, logging y markers
├── requirements.txt
├── datos/
│   ├── usuarios.json             # usuario base para los tests que necesitan login
│   ├── login_users.csv           # usuarios válidos e inválidos
│   ├── checkout_data.json        # clientes y productos para el checkout
│   └── api_data.json             # datos para los tests de API
├── pages/                        # Page Object Model
│   ├── base_page.py              # esperas, clicks y escritura comunes
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/
│   │   ├── conftest.py           # fixtures logged_driver e inventory_page
│   │   ├── test_login.py
│   │   ├── test_inventory.py
│   │   ├── test_cart.py
│   │   ├── test_checkout.py
│   │   └── test_known_bugs.py    # bugs conocidos (xfail)
│   └── api/
│       ├── conftest.py           # fixture del cliente de API
│       └── test_posts_api.py
├── utils/
│   ├── helpers.py                # navegador, lectura de datos y capturas
│   └── api_client.py             # wrapper de requests con logging
└── reports/                      # reporte HTML, log y capturas (se generan al correr)
```

## Decisiones que tomé

- **Los tests no tocan Selenium.** Llaman a métodos de las páginas (`login()`, `add_product_to_cart()`, `go_to_checkout()`). Si cambia un selector, se corrige en un solo lugar.
- **Un navegador nuevo por test.** Es más lento que reutilizarlo, pero ningún test depende del estado que dejó otro (carrito, sesión).
- **Esperas explícitas, nunca `sleep`.** Todo pasa por `BasePage`, que espera a que el elemento sea visible o clickeable.
- **Datos fuera del código.** Para probar otro usuario o cliente basta con agregar una fila al CSV o un objeto al JSON.
- **Validar más de una cosa en los negativos.** En un login inválido no solo reviso el mensaje, también que no haya entrado al inventario.
- **Bugs conocidos como `xfail`.** Encontré 3 defectos con `problem_user`. En vez de dejar tests en rojo, cada uno describe el comportamiento correcto y queda vinculado a su BUG-ID. Si el bug se corrige, el reporte lo muestra como XPassed.
- **Mensajes en los assert.** Cuando algo falla, el reporte dice qué se esperaba y qué llegó, sin tener que abrir el código.

## Casos cubiertos

### UI (saucedemo.com)

| Archivo              | Casos                                                                                                                         |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `test_login.py`      | Login exitoso con 3 usuarios · 4 negativos (usuario bloqueado, contraseña incorrecta, usuario vacío, contraseña vacía)        |
| `test_inventory.py`  | Título · menú, filtro y carrito visibles · 6 productos con nombre y precio · orden por precio asc/desc · orden por nombre Z-A |
| `test_cart.py`       | Agregar un producto (contador y carrito) · agregar varios · quitar uno                                                        |
| `test_checkout.py`   | Compra completa con 2 clientes (valida subtotal y mensaje final) · 3 negativos de campos obligatorios                         |
| `test_known_bugs.py` | 3 defectos de `problem_user`, marcados como `xfail`                                                                           |

### API (JSONPlaceholder)

| Método     | Caso                                                             |
| ---------- | ---------------------------------------------------------------- |
| GET        | Post por id (estado, Content-Type, estructura y tipos)           |
| GET        | Posts filtrados por usuario (parametrizado con 3 usuarios)       |
| GET        | Post inexistente → 404 (escenario de error)                      |
| POST       | Crear post (parametrizado, valida 201 y que devuelva lo enviado) |
| DELETE     | Borrar post → 200                                                |
| Encadenado | Post → autor del post → comentarios del post                     |

> JSONPlaceholder es una API de práctica: POST y DELETE responden bien pero no guardan cambios. Por eso el encadenamiento lo hice con datos que sí existen.

## Instalación

Requisitos: Python 3.10 o superior y Google Chrome. El driver de Chrome lo descarga Selenium solo.

```bash
git clone https://github.com/haroldognjunior/proyecto-final-automation-testing-Haroldo-Gomes-Nogueira-Junior.git
cd proyecto-final-automation-testing-haroldo-nogueira

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Ejecución

Todo (UI + API), con el reporte HTML incluido:

```bash
pytest
```

Solo una parte:

```bash
pytest -m ui      # solo interfaz
pytest -m api     # solo API
pytest tests/ui/test_login.py
```

Sin abrir la ventana del navegador:

```bash
HEADLESS=1 pytest                  # Linux / Mac
$env:HEADLESS=1; pytest            # Windows PowerShell
```

## Reportes

Después de cada ejecución, en `reports/`:

| Archivo         | Qué contiene                                                                   |
| --------------- | ------------------------------------------------------------------------------ |
| `reporte.html`  | Resumen de la corrida                                                          |
| `ejecucion.log` | Log completo con fecha y hora de cada paso                                     |
| `screenshots/`  | Una captura por cada test de UI fallido: `nombre_del_test_AAAAMMDD_HHMMSS.png` |

### Cómo leer el reporte HTML

- Arriba está el **resumen**: cuántos tests corrieron y cuántos quedaron en cada estado. Haciendo click en un estado se filtra la lista.
  - **Passed**: el test pasó.
  - **Failed**: falló una validación. Al expandir la fila se ven el error, el log del test y la **captura de pantalla**.
  - **Error**: falló la preparación (por ejemplo, el login previo). También trae captura.
  - **XFailed**: bug conocido que sigue presente, es lo esperado. Si aparece **XPassed**, el bug se corrigió y el test se puede pasar a normal.
- La columna **Duration** muestra cuánto tardó cada test.
- Al expandir cualquier fila se ve su log: qué usuario usó, qué productos agregó, qué requests mandó y qué respondió la API.

## CI con GitHub Actions

`.github/workflows/tests.yml` corre todos los tests en modo headless en cada push a `main` y en cada pull request. Los reportes quedan como artefacto descargable en **Actions** → la ejecución → **Artifacts**.
