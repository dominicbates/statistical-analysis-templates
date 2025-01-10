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
