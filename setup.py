from setuptools import setup, Extension
from torch.utils import cpp_extension
import os

extension_name = "exllamav2_ext"
verbose = False
ext_debug = False

precompile = 'EXLLAMA_NOCOMPILE' not in os.environ

windows = (os.name == "nt")

extra_cflags = ["/Ox"] if windows else ["-O3"]

if ext_debug:
    extra_cflags += ["-ftime-report", "-DTORCH_USE_CUDA_DSA"]

extra_compile_args = {
    "cxx": extra_cflags,
    "nvcc": ["-lineinfo", "-O3"],
}

setup_kwargs = {
    "ext_modules": [
        cpp_extension.CUDAExtension(
            extension_name,
            [
                "exllamav2/exllamav2_ext/ext.cpp",
                "exllamav2/exllamav2_ext/cuda/pack_tensor.cu",
                "exllamav2/exllamav2_ext/cuda/quantize.cu",
                "exllamav2/exllamav2_ext/cuda/q_matrix.cu",
                "exllamav2/exllamav2_ext/cuda/q_attn.cu",
                "exllamav2/exllamav2_ext/cuda/q_mlp.cu",
                "exllamav2/exllamav2_ext/cuda/q_gemm.cu",
                "exllamav2/exllamav2_ext/cuda/rms_norm.cu",
                "exllamav2/exllamav2_ext/cuda/rope.cu",
                "exllamav2/exllamav2_ext/cpp/quantize_func.cpp",
                "exllamav2/exllamav2_ext/cpp/sampling.cpp"
            ],
            extra_compile_args=extra_compile_args,
            libraries=["cublas"] if windows else [],
        )],
    "cmdclass": {"build_ext": cpp_extension.BuildExtension}
} if precompile else {}

version = "0.0.4"

setup(
    name = "exllamav2",
    version = version,
    packages = ["exllamav2", "exllamav2.generator"],
    url = "https://github.com/turboderp/exllamav2",
    license = "AGPL",
    author = "bb",
    install_requires = [
        "pandas",
        "ninja",
        "fastparquet",
        "torch>=2.0.1",
        "safetensors>=0.3.2",
        "sentencepiece>=0.1.97",
    ],
    include_package_data = True,
    verbose = verbose,
    **setup_kwargs,
)
