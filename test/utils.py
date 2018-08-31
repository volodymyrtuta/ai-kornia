import torch


# test utilites


def create_eye_batch(batch_size, eye_size):
    """Creates a batch of identity matrices of shape Bx3x3
    """
    return torch.eye(eye_size).view(
        1, eye_size, eye_size).expand(batch_size, -1, -1)


def create_random_homography(batch_size, eye_size, std_val=1e-3):
    """Creates a batch of random homographies of shape Bx3x3
    """
    std = torch.FloatTensor(batch_size, eye_size, eye_size)
    eye = create_eye_batch(batch_size, eye_size)
    return eye + std.uniform_(-std_val, std_val)


def tensor_to_gradcheck_var(tensor):
    """Converts the input tensor to a valid variable to check the gradient.
      `gradcheck` needs 64-bit floating point and requires gradient.
    """
    tensor = tensor.type(torch.DoubleTensor)
    return tensor.requires_grad_(True)


def compute_mse(x, y):
    """Computes the mean square error between the inputs.
    """
    return torch.sqrt(((x - y) ** 2).sum())


def compute_patch_error(x, y, h, w):
    """Compute the absolute error between patches.
    """
    return torch.abs(x - y)[..., h // 4:-h // 4, w // 4:-w // 4].mean()
