def replace_known_datasets(code: str) -> str:
    known_datasets = {
        "iris": "scikit-learn/iris",
        "mnist": "mnist",
        "imdb": "imdb",
        "ag_news": "ag_news",
        "emotion": "dair-ai/emotion",
        "yelp": "yelp_polarity"
    }

    for short_name, full_name in known_datasets.items():
        code = code.replace(f"load_dataset('{short_name}')", f"load_dataset('{full_name}')")
        code = code.replace(f'load_dataset("{short_name}")', f'load_dataset("{full_name}")')
    return code
