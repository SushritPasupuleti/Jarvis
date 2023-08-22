from huggingface_hub import hf_hub_download 

downloaded_model_path = hf_hub_download(
    repo_id="openlm-research/open_llama_3b",
    filename="pytorch_model.bin",
    # use_auth_token=True
)
print("Path: ", downloaded_model_path)
