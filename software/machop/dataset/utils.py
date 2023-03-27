import logging
import os

from .nlp import dataset_factory as nlp_dataset_factory
from .vision import build_dataset
from .vision import info as vision_dataset_info

logger = logging.getLogger(__name__)


def get_dataset(name, nlp_task_args={}):
    if name in ["cifar10", "cifar100", "imagenet"]:
        path = os.path.abspath(f"./data/{name}")
        train_dataset, _ = build_dataset(dataset_name=name, path=path, train=True)
        val_dataset, _ = build_dataset(dataset_name=name, path=path, train=False)
        test_dataset, _ = build_dataset(dataset_name=name, path=path, train=False)
        pred_dataset = None
    elif name in nlp_dataset_factory:
        # get dataset cls
        dataset_cls = nlp_dataset_factory[name]
        args = nlp_task_args
        # Classification style tasks
        if name in ["sst2", "SST2"]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = None
            pred_dataset = dataset_cls(split="test", **args)
        elif name in ["mnli", "MNLI"]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation_matched", **args)
            test_dataset = None
            pred_dataset = dataset_cls(split="test_matched", **args)
        elif name in ["qnli", "QNLI"]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = None
            pred_dataset = dataset_cls(split="test", **args)
        elif name in ["boolq", "BoolQ"]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = None
            pred_dataset = dataset_cls(split="test", **args)
        # Translation tasks
        elif name in [
            "iwslt2017_en_de",
            "IWSLT2017_EN_DE",
            "iwslt2017_de_en",
            "IWSLT2017_DE_EN",
            "iwslt2017_en_fr",
            "IWSLT2017_EN_FR",
            "iwslt2017_en_ch",
            "IWSLT2017_EN_CH",
            "wmt16_ro_en",
            "WMT16_RO_EN",
            "wmt19_de_en",
            "WMT19_DE_EN",
            "wmt19_zh_en",
            "WMT19_ZH_EN",
        ]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = dataset_cls(split="test", **args)
            pred_dataset = None
        # elif name in ["opus_en_fr", "OPUS_EN_FR"]:
        #     train_dataset = dataset_cls(split="train", **args)
        #     val_dataset = dataset_cls(split="validation", **args)
        #     test_dataset = dataset_cls(split="test", **args)

        elif name in ["multi30k", "MULTI30K"]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = dataset_cls(split="test", **args)
            pred_dataset = None
        # elif name in ["wmt16_ro_en", "WMT16_RO_EN"]:
        #     train_dataset = dataset_cls(split="train", **args)
        #     val_dataset = dataset_cls(split="validation", **args)
        #     test_dataset = dataset_cls(split="test", **args)
        #     pred_dataset = None
        # Language Modeling
        elif name in ["wikitext2", "WIKITEXT2", "wikitext103", "WIKITEXT103"]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = dataset_cls(split="test", **args)
            pred_dataset = None
        elif name in ["c4", "C4"]:
            logger.warning(
                "C4 dataset is realative large. The downloading and preproccesing may take a long time"
            )
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = None
            pred_dataset = dataset_cls(split="test", **args)
        elif name in ["ptb", "PTB"]:
            train_dataset = dataset_cls(split="train", **args)
            val_dataset = dataset_cls(split="validation", **args)
            test_dataset = dataset_cls(split="test", **args)
            pred_dataset = None
        # info = {"num_classes": train_dataset.num_classes}
    else:
        raise ValueError(f"Dataset {name} is not supported.")

    if test_dataset is None and pred_dataset is None:
        logger.info("Both the test dataset and pred dataset are not available")
    elif test_dataset is None:
        logger.info(
            "The test dataset is not available, but the pred dataset is available"
        )
    else:
        logger.info(
            "Ground truth labels are available in the test dataset. No pred dataset."
        )

    return train_dataset, val_dataset, test_dataset, pred_dataset


def get_dataset_info(name):
    if name in ["cifar10", "cifar100", "imagenet"]:
        info = vision_dataset_info[name]
    elif name in nlp_dataset_factory:
        # get dataset cls
        dataset_cls = nlp_dataset_factory[name]
        info = {"num_classes": getattr(dataset_cls, "num_classes", None)}
    else:
        raise ValueError(f"Dataset {name} is not supported")
    return info


available_datasets = [
    "cifar10",
    "cifar100",
    "imagenet",
    "sst2",
    "mnli",
    "qnli",
    "boolq",
    "iwslt2017_en_de",
    "iwslt2017_de_en",
    "iwslt2017_en_fr",
    "iwslt2017_en_ch",
    "wmt16_ro_en",
    "wmt19_de_en",
    "wmt19_zh_en",
    "multi30k",
    "wikitext2",
    "wikitext103",
    "c4",
    "ptb",
]
