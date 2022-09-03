import sys
import sysconfig
import types
from importlib.abc import Loader
from importlib.machinery import PathFinder, ModuleSpec
from pathlib import Path
from typing import Iterable, Any, Dict, Sequence, Optional, Union


class Fix(PathFinder):
    @classmethod
    def find_spec(
        cls,
        fullname: str,
        path: Optional[Sequence[Union[bytes, str]]] = ...,
        target: Optional[types.ModuleType] = ...,
    ) -> Optional[ModuleSpec]:
        return ModuleSpec(fullname, BeNice())

    @classmethod
    def lgtm(cls):
        if isinstance(sys.meta_path[-1], Fix):
            sys.meta_path[-1] = Fix()
        else:
            sys.meta_path.append(Fix())

    @classmethod
    def for_good(cls):
        site_packages = Path(sysconfig.get_paths()["purelib"])
        site_packages.joinpath("itsfine.py").write_text(Path(__file__).read_text())
        site_packages.joinpath("itsfine.pth").write_text("import itsfine")


class BeNice(Loader):
    def load_module(self, fullname: str) -> types.ModuleType:
        # noinspection PyTypeChecker
        return ItsFine()

    def module_repr(self, module: types.ModuleType) -> str:
        return ""

    def create_module(self, spec: ModuleSpec) -> types.ModuleType:
        # noinspection PyTypeChecker
        return ItsFine()

    def exec_module(self, module: types.ModuleType) -> None:
        pass


class ItsFine:
    attrs: Dict[str, Any] = dict()

    def __init__(self, *_args, **kwargs) -> None:
        self.attrs = kwargs

    def __setattr__(self, name: str, value: Any) -> None:
        self.attrs[name] = value

    def __getattr__(self, item):
        return self.attrs.get(item) or ItsFine()

    def __getitem__(self, item):
        return self.attrs.get(item) or ItsFine()

    def __hash__(self) -> int:
        return hash(id(self))

    def __eq__(self, o: object) -> bool:
        return False

    def __str__(self) -> str:
        return "All good"

    def __repr__(self) -> str:
        attrs = ", ".join(
            repr(k) + ": " + str(v)
            for k, v in self.attrs.items()
            if not (type(k) == str and k in ["__spec__", "attrs"])
        )
        return f"All good {{{attrs}}}"

    def __delattr__(self, name: str) -> None:
        if name in self.attrs:
            del self.attrs[name]

    def __sizeof__(self) -> int:
        return 0

    def __reduce__(self) -> str:
        return ""

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

    def __dir__(self) -> Iterable[str]:
        return []

    def __call__(self, *args, **kwargs) -> "ItsFine":
        return ItsFine()

    def __iter__(self):
        yield


Fix.lgtm()
