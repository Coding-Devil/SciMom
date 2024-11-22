

# Zephyr 7B β 🤖
> The Zephyr 7B β is a next-gen GPT-like Large Language Model (LLM) fine-tuned from Mistral-7B-v0.1, containing 7 billion parameters. This model is optimized for educational tasks and excels at science-related Q&A with high accuracy and performance.

Trained using Ultrachat Feedbacks!
Quick & Smart: Handles easy to tough topics like a pro.
Accurate: Reliable answers every time.

### Built for my mom, with love ❤️.
---
# Model Card for Mistral 7B SFT β

This model is a fine-tuned version of [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) on the HuggingFaceH4/ultrachat_200k dataset. It is the SFT model that was used to train Zephyr-7B-β with Direct Preference Optimization.

It achieves the following results on the evaluation set:
- Loss: 0.9399

## Model description

- **Model type:** A 7B parameter GPT-like model fine-tuned on a mix of publicly available, synthetic datasets.
- **Language(s) (NLP):** Primarily English
- **License:** MIT
- **Finetuned from model:** [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1)

### Model Sources
- **Repository:** https://github.com/huggingface/alignment-handbook
---

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 8
- eval_batch_size: 16
- seed: 42
- distributed_type: multi-GPU
- num_devices: 16
- gradient_accumulation_steps: 4
- total_train_batch_size: 512
- total_eval_batch_size: 256
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 1

### Training results

| Training Loss | Epoch | Step | Validation Loss |
|:-------------:|:-----:|:----:|:---------------:|
| 0.9367        | 0.67  | 272  | 0.9397          |
