# coding=utf-8
""" Simple testing calling the Para CLI """
import pytest
import os
from pathlib import Path
from paralang import InFileNotFoundError as ParaFileNotFoundError, \
    UserInputError

from paralang_cli import cli_run_output_dir_validation, cli_create_process
from paralang_cli.logging import cli_set_avoid_print_banner_overwrite

from . import (add_folder, overwrite_builtin_input, reset_input,
               create_test_file, BASE_TEST_PATH)

LOG_PATH = 'para.log'
ENCODING = 'utf-8'
main_file_path = BASE_TEST_PATH / "test_files" / "main.para"

# Avoiding printing the banner (CLI)
cli_set_avoid_print_banner_overwrite(True)


class TestCLISetup:
    @staticmethod
    def teardown_method(_):
        """
        This method is being called after each test case, and it will revert
        input back to the original function
        """
        reset_input()

    def test_build_exists_setup(self):
        add_folder("build")
        create_test_file("build", "example.txt")

        overwrite_builtin_input('True')
        cli_run_output_dir_validation(False, True, BASE_TEST_PATH)
        assert not os.path.exists(
            _ := str(BASE_TEST_PATH / "build_2" / "example.txt")
        ), _
        assert os.path.exists(
            _ := str(BASE_TEST_PATH / "build" / "example.txt")
        ), _

        create_test_file("build", "example.txt")

        overwrite_builtin_input('False')
        cli_run_output_dir_validation(True, True, BASE_TEST_PATH)
        assert not os.path.exists(
            _ := str(BASE_TEST_PATH / "build" / "example.txt")
        ), _
        add_folder("build")

    def test_dist_exists_setup(self):
        add_folder("dist")
        create_test_file("dist", "example.txt")

        overwrite_builtin_input('True')  # Overwrite data -> True
        cli_run_output_dir_validation(True, False, BASE_TEST_PATH)
        assert not os.path.exists(
            _ := str(BASE_TEST_PATH / "dist_2" / "example.txt")
        ), _
        assert os.path.exists(
            _ := str(BASE_TEST_PATH / "dist" / "example.txt")
        ), _

        create_test_file("dist", "example.txt")
        overwrite_builtin_input('False')  # Overwrite data -> False
        cli_run_output_dir_validation(True, True, BASE_TEST_PATH)
        assert not os.path.exists(
            _ := str(BASE_TEST_PATH / "dist" / "example.txt")
        ), _
        add_folder("dist")

    def test_simple_setup_compilation_process(self):
        b_path: Path = add_folder("build")
        d_path: Path = add_folder("dist")

        p = cli_create_process(
            file=main_file_path,
            log_path=LOG_PATH,
            encoding=ENCODING,
            build_path=b_path,
            dist_path=d_path
        )

        assert p.build_path == b_path
        assert p.dist_path == d_path

    @pytest.mark.parametrize(
        "path", [
            "not_existing.para", "not_existing"
        ]
    )
    def test_wrong_path_compilation_process_1(self, path: str):
        b_path: Path = add_folder("build")
        d_path: Path = add_folder("dist")
        try:
            p = cli_create_process(
                file=path,
                log_path=LOG_PATH,
                encoding=ENCODING,
                build_path=b_path,
                dist_path=d_path
            )
            assert False
        except ParaFileNotFoundError as e:
            ...

    @pytest.mark.parametrize(
        "path", [
            "", "", "ddf $  &/`='|.*"
        ]
    )
    def test_wrong_path_compilation_process_2(self, path: str):
        b_path: Path = add_folder("build")
        d_path: Path = add_folder("dist")
        try:
            p = cli_create_process(
                file=path,
                log_path=LOG_PATH,
                encoding=ENCODING,
                build_path=b_path,
                dist_path=d_path
            )
            assert False
        except UserInputError:
            ...
