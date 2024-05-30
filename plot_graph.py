import matplotlib.pyplot as plt

def plot_graph(timestamps, temp_water, temp_ref):
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temp_water, label='Water Temperature')
    plt.axhline(y=temp_ref, color='r', linestyle='--', linewidth=1, label='Temperature Reference')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (C)')
    plt.title('Water Temperature Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()