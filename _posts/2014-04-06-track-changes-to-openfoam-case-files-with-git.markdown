---
comments: true
date: 2014-04-06 23:17:49+00:00
layout: post
slug: track-changes-to-openfoam-case-files-with-git
title: Track changes to OpenFOAM case files with Git
tags:
- OpenFOAM
---

OpenFOAM cases are setup through a hierarchy of text files. [Git](http://git-scm.com) is made to track changes in code, which is text. This makes Git a perfect candidate for tracking changes in simulation settings and parameters. In this post I will not really give a full picture of Git's operation and capabilities, but detail how I use Git with OpenFOAM cases.



## Why track changes?


Setting up an OpenFOAM case can be a real headache, since there are so many settings and parameters to change. In my experience, it's nice to be able to keep track of settings that worked, in case I change something and the simulation starts crashing. With Git it's easy to "check out" the last configuration that worked, and also keep track of what changes had favorable or negative effects, using commit messages.



## Branches


Git has the ability to create branches, that is, versions of files that one may switch between and edit independently. This is useful for OpenFOAM cases, because sometimes it's desirable to run multiple cases with some parameter variation. For example, one might want to run one simulation with a low Reynolds number mesh and one with a high Reynolds number mesh. One may also want a case that can be run with different versions of OpenFOAM. By putting these files on different branches, one can switch between these two sets of parameters with a single `checkout` command.



## Sharing, collaboration, and storage


Git has become the most popular way to share and collaborate on code, through the website [GitHub](http://github.com). Using GitHub, another user may "fork" a set of case files, make some changes, and submit a "pull request" back to the main repository. This can be much more convenient than simply sharing zipped up folders of entire cases, as changes are more visible and reversible. Putting case files in a remote repository (private repositories can be hosted for free on [BitBucket](http://bitbucket.org)) is also a nice way to keep things backed up.



## How to set up a Git repository inside a case


The first important step is to create a `.gitignore` file in the top level case directory. Inside this file, you tell Git the file names or name patterns to not track. For OpenFOAM simulations, it is probably undesirable to track the actual simulation results, since this will grow the size of the repository significantly every time the simulation results are committed, i.e., all committed results would be saved for all time. My sample `.gitignore` file is shown below:




    *.gz
    log.*
    postProcessing
    *~
    processor*
    [0-9]*
    [0-9]*.[0-9]*
    !0.org
    constant/extendedFeatureEdgeMesh
    *.eMesh
    constant/polyMesh/*
    !constant/polyMesh/blockMeshDict
    constant/cellToRegion
    *.OpenFOAM




Note that I also ignore application logs, though these may be valuable troubleshooting tools. For example, one could checkout a previous commit, look at a log and compare with a newer version. However, these logs can get big, so I leave general performance information to the commit messages.

After a proper `.gitignore` file has been created, a repository can be initialized by running `git init` in a terminal (inside the top level case directory). Running `git status` will then list all the files that are not yet tracked. To add all of these files and create the first commit, run



    git add -A
    git commit -m "Initial commit message goes here"




Next, you may want to create a remote repository and set the remote location for the local repository. If using GitHub, create a new empty repository and follow [these instructions](https://help.github.com/articles/adding-a-remote) for pointing your repository there.

Next, "push" your local changes to the remote by running



    git push origin master



This pushes the changes to the master branch of the remote repo.

The case is now set to be tracked with Git. You can now continue on, and save your path towards, the perfect OpenFOAM case!
