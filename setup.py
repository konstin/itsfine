"""
                                       ` )
                              (         (
                               )      (
                             )          )
                            (          ( ,
                           _ _)_      .-Y.
                .--._ _.--'.',T.\_.--' (_)`.
              .'_.   `  _.'  `-'    __._.--;
             /.'  `.  -'     ___.--' ,--.  :       o       ,-. _
            : |  xX|       ,'  .-'`.(   |  '      (   o  ,' .-' `,
           :  `.  .'    ._'-,  \   | \  ||/        `.{  / .'    :
          .;    `'    ,',\|\|   \  |  `.;'     .__(()`./.'  _.-'
          ;           |   ` `    \.'|\\ :      ``.-. _ '_.-'
         .'           ` /|,         `|\\ \        -'' \  \
         :             \`/|,-.       `|\\ :         ,-'| `-.
         :        _     \`/  |   _   .^.'\ \          -'> \_
         `;      --`-.   \`._| ,' \  |  \ : \           )`.\`-
          :.      .---\   \   ,'   | '   \ : .          `  `.\_,/
           :.        __\   `. :    | `-.-',  :               `-'
           `:.     -'   `.   `.`---'__.--'  /
            `:         __.\    `---'      _'
             `:.     -'    `.       __.--'
              `:.          __`--.--'\
         -bf-  `:.      --'     __   `.
"""
import tarfile
from argparse import ArgumentParser
from base64 import urlsafe_b64encode
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

NAME = "itsfine"
VERSION = "0.1.0"

dist_info = f"{NAME}-{VERSION}.dist-info"

# very ugly not-using-an-email-writer solution
metadata = f"""
Metadata-Version: 2.1
Name: {NAME}
Version: {VERSION}
Description-Content-Type: text/markdown


{Path('Readme.md').read_text()}
""".strip()

wheel_wheel = f"""
Wheel-Version: 1.0
Generator: {NAME} ({VERSION})
Root-Is-Purelib: true
Tag: py3-none-any
""".strip()

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest="subcommand")
egg_info_parser = subparsers.add_parser("egg_info")
egg_info_parser.add_argument("--egg-base")
bdist_wheel_parser = subparsers.add_parser("bdist_wheel")
bdist_wheel_parser.add_argument("-d")
_sdist_parser = subparsers.add_parser("sdist")


def record_hash(data: str):
    """https://packaging.python.org/en/latest/specifications/recording-installed-packages/#the-record-file"""
    hashed = sha256(data.encode()).digest()
    return "sha256=" + urlsafe_b64encode(hashed).decode().rstrip("=")


args = parser.parse_args()
if args.subcommand == "egg_info":
    egg_info_dir = Path(args.egg_base).joinpath(f"{NAME}-{VERSION}-py3.egg-info")
    egg_info_dir.mkdir()
    egg_info_dir.joinpath("PKG-INFO").write_text(metadata)
elif args.subcommand == "bdist_wheel":
    whl_file = Path(args.d).joinpath(f"{NAME}-{VERSION}-py3-none-any.whl")
    with ZipFile(whl_file, "w") as wheel:
        wheel.write("itsfine.py")

        wheel.writestr(
            f"{dist_info}/WHEEL",
            wheel_wheel,
        )
        wheel.writestr(f"{NAME}-{VERSION}.dist-info/METADATA", metadata)
        record = f"""
{dist_info}/METADATA,{record_hash(metadata)},{len(metadata)}
{dist_info}/WHEEL,{record_hash(wheel_wheel)},{len(wheel_wheel)}
{dist_info}/RECORD,,
itsfine.py,{record_hash(Path('itsfine.py').read_text())},{len(Path('itsfine.py').read_text())}
        """.strip()
        wheel.writestr(f"{NAME}-{VERSION}.dist-info/RECORD", "")
elif args.subcommand == "sdist":
    with tarfile.open(f"{NAME}-{VERSION}.tar.gz", "w:gz") as sdist:
        tarinfo = tarfile.TarInfo(f"{NAME}-{VERSION}/PKG-INFO")
        tarinfo.size = len(metadata)
        sdist.addfile(tarinfo, BytesIO(metadata.encode()))
        sdist.add("setup.py", f"{NAME}-{VERSION}/setup.py")
        sdist.add("itsfine.py", f"{NAME}-{VERSION}/itsfine.py")
        sdist.add("Readme.md", f"{NAME}-{VERSION}/Readme.md")
