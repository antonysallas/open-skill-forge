#!/usr/bin/env python3
"""
CUDA Device Detection and CUDA Cores Counter
Detects NVIDIA GPUs and counts the actual number of CUDA cores.

IMPORTANT: CUDA Core Counting Methodology
------------------------------------------
NVIDIA does NOT expose CUDA core counts through their APIs (PyTorch, CUDA Runtime,
nvidia-smi, etc.). These APIs only provide:
- Number of Streaming Multiprocessors (SMs)
- Compute Capability (e.g., 8.6, 10.0)

The CUDA cores per SM varies by architecture and must be looked up from NVIDIA's
public specifications. This is the standard approach used by all GPU monitoring tools.

To add support for new GPUs:
1. Find the compute capability (script will show it)
2. Look up the architecture and cores/SM from NVIDIA specs
3. Add entry to the cores_per_sm_dict in get_cuda_cores_per_sm()

For RTX 5090 (Blackwell, SM 10.0): 128 cores/SM is already supported.

Architecture Reference:
- Kepler (2012): 192 cores/SM
- Maxwell (2014): 128 cores/SM
- Pascal (2016): 64-128 cores/SM
- Volta/Turing (2017-2018): 64 cores/SM
- Ampere (2020): 64-128 cores/SM
- Ada Lovelace (2022): 128 cores/SM
- Hopper (2022): 128 cores/SM
- Blackwell (2024): 128 cores/SM
"""

import sys
import subprocess
import platform
import time

def get_architecture_name(major, minor):
    """Get the architecture name based on compute capability."""
    arch_map = {
        3: "Kepler",
        5: "Maxwell",
        6: "Pascal",
        7: "Volta/Turing",
        8: "Ampere/Ada Lovelace",
        9: "Hopper",
        10: "Blackwell",
        11: "Blackwell",  # Mobile Blackwell variants
        12: "Blackwell",  # Mobile Blackwell variants
    }
    return arch_map.get(major, f"Unknown (SM {major}.{minor})")

def get_cuda_cores_per_sm(major, minor, device_name=""):
    """
    Get the number of CUDA cores per Streaming Multiprocessor (SM)
    based on the GPU's compute capability.

    Note: NVIDIA does not expose CUDA core counts through their APIs.
    This mapping is based on publicly available architecture specifications.

    Args:
        major: Major compute capability version
        minor: Minor compute capability version
        device_name: GPU device name (for better unknown GPU handling)

    Returns:
        tuple: (cores_per_sm, is_estimated)
            - cores_per_sm: Number of CUDA cores per SM
            - is_estimated: True if this is an estimate for unknown architecture
    """
    # Architecture-specific CUDA cores per SM
    cores_per_sm_dict = {
        # Kepler Architecture (2012-2014)
        (3, 0): 192,  # GK110 (Tesla K40, K80)
        (3, 5): 192,  # GK110B, GK210 (Tesla K40, K80)
        (3, 7): 192,  # GK210

        # Maxwell Architecture (2014-2015)
        (5, 0): 128,  # GM107, GM108 (GTX 750, GTX 750 Ti)
        (5, 2): 128,  # GM200, GM204, GM206 (GTX 980, GTX 980 Ti, GTX 970, GTX 960, GTX 950)
        (5, 3): 128,  # GM20B (Tegra X1)

        # Pascal Architecture (2016-2017)
        (6, 0): 64,   # GP100 (Tesla P100)
        (6, 1): 128,  # GP102, GP104, GP106, GP107 (GTX 1080 Ti, GTX 1080, GTX 1070, GTX 1060)
        (6, 2): 128,  # GP10B (Tegra X2)

        # Volta Architecture (2017)
        (7, 0): 64,   # GV100 (Tesla V100)

        # Turing Architecture (2018-2019)
        (7, 5): 64,   # TU102, TU104, TU106, TU116, TU117 (RTX 2080 Ti, RTX 2080, RTX 2070, RTX 2060, GTX 1660)

        # Ampere Architecture (2020-2021)
        (8, 0): 64,   # GA100 (A100)
        (8, 6): 128,  # GA102, GA103, GA104, GA106, GA107 (RTX 3090, RTX 3080, RTX 3070, RTX 3060)
        (8, 7): 128,  # GA10B (Jetson Orin, RTX 3050)

        # Ada Lovelace Architecture (2022-2023)
        (8, 9): 128,  # AD102, AD103, AD104, AD106, AD107 (RTX 4090, RTX 4080, RTX 4070, RTX 4060)

        # Hopper Architecture (2022-2023)
        (9, 0): 128,  # GH100 (H100, H200)

        # Blackwell Architecture (2024-2025)
        (10, 0): 128,  # GB100, GB102 (RTX 5090, RTX 5080, B100, B200)
        (11, 0): 128,  # Mobile Blackwell variants
        (12, 0): 128,  # Mobile Blackwell variants (RTX 5090 Laptop GPU)
    }

    if (major, minor) in cores_per_sm_dict:
        return cores_per_sm_dict[(major, minor)], False

    # Unknown architecture - provide estimate with warning
    # Modern architectures (7.0+) typically use 64 or 128 cores per SM
    estimated_cores = 128 if major >= 8 else 64
    return estimated_cores, True

def check_cuda_installation():
    """Check if CUDA is installed on the system."""
    print("🔍 Checking CUDA Installation...")
    print("=" * 50)

    # Check if nvidia-smi is available
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ NVIDIA Driver detected")
            print("📊 GPU Information:")
            print(result.stdout)
            return True
        else:
            print("❌ NVIDIA Driver not found or not working")
            print("Error:", result.stderr)
            return False
    except FileNotFoundError:
        print("❌ nvidia-smi command not found")
        print("   This usually means NVIDIA drivers are not installed")
        return False
    except subprocess.TimeoutExpired:
        print("❌ nvidia-smi command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running nvidia-smi: {e}")
        return False

def check_pytorch_cuda():
    """Check PyTorch CUDA support and count CUDA cores."""
    print("\n🔥 Checking PyTorch CUDA Support...")
    print("=" * 50)

    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")

        if torch.cuda.is_available():
            print(f"✅ CUDA is available in PyTorch")
            print(f"📊 CUDA version: {torch.version.cuda}")
            print(f"🔢 Number of GPU devices detected: {torch.cuda.device_count()}")
            print()

            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                device_name = props.name
                device_capability = (props.major, props.minor)
                device_memory = props.total_memory / 1024**3
                sm_count = props.multi_processor_count
                arch_name = get_architecture_name(props.major, props.minor)

                # Calculate CUDA cores
                cores_per_sm, is_estimated = get_cuda_cores_per_sm(props.major, props.minor, device_name)
                total_cuda_cores = sm_count * cores_per_sm

                print(f"   🎮 GPU {i}: {device_name}")
                print(f"      Architecture: {arch_name}")
                print(f"      Compute Capability: {device_capability[0]}.{device_capability[1]}")
                print(f"      Total Memory: {device_memory:.1f} GB")
                print(f"      Streaming Multiprocessors (SMs): {sm_count}")
                print(f"      CUDA Cores per SM: {cores_per_sm}")

                if is_estimated:
                    print(f"      ⚠️  ESTIMATED Total CUDA Cores: ~{total_cuda_cores:,}")
                    print(f"      ⚠️  Warning: Unknown architecture - this is an estimate!")
                    print(f"      Please report this GPU to improve accuracy.")
                else:
                    print(f"      ⭐ Total CUDA Cores: {total_cuda_cores:,}")

                # These attributes may not be available in all PyTorch versions
                try:
                    if hasattr(props, 'max_threads_per_block'):
                        print(f"      Max Threads per Block: {props.max_threads_per_block}")
                    if hasattr(props, 'max_threads_per_multi_processor'):
                        print(f"      Max Threads per SM: {props.max_threads_per_multi_processor:,}")
                except Exception:
                    pass

                print()

            return True
        else:
            print("❌ CUDA is not available in PyTorch")
            print("   PyTorch was likely installed without CUDA support")
            return False

    except ImportError:
        print("❌ PyTorch is not installed")
        print("   Install with: pip install torch")
        return False
    except Exception as e:
        print(f"❌ Error checking PyTorch CUDA: {e}")
        return False

def check_tensorflow_cuda():
    """Check TensorFlow CUDA support."""
    print("\n🧠 Checking TensorFlow CUDA Support...")
    print("=" * 50)

    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")

        # Check if CUDA is available
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ CUDA is available in TensorFlow")
            print(f"🔢 Number of GPU devices: {len(gpus)}")

            for i, gpu in enumerate(gpus):
                print(f"   GPU {i}: {gpu.name}")
                # Get GPU details
                try:
                    gpu_details = tf.config.experimental.get_device_details(gpu)
                    if gpu_details:
                        compute_capability = gpu_details.get('compute_capability', 'Unknown')
                        print(f"     Compute Capability: {compute_capability}")
                        print(f"     Device Name: {gpu_details.get('device_name', 'Unknown')}")
                except Exception:
                    pass

            return True
        else:
            print("❌ No GPU devices found in TensorFlow")
            print("   TensorFlow was likely installed without CUDA support")
            return False

    except ImportError:
        print("❌ TensorFlow is not installed")
        print("   Install with: pip install tensorflow")
        return False
    except Exception as e:
        print(f"❌ Error checking TensorFlow CUDA: {e}")
        return False

def check_cupy():
    """Check CuPy CUDA support and count CUDA cores."""
    print("\n☕ Checking CuPy CUDA Support...")
    print("=" * 50)

    try:
        import cupy as cp
        print(f"✅ CuPy version: {cp.__version__}")

        # Get CUDA device count
        device_count = cp.cuda.runtime.getDeviceCount()
        print(f"✅ CUDA is available in CuPy")
        print(f"🔢 Number of CUDA devices: {device_count}")
        print()

        for i in range(device_count):
            with cp.cuda.Device(i):
                props = cp.cuda.runtime.getDeviceProperties(i)
                device_name = props['name'].decode()
                sm_count = props['multiProcessorCount']
                major = props['major']
                minor = props['minor']
                arch_name = get_architecture_name(major, minor)

                # Calculate CUDA cores
                cores_per_sm, is_estimated = get_cuda_cores_per_sm(major, minor, device_name)
                total_cuda_cores = sm_count * cores_per_sm

                print(f"   🎮 GPU {i}: {device_name}")
                print(f"      Architecture: {arch_name}")
                print(f"      Compute Capability: {major}.{minor}")
                print(f"      Streaming Multiprocessors: {sm_count}")

                if is_estimated:
                    print(f"      ⚠️  ESTIMATED Total CUDA Cores: ~{total_cuda_cores:,}")
                    print(f"      ⚠️  Warning: Unknown architecture - this is an estimate!")
                else:
                    print(f"      ⭐ Total CUDA Cores: {total_cuda_cores:,}")
                print()

        return True

    except ImportError:
        print("❌ CuPy is not installed")
        print("   Install with: pip install cupy-cuda11x (or cupy-cuda12x)")
        return False
    except Exception as e:
        print(f"❌ Error checking CuPy CUDA: {e}")
        return False

def run_cuda_test():
    """Run a simple CUDA computation test."""
    print("\n🧪 Running CUDA Computation Test...")
    print("=" * 50)

    try:
        import torch

        if torch.cuda.is_available():
            # Create test tensors
            device = torch.device('cuda')
            print(f"🔄 Testing computation on device: {device}")

            # Test matrix multiplication
            a = torch.randn(1000, 1000, device=device)
            b = torch.randn(1000, 1000, device=device)

            print("   Performing matrix multiplication (1000x1000)...")
            start_time = time.time()
            c = torch.matmul(a, b)
            torch.cuda.synchronize()  # Wait for GPU to finish
            end_time = time.time()

            print(f"✅ CUDA computation successful!")
            print(f"   Time taken: {end_time - start_time:.4f} seconds")
            print(f"   Result shape: {c.shape}")
            print(f"   Result device: {c.device}")

            return True
        else:
            print("❌ CUDA not available for testing")
            return False

    except Exception as e:
        print(f"❌ Error during CUDA test: {e}")
        return False

def get_system_info():
    """Get system information."""
    print("💻 System Information")
    print("=" * 50)
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    print(f"Architecture: {platform.machine()}")

def main():
    """Main function to run all CUDA checks."""
    print("🚀 CUDA Device Detection and CUDA Cores Counter")
    print("=" * 60)
    print()
    print("ℹ️  Note: CUDA Cores = Streaming Multiprocessors × Cores per SM")
    print("   The number varies by GPU architecture (Turing, Ampere, etc.)")
    print()

    get_system_info()

    # Check CUDA installation
    cuda_installed = check_cuda_installation()

    # Check PyTorch CUDA support (includes CUDA core counting)
    pytorch_cuda = check_pytorch_cuda()

    # Check TensorFlow CUDA support
    tensorflow_cuda = check_tensorflow_cuda()

    # Check CuPy CUDA support (includes CUDA core counting)
    cupy_cuda = check_cupy()

    # Run computation test if CUDA is available
    if pytorch_cuda:
        run_cuda_test()

    # Summary
    print("\n📋 Summary")
    print("=" * 50)
    print(f"NVIDIA Driver: {'✅ Available' if cuda_installed else '❌ Not Available'}")
    print(f"PyTorch CUDA: {'✅ Available' if pytorch_cuda else '❌ Not Available'}")
    print(f"TensorFlow CUDA: {'✅ Available' if tensorflow_cuda else '❌ Not Available'}")
    print(f"CuPy CUDA: {'✅ Available' if cupy_cuda else '❌ Not Available'}")

    if pytorch_cuda:
        import torch
        print(f"\n🎯 Total GPU Devices Found: {torch.cuda.device_count()}")

        # Show CUDA cores summary
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            cores_per_sm, is_estimated = get_cuda_cores_per_sm(props.major, props.minor, props.name)
            total_cores = props.multi_processor_count * cores_per_sm

            if is_estimated:
                print(f"   GPU {i} ({props.name}): ~{total_cores:,} CUDA Cores (ESTIMATED)")
            else:
                print(f"   GPU {i} ({props.name}): {total_cores:,} CUDA Cores")

    print("\n🎯 Recommendations:")
    if not cuda_installed:
        print("   • Install NVIDIA drivers from: https://www.nvidia.com/drivers/")
    if not pytorch_cuda:
        print("   • Install PyTorch with CUDA: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    if not tensorflow_cuda:
        print("   • Install TensorFlow with CUDA: pip install tensorflow[and-cuda]")
    if not cupy_cuda:
        print("   • Install CuPy: pip install cupy-cuda11x (or cupy-cuda12x)")

    print("\n" + "=" * 60)
    print("✨ Script completed!")

if __name__ == "__main__":
    main()