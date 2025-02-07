""" 
Estimates a non-linear warp field, the lenna image is randomly deformed using
the spline deformation model.
"""

import numpy as np
import scipy.ndimage as nd
import scipy.misc as misc

from register.models import model
from register.metrics import metric
from register.samplers import sampler

from register.visualize import plot
from register import register

def warp(image):
    """
    Randomly warps an input image using a cubic spline deformation.
    """
    coords = register.Coordinates(
        [0, image.shape[0], 0, image.shape[1]]
        )
        
    mymodel = model.Projective(coords)
    mysampler = sampler.CubicConvolution(coords)

    p = mymodel.identity
    #TODO: Understand the effect of parameter magnitude:
    p += np.random.rand(p.shape[0]) * 0.1 - 0.05
    
    return mysampler.f(image, mymodel.warp(p)).reshape(image.shape)


image = misc.lena().astype(np.double)
image = nd.zoom(image, 0.30)
template = warp(image)

# Coerce the image data into RegisterData.
image = register.RegisterData(image)
template = register.RegisterData(template)

# Smooth the template and image.
image.smooth(0.5)
template.smooth(0.5)

# Form the affine registration instance.
reg = register.Register(
    model.Projective,
    metric.Residual,
    sampler.CubicConvolution
    )

# Compute an affine registration between the template and image.
p, warp, img, error = reg.register(
    image,
    template,
    alpha=0.00002,
    verbose=True,
    plotCB=plot.gridPlot
    )


plot.show()
