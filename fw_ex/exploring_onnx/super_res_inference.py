from PIL import Image
import torchvision.transforms as transforms
import onnxruntime
import numpy as np

ort_session = onnxruntime.InferenceSession(
    "super_resolution.onnx", providers=["CPUExecutionProvider"]
)


def to_numpy(tensor):
    return (
        tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()
    )


print("Ort session ready. Processing image")

img = Image.open("./cat_224x224.jpg")

resize = transforms.Resize([224, 224])
img = resize(img)

img_ycbcr = img.convert("YCbCr")
img_y, img_cb, img_cr = img_ycbcr.split()
# Then we split the image into its Y, Cb, and Cr components.
# These components represent a grayscale image (Y), and the
# blue-difference (Cb) and red-difference (Cr)
# chroma components. The Y component being more sensitive to the human eye, we are interested in this component which we will be transforming. After extracting the Y component, we convert it to a tensor which will be the input of our model.

to_tensor = transforms.ToTensor()
img_y = to_tensor(img_y)
img_y.unsqueeze_(0)
print("Running the image through the ort_session")
ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(img_y)}
ort_outs = ort_session.run(None, ort_inputs)
img_out_y = ort_outs[0]
print("Constructing the image back")
img_out_y = Image.fromarray(np.uint8((img_out_y[0] * 255.0).clip(0, 255)[0]), mode="L")

# get the output image follow post-processing step from PyTorch implementation
final_img = Image.merge(
    "YCbCr",
    [
        img_out_y,
        img_cb.resize(img_out_y.size, Image.BICUBIC),
        img_cr.resize(img_out_y.size, Image.BICUBIC),
    ],
).convert("RGB")

# Save the image, we will compare this with the output image from mobile device
final_img.save("./cat_superres_with_ort.jpg")

# Save resized original image (without super-resolution)
img = transforms.Resize([img_out_y.size[0], img_out_y.size[1]])(img)
img.save("./cat_resized.jpg")
