# Developed by S.C.T. & B.A.H. Spring 2025 for Internetworking of Things

import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
from scipy.signal import welch
from collections import deque
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

FREQ = 314.5e6 #center freq
SAMPLE_RATE = 2.4e6
SAMPLE_SIZE = 256 * 1024
POWER_THRESHOLD_DB = -75  # determines noise floor
ROLLING_WINDOW = 5       

print("[*] Initializing SDRs...")
sdr1 = RtlSdr(0)  # init left sdr (first to plug in)
sdr2 = RtlSdr(1)  # init right sdr

for sdr in [sdr1, sdr2]:
    sdr.sample_rate = SAMPLE_RATE
    sdr.center_freq = FREQ
    sdr.gain = 'auto'

history1 = deque(maxlen=ROLLING_WINDOW)
history2 = deque(maxlen=ROLLING_WINDOW)


plt.ion() #plot init
fig, ax = plt.subplots()
bars = ax.bar(['⬅️ SDR 0 (Left)', 'SDR 1 (Right) ➡️'], [0, 0], color=['blue', 'green'])

power_labels = [
    ax.text(i, 0, '', ha='center', va='bottom', fontsize=12, fontweight='bold', color='white')
    for i in range(2)
]

direction_text = ax.text(0.5, 1.12, '', ha='center', va='bottom', transform=ax.transAxes, fontsize=16, fontweight='bold')
ax.axvline(x=0.5, color='gray', linestyle='--', linewidth=1)

ax.set_ylim(-100, -60)
ax.set_ylabel('Signal Power (dB)', fontsize=12)
ax.set_title('🔍 Real-Time Key Fob Signal Direction HUD', fontsize=14)

def get_power(samples):
    freqs, Pxx = welch(samples, fs=SAMPLE_RATE, nperseg=1024, return_onesided=False)
    return 10 * np.log10(np.mean(Pxx))

def average(queue):
    return sum(queue) / len(queue) if queue else -999

prev_direction = ""

try:
    while True:
        samples1 = sdr1.read_samples(SAMPLE_SIZE)
        samples2 = sdr2.read_samples(SAMPLE_SIZE)

        power1 = get_power(samples1)
        power2 = get_power(samples2)

        history1.append(power1)
        history2.append(power2)

        avg1 = average(history1)
        avg2 = average(history2)

        print(f"[Power] SDR 0: {avg1:.2f} dB | SDR 1: {avg2:.2f} dB") #top header

      
        bars[0].set_height(avg1)
        bars[1].set_height(avg2)

        power_labels[0].set_position((bars[0].get_x() + bars[0].get_width() / 2, avg1 + 1))
        power_labels[0].set_text(f'{avg1:.1f} dB')

        power_labels[1].set_position((bars[1].get_x() + bars[1].get_width() / 2, avg2 + 1))
        power_labels[1].set_text(f'{avg2:.1f} dB')

        # direction logic below
        diff = abs(avg1 - avg2)
        confidence = f"(Δ {diff:.1f} dB)"

        if avg1 > POWER_THRESHOLD_DB or avg2 > POWER_THRESHOLD_DB:
            if diff < 1:
                direction = f"↔ Equal | Avg: {(avg1 + avg2)/2:.1f} dB"
            elif avg1 > avg2:
                direction = f"⬅️ Left Stronger {confidence} | {avg1:.1f} dB"
            else:
                direction = f"➡️ Right Stronger {confidence} | {avg2:.1f} dB"
        else:
            direction = f"❌ No Signal" #if lower than noise floor

       
        if direction != prev_direction:
            direction = "🔄 " + direction
        prev_direction = direction

        direction_text.set_text(direction)
        plt.pause(0.2)

except KeyboardInterrupt:
    print("\n[*] Exiting...")
finally:
    sdr1.close()
    sdr2.close()
    plt.ioff()
    plt.show()
