import matplotlib.pyplot as plt
import numpy as np


def marginals_hist(vals, 
                   feature_name, 
                   create_new_fig = True, 
                   color='C0'):
    '''
    Plots histogram of values and shows 1-sigma and 2-sigma intervals.
    Made for plotting the marginals from trace values

    Args:
    - vals [array]: A 1d array of values (e.g. {trace}.flatten())
    - feature_name [str]: Name to plot on title
    '''

    # Compute histogram
    (counts, bins) = np.histogram(vals, bins = 100)
    counts = counts/counts.max()
    bin_size = bins[1] - bins[0]

    # For plotting hist
    def plot_hist_from_counts(bins, counts, alpha, color, label=None):
        '''
        Plot a histogram from a set of bins and counts with a black
        border around the range
        '''
        plt.hist(bins[:-1]+(bin_size/2), bins, weights=counts, alpha = alpha, color=color, label=label);
        plt.hist(bins[:-1]+(bin_size/2), bins, weights=counts, histtype='step',color='k',linewidth=0.5);
    
    # 1 and 2 sigma values
    sigma_1_low, sigma_1_high = np.percentile(vals, [15.9, 84.1])
    sigma_2_low, sigma_2_high = np.percentile(vals, [2.3, 97.7])
    
    # Mask for bins
    m_1_sigma = (bins[:-1] >= sigma_1_low) & (bins[1:] <= sigma_1_high)
    m_2_sigma = (bins[:-1] >= sigma_2_low) & (bins[1:] <= sigma_2_high)

    # Create new figure if required
    if create_new_fig is True:
        plt.figure(figsize=(4,3))
    
    # Plot full range
    plot_hist_from_counts(bins, 
                          counts, 
                          alpha = 0.4,
                          color = color, 
                          label = None)
    
    # Plot 2 sigma limits
    plot_hist_from_counts(np.array(list(bins[:-1][m_2_sigma])+[bins[:-1][m_2_sigma][-1]+bin_size]), 
                          counts[m_2_sigma], 
                          alpha = 0.7, 
                          color = color,
                          label = '2σ (95%)')
    
    # Plot 1 sigma limits
    plot_hist_from_counts(np.array(list(bins[:-1][m_1_sigma])+[bins[:-1][m_1_sigma][-1]+bin_size]), 
                          counts[m_1_sigma], 
                          alpha = 1, 
                          color = color,
                          label = '1σ (68%)')
    
    plt.legend()
    plt.title(feature_name)






def plot_all_marginals(trace,
                       parameters=None,
                       parameter_names = None,
                       grid_shape = (2,2), 
                       figsize = None):
    '''
    Function that accepts a trace, and plots all marginals nicely.

    Args:
    - parameters: A list of paramters in `trace` to plot (e.g. ['betas', 'intercept']
    - parameter_names: A dict of paramter names or sub-names for adding to the plot E.g.
        {'betas':['f1', 'f2', 'f3'], 
         'intercept': 'intercept'}
    - grid_shape: A tuple containing the number of rows and columns for the plot
    '''

    # Set if args are None
    if parameters == None:
        parameters = list(trace.posterior)
    rows, cols = grid_shape
    if figsize == None:
        figsize = (cols * 3.5, rows * 2.75)
        
        
    # Loop through parameters to count n. plots
    tot = 0
    for param in parameters:
        # Count parameters
        if len(trace.posterior[param].shape) == 3:
            tot += trace.posterior[param].shape[-1] # If several sub-parameters, add all
        else:
            tot += 1 # Otherwise just add 1 parameter
    
    # Check if fits in grid
    if tot > (grid_shape[0]*grid_shape[1]):
        raise ValueError(f'Total number of parameters to plot (n = {tot}) exceeds grid size ({grid_shape[0]} * {grid_shape[1]}). Increase grid size to fit all parameter plots or pick fewer parameters ({str(parameters)})')
    
    # Create plot
    fig, axes = plt.subplots(rows, cols, figsize=figsize)  # Adjust figure size as needed
    
    # Loop through parameters and plot
    count = 0
    color_count = 0
    for param in parameters:
        
        # If parameter has several sub-parameters
        if len(trace.posterior[param].shape) == 3:
            param_count = 0
            for n in range(trace.posterior[param].shape[-1]):
                # Extract values and feature name
                vals = trace.posterior[param].values[:,:,n].flatten()
                try:
                    f_name = parameter_names[param][param_count]
                except:
                    f_name = param + '_' + str(param_count+1)
    
                # Make plot
                plt.subplot(rows, cols, count+1)
                marginals_hist(vals, f_name, create_new_fig=False, color='C'+str(color_count))
                count += 1; param_count += 1
        else:
            # Extract values and feature name
            vals = trace.posterior[param].values.flatten()
            try:
                f_name = parameter_names[param]
            except:
                f_name = str(param)
    
            # Make plot
            plt.subplot(rows, cols, count+1)
            marginals_hist(vals, f_name, create_new_fig=False, color='C'+str(color_count))
            count += 1 
    
        # Go to next colour
        color_count+=1
    
    # Adjust layout
    plt.tight_layout()

