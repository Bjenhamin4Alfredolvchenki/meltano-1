import os
from unittest import mock

import dotenv
import pytest
from meltano.core.plugin.command import UndefinedEnvVarError
from meltano.core.plugin_invoker import UnknownCommandError
from meltano.core.venv_service import VirtualEnv


class TestPluginInvoker:
    @pytest.fixture
    def plugin_invoker(self, utility, session, plugin_invoker_factory):
        subject = plugin_invoker_factory(utility)
        with subject.prepared(session):
            yield subject

    @pytest.fixture
    def nonpip_plugin_invoker(self, nonpip_tap, session, plugin_invoker_factory):
        subject = plugin_invoker_factory(nonpip_tap)
        with subject.prepared(session):
            yield subject

    def test_env(self, project, tap, session, plugin_invoker_factory):
        project.dotenv.touch()
        dotenv.set_key(project.dotenv, "DUMMY_ENV_VAR", "from_dotenv")
        dotenv.set_key(project.dotenv, "TAP_MOCK_TEST", "from_dotenv")

        subject = plugin_invoker_factory(tap)
        with subject.prepared(session):
            env = subject.env()

        # .env
        assert env["DUMMY_ENV_VAR"] == "from_dotenv"

        # Project env
        assert env["MELTANO_PROJECT_ROOT"] == str(project.root)

        # Project settings
        assert env["MELTANO_CLI_LOG_LEVEL"] == "info"

        # Plugin info
        assert env["MELTANO_EXTRACTOR_NAME"] == tap.name

        # Plugin settings
        assert env["MELTANO_EXTRACT_TEST"] == env["TAP_MOCK_TEST"] == "from_dotenv"
        assert env["MELTANO_EXTRACT__SELECT"] == env["TAP_MOCK__SELECT"] == '["*.*"]'

        # Plugin execution environment
        venv = VirtualEnv(project.venvs_dir(tap.type, tap.name))
        assert env["VIRTUAL_ENV"] == str(venv.root)
        assert env["PATH"].startswith(str(venv.bin_dir))
        assert "PYTHONPATH" not in env

    def test_unknown_command(self, plugin_invoker):
        with pytest.raises(UnknownCommandError) as err:
            plugin_invoker.invoke(command="foo")

        assert err.value.command == "foo"  # noqa: WPS441
        assert "supports the following commands" in str(err.value)  # noqa: WPS441

    def test_expand_exec_args(self, plugin_invoker):
        exec_args = plugin_invoker.exec_args(
            "extra",
            "args",
            command="cmd",
            env={
                "ENV_VAR_ARG": "env-var-arg",
            },
        )

        assert exec_args[0].endswith("utility-mock")
        assert exec_args[1:] == ["utility", "--option", "env-var-arg", "extra", "args"]

    def test_expand_command_exec_args(self, plugin_invoker):
        exec_args = plugin_invoker.exec_args(
            "extra",
            "args",
            command="cmd",
            env={
                "ENV_VAR_ARG": "env-var-arg",
            },
        )

        assert exec_args[0].endswith("utility-mock")
        assert exec_args[1:] == ["utility", "--option", "env-var-arg", "extra", "args"]

    def test_undefined_env_var(self, plugin_invoker):
        with pytest.raises(UndefinedEnvVarError) as err:
            plugin_invoker.invoke(command="cmd")

        assert (
            "Command 'cmd' referenced unset environment variable '$ENV_VAR_ARG' in an argument"
            in str(err.value)  # noqa: WPS441
        )

    @pytest.mark.parametrize(
        "executable_str,assert_fn",
        [
            ("tap-test", lambda exe: exe == "tap-test"),
            ("./tap-test", lambda exe: exe.endswith("meltano_project/tap-test")),
            ("/apps/tap-test", lambda exe: exe == "/apps/tap-test"),
        ],
    )
    def test_expand_nonpip_command_exec_args(
        self, nonpip_plugin_invoker, session, executable_str, assert_fn
    ):
        nonpip_plugin_invoker.plugin.executable = executable_str
        exec_args = nonpip_plugin_invoker.exec_args()

        assert assert_fn(exec_args[0])

        nonpip_plugin_invoker.prepare(session)
        env = nonpip_plugin_invoker.env()

        assert "VIRTUAL_ENV" not in env
        assert "PYTHONPATH" not in env
