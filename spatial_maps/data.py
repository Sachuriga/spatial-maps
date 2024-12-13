from scipy.ndimage import gaussian_filter1d
import numpy as np

def pos2speed(t,x,y,filter_speed=True,min_speed=0.05):
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


    if filter_speed==True:
        smoothed_speed = gaussian_filter1d(speeds, sigma=sigma)
        mask = (smoothed_speed>=min_speed)
        speeds = smoothed_speed[mask]

    xx=x[1:]
    yy=y[1:]
    tt=t[1:]
    x = xx[mask]
    y= yy[mask]
    t = tt[mask]

    combined_array = np.column_stack((t, x, y))

    return combined_array, mask, speeds

def speed_filtered_spikes(spikes_time,t,mask):
    t_ = np.append(t[1:], t[1:][-1] + np.median(np.diff(t[1:])))
    t_ = np.append(t[1:], t[1:][-1] + np.median(np.diff(t[1:])))
    spikes_in_bin, _ = np.histogram(spikes_time, t_)
    spk = spikes_in_bin[mask]

    return spk