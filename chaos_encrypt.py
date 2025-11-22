from PIL import Image
import numpy as np

def logistic_map(x0, r, length):
    x = [x0]
    for _ in range(length - 1):
        x.append(r * x[-1] * (1 - x[-1]))
    return np.array(x)

def tent_map(x0, mu, length):
    x = [x0]
    for _ in range(length - 1):
        if x[-1] < mu:
            x.append(x[-1] / mu)
        else:
            x.append((1 - x[-1]) / (1 - mu))
    return np.array(x)

def chebyshev_map(x0, k, length):
    x = [x0]
    for _ in range(length - 1):
        x.append(np.cos(k * np.arccos(np.clip(x[-1], -1, 1))))
    return np.array(x)

def encrypt_image(img_path,
                  logistic_params=(0.5, 3.99),
                  tent_params=(0.5, 0.7),
                  cheb_params=(0.5, 2)):
    # Step 1: Load image and show shape
    img = Image.open(img_path).convert('L')
    img_array = np.array(img)
    pixels = img_array.flatten()
    length = len(pixels)
    print("\nEncryption Info:")
    print(f"Image shape: {img_array.shape}")        # Example: (256, 256)
    print(f"Logistic map parameters: {logistic_params}")
    print(f"Tent map parameters: {tent_params}")
    print(f"Chebyshev map parameters: {cheb_params}\n")

    # Step 2: Generate chaotic sequences
    log_seq = logistic_map(*logistic_params, length)
    tent_seq = tent_map(*tent_params, length)
    cheb_seq = chebyshev_map(*cheb_params, length)

    # Step 3 & 4: Permutation key and pixel shuffle
    perm_key = np.argsort(log_seq + tent_seq + cheb_seq)
    permuted_pixels = pixels[perm_key]

    # Step 5 & 6: Diffusion key and pixel masking
    diff_key = ((log_seq + tent_seq + cheb_seq) * 255) % 256
    diff_key = diff_key.astype('uint8')
    encrypted_pixels = np.bitwise_xor(permuted_pixels, diff_key)

    encrypted_img_array = encrypted_pixels.reshape(img_array.shape)
    encrypted_img = Image.fromarray(encrypted_img_array)
    encrypted_img.save('encrypted_image.png')
    print("Encrypted image saved as 'encrypted_image.png'")
    print("Record the image shape and ALL parameters for decryption.\n")
    return 'encrypted_image.png', img_array.shape

# Usage example:
encrypt_image('example.png')
