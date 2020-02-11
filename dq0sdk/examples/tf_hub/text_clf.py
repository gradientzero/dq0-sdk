





albert_module = hub.Module(
    "https://tfhub.dev/google/albert_base/2",
    trainable=True)
albert_inputs = dict(
    input_ids=input_ids,
    input_mask=input_mask,
    segment_ids=segment_ids)
albert_outputs = albert_module(albert_inputs, signature="tokens", as_dict=True)
pooled_output = albert_outputs["pooled_output"]
sequence_output = albert_outputs["sequence_output"]