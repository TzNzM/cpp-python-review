import numpy as np

# 图像维度变换
images = np.arange(4 * 3 * 2 * 2, dtype=np.float32).reshape(4, 3, 2, 2)
labels = np.array([0, 2, 1, 2], dtype=np.int64)
masks = labels != 2
filter_images = images[masks]
assert filter_images.shape == (2, 3, 2, 2)
assert filter_images.ndim == 4
assert filter_images.dtype == np.float32
channel_images = filter_images[:,1,:,:]
channel_images = np.expand_dims(channel_images,1)
assert channel_images.shape == (2, 1, 2, 2)
assert channel_images.ndim == 4
assert channel_images.dtype == np.float32
# N,C,H,W = channel_images.shape
new_images = channel_images.transpose(0, 2, 3, 1)
assert new_images.shape == (2, 2, 2, 1)
assert new_images.ndim == 4
assert new_images.dtype == np.float32

# view 与 .copy()
# view的情况:
a = np.arange(6)
b = a[1:4]
b[0] = 100
print(b)
print(a)

# copy的情况:
a = np.arange(6)

c = a[1:4].copy()
c[0] = 100
print(c)
print(a)
