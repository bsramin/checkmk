import StringIO
import tarfile

import cmk.utils.crash_reporting
import cmk.gui.crash_reporting as crash_reporting


def test_gui_crash_report_registry():
    assert cmk.utils.crash_reporting.crash_report_registry["gui"] \
            == crash_reporting.GUICrashReport


def test_gui_crash_report_get_packed(register_builtin_html):
    store = crash_reporting.CrashReportStore()
    try:
        raise ValueError("DINGELING")
    except Exception:
        crash = crash_reporting.GUICrashReport.from_exception()
        store.save(crash)
        crash_dir = crash.crash_dir()

    tgz = crash_reporting._pack_crash_report(store.load_serialized_from_directory(crash_dir))
    buf = StringIO.StringIO(tgz)
    with tarfile.open(mode="r:gz", fileobj=buf) as tar:
        assert tar.getnames() == ["crash.info"]
