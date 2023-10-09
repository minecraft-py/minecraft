# minecraftpy, a sandbox game
# Copyright (C) 2020-2023 minecraftpy team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from collections import namedtuple
from typing import Union


class NameSpace(namedtuple("NameSpace", ["main", "directory", "sub"])):
    def relative(self, other: Union[str, NameSpace]) -> NameSpace:
        if not isinstance(other, NameSpace):
            other = get_namespace(other)
        if self.main != other.main:
            return other
        if len(self.directory) < len(other.directory):
            return other
        if not all(map(lambda x: x[0] == x[1], zip(self.directory, other.directory))):
            return other
        return NameSpace(self.main, self.directory, other.sub)


def is_namespace(s: str, /) -> bool:
    """Determines if a string is a namespace.

    The namespace should satisfy
    `[top-level namespace]:<directory>/<sub-namespace1>.<sub-namespace2>...<sub-namespace n>`.

    The top-level namespace may be omitted, defaulting to `minecraft`; sub-namespaces
    are separated by `.`.

    Use `str.partition()` to detect if a namespace is legal.
    """
    check = []
    if s.partition(":")[1]:
        check.append(s.partition(":")[0].isidentifier())
        s = s.partition(":")[2]
    while s.partition("/")[1]:
        check.append(s.partition("/")[0].isidentifier())
        s = s.partition("/")[2]
    check.append(all([sub.isidentifier() for sub in s.split(".")]))
    return all(check)


def get_namespace(s: str, /) -> NameSpace:
    assert is_namespace(s)
    main = "minecraft"
    directory = []
    if s.partition(":")[1]:
        main = s.partition(":")[0]
        s = s.partition(":")[2]
    while s.partition("/")[1]:
        directory.append(s.partition("/")[0])
        s = s.partition("/")[2]
    sub = s.split(".")
    return NameSpace._make([main, directory, sub])


__all__ = "NameSpace", "is_namespace", "get_namespace"
