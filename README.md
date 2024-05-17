# Lesson Builder

Deploy a directory of lesson files to a static website with vuepress. 

## Creating a lesson plan

TBD, but here is what a lesson plan directory looks like:

```
├── about.md
├── assets
│   ├── Flag.png
│   └── word-logo.png
├── config.yml
├── index.md
├── intro.md
├── lesson-plan.yaml
├── lesson1.md
└── lesson2.md
```


## Setup and run 

### Install the lesson builder program and vuepress

Install the lesson plan program 

Install vuepress, [see these instructions for details](https://vuepress.vuejs.org/guide/getting-started.html). 
in this example, we will be using `yarn` rather than `npm` to install vuepress.

If you are developing locally:

```bash 
python -mvenv .venv
source .venv/bin/activate
pip install -e git+https://github.com/league-infrastructure/lesson-builder.git#egg=lesson-builder
```


### Prepare a lesson repo

First, create a new repo and clone it. Then create a new vuepress project in 
the Git repo. 

If you want to deploy to github pages with `jtl deploy`, the `doc` directory
( which is the default for `yarn create vuepress-site`) must be in a repo that 
has an origin at Github. If you aren't going to deploy -- for example, if you
just want to develop locally -- they you can create the vuepress site anywhere.

You can use JTL to create the site, or you can use the vuepress cli. 

```bash
jtl installvp
# Or
yarn create vuepress-site && (cd docs && yarn install)
```
You can also just [use the LevelX repo template](https://github.com/league-curriculum/LevelX.git), which has the `docs` directory
already configured for vuepress. 

```bash


### Fetch source lessons and assignment

Get some lessons plans. You can get them from anywhere, or make a new one, but
in this example we will use the League lessons repo.We also need some 
assignments, so get those too. 

```bash
(mkdir -p lessons && cd lessons &&  git clone https://github.com/league-python/PythonLessons.git )
(mkdir -p assignments && cd assignments && git clone https://github.com/League-central/python-modules.git)
```
Now we can build the lessons plans into a website. 

### Build and Serve

```bash
jtl -vv build -l lessons/PythonLessons/Level0/HourOfPython -d docs -a assignments
```
This shoudl result in lesson pages in `docs/src/lessons`

Run the development server. This assumes that the website is in the `docs` directory
    
```bash
./jtl serve
```

Deploy the site to github pages. Note that deploy will only work if the `docs` 
directory is in a github repo, and the repo is set to produce web pages from
the root of the gh-pages branch

```bash
./jtl deploy
```

NOTE: the `base:` key in the lessons plan `config.yml` file  must be the directory 
below the doman in the URL of your Github page, so if the repo name is 
'Level0', then `config.yaml` must have `base: /Level0/`. This will be set
autmatically ig you are in a github repo.

If you get a bunch of nasty errors during deploy, you may need to work around 
a budgwith OpenSSL and Node 17:

```bash
NODE_OPTIONS=--openssl-legacy-provider ./jtl deploy
```

### Configure Github pages

To setup Github pages, go to the settings tab of the repo, select the "Pages"
section. Set the source to the `gh-pages` branch, and the directory to `/`.

Wait about 5 minutes, and reload the settings page. When your site is ready, 
you will see a URL at the top of the page.

