import os
from torch.utils.data import Dataset
import os
import json
import numpy as np
import torch
from utils_prompt import *

img_shape = {
    "resnet": (512, 2048),
    "clip": (49, 2048),
    "detr": (100, 256),
    "vit": (145, 1024),
    "dinov2_giant": (257, 1536),
    "dinov2_large": (257, 1024),
    "blip_large": (577, 1024),
    "blip2_flant5_xl": (257, 1408),
    "blip2_flant5_xxl": (257, 1408),
    "clip_b16": (197, 768),
    "clip_l14_336": (577, 1024),
    "convnextv2_huge": (2816, 256),
    "sam_base": (256, 4096),
    "sam_large": (256, 4096),
    "sam_huge": (256, 4096),
}

def load_data_std(args):
    problems = json.load(open(os.path.join(args.data_root, 'scienceqa/multi_cot_merge_235B_V3_R1Q8B_R1_1000_1000_cleaning.json')))
    pid_splits = json.load(open(os.path.join(args.data_root, 'scienceqa/pid_splits.json')))
    captions = json.load(open(args.caption_file))["captions"]

    for qid in problems:
        problems[qid]['caption'] = captions[qid] if qid in captions else ""

    train_qids = pid_splits['%s' % (args.train_split)]
    val_qids = pid_splits['%s' % (args.val_split)]
    test_qids = pid_splits['%s' % (args.test_split)]
    print(f"number of train problems: {len(train_qids)}\n")
    print(f"number of val problems: {len(val_qids)}\n")
    print(f"number of test problems: {len(test_qids)}\n")

    qids = {'train': train_qids, 'val':val_qids,'test':test_qids}
    return problems, qids,

def load_data_img(args):
    problems = json.load(open(os.path.join(args.data_root, 'scienceqa/multi_cot_merge_235B_V3_R1Q8B_R1_1000_1000_cleaning.json')))
    pid_splits = json.load(open(os.path.join(args.data_root, 'scienceqa/pid_splits.json')))
    captions = json.load(open(args.caption_file))["captions"]
    name_maps = json.load(open('./data/name_map.json'))

    # check
    if args.img_type == "resnet":
        image_features = np.load('./vision_features/resnet.npy')
        image_features = np.expand_dims(image_features, axis=1)
        image_features = image_features.repeat(512, axis=1)
    elif args.img_type == "clip":
        image_features = np.load('./vision_features/clip.npy')
    elif args.img_type == "detr":
        image_features = np.load('./vision_features/detr.npy')
    elif args.img_type == "vit":
        image_features = torch.load("./vision_features/vit.pth")
    elif args.img_type == "dinov2_giant":
        image_features = torch.load("./vision_features/dinov2_giant.pth")
    elif args.img_type == "dinov2_large":
        image_features = torch.load("./vision_features/dinov2_large.pth")
    elif args.img_type == "blip_large":
        image_features = torch.load("./vision_features/blip_large.pth")
    elif args.img_type == "blip2_flant5_xl":
        image_features = torch.load("./vision_features/blip2_flant5_xl.pth")
    elif args.img_type == "blip2_flant5_xxl":
        image_features = torch.load("./vision_features/blip2_flant5_xxl.pth")
    elif args.img_type == "clip_b16":
        image_features = torch.load("./vision_features/clip_b16.pth")
    elif args.img_type == "clip_l14_336":
        image_features = torch.load("./vision_features/clip_l14_336.pth")
    elif args.img_type == "convnextv2_huge":
        image_features = torch.load("./vision_features/convnextv2_huge.pth")
    elif args.img_type == "sam_base":
        image_features = torch.load("./vision_features/sam_base.pth")
    elif args.img_type == "sam_large":
        image_features = torch.load("./vision_features/sam_large.pth")
    elif args.img_type == "sam_huge":
        image_features = torch.load("./vision_features/sam_huge.pth")
    else:
        image_features = np.load('./vision_features/detr.npy')
    print("img_features size: ", image_features.shape)

    for qid in problems:
        problems[qid]['caption'] = captions[qid] if qid in captions else ""

    train_qids = pid_splits['%s' % (args.train_split)]
    val_qids = pid_splits['%s' % (args.val_split)]
    test_qids = pid_splits['%s' % (args.test_split)]
    print(f"number of train problems: {len(train_qids)}\n")
    print(f"number of val problems: {len(val_qids)}\n")
    print(f"number of test problems: {len(test_qids)}\n")

    qids = {'train': train_qids, 'val':val_qids,'test':test_qids}
    return problems, qids, name_maps, image_features


class ScienceQADatasetStd(Dataset):
    def __init__(self, problems, qids, tokenizer, source_len, target_len, args, test_le=None):
        self.tokenizer = tokenizer
        self.problems = problems
        self.qids = qids
        self.source_len = source_len
        self.target_len = target_len
        self.args = args

        # Optional: test_le 对应的 lecture 预测结果
        if test_le is not None:
            self.test_le_data = json.load(open(test_le))["preds"]
        else:
            self.test_le_data = None

    def __len__(self):
        return len(self.qids)

    def __getitem__(self, index):
        qid = self.qids[index]
        problem = self.problems[qid]
        curr_le_data = self.test_le_data[index] if self.test_le_data is not None else None

        # 每次动态构造
        prompt, target = build_train_pair(self.problems, qid, self.args, curr_le_data)

        # 清理
        source_text = " ".join(prompt.strip().split())
        target_text = " ".join(target.strip().split())

        # 编码
        source = self.tokenizer.batch_encode_plus(
            [source_text],
            max_length=self.source_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        target = self.tokenizer.batch_encode_plus(
            [target_text],
            max_length=self.target_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        source_ids = source["input_ids"].squeeze()
        source_mask = source["attention_mask"].squeeze()
        target_ids = target["input_ids"].squeeze().tolist()

        return {
            "input_ids": source_ids,
            "attention_mask": source_mask,
            "labels": target_ids,
        }



class ScienceQADatasetImg(Dataset):
    def __init__(
        self, problems, qids, name_maps, tokenizer, source_len, target_len, args, image_features, test_le=None
    ):
        self.tokenizer = tokenizer
        self.problems = problems
        self.qids = qids
        self.name_maps = name_maps
        self.image_features = image_features
        self.source_len = source_len
        self.target_len = target_len
        self.args = args
        self.hardsamplemine = args.hardsamplemine
        self.test_le_data = None

        if test_le is not None:
            self.test_le_data = json.load(open(test_le))["preds"]

        self.img_shape = img_shape[args.img_type]
        self.image_cache = self._cache_image_features()

    def _cache_image_features(self):
        image_ids = []
        for qid in self.qids:
            if str(qid) in self.name_maps:
                vec = self.image_features[int(self.name_maps[str(qid)])]
                image_ids.append(torch.tensor(vec).float())
            else:
                image_ids.append(torch.zeros(self.img_shape, dtype=torch.float))
        return image_ids

    def __len__(self):
        return len(self.qids)

    def __getitem__(self, index):
        qid = self.qids[index]
        problem = self.problems[qid]
        curr_le_data = self.test_le_data[index] if self.test_le_data else None
        image_ids = self.image_cache[index]

        if self.hardsamplemine and curr_le_data is None:
            prompt, target, pos_targets, neg_targets = build_train_pair_new(
                self.problems, qid, self.args, curr_le_data
            )
        else:
            prompt, target = build_train_pair(self.problems, qid, self.args, curr_le_data)
            pos_targets, neg_targets = [], []

        # Tokenize input prompt
        prompt = " ".join(prompt.strip().split())
        source = self.tokenizer(
            prompt,
            max_length=self.source_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        source_ids = source["input_ids"].squeeze()
        source_mask = source["attention_mask"].squeeze()

        # Tokenize target
        target = " ".join(target.strip().split())
        tgt = self.tokenizer(
            target,
            max_length=self.target_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        target_ids = tgt["input_ids"].squeeze().tolist()

        # Hard mining case
        if self.hardsamplemine and curr_le_data is None:
            # 使用 tokenizer.batch_encode_plus 批量标记化
            pos_encodings = self.tokenizer.batch_encode_plus(
                pos_targets,
                max_length=self.target_len,
                padding="max_length",
                truncation=True,
                return_tensors="pt",
            )

            neg_encodings = self.tokenizer.batch_encode_plus(
                neg_targets,
                max_length=self.target_len,
                padding="max_length",
                truncation=True,
                return_tensors="pt",
            )


            # pos_target_ids = pos_encodings["input_ids"].squeeze().tolist()
            # neg_target_ids = neg_encodings["input_ids"].squeeze().tolist()
            pos_target_ids = pos_encodings["input_ids"].tolist()
            neg_target_ids = neg_encodings["input_ids"].tolist()
            # pos_target_ids = []
            # for pos_t in pos_targets:
            #     pos_t = " ".join(pos_t.strip().split())
            #     ids = self.tokenizer(
            #         pos_t,
            #         max_length=self.target_len,
            #         padding="max_length",
            #         truncation=True,
            #         return_tensors="pt",
            #     )["input_ids"].squeeze().tolist()
            #     pos_target_ids.append(ids)

            # neg_target_ids = []
            # for neg_t in neg_targets:
            #     neg_t = " ".join(neg_t.strip().split())
            #     ids = self.tokenizer(
            #         neg_t,
            #         max_length=self.target_len,
            #         padding="max_length",
            #         truncation=True,
            #         return_tensors="pt",
            #     )["input_ids"].squeeze().tolist()
            #     neg_target_ids.append(ids)

            return {
                "input_ids": source_ids,
                "attention_mask": source_mask,
                "image_ids": image_ids,
                "labels": target_ids,
                "pos_labels": pos_target_ids,
                "neg_labels": neg_target_ids,
            }

        return {
            "input_ids": source_ids,
            "attention_mask": source_mask,
            "image_ids": image_ids,
            "labels": target_ids,
        }
