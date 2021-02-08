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

1. Install [`docker`](https://docs.docker.com/get-docker/). Double-check
   after installation that `docker` is properly installed, by typing:

   ```bash
   docker run hello-world
   # Hello from Docker.
   # This message shows that your installation appears to be working correctly.
   ```

2. Pull the docker image that contains dependency software to generate the website:

   ```bash
   docker pull gaow/jnbinder
   ```

3. Make a personal copy of this repository:

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

4. Load the docker command to generate web-pages:

     ```bash
     source jnbinder_docker.sh
     ```
   After this, command prompt `jnbinder` should be available from your terminal.
   To verify, the following command should display the command interface:

    ```bash
    jnbinder -h
    ```

5. Inside your new project directory, clean up and then re-generate
   all the webpages using the SoS release script:

   ```bash
   jnbinder clean
   jnbinder -s force
   ```

   **Important note:** Building the webpages from the Jupyter
   notebooks does not actually run the code in the notebooks. In fact
   when executed from our `docker` image the computation of your notebook
   cannot be reproduced because the image does not have your computing environment
   under which the notebooks are developed. If you
   would like to run the code prior to generating the webpages, this
   must be done interactively in Jupyter, or from the command line
   using `jupyter nbconvert --execute`.

   All the webpages are created and stored in the "docs"
   directory. This is convenient for git repositories hosted on
   Github because 
   [Github Pages](https://help.github.com/categories/github-pages-basics)
   can be configured to publish the webpages from the "docs" folder.

6. View the newly generated home page `docs/index.html` in your
   favorite Web browser.

7. If you would like to upload your new git repository to a git
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

8. You are now ready to adapt the Jupyter-notebook-based website for
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

+ The website is built by [`jnbinder`](https://github.com/vatlab/jnbinder),
  distributed as docker image `gaow/jnbinder`. 
 
+ `jnbinder` does not make any formal releases. This repo releases / ships with
  its latest stable version.
  
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

`ipynb website` was developed by:

Peter Carbonetto and Gao Wang<br>
Dept. of Human Genetics<br>
University of Chicago<br>

[John Blischak](https://github.com/jdblischak),
[Matthew Stephens](http://stephenslab.uchicago.edu) and others have
also contributed to the development of this software.
