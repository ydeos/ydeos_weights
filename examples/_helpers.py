# coding: utf-8

r"""Helper functions for the examples."""

import os


def path_from_file(file_origin: str, relative_path: str) -> str:
    r"""Builds an absolute path from a file using a relative path."""
    if not os.path.isfile(file_origin):
        msg = "The file_origin parameter refers to a path that does not exist"
        raise ValueError(msg)
    dir_of_file_origin = os.path.dirname(os.path.realpath(file_origin))
    return os.path.abspath(os.path.join(dir_of_file_origin, relative_path))
