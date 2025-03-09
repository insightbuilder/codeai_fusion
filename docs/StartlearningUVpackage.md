# UV package & Commands

- [x] Make a list of commands and what they do

  - [x] tested uv install python
    <aside>
    💡

    uv python find > lead to surprise of finding
    3.9 to 3.11 all of which are under

    /home/uberdev/.local/share/uv/python/

    uv python install 3.9 > installs in above path

    uv python uninstall 3.9 > deletes it from the
    path

    </aside>

    - [x] tested uv run

    <aside>
    💡

    uv run [example.py](http://example.py) > exec
    the script

    uv run —no-project
    [script.py](http://script.py) > ignores the
    pjt environment, doesn’t take your OS environ
    also

    </aside>

    - [x] uv add tested

    <aside>
    💡

    uv add —srcipt [example.py](http://example.py)
    ‘pandas’ > this adds the ‘pandas’ on top of
    the script.py

    uv add pandas > adds pandas to pyproject.toml

    </aside>

    - [x] tested uv lock

    <aside>
    💡

    uv lock > just uv.lock in the folder

    uv lock —script
    [script.py](http://script.py) > has to add
    script.py.lock (ensure uv self update is
    executed)

    </aside>

    - [x] tested uv tree

    <aside>
    💡

    uv tree > provides dep tree on the project

    uv tree —script
    [script.py](http://script.py) > provide dep
    tree on the script alone

    </aside>

    - [x] Understand project structure

    <aside>
    💡

    uv init > creates the project structure

    uv sync > updates the .venv with the packages,
    however pip freeze shows all the packages in
    the system, which is not correct.

    - When executed ‘python script.py’, if the
    package is not in pyproject.toml then it
    throws error
    </aside>
    - [ ] Understand how distribution works

    Python projects are typically distributed as
    both source distributions (sdists) and binary
    distributions (wheels). The former is
    typically a `.tar.gz` or `.zip` file
    containing the project's source code along
    with some additional metadata, while the
    latter is a `.whl` file containing pre-built
    artifacts that can be installed directly.

    <aside>
    💡

    uv build —sdist > builds tar.gz build files

    uv build —wheel > build binary .whl file

    uv build > gives both into ./dist folder

    </aside>

    - [ ] Understandin entry points

    https://docs.astral.sh/uv/concepts/projects/config/#entry-points

    <aside>
    💡

    [project.scripts]

    hello = "example:hello"

    uv run hello > will execute the hello()
    function

    </aside>

    > The above did not work, then a bit of
    > digging found below

    https://docs.astral.sh/uv/concepts/projects/init/#applications

    The projects are created in a fashion to be
    packaged or to be used as app

    <aside>
    💡

    uv init —app testapp

    which creates the tree like below

    testapp ├── [main.py](http://main.py/) ├──
    pyproject.toml └──
    [README.md](http://readme.md/)

    </aside>

    When you want the package like those you see
    in mcp servers

    <aside>
    💡

    uv init —package testpkg

    testpkg/ ├── pyproject.toml ├──
    [README.md](http://readme.md/) └── src └──
    testpkg └── **init**.py

    </aside>

With the above understanding pushing to the pypi
is for another day altogether

https://packaging.python.org/en/latest/guides/section-build-and-publish/
