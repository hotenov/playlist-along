"""Nox sessions."""
from pathlib import Path
import shutil
import sys
from textwrap import dedent

import nox


try:
    from nox_poetry import Session
    from nox_poetry import session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message))


package = "playlist_along"
python_versions = ["3.9", "3.8", "3.7", "3.6"]
nox.options.sessions = (
    "safety",
    "mypy",
    "tests",
    # "typeguard",  # wait for Click 8.0 release
    "xdoctest",
    "docs-build",
)


@session(python="3.9")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["src", "tests", "docs/conf.py"]
    session.install(".")
    session.install("mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install("coverage[toml]", "pytest", "pygments", "pytest-datafiles", "pytest-mock")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage")


@session
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    # Do not use session.posargs unless this is the only session.
    nsessions = len(session._runner.manifest)
    has_args = session.posargs and nsessions == 1
    args = session.posargs if has_args else ["report"]

    session.install("coverage[toml]")

    if not has_args and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(python=python_versions)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    session.install(".")
    session.install("pytest", "typeguard", "pygments", "pytest-datafiles", "pytest-mock")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@session(python=python_versions)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", package, *args)


@session(name="docs-build", python="3.8")
def docs_build(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-click", "furo", "sphinx-inline-tabs")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@session(python="3.8")
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-click", "furo", "sphinx-inline-tabs")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
