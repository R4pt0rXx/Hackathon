import numpy as np


data = np.random.randn(100)

x = np.array(data)
y = np.roll(x, 5) + np.random.randn(100)


ndata = x #- np.mean(x)
mdata = y #- np.mean(y)

acorr = sc.signal.correlate(ndata, mdata, "full", "fft")
print(acorr.argmax()-(len(ndata)-1))