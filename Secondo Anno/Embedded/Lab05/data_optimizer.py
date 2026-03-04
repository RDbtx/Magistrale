import os, struct


def q88_q17_converter(data: bytes) -> bytearray:
    """
    Converts Q8.8 input data to Q1.7 format. The function reads the input
    as signed int16 values, rescales from Q8.8 to Q1.7 by
    computing round(v / 2), saturates each result to the
    signed int8 representable range [-128, 127],
    and recreates the output as signed int8.

    Inputs:
    - data: raw bytes buffer containing 16-bit signed values (little-endian).

    Outputs:
    - out: a bytearray containing the converted 8-bit signed values.
    """

    out = bytearray()

    for (v,) in struct.iter_unpack('<h', data): #used to read the little endian 16 bit data
        if v >= 0:
            v = (v + 1) // 2
        else:
            v = -(((-v) + 1) // 2)

        # Saturate to signed int8 range
        if v > 127:
            v = 127
        elif v < -128:
            v = -128

        out.extend(struct.pack('b', v)) #converts the integer value v into one byte

    return out


def image_optimizer(image_16bit_bin: str, output_dir: str) -> None:
    """
    Optimizes an image .bin file for UART transmission by reducing it to 8-bit payload.
    The input file is assumed to be composed of 16-bit samples (two bytes per pixel).
    This function discards the MSB byte, since it is usually composed by only zeroes
    and keeps only the LSB byte of each 16-bit

    Inputs:
    - image_16bit_bin: path to the input image .bin file (16-bit samples).
    - output_dir: directory where the optimized file will be written.

    """
    os.makedirs(output_dir, exist_ok=True)
    out_name = os.path.basename(image_16bit_bin).replace(".bin", "_optimized.bin")

    with open(image_16bit_bin, "rb") as f:
        data = f.read()

    lsb = data[::2]
    msb = data[1::2]

    print(os.path.join(output_dir, out_name))
    with open(os.path.join(output_dir, out_name), "wb") as f:
        f.write(lsb)


def biases_optimizer(bias_file: str, output_dir: str) -> None:
    """
    Optimizes a bias .bin file by converting 16-bit signed
    values to 8-bit signed values in Q1.7 format. Each element is
    converted by clipping to [-128, 127] and storing it as int8.

    Inputs:
    - bias_file: path to the input bias .bin file (16-bit signed values).
    - output_dir: directory where the optimized file will be written.

    """
    os.makedirs(output_dir, exist_ok=True)
    out_name = os.path.basename(bias_file).replace(".bin", "_optimized.bin")

    with open(bias_file, "rb") as f:
        data = f.read()

    optimized_data = q88_q17_converter(data)

    with open(os.path.join(output_dir, out_name), "wb") as f:
        f.write(optimized_data)


def weights_optimizer(weight_file: str, output_dir: str) -> None:
    """
    Optimizes a weights .bin file by converting 16-bit signed
    values to 8-bit signed values in Q1.7 format. Each element is
    converted by clipping to [-128, 127] and storing it as int8.

    Inputs:
    - bias_file: path to the input bias .bin file (16-bit signed values).
    - output_dir: directory where the optimized file will be written.

    """
    os.makedirs(output_dir, exist_ok=True)
    out_name = os.path.basename(weight_file).replace(".bin", "_optimized.bin")

    with open(weight_file, "rb") as f:
        data = f.read()

    optimized_data = q88_q17_converter(data)

    with open(os.path.join(output_dir, out_name), "wb") as f:
        f.write(optimized_data)


if __name__ == "__main__":
    image_dir = "/Volumes/HDD Esterna/Progetti/PyCharm_Projects/blackboard/Embedded/images"
    biases_dir = "/Volumes/HDD Esterna/Progetti/PyCharm_Projects/blackboard/Embedded/biases"
    weight_dir = "/Volumes/HDD Esterna/Progetti/PyCharm_Projects/blackboard/Embedded/weights"

    image_out = os.path.join(image_dir, "output")
    biases_out = os.path.join(biases_dir, "output")
    weights_out = os.path.join(weight_dir, "output")

    for image in os.listdir(image_dir):
        if image.endswith(".bin"):
            image_optimizer(os.path.join(image_dir, image), image_out)

    for bias in os.listdir(biases_dir):
        if bias.endswith(".bin"):
            biases_optimizer(os.path.join(biases_dir, bias), biases_out)

    for weight in os.listdir(weight_dir):
        if weight.endswith(".bin"):
            weights_optimizer(os.path.join(weight_dir, weight), weights_out)

    biases_directory = "/Volumes/HDD Esterna/Progetti/PyCharm_Projects/blackboard/Embedded/biases/output"
    for bias in os.listdir(biases_directory):
        with open(os.path.join(biases_directory, bias), "rb") as f:
            data = f.read()
            print(f"{bias} = {len(data)}")

    weights_directory = "/Volumes/HDD Esterna/Progetti/PyCharm_Projects/blackboard/Embedded/weights/output"
    for weight in os.listdir(weights_directory):
        with open(os.path.join(weights_directory, weight), "rb") as f:
            data = f.read()
            print(f"{weight} = {len(data)}")
