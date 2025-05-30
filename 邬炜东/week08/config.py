Config = {
    "model_path": "./model.bin",
    "train_data_path": "./data/train.json",
    "eval_data_path": "./data/valid.json",
    "schema_data_path": "./data/schema.json",
    "vocab_path": "chars.txt",
    "model_type": "bert",
    "max_length": 20,
    "hidden_size": 128,
    "kernel_size": 3,
    "num_layers": 4,
    "epochs": 15,
    "batch_size": 64,
    "pooling_style": "avg",
    "optimizer": "adam",
    "learning_rate": 1e-4,
    "pretrain_model_path": "../bert-base-chinese/bert-base-chinese",
    "seed": 987,
    "train_num": 512,
    "predict_num": 464
}
