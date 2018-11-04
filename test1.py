import numpy as np
from Utils.data_utils import plot_conv_images


def conv_forward(x, w, b):
    (N, H, W, C),(F, WH, WW, C)= x.shape ,w.shape
    H_prime,W_prime= 1 + (H - WH) , 1 + (W - WW)
    out = np.zeros([N, H_prime, W_prime, F])
    H_prime ,W_prime = 1 + (H - WH),1 + (W - WW)
    out = np.zeros([N, H_prime, W_prime, F])
    for n in range(N):
        for f in range(F):
            for h_prime in range(H_prime):
                for w_prime in range(W_prime):
                    window = x[n, h_prime:h_prime + WH, w_prime: w_prime + WW, :]
                    out[n, h_prime, w_prime, f] = np.sum(window * w[f, :, :, :]) + b[f]
    cache = (x, w, b)
    return out, cache


def conv_backward(dout, cache):
    (x, w, b),(N, H, W, C) = cache,x.shape
    (F, WH, WW, C),(_, H_prime, W_prime, _) = w.shape, dout.shape
    dx,dw,db = np.zeros_like(x),np.zeros_like(w),np.zeros_like(b)
    for n in range(N):
        for f in range(F):
            for h_prime in range(H_prime):
                for w_prime in range(W_prime):
                    dx[n, h_prime:h_prime + WH, w_prime:w_prime + WW, :] += w[f, :, :, :] * dout[n, h_prime, w_prime, f]
                    dw[f, :, :, :] += x[n, h_prime:h_prime + WH, w_prime:w_prime + WW, :] * dout[n, h_prime, w_prime, f]
                    db[f] += dout[n, h_prime, w_prime, f]
    return dx, dw, db

def max_pool_forward(x, pool_param):
    (N, H, W, C),stride = x.shape ,pool_param['stride']
    pool_height,pool_width = pool_param['pool_height'] ,pool_param['pool_width']
    H_prime = np.floor(1 + (H - pool_height) / stride[1]).astype(int)
    W_prime = np.floor(1 + (W - pool_width) / stride[2]).astype(int)
    out = np.zeros((N, H_prime, W_prime, C))
    for n in range(N):
        for h in range(H_prime):
            for w in range(W_prime):
                h1 = h * stride[1]
                h2 = h * stride[1] + pool_height
                w1 = w * stride[2]
                w2 = w * stride[2] + pool_width
                window = x[n, h1:h2, w1:w2, :]
                out[n, h, w, :] = np.max(window.reshape((pool_height * pool_width, C)), axis=0)
    cache = (x, pool_param)
    return out, cache
def max_pool_backward(dout, cache):
    (x, pool_param),(N, H, W, C) ,stride = cache ,x.shape ,pool_param['stride']
    pool_height ,pool_width = pool_param['pool_height'],pool_param['pool_width']
    H_prime = np.floor(1 + (H - pool_height) / stride[1]).astype(int)
    W_prime = np.floor(1 + (W - pool_width) / stride[2]).astype(int)
    dx = np.zeros_like(x)
    for n in range(N):
        for h in range(H_prime):
            for w in range(W_prime):
                h1 = h * stride[1]
                h2 = h * stride[1] + pool_height
                w1 = w * stride[2]
                w2 = w * stride[2] + pool_width
                window = x[n, h1:h2, w1:w2, :]
                window2 = window.reshape((C, pool_height * pool_width))
                max_index = np.argmax(window2, axis=1)
                window3 = np.zeros_like(window2)
                print('dout: ', dout, dout[n, h, w, :])
                print('window3: ', window3)
                window3[np.arange(C), max_index] = dout[n, h, w, :]
                print('window3: ', window3)
                dx[n, h1:h2, w1:w2, :] = window3.reshape(1, pool_height, pool_width, C)
    return dx

def _rel_error(x, y):
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def Test_conv_forward():
    x_shape,w_shape = (2, 5, 5, 3) ,(2, 2, 4, 3)
    x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
    w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
    b = np.linspace(-0.1, 0.05, num=2)
    out, _ = conv_forward(x, w, b)
    correct_out = np.array([[[[0.04733114, -0.094658], [0.02481508, -0.04314865]],
                             [[-0.06524918, 0.16288876], [-0.08776524, 0.21439812]],
                             [[-0.1778295, 0.42043553], [-0.20034557, 0.47194488]],
                             [[-0.29040982, 0.67798229], [-0.31292589, 0.72949165]]],

                            [[[-0.51557047, 1.19307582], [-0.53808653, 1.24458518]],
                             [[-0.62815079, 1.45062259], [-0.65066686, 1.50213194]],
                             [[-0.74073112, 1.70816936], [-0.76324718, 1.75967871]],
                             [[-0.85331144, 1.96571612], [-0.8758275, 2.01722547]]]])
    return _rel_error(out, correct_out)

def Test_conv_forward_IP(x):
    w ,w[0, 1, 1, :] = np.zeros((2, 3, 3, 3)) ,[0.3, 0.6, 0.1]
    w[1, :, :, 2] ,b = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]] ,np.array([0, 128])
    out, _ = conv_forward(x, w, b)
    plot_conv_images(x, out)
    return
def Test_max_pool_forward():
    x_shape ,x = (2, 5, 5, 3) ,np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
    pool_param = {'pool_width': 2, 'pool_height': 3, 'stride': [1, 2, 4, 1]}
    out, _ = max_pool_forward(x, pool_param)
    correct_out = np.array([[[[0.03288591, 0.03691275, 0.0409396]],
                             [[0.15369128, 0.15771812, 0.16174497]]],
                            [[[0.33489933, 0.33892617, 0.34295302]],
                             [[0.4557047, 0.45973154, 0.46375839]]]])
    return _rel_error(out, correct_out)

def _eval_numerical_gradient_array(f, x, df, h=1e-5):
    grad = np.zeros_like(x)
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        ix = it.multi_index
        p = np.array(x)
        p[ix] = x[ix] + h
        pos = f(p)
        p[ix] = x[ix] - h
        neg = f(p)
        grad[ix] = np.sum((pos - neg) * df) / (2 * h)
        it.iternext()
    return grad


def Test_conv_backward():
    """ Test conv_backward function """
    x = np.random.randn(2, 5, 5, 3)
    w = np.random.randn(2, 2, 4, 3)
    b = np.random.randn(2, )
    dout = np.random.randn(2, 4, 2, 2)

    out, cache = conv_forward(x, w, b)
    dx, dw, db = conv_backward(dout, cache)

    dx_num = _eval_numerical_gradient_array(lambda x: conv_forward(x, w, b)[0], x, dout)
    dw_num = _eval_numerical_gradient_array(lambda w: conv_forward(x, w, b)[0], w, dout)
    db_num = _eval_numerical_gradient_array(lambda b: conv_forward(x, w, b)[0], b, dout)

    return (_rel_error(dx, dx_num), _rel_error(dw, dw_num), _rel_error(db, db_num))


def Test_max_pool_backward():
    """ Test max_pool_backward function """
    x = np.random.randn(2, 5, 5, 3)
    pool_param = {'pool_width': 2, 'pool_height': 3, 'stride': [1, 2, 4, 1]}
    dout = np.random.randn(2, 2, 1, 3)

    out, cache = max_pool_forward(x, pool_param)
    dx = max_pool_backward(dout, cache)

    dx_num = _eval_numerical_gradient_array(lambda x: max_pool_forward(x, pool_param)[0], x, dout)
    return _rel_error(dx, dx_num)