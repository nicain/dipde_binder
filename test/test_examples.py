import os
import subprocess
import tempfile
import nbformat
import inspect
import sys
import dipde
import git

examples_dir = os.path.join(os.path.dirname(__file__), '../')

# Check that dipde is set to correct branch
dipde_git_repo_location = os.path.join((os.path.dirname(inspect.getfile(dipde))), '../')
dipde_git_repo = git.Repo(dipde_git_repo_location)
dipde_branch_list = [line[17:29] for line  in open(os.path.join(examples_dir, 'Dockerfile')).readlines() if line[:16] == 'ARG DIPDE_BRANCH']
assert len(dipde_branch_list) == 1
dipde_branch_name = dipde_branch_list[0]
assert dipde_git_repo.active_branch.name == dipde_branch_name



def _notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ['jupyter', "nbconvert", "--to", "notebook", "--execute",
          "--ExecutePreprocessor.timeout=60",
          "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
                     for output in cell["outputs"]\
                     if output.output_type == "error"]

    return nb, errors

def _test_file_name(file_name):
    nb, errors = _notebook_run(os.path.join(examples_dir, file_name))
    assert errors == []

def test_tutorial(): _test_file_name('tutorial.ipynb')

def test_singlepop(): _test_file_name('singlepop.ipynb')

def test_singlepop_live(): _test_file_name('singlepop_live.ipynb')

def test_recurrent_live(): _test_file_name('recurrent_live.ipynb')




# def test_singlepop_live():
#     nb, errors = _notebook_run(os.path.join(examples_dir, 'singlepop_live.ipynb'))
#     assert errors == []


if __name__ == "__main__":

    fset = [obj for name, obj in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(obj) if name[:5] == 'test_']

    for test_function in fset:
        test_function()

