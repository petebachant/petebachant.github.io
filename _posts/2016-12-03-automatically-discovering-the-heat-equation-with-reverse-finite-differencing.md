---
title: "Automatically 'discovering' the heat equation with reverse finite differencing"
date: 2016-12-03
layout: post
comments: true
---

<a href="https://zenodo.org/badge/latestdoi/72929661"><img src="https://zenodo.org/badge/72929661.svg" alt="DOI"></a>

To date, most higher level physical knowledge has been derived from simpler first principles. However, these techniques have still not given a fully predictive understanding of turbulent flow. We have the exact deterministic governing equations (Navier--Stokes), but can't solve them for most useful cases. As such, it could be of interest to find a different quantity, other than momentum, for which we can find some conservation or transport equation, that will be feasible to solve, i.e., does not have the scale resolution requirements of a direct numerical simulation. Or, perhaps, we may want to follow one of the current turbulence modeling paradigms but uncover an equation to relate the unresolved to the resolved information, e.g., Reynolds stresses to mean velocity.

As a first step towards this goal, we want to see if the process of deriving physical laws or theories can be automated. For example, can we posit a generic homogeneous PDE, such as
$$
A \frac{\partial u}{\partial t} = B \frac{\partial u}{\partial x} + C \frac{\partial^2 u}{\partial x^2} ...,
$$
solve for the coefficients $[A, B, C,...]$, eliminate the terms for which coefficients are small, then be left with an analytically or computationally feasible equation?

For a first example, here we look at the 1-D heat or diffusion equation, for which an analytical solution can be obtained.
We will use two terms we know apply (the time derivative $u_t$ and second spatial derivative $u_xx$), and three that don't (first order linear transport $u_x$, nonlinear advection $uu_x$, and a constant offset $E$):

$$
A u_t = B u_x + C u_{xx} + D uu_x + E,
$$

with the initial condition
$$
u(x, 0) = \sin(4\pi x).
$$

We will use the analytical solution as our dataset on which we want to uncover the governing PDE:
$$
u(x,t) = \sin(4\pi x) e^{-16\pi^2 \nu t},
$$

from which our method should be able to determine that $A=1$, $C=\nu = 0.1$, and $B=D=E=0$.

First, we will use the analytical solution and analytical partial derivatives.


```python
import numpy as np
from numpy.testing import assert_almost_equal

# Specify diffusion coefficient
nu = 0.1


def analytical_soln(xmax=1.0, tmax=0.2, nx=1000, nt=1000):
    """Compute analytical solution."""
    x = np.linspace(0, xmax, num=nx)
    t = np.linspace(0, tmax, num=nt)
    u = np.zeros((len(t), len(x))) # rows are timesteps
    for n, t_ind in enumerate(t):
        u[n, :] = np.sin(4*np.pi*x)*np.exp(-16*np.pi**2*nu*t_ind)
    return u, x, t


u, x, t = analytical_soln()

# Create vectors for analytical partial derivatives
u_t = np.zeros(u.shape)
u_x = np.zeros(u.shape)
u_xx = np.zeros(u.shape)

for n in range(len(t)):
    u_t[n, :] = -16*np.pi**2*nu*np.sin(4*np.pi*x)*np.exp(-16*np.pi**2*nu*t[n])
    u_x[n, :] = 4*np.pi*np.cos(4*np.pi*x)*np.exp(-16*np.pi**2*nu*t[n])
    u_xx[n, :] = -16*np.pi**2*np.sin(4*np.pi*x)*np.exp(-16*np.pi**2*nu*t[n])

# Compute the nonlinear convective term (that we know should have no effect)
uu_x = u*u_x

# Check to make sure some random point satisfies the PDE
i, j = 15, 21
assert_almost_equal(u_t[i, j] - nu*u_xx[i, j], 0.0)
```

Okay, so now that we have our data to work on, we need to form a system of equations $KM=0$ to solve for the coefficients $M$:

$$
\left[
\begin{array}{ccccc}
{u_t}_0 & -{u_x}_0 & -{u_{xx}}_0 & -{uu_x}_0 & -1 \\
{u_t}_1 & -{u_x}_1 & -{u_{xx}}_1 & -{uu_x}_1 & -1 \\
{u_t}_2 & -{u_x}_2 & -{u_{xx}}_2 & -{uu_x}_2 & -1 \\
{u_t}_3 & -{u_x}_3 & -{u_{xx}}_3 & -{uu_x}_3 & -1 \\
{u_t}_4 & -{u_x}_4 & -{u_{xx}}_4 & -{uu_x}_4 & -1
\end{array}
\right]
\left[
\begin{array}{c}
A \\
B \\
C \\
D \\
E
\end{array}
\right] =
\left[
\begin{array}{c}
0 \\
0 \\
0 \\
0 \\
0
\end{array}
\right],
$$

for which each of the subscript indices $[0...4]$ corresponds to random points in space and time.


```python
# Create K matrix from the input data using random indices

nterms = 5 # total number of terms in the equation
ni, nj = u.shape
K = np.zeros((5, 5))

# Pick data from different times and locations for each row

for n in range(nterms):
    i = int(np.random.rand()*(ni - 1)) # time index
    j = int(np.random.rand()*(nj - 1)) # space index
    K[n, 0] = u_t[i, j]
    K[n, 1] = -u_x[i, j]
    K[n, 2] = -u_xx[i, j]
    K[n, 3] = -uu_x[i, j]
    K[n, 4] = -1.0


# We can't solve this matrix because it's singular, but we can try singular value decomposition
# I found this solution somewhere on Stack Overflow but can't find the URL now; sorry!

def null(A, eps=1e-15):
    """Find the null space of a matrix using singular value decomposition."""
    u, s, vh = np.linalg.svd(A)
    null_space = np.compress(s <= eps, vh, axis=0)
    return null_space.T


M = null(K, eps=1e-5)
coeffs = (M.T/M[0])[0]
for letter, coeff in zip("ABCDE", coeffs):
    print(letter, "=", np.round(coeff, decimals=5))
```

    A = 1.0
    B = 0.0
    C = 0.1
    D = -0.0
    E = 0.0


This method tells us that our data fits the equation

$$
u_t = 0u_x + 0.1u_{xx} + 0uu_x + 0,
$$

or

$$
u_t = \nu u_{xx},
$$

which is what we expected!

## Would this method work with experimental data?

So far, we've been using analytical partial derivatives from the exact solution. However, imagine we had various temperature probes on a physical model of a heat conducting system, which were sampled in time. We can sample the analytical solution at specified points, but add some Gaussian noise to approximate a sensor in the real world. Can we still unveil the heat equation with this added noise? To compute the derivatives, we'll use finite differences, which would imply we may need to put multiple probes close to each other at a given location to resolve the spatial derivatives, but for now we will assume we can specify our spatial and temporal resolution.


```python
# Create a helper function compute derivatives with the finite difference method

def diff(dept_var, indept_var, index=None, n_deriv=1):
    """Compute the derivative of the dependent variable w.r.t. the independent at the
    specified array index. Uses NumPy's `gradient` function, which uses second order
    central differences if possible, and can use second order forward or backward
    differences. Input values must be evenly spaced.

    Parameters
    ----------
    dept_var : array of floats
    indept_var : array of floats
    index : int
        Index at which to return the numerical derivative
    n_deriv : int
        Order of the derivative (not the numerical scheme)
    """
    # Rename input variables
    u = dept_var.copy()
    x = indept_var.copy()
    dx = x[1] - x[0]
    for n in range(n_deriv):
        dudx = np.gradient(u, dx, edge_order=2)
        u = dudx.copy()
    if index is not None:
        return dudx[index]
    else:
        return dudx


# Test this with a sine
x = np.linspace(0, 6.28, num=1000)
u = np.sin(x)
dudx = diff(u, x)
d2udx2 = diff(u, x, n_deriv=2)
assert_almost_equal(dudx, np.cos(x), decimal=5)
assert_almost_equal(d2udx2, -u, decimal=2)


def detect_coeffs(noise_amplitude=0.0):
    """Detect coefficients from analytical solution."""
    u, x, t = analytical_soln(nx=500, nt=500)
    # Add Gaussian noise to u
    u += np.random.randn(*u.shape) * noise_amplitude
    nterms = 5
    ni, nj = u.shape
    K = np.zeros((5, 5))
    for n in range(nterms):
        i = int(np.random.rand()*(ni - 1))
        j = int(np.random.rand()*(nj - 1))
        u_t = diff(u[:, j], t, index=i)
        u_x = diff(u[i, :], x, index=j)
        u_xx = diff(u[i, :], x, index=j, n_deriv=2)
        uu_x = u[i, j] * u_x
        K[n, 0] = u_t
        K[n, 1] = -u_x
        K[n, 2] = -u_xx
        K[n, 3] = -uu_x
        K[n, 4] = -1.0
    M = null(K, eps=1e-3)
    coeffs = (M.T/M[0])[0]
    for letter, coeff in zip("ABCDE", coeffs):
        print(letter, "=", np.round(coeff, decimals=3))


for noise_level in np.logspace(-10, -6, num=5):
    print("Coefficients for noise amplitude:", noise_level)
    try:
        detect_coeffs(noise_amplitude=noise_level)
    except ValueError:
        print("FAILED")
    print("")
```

    Coefficients for noise amplitude: 1e-10
    A = 1.0
    B = -0.0
    C = 0.1
    D = 0.0
    E = -0.0

    Coefficients for noise amplitude: 1e-09
    A = 1.0
    B = 0.0
    C = 0.1
    D = -0.0
    E = -0.0

    Coefficients for noise amplitude: 1e-08
    A = 1.0
    B = 0.0
    C = 0.1
    D = -0.001
    E = 0.0

    Coefficients for noise amplitude: 1e-07
    FAILED

    Coefficients for noise amplitude: 1e-06
    FAILED



We see that the method breaks down for noise with amplitude on the order of $1 \times 10^{-6}$, which is not great considering the amplitude of the initial condition is $O(1)$, but not too bad for a first start. Some filtering or more stable finite difference schemes might be necessary to apply this technique to real experimental data.

## Conclusions and future work

A simple algorithm was developed to detect the governing PDE from a given analytical solution. The algorithm uses "reverse" finite differences to sample the solution at random points, assembles a linear system of equations, and solves these using singular value decomposition to find the constant, homogeneous coefficients associated with terms of interest. Using an analytical solution to the heat equation, the algorithm successfully identified that the system's evolution was only affected by diffusion, whereas additional terms for convection and first order wave propagation were shown to be insignificant.

When subjected to Gaussian noise (to simulate experimental data), the algorithm failed for noise amplitudes roughly 6 orders of magnitude smaller than the amplitude of the initial condition. This shows an important weakness for looking at noisy data or higher derivatives, and may necessitate filtering or more robust linear solution techniques.

The example presented here is admittedly trivial. However, it could be used to develop new theories or models for more complex systems, e.g., turbulent flow. For example, we may take the Reynolds-averaged Navier--Stokes equations:
$$
\frac{\partial U_i}{\partial t} + U_j \frac{\partial U_i}{\partial x_j}
= -\frac{1}{\rho}\frac{\partial P}{\partial x_i} + \nu \frac{\partial^2 U_i}{\partial x_j^2}
  -\frac{\partial}{\partial x_j} \overline{u_i^\prime u_j^\prime},
$$
and attempt to solve for the Reynolds stresses (the last term on the RHS, a.k.a., the "closure problem") in terms of many arbitrary combinations of the mean velocity and/or pressure, and their partial derivatives---where numerical values for all could be computed from a direct numerical simulation (DNS) of the exact Navier--Stokes equations.

Most likely, resulting equations would not be theoretically correct, and the dimensions of their coefficients may not be able to be formulated in terms of physical parameters, e.g., viscosity. However, the equations would still satisfy the exact equations within some tolerance, and could prove to be useful models that would not have been derived via conventional analytical or phenomenological means.
