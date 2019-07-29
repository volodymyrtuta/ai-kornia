import pytest

import kornia as kornia
import kornia.testing as utils  # test utils

import torch
from torch.testing import assert_allclose
from torch.autograd import gradcheck


class TestCornerHarris:
    def test_shape(self):
        inp = torch.ones(1, 3, 4, 4)
        sobel = kornia.feature.CornerHarris(k=0.04)
        assert sobel(inp).shape == (1, 3, 4, 4)

    def test_shape_batch(self):
        inp = torch.zeros(2, 6, 4, 4)
        sobel = kornia.feature.CornerHarris(k=0.04)
        assert sobel(inp).shape == (2, 6, 4, 4)

    def test_corners(self):
        inp = torch.tensor([[[
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
        ]]])

        expected = torch.tensor([[[
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
        ]]])

        scores = kornia.feature.corner_harris(inp, k=0.04)
        assert_allclose(scores, expected)

    def test_corners_batch(self):
        inp = torch.tensor([[
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
        ], [
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 1., 1., 1., 0., 0.],
            [0., 1., 1., 1., 1., 0., 0.],
            [0., 1., 1., 1., 1., 0., 0.],
            [0., 1., 1., 1., 1., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
        ]]).repeat(2, 1, 1, 1)

        expected = torch.tensor([[
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
        ], [
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 1., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 1., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
        ]])

        scores = kornia.feature.corner_harris(inp, k=0.04)
        assert_allclose(scores, expected)

    def test_gradcheck(self):
        k = 0.04
        batch_size, channels, height, width = 1, 2, 5, 4
        img = torch.rand(batch_size, channels, height, width)
        img = utils.tensor_to_gradcheck_var(img)  # to var
        assert gradcheck(kornia.feature.corner_harris, (img, k),
                         raise_exception=True)

    @pytest.mark.skip(reason="turn off all jit for a while")
    def test_jit(self):
        @torch.jit.script
        def op_script(input, k):
            return kornia.feature.corner_harris(input, k)
        k = torch.tensor(0.04)
        img = torch.rand(2, 3, 4, 5)
        actual = op_script(img, k)
        expected = kornia.feature.corner_harris(img, k)
        assert_allclose(actual, expected)
