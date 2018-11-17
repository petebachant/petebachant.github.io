---
layout: post
title: "Updating OpenFOAM case files for 3.0.x"
date: "2015-11-30"
description: ""
category:
tags: []
---

[OpenFOAM](https://openfoam.org) recently released version 3.0.0 of their
open-source CFD toolbox. With an incremented major version number some
non-backwards-compatible changes are expected. This post describes the ones I've
run into thus far, and how I've addressed them
([example](https://github.com/petebachant/UNH-RVAT-turbinesFoam/commit/b5ccda0b0c139e1f5d45b2802f25f719def94002)).

`constant/turbulenceProperties` now contains all turbulence modeling parameters,
rather than separating these into `RASProperties` and/or `LESProperties` files.
To address this, I simply removed `Model` from the `simulationType` entry, and
include the "legacy" properties file in the appropriate subdictionary.

Old:

```c++
simulationType      RASModel;
```

New:

```c++
simulationType      RAS;

RAS
{
    #include "RASProperties"
}
```

Some `fvOptions` are now derived from a new `cellSetOption` class, which
apparently expects the `selectionMode` and `cellSet` entries to be inside the
option coefficients, rather than in the top level subdictionary. The `fvOptions`
file's default location has also been moved from `system` to `constant`, though
cases will still run with the `fvOptions` in `system`.

Lastly, the divergence scheme keyword for the effective viscous stress has been
renamed. To fix this, simply change `div((nuEff*dev(T(grad(U)))))` to
`div((nuEff*dev2(T(grad(U)))))` in `system/fvSchemes.divSchemes`.

There are surely more changes to be made, but these are the ones I found
absolutely necessary to get cases running again. Please leave a comment if you
encounter any additional snags migrating your own.
