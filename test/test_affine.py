import pytest

import torch
import torchgeometry as tgm
from torch.autograd import gradcheck
from torch.testing import assert_allclose

import utils
from common import device_type


class TestRotate:
    def test_smoke(self):
        angle = 0.0
        angle_t = torch.tensor([angle])
        assert str(tgm.Rotate(angle=angle_t)) == 'Rotate(angle=0.0, center=None)'

    def test_angle90(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 2.],
            [3., 4.],
            [5., 6.],
            [7., 8.],
        ]])
        expected = torch.tensor([[
            [0., 0.],
            [4., 6.],
            [3., 5.],
            [0., 0.],
        ]])
        # prepare transformation
        angle = torch.tensor([90.])
        transform = tgm.Rotate(angle)
        assert_allclose(transform(inp), expected)
        
    def test_angle90_batch2(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 2.],
            [3., 4.],
            [5., 6.],
            [7., 8.],
        ]]).repeat(2, 1, 1, 1)
        expected = torch.tensor([[[
            [0., 0.],
            [4., 6.],
            [3., 5.],
            [0., 0.],
        ]],[[
            [0., 0.],
            [5., 3.],
            [6., 4.],
            [0., 0.],
        ]]])
        # prepare transformation
        angle = torch.tensor([90., -90.])
        transform = tgm.Rotate(angle)
        assert_allclose(transform(inp), expected)

    def test_angle90_batch2_broadcast(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 2.],
            [3., 4.],
            [5., 6.],
            [7., 8.],
        ]]).repeat(2, 1, 1, 1)
        expected = torch.tensor([[[
            [0., 0.],
            [4., 6.],
            [3., 5.],
            [0., 0.],
        ]],[[
            [0., 0.],
            [4., 6.],
            [3., 5.],
            [0., 0.],
        ]]])
        # prepare transformation
        angle = torch.tensor([90.])
        transform = tgm.Rotate(angle)
        assert_allclose(transform(inp), expected)

    def test_gradcheck(self):
        # test parameters
        angle = torch.tensor([90.])
        angle = utils.tensor_to_gradcheck_var(
            angle, requires_grad=False)  # to var

        # evaluate function gradient
        input = torch.rand(1, 2, 3, 4)
        input = utils.tensor_to_gradcheck_var(input)  # to var
        assert gradcheck(tgm.rotate, (input, angle,), raise_exception=True)

    @pytest.mark.skip('Need deep look into it since crashes everywhere.')
    def test_jit(self):
        angle = torch.tensor([90.])
        batch_size, channels, height, width = 2, 3, 64, 64
        img = torch.ones(batch_size, channels, height, width)
        rot = tgm.Rotate(angle)
        rot_traced = torch.jit.trace(tgm.Rotate(angle), img)
        assert_allclose(rot(img), rot_traced(img))


class TestTranslate:
    def test_dxdy(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 2.],
            [3., 4.],
            [5., 6.],
            [7., 8.],
        ]])
        expected = torch.tensor([[
            [0., 1.],
            [0., 3.],
            [0., 5.],
            [0., 7.],
        ]])
        # prepare transformation
        translation = torch.tensor([[1., 0.]])
        transform = tgm.Translate(translation)
        assert_allclose(transform(inp), expected)

    def test_dxdy_batch(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 2.],
            [3., 4.],
            [5., 6.],
            [7., 8.],
        ]]).repeat(2, 1, 1, 1)
        expected = torch.tensor([[[
            [0., 1.],
            [0., 3.],
            [0., 5.],
            [0., 7.],
        ]],[[
            [0., 0.],
            [0., 1.],
            [0., 3.],
            [0., 5.],
        ]]])
        # prepare transformation
        translation = torch.tensor([[1., 0.], [1., 1.]])
        transform = tgm.Translate(translation)
        assert_allclose(transform(inp), expected)

    def test_dxdy_batch_broadcast(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 2.],
            [3., 4.],
            [5., 6.],
            [7., 8.],
        ]]).repeat(2, 1, 1, 1)
        expected = torch.tensor([[[
            [0., 1.],
            [0., 3.],
            [0., 5.],
            [0., 7.],
        ]],[[
            [0., 1.],
            [0., 3.],
            [0., 5.],
            [0., 7.],
        ]]])
        # prepare transformation
        translation = torch.tensor([[1., 0.]])
        transform = tgm.Translate(translation)
        assert_allclose(transform(inp), expected)

    def test_gradcheck(self):
        # test parameters
        translation = torch.tensor([[1., 0.]])
        translation = utils.tensor_to_gradcheck_var(
            translation, requires_grad=False)  # to var

        # evaluate function gradient
        input = torch.rand(1, 2, 3, 4)
        input = utils.tensor_to_gradcheck_var(input)  # to var
        assert gradcheck(tgm.translate, (input, translation,), raise_exception=True)

    @pytest.mark.skip('Need deep look into it since crashes everywhere.')
    def test_jit(self):
        translation = torch.tensor([[1., 0.]])
        batch_size, channels, height, width = 2, 3, 64, 64
        img = torch.ones(batch_size, channels, height, width)
        trans = tgm.Translate(translation)
        trans_traced = torch.jit.trace(tgm.Translate(translation), img)
        assert_allclose(trans(img), trans_traced(img))


class TestScale:
    def test_scale_factor_2(self):
        # prepare input data
        inp = torch.tensor([[
            [0., 0., 0., 0.],
            [0., 1., 1., 0.],
            [0., 1., 1., 0.],
            [0., 0., 0., 0.]
        ]])
        # prepare transformation
        scale_factor = torch.tensor([2.])
        transform = tgm.Scale(scale_factor)
        assert_allclose(transform(inp).sum().item(), 12.25)
        
    def test_scale_factor_05(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.]
        ]])
        expected = torch.tensor([[
            [0., 0., 0., 0.],
            [0., 1., 1., 0.],
            [0., 1., 1., 0.],
            [0., 0., 0., 0.]
        ]])
        # prepare transformation
        scale_factor = torch.tensor([0.5])
        transform = tgm.Scale(scale_factor)
        assert_allclose(transform(inp), expected)

    def test_scale_factor_05_batch2(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.]
        ]]).repeat(2, 1, 1, 1)
        expected = torch.tensor([[
            [0., 0., 0., 0.],
            [0., 1., 1., 0.],
            [0., 1., 1., 0.],
            [0., 0., 0., 0.]
        ]])
        # prepare transformation
        scale_factor = torch.tensor([0.5, 0.5])
        transform = tgm.Scale(scale_factor)
        assert_allclose(transform(inp), expected)

    def test_scale_factor_05_batch2_broadcast(self):
        # prepare input data
        inp = torch.tensor([[
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.]
        ]]).repeat(2, 1, 1, 1)
        expected = torch.tensor([[
            [0., 0., 0., 0.],
            [0., 1., 1., 0.],
            [0., 1., 1., 0.],
            [0., 0., 0., 0.]
        ]])
        # prepare transformation
        scale_factor = torch.tensor([0.5])
        transform = tgm.Scale(scale_factor)
        assert_allclose(transform(inp), expected)

    def test_gradcheck(self):
        # test parameters
        scale_factor = torch.tensor([0.5])
        scale_factor = utils.tensor_to_gradcheck_var(
            scale_factor, requires_grad=False)  # to var

        # evaluate function gradient
        input = torch.rand(1, 2, 3, 4)
        input = utils.tensor_to_gradcheck_var(input)  # to var
        assert gradcheck(tgm.scale, (input, scale_factor,),
            raise_exception=True)

    @pytest.mark.skip('Need deep look into it since crashes everywhere.')
    def test_jit(self):
        scale_factor = torch.tensor([0.5])
        batch_size, channels, height, width = 2, 3, 64, 64
        img = torch.ones(batch_size, channels, height, width)
        trans = tgm.Scale(scale_factor)
        trans_traced = torch.jit.trace(tgm.Scale(scale_factor), img)
        assert_allclose(trans(img), trans_traced(img))

