from NoKeeA.UI import start_ui
from huggingface_hub import snapshot_download


def main():
    """Start the NoKeeA application"""
    snapshot_download(repo_id="Salesforce/blip2-opt-2.7b",
                      local_dir="blip2_model")

    start_ui()


if __name__ == "__main__":
    main()
