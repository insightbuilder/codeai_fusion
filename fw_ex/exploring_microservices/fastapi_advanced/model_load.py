import torch
from transformers import BertTokenizer, BertModel
import onnx
from onnxruntime_tools import optimizer
from onnxruntime_tools.transformers.onnx_model_bert import BertOptimizationOptions
import onnxruntime as ort

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
print("Model download started")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()

print("Model conversion started")

dummy_text = "Lets push sentences into model"
inputs = tokenizer(dummy_text, return_tensors="pt")

dummy_input_ids = inputs["input_ids"]
dummy_attn_masks = inputs["attention_mask"]

torch.onnx.export(
    model,
    (dummy_input_ids, dummy_attn_masks),
    "bert_model.onnx",
    input_names=["input_ids", "attention_mask"],
    output_names=["last_hidden_state", "pooler_output"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "last_hidden_state": {0: "batch_size", 1: "sequence_length"},
        "pooler_output": {0: "batch_size"},
    },
    opset_version=14,
)

print("Model converted to onnx")

onnx_load = onnx.load("bert_model.onnx")

onnx.checker.check_model(onnx_load)

print("Model is ready to use...")

# optimize = BertOptimizationOptions("bert")
# optimize.enable_embed_layer_norm = False

# optimized_model_path = optimizer.optimize_model(
#     "bert_model.onnx", model_type="bert", optimization_options=optimize, use_gpu=False
# ).model_path

# print(f"Model saved after optimization: {optimized_model_path}")
# print("loading model for inference in the runtime")

onnx_session = ort.InferenceSession("bert_model.onnx")

input_onnx = {
    "input_ids": dummy_input_ids.numpy(),
    "attention_mask": dummy_attn_masks.numpy(),
}

print("starting inference")

outputs = onnx_session.run(None, input_onnx)

print(f"Infered output: {outputs}")
