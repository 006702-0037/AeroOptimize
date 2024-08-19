import numpy as np

'''
estimates the value which a set of points will converge to

the results obtained by unsteady analysis fluctuate decreasingly about some value
this value represents the final 'steady' result of the propeller
this function may be used to estimate this value 


disclaimer: i dont really know the proper way to do this.

the closest problem I could find to this was damped oscillations
but most formulas I saw regarding this typically assumed continuous and harmonic motion
which sucks, cause unsteady analysis data is discrete and not harmonic

The approach I thought of finds the value which minimizes the average (mean) offset between itself and the data
It starts in the middle of the data, because left values fluctuate the most and are therefore outliers.


Now, this sounds thought out, but Im actually an idiot, and have no way of proving if this is the correct approach

Who knows? 
Maybe theres an equation to do this exact thing? 
Maybe this thing doesnt need to be done at all cause my methodology is inherently flawed?
Maybe its possible to just find the steady state values, and im being a dumbass?

While I contemplate these and other important questions, here's some other things probably worth a try:

        # find average value over entire graph
        # approximate with a harmonic and use dampening equations
        # find linear regression with smallest standard error and slope closest to 0
        # use moving median
'''


def convergence(data, precision=0.01):
    best_mean = [0, max(data)]
    cutoffs = round(len(data) * 0.50)

    for c in range(cutoffs):
        for i in np.arange(min(data[c:]), max(data[c:]), precision):
            mean_offset = sum([abs(ii - i) for ii in data[c:]]) / len(data[c:])
            if mean_offset < best_mean[1]:
                best_mean[1] = mean_offset
                best_mean[0] = i

    return best_mean[0]
