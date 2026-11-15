"""
Fixtures y hooks compartidos por todos los tests.

Cada test recibe su propio navegador, así la falla de uno no
arrastra a los demás (igual que en la pre-entrega).
"""
import logging

import pytest

from utils.helpers import create_driver, save_screenshot

log = logging.getLogger("conftest")


@pytest.fixture
def driver(request):
    # Antes del yield = setup, después = teardown (como beforeEach / afterEach)
    log.info("===== Inicio: %s =====", request.node.name)
    browser = create_driver()
    yield browser
    browser.quit()
    log.info("===== Fin: %s =====", request.node.name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test de UI falla, guarda la captura y la adjunta al reporte HTML."""
    outcome = yield
    report = outcome.get_result()

    # "setup" también cuenta: si falla el login previo quiero ver la pantalla
    if report.when not in ("setup", "call") or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:  # tests de API: no hay navegador
        return

    save_screenshot(browser, item.name)

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html:
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(browser.get_screenshot_as_base64(), "Captura"))
        report.extras = extras


def pytest_html_report_title(report):
    report.title = "Proyecto final - Automation Testing - Haroldo Nogueira"
