""" 
Estimates a linear warp field, using an image pyramid to speed up the 
computation.
"""

import scipy.ndimage as nd
import scipy.misc as misc

from register.models import model
from register.metrics import metric
from register.samplers import sampler

from register.visualize import plot
from register import register

# Form some test data (lena, lena rotated 20 degrees)
image = register.RegisterData(misc.lena())
template = register.RegisterData(
    nd.rotate(image.data, 20, reshape=False)
    )

# Form the registrator.
affine = register.Register(
    model.Affine,
    metric.Residual,
    sampler.Bilinear
    )

# Image pyramid registration can be executed like so:
pHat = None
for factor in [20, 10, 5]:
    
    if pHat is not None:
        scale = downImage.coords.spacing / factor
        # FIXME: Find a nicer way to do this.
        pHat = model.Affine.scale(pHat, scale)
        
    downImage = image.downsample(factor) 
    downTemplate = template.downsample(factor) 
    
    p, _warp, _img, _error = affine.register(
        downImage,
        downTemplate,
        p=pHat,
        plotCB=plot.gridPlot,
        verbose=True
        )

    pHat = p

plot.show()
