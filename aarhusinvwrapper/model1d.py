import logging

import numpy

logger = logging.getLogger(__name__)
    

def thks2tops(thks):
    """Convert layer thicknesses to depths to layer tops."""
    tops = [0] + [numpy.sum(thks[:i]) for i in range(1, len(thks))]
    return numpy.asarray(tops)
    
    
def tops2thks(tops):
    """Convert depths to layer tops to layer thicknesses."""
    if tops[0] < 0:
        tops[0] = -1 * tops[0]
    thks = [tops[i] - tops[i-1] for i in range(1, len(tops))] + [0]
    return np.asarray(thks)
    
    
# def plot(tops, resxy, resyx, horiz_lines=True, z1=None, z0=1, lw=0.2,
#          res0=None, res1=None, mxy=None, myx=None,
#          depth_scale="log", modes="both",
#          fig=None, fign=None, ax=None, clf=False):
#     """Plot 1D model depth section.

#     Args:
#         - *tops, resxy, resyx*: 1d arrays
#         - *modes*: str, modes to plot, one of 'both', 'xy', 'yx'
#         - *depth_scale*: either 'log' or 'linear'
#         - *mxy, myx*: dictionaries for matplotlib.pyplot.plot() line styles etc.

#     """
#     if ax is None:
#         if fig is None:
#             fig = plt.figure(fign)
#         if clf:
#             fig.clf()
#         ax = fig.add_subplot(111)
#     if z1 is None:
#         z1 = np.max(tops)
#         z1 += 0.05 * z1
#     k = len(tops)
#     mxy0 = dict(color='k', lw=1, ls='-')
#     myx0 = dict(color='k', lw=1, ls=':')
#     if mxy is not None:
#         mxy0.update(mxy)
#     if myx is not None:
#         myx0.update(myx)
#     mxy = mxy0
#     myx = myx0
#     if modes == "xy" or modes == "both":
#         ax.plot([resxy[0], resxy[0]], [z0, tops[1]], **mxy)
#     if modes == "yx" or modes == "both":
#         ax.plot([resyx[0], resyx[0]], [z0, tops[1]], **myx)
#     for ki in range(1, k):
#         if horiz_lines:
#             if modes == "xy" or modes == "both":
#                 ax.plot([resxy[ki - 1], resxy[ki]], [tops[ki], tops[ki]], **mxy)
#             if modes == "yx" or modes == "both":
#                 ax.plot([resyx[ki - 1], resyx[ki]], [tops[ki], tops[ki]], **myx)
#         if ki == (k - 1):
#             zn = ((tops[ki] - tops[ki - 1]) / 2) + tops[ki]
#         else:
#             zn = tops[ki + 1]
#         if modes == "xy" or modes == "both":
#             ax.plot([resxy[ki], resxy[ki]], [tops[ki], zn], **mxy)
#         if modes == "yx" or modes == "both":
#             ax.plot([resyx[ki], resyx[ki]], [tops[ki], zn], **myx)
#     ax.set_ylim(z1, z0)
#     ax.set_xlim(res0, res1)
#     ax.set_xscale("log")
#     if res0 and res1:
#         ax.set_xlim(res0, res1)
#     if depth_scale.startswith("log"):
#         ax.set_yscale("log")
        

def res_at_depth(tops, rhos, z):
    """Return model's resistivity at depth z."""
    k = len(tops)
    assert k == len(rhos)
    for ki in range(k):
        if z == tops[ki]:
            if ki == 0:
                return rhos[0]
            elif ki == k - 1:
                return rhos[ki]
            else:
                return 10 ** ((numpy.log10(rhos[ki]) + numpy.log10(rhos[ki - 1])) / 2)
        elif z > tops[ki]:
            if ki == k - 1:
                return rhos[ki]
            elif z < tops[ki + 1]:
                return rhos[ki]
            else:
                continue
    logger.error("didn't find z=%s in model tops=%s rhos=%s?" % (z, tops, rhos))