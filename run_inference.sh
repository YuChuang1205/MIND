# base
CUDA_VISIBLE_DEVICES=0 python main.py \
    --data_root ./data/ScienceQA/data \
    --caption_file ./data/instruct_captions_qwen72b_ok.json \
    --model declare-lab/flan-alpaca-base \
    --user_msg rationale --img_type blip2_flant5_xxl \
    --bs 8 --eval_bs 8 --epoch 200 --start_epoch 0 --lr 8e-5 --output_len 512 --margin 0.2 --alpha 1 \
    --per_pos_neg 5  --topk 1 --phase1_cot_num 1001  \
    --use_caption --use_generate --final_eval --hardsamplemine --prompt_format QCM-E \
    --output_dir experiments_y_001 \
    --evaluate_dir experiments_y_001/rationale_declare-lab-flan-alpaca-base_blip2_flant5_xxl_QCM-E_lr8e-05_bs8_op512_ep200


CUDA_VISIBLE_DEVICES=0 python main.py \
    --data_root ./data/ScienceQA/data \
    --caption_file ./data/instruct_captions_qwen72b_ok.json \
    --model declare-lab/flan-alpaca-base \
    --user_msg rationale --img_type blip2_flant5_xxl \
    --bs 8 --eval_bs 8 --epoch 200 --start_epoch 50 --lr 8e-5 --output_len 512 \
    --phase2_cot_num 1001 --phase2_use_neg_input --phase2_use_pos_output --phase2_cot_out_choose_num 1001 \
    --use_caption --use_generate --prompt_format QCMG-AE \
    --output_dir experiments_y_001 \
    --eval_le experiments_y_001/rationale_declare-lab-flan-alpaca-base_blip2_flant5_xxl_QCM-E_lr8e-05_bs8_op512_ep200/predictions_ans_eval.json \
    --test_le experiments_y_001/rationale_declare-lab-flan-alpaca-base_blip2_flant5_xxl_QCM-E_lr8e-05_bs8_op512_ep200/predictions_ans_test.json \
    --evaluate_dir experiments_y_001/rationale_declare-lab-flan-alpaca-base_blip2_flant5_xxl_QCMG-AE_lr8e-05_bs8_op512_ep200
CUDA_VISIBLE_DEVICES=0 python test.py --size 60000 --gpus 1 --interval 0.01;


