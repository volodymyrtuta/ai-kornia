
---


*Kornia* is a differentiable computer vision library for [PyTorch](https://pytorch.org).

It consists of a set of routines and differentiable modules to solve generic computer vision problems. At its core, the package uses *PyTorch* as its main backend both for efficiency and to take advantage of the reverse-mode auto-differentiation to define and compute the gradient of complex functions.



<!--<div align="center">
  <img src="http://drive.google.com/uc?export=view&id=1KNwaanUdY1MynF0EYfyXjDM3ti09tzaq">
</div>-->

## Overview

Inspired by existing packages, this library is composed by a subset of packages containing operators that can be inserted within neural networks to train models to perform image transformations, epipolar geometry, depth estimation, and low-level image processing such as filtering and edge detection that operate directly on tensors.

At a granular level, Kornia is a library that consists of the following components:


## Installation

### From pip:

  ```bash
  pip install kornia
  pip install kornia[x]  # to get the training API !
  ```

<details>
  <summary>Other installation options</summary>

  #### From source:

  ```bash
  python setup.py install
  ```

  #### From source with symbolic links:

  ```bash
  pip install -e .
  ```

  #### From source using pip:

  ```bash
  pip install git+https://github.com/kornia/kornia
  ```

</details>


## Examples

Run our Jupyter notebooks [tutorials](https://kornia.github.io/tutorials) to learn to use the library.



:triangular_flag_on_post: **Updates**
- :white_check_mark: [Image Matching](https://kornia.readthedocs.io/en/latest/applications/image_matching.html) Integrated to [Huggingface Spaces](https://huggingface.co/spaces). See [Gradio Web Demo](https://huggingface.co/spaces/akhaliq/Kornia-LoFTR).
- :white_check_mark: [Face Detection](https://kornia.readthedocs.io/en/latest/applications/face_detection.html) Integrated to [Huggingface Spaces](https://huggingface.co/spaces). See [Gradio Web Demo](https://huggingface.co/spaces/frapochetti/blurry-faces).

## Cite

If you are using kornia in your research-related documents, it is recommended that you cite the paper. See more in [CITATION](./CITATION.md).

  ```bibtex
  @inproceedings{eriba2019kornia,
    author    = {E. Riba, D. Mishkin, D. Ponsa, E. Rublee and G. Bradski},
    title     = {Kornia: an Open Source Differentiable Computer Vision Library for PyTorch},
    booktitle = {Winter Conference on Applications of Computer Vision},
    year      = {2020},
    url       = {https://arxiv.org/pdf/1910.02190.pdf}
  }
  ```

## Contributing
We appreciate all contributions. If you are planning to contribute back bug-fixes, please do so without any further discussion. If you plan to contribute new features, utility functions or extensions, please first open an issue and discuss the feature with us. Please, consider reading the [CONTRIBUTING](./CONTRIBUTING.md) notes. The participation in this open source project is subject to [Code of Conduct](./CODE_OF_CONDUCT.md).


## Community
- **Forums:** discuss implementations, research, etc. [GitHub Forums](https://github.com/kornia/kornia/discussions)
- **GitHub Issues:** bug reports, feature requests, install issues, RFCs, thoughts, etc. [OPEN](https://github.com/kornia/kornia/issues/new/choose)
- **Slack:** Join our workspace to keep in touch with our core contributors and be part of our community. [JOIN HERE](https://join.slack.com/t/kornia/shared_invite/zt-csobk21g-2AQRi~X9Uu6PLMuUZdvfjA)
- For general information, please visit our website at www.kornia.org

<a href="https://github.com/Kornia/kornia/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Kornia/kornia" width="75%" height="75%" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
