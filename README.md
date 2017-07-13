# Simple data science website using Jupyter notebooks

This repository is an adaptable template for publishing websites from
[Jupyter interactive notebooks](https://jupyter.org).

*Please clone and adapt this repository for your own project.*

View the demo project website
[here](https://stephenslab.github.io/ipynb-website).

This website template is based on
[jnbinder](https://github.com/gaow/jnbinder).

## License

Copyright (c) 2017, Peter Carbonetto & Gao Wang.

All source code and software in this repository are made available
under the terms of the [MIT license](https://opensource.org/licenses/MIT).

## Quick Start

To start your own Jupyter-notebook-based research website, please
follow these steps. *Note:* These instructions assume that you are
managing your project files inside a git repository, but this is not
strictly necessary; if you prefer not to do this, simply skip the git
commands in the steps below. (For a quick introduction to git, see
[here](https://swcarpentry.github.io/git-novice) or
[here](https://doi.org/10.1371/journal.pcbi.1004668 ).)

1. Install Python >= 3.5 and Jupyter. The recommended way to do this
is to download and install
[Anaconda 3](https://www.continuum.io/anaconda-overview). Note that
Python >= 3.5 comes with [pip](https://pip.pypa.io).

2. *Note of caution:* If you already have Jupyter installed for
Python 2.x (e.g., Anaconda 2), then you will need to be careful that
you install SoS for Python 3.x in the next step. To make sure, before
running the commands below, run `pip --version`.)

3. Install [SoS](https://github.com/vatlab/SOS) ("Script of Scripts")
for Python 3.x:

   ```bash
   pip install sos
   ```

   Note that you may need to include the `--user` flag if you do not
   have administrative privileges on the computer.

4. [Download](https://github.com/stephenslab/ipynb-website/archive/master.zip),
or clone the latest version of this repository from Github.

5. Install [git](https://git-scm.com/downloads). 

6. Create a new git repository (`git init ...`), copy all the files
from this repository to the new repository folder, then add these
files to the new repository (using `git add ...` and `git commit
-a`). Alternatively, create a new folder (`mkdir ...`) and add copy
the files to this new folder.

7. Inside your new project directory, re-generate all the webpages
using the SoS release script:

   ```bash
   sos-runner ./release -s force
   ```

8. View the newly generated home page `docs/index.html` in your
favorite Web browser.

9. You are now ready to adapt the Jupyter-notebook-based website for
   your own project:

   + Modify the website settings by editing `config.yml`. See the
     comments in this file for more detailed instructions.

   + Copy, rename or delete the notebooks in the "analysis", "setup"
     and "license" directories.

   + Edit the notebooks interactively in Jupyter.

   + After you are satisfied with your changes, re-build the modified
     webpages by running `sos-runner release`, or use `sos-runner
     release -s force` to re-build all the webpages, then commit your
     changes to the git repository.

   + Push your changes (`git remote add ...` and `git push ...`) to
     your favourite git hosting website ([Github](http://github.com),
     [GitLab](http://gitlab.com), [Bitbucket](https://bitbucket.org),
     *etc.*).

## More setup details

+ The [jnbinder](https://github.com/gaow/jnbinder) tool is used to
  generate the webpages from the Jupyter notebooks. To retrieve the
  most up-to-date version of jnbinder for your project, run this
  command in the main directory of your repository:

  ```bash
  sos-runner ./release.sos upgrade-jnbinder
  ```

## Tips for adapting this repository for your project

+ There are many things that can be done; we will only describe here
some of the simpler modifications that can be made.

+ [Link](https://bootswatch.com) to gallery of Bootstrap themes.

+ Note that not all themes will show up consistently due to conflicts
  between CSS files.

## Credits

**ipynb-website** was developed by:

Peter Carbonetto and Gao Wang<br>
Dept. of Human Genetics<br>
University of Chicago<br>

[John Blischak](https://github.com/jdblischak),
[Matthew Stephens](http://stephenslab.uchicago.edu) and others have
also contributed to the development of this software.
