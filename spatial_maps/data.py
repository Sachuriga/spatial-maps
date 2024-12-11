from scipy.ndimage import gaussian_filter1d
import numpy as np

def pos2speed(t,x,y,filter_speed=True):
    delta_X = np.diff(x)
    delta_Y = np.diff(y)
    sampling_intervals = np.diff(t)
    average_sampling_interval = np.median(sampling_intervals)
    interval =round(average_sampling_interval, 4)
    samplingrate = 1/interval
    n = samplingrate * 0.4
    truncate = 4.0  # 默认值
    # 计算 sigma
    sigma = (n - 1) / (2 * truncate)

    # Calculate distances between points
    delta_S = np.sqrt(delta_X**2 + delta_Y**2)
    speeds = delta_S*samplingrate

    # Compute instantaneous speeds
    smoothed_speed = gaussian_filter1d(speeds, sigma=sigma)
    mask = (smoothed_speed>=0.05)

    if filter_speed==True:
        return mask, smoothed_speed
    else:
        return smoothed_speed