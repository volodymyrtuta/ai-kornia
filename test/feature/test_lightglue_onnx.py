import pytest
import torch

from kornia.feature import OnnxLightGlue
from kornia.feature.lightglue_onnx.utils import normalize_keypoints

try:
    import onnxruntime as ort
except ImportError:
    ort = None


@pytest.mark.skipif(ort is None, reason="OnnxLightGlue requires onnxruntime-gpu")
@pytest.mark.skipif(not torch.cuda.is_available(), reason="OnnxLightGlue requires CUDA")
class TestOnnxLightGlue:
    @pytest.mark.slow
    @pytest.mark.parametrize("weights", OnnxLightGlue.MODEL_URLS.keys())
    def test_pretrained_weights(self, weights):
        model = OnnxLightGlue(weights)
        assert model is not None

    @pytest.mark.slow
    def test_forward(self):
        model = OnnxLightGlue()

        device = torch.device("cuda")
        kpts = torch.zeros(1, 5, 2, device=device)
        desc = torch.zeros(1, 5, 128, device=device)
        image = torch.zeros(1, 3, 10, 10)
        outputs = model(
            {
                "image0": {"keypoints": kpts, "descriptors": desc, "image": image},
                "image1": {"keypoints": kpts, "descriptors": desc, "image": image},
            }
        )

        assert "matches" in outputs
        assert "scores" in outputs

    def test_normalize_keypoints(self):
        kpts = torch.randint(0, 100, (1, 5, 2))
        size = torch.tensor([[100, 100]])
        kpts = normalize_keypoints(kpts, size)
        assert torch.all(torch.abs(kpts) <= 1).item()

    @pytest.mark.slow
    def test_exception(self):
        with pytest.raises(RuntimeError) as e:
            OnnxLightGlue(device="invalid device")
        assert "Invalid device string: 'invalid device'" in str(e)

        model = OnnxLightGlue()

        device = torch.device("cuda")
        kpts = torch.zeros(1, 5, 2, device=device)
        desc = torch.zeros(1, 5, 128, device=device)
        image = torch.zeros(1, 3, 10, 10)

        # Missing input
        with pytest.raises(Exception) as e:
            model({"image0": {"keypoints": kpts, "descriptors": desc, "image": image}})
        assert "Missing key image1 in data" in str(e)

        # Wrong dtype
        with pytest.raises(Exception) as e:
            model(
                {
                    "image0": {
                        "keypoints": torch.zeros(1, 5, 2, dtype=torch.int32, device=device),
                        "descriptors": desc,
                        "image": image,
                    },
                    "image1": {"keypoints": kpts, "descriptors": desc, "image": image},
                }
            )
        assert "Wrong dtype" in str(e)

        # Wrong device
        with pytest.raises(Exception) as e:
            model(
                {
                    "image0": {"keypoints": torch.zeros(1, 5, 2, device="cpu"), "descriptors": desc, "image": image},
                    "image1": {"keypoints": kpts, "descriptors": desc, "image": image},
                }
            )
        assert "Wrong device" in str(e)

        # Wrong shapes
        with pytest.raises(Exception) as e:
            model(
                {
                    "image0": {"keypoints": torch.zeros(1, 4, 2, device=device), "descriptors": desc, "image": image},
                    "image1": {"keypoints": kpts, "descriptors": desc, "image": image},
                }
            )
        assert "Number of keypoints does not match number of descriptors" in str(e)

        with pytest.raises(Exception) as e:
            model(
                {
                    "image0": {"keypoints": kpts, "descriptors": torch.zeros(1, 5, 127, device=device), "image": image},
                    "image1": {"keypoints": kpts, "descriptors": desc, "image": image},
                }
            )
        assert "Descriptors' dimensions do not match" in str(e)
