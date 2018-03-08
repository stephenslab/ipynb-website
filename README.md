# ipynb website: Simple data science website using Jupyter notebooks

This repository is an adaptable framework for publishing websites from
[Jupyter interactive notebooks](https://jupyter.org).

*Please copy and adapt this repository for your own project.*

View the demo project website
[here](https://stephenslab.github.io/ipynb-website).

If you find any problems, or would like to suggest new features,
please open an
[Issue](https://github.com/stephenslab/ipynb-website/issues). We also
encourage community contributions, e.g., by forking the repository,
making your suggested changes, and issuing a pull request.

## License

Copyright (c) 2017, Peter Carbonetto & Gao Wang.

All source code and software in this repository are made available
under the terms of the [MIT license](https://opensource.org/licenses/MIT).

## Quick Start

To start your own Jupyter-notebook-based research website, please
follow these steps.

*Note:* These instructions assume that you are managing your project
files inside a git repository, but this is not strictly necessary; if
you prefer not to do this, skip the git commands in the steps
below. (For an introduction to git, see
[here](https://swcarpentry.github.io/git-novice) or
[here](https://doi.org/10.1371/journal.pcbi.1004668).)

1. Install Python >= 3.6 and Jupyter. The recommended way to do this
   is to download and install
   [Anaconda 3](https://www.continuum.io/anaconda-overview). Note that
   Python >= 3.6 comes with [pip](https://pip.pypa.io), so you should
   not need to install it separately.

2. **Please also note:** If you already have Jupyter installed for
   Python 2.x (e.g., Anaconda 2), or any other version of Python, then
   in the next step you will need to be careful that you install SoS
   for the same Python >= 3.6. In other words, you need Jupyter and
   SoS to be installed with the same Python >= 3.6. Run `pip
   --version` to make sure.)
   
   ```bash
   pip --version
   # pip 9.0.1 from /Users/pcarbo/anaconda3/lib/python3.6/site-packages (python 3.6)
   ```

3. Install [SoS](https://github.com/vatlab/SOS) ("Script of Scripts")
   for Python 3.6:

   ```bash
   pip install sos-essentials
   ```

   Note that you may need to
   include the `--user` flag if you do not have administrative
   privileges on the computer.

   If you get a warning, "Could not find .egg-info directory in
   install record for sos...", please ignore it.

4. Install [git](https://git-scm.com/downloads). 

5. At this point, you should have all the software you need to build
   webpages from the Jupyter notebooks. Please double-check this. For
   example, this is the setup on my MacBook Air with macOS 10.12.5:

   ```bash
   which python; python --version
   # /Users/pcarbo/anaconda3/bin/python
   # Python 3.6.1 :: Anaconda 4.4.0 (x86_64)
   which jupyter; jupyter --version
   # /Users/pcarbo/anaconda3/bin/jupyter
   # 4.3.0
   which sos; sos --version
   # /Users/pcarbo/anaconda3/bin/sos
   # sos 0.9.10.16 for Python 3.6.1
   which git; git --version
   $ which git; git --version
   # /usr/bin/git
   # git version 2.9.3 (Apple Git-75)
   ```

6. Make a personal copy of this repository:

   + Download the [latest release](https://github.com/stephenslab/ipynb-website/releases/tag/v0.9.3) of this repository from Github.

   + Create a new git repository (`git init ...`), copy all the files
     from this repository to the new repository folder.

   + Change the working directory to the new repository folder and
     commit these files to the new repository:

     ```bash
     git add ./
     git commit
     ```

   + Alternatively, if you are not using git, create a new folder
     (`mkdir ...`) and add copy the files to this new folder.

7. Inside your new project directory, clean up and then re-generate
   all the webpages using the SoS release script:

   ```bash
   sos run release.sos clean
   sos run release.sos -s force
   ```

   Or, simply:

   ```bash
   ./release.sos clean
   ./release.sos -s force
   ```
   if `release.sos` is granted executable permission.

   **Important note:** Building the webpages from the Jupyter
   notebooks does not actually run the code in the notebooks. If you
   would like to run the code prior to generating the webpages, this
   must be done interactively in Jupyter, or from the command line
   using `jupyter nbconvert --execute`.

   All the webpages are created and stored in the "docs"
   directory. This is convenient for git repositories hosted on
   Github because 
   [Github Pages](https://help.github.com/categories/github-pages-basics)
   can be configured to publish the webpages from the "docs" folder.

8. View the newly generated home page `docs/index.html` in your
   favorite Web browser.

9. If you would like to upload your new git repository to a git
   hosting website, do the following:

   + Create a new empty repository on tour favorite git hosting
     website (e.g., [Github](http://github.com),
     [GitLab](http://gitlab.com), [Bitbucket](https://bitbucket.org).
     Currently, only Github has been tested; other sites may work as
     well, but may not support all the website publishing features.

   + Determine the URL of the host repository, and add this URL to the
     repository on your computer with `git remote add origin ...`.

   + Upload to the host repository with `git push origin master`.

   + Configure the repository settings to publish the webpages; e.g.,
     using [Github Pages](https://help.github.com/categories/github-pages-basics)).

10. You are now ready to adapt the Jupyter-notebook-based website for
   your own project:

   + Modify the website settings by editing `config.yml`. See the
     comments in this file for more detailed instructions.

   + Copy, rename or delete the notebooks in the "analysis", "setup"
     and "license" directories.

   + Edit the notebooks interactively in Jupyter.

   + After you are satisfied with your changes, re-build the modified
     webpages by running `sos run release.sos`, or use
     `sos run release.sos -s force` to re-build all the webpages,
     then commit your changes to the git repository.

## More setup details

+ Whenever you make global changes to the website (e.g., you change
  the Boostrap theme in `config.yml`), use the `-s force` option to force
  updates to all the webpages, not just the ones that have been modified.

+ The website is built by [`jnbinder`](https://github.com/vatlab/jnbinder)
  which does not make any formal releases. This repo releases / ships with
  its latest stable version.
  
  To upgrade `jnbinder` to its latest, type:
  ```
  ./release.sos upgrade-jnbinder
  ```
  
  If you are on version < 0.9.2 you need to run this command twice to upgrade:
  ```
   ./release.sos upgrade-jnbinder  
   ./release.sos upgrade-jnbinder
  ```

## Tips for adapting this framework for your project

+ You can add option `-j` to the command if you want to control the 
  number of parallel processes that generate the notebook. For example
  `-j 8` uses 8 processes.

+ The `include_dir` setting in `config.yml` specifies the project
  subdirectories containing Jupyter notebooks to render into
  webpages. If no `index.ipynb` file is provided within a given
  subdirectory, an index will automatically be generated that lists
  links to all notebooks under that directory.

+ There is also the option of adding a table of contents to each
  notebook by setting `notebook_toc: True` in `config.yml`.

+ For the table of contents and the automatically generated index, it
  is recommended that the notebooks have descriptive names; e.g.,
  `Plot_station_map.ipynb`. All underscores are automatically treated
  as spaces, so `Plot_station_map.ipynb` will show as "Plot station
  map" in the index file and table of contents.

+ So far, only the Cerulean, Flatly and Readable Bootstrap themes have
  been adapted and tested for this framework. It is possible to select
  other themes (see [here](https://bootswatch.com) for a larger
  collection), although they may not work as well. Also note that
  there may be style conflicts or inconsistencies in the included CSS
  files; please report these style conflicts by posting an
  [Issue](https://github.com/stephenslab/ipynb-website/issues).

+ For more website customization details, please refer to the comments
  in the [config.yml](config.yml) file.

## Credits

**ipynb website** was developed by:

Peter Carbonetto and Gao Wang<br>
Dept. of Human Genetics<br>
University of Chicago<br>

[John Blischak](https://github.com/jdblischak),
[Matthew Stephens](http://stephenslab.uchicago.edu) and others have
also contributed to the development of this software.
