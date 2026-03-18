'''
Adapted from https://github.com/lupantech/ScienceQA
'''

from dataclasses import dataclass
from typing import List, Optional
import random
import sys


def get_question_text(problem):
    question = problem['question'].replace("\n", "\\n")
    return question


def get_question_text_random(problem, max_choose_num=4, curr_le_data=None):
    if curr_le_data != None:
        question = problem['question'].replace("\n", "\\n")
    else:
        random_num = random.randint(0, max_choose_num - 1)
        if random_num == 0:
            question = problem['question'].replace("\n", "\\n")
        else:
            adjusted_question_name = 'adjusted_question_' + str(random_num)
            question = problem[adjusted_question_name].replace("\n", "\\n")
    return question


def get_context_text(problem, use_caption):
    txt_context = problem['hint']
    img_context = problem['caption'] if use_caption else ""
    context = " ".join([txt_context, img_context]).strip()
    if context == "":
        context = "N/A"
    return context


def get_context_text_random(problem, use_caption, max_choose_num=4, curr_le_data=None):
    img_context = problem['caption'] if use_caption else ""
    if curr_le_data != None:
        txt_context = problem['hint']
        context = " ".join([txt_context, img_context]).strip()

    else:
        random_num = random.randint(0, max_choose_num - 1)
        if random_num == 0:
            txt_context = problem['hint']
            context = " ".join([txt_context, img_context]).strip()
        else:
            adjusted_hint_name = 'adjusted_hint_' + str(random_num)
            hint = problem[adjusted_hint_name].replace("\n", "\\n")
            context = " ".join([hint, img_context]).strip()

    if context == "":
        context = "N/A"
    else:
        pass
    return context


def get_choice_text(probelm, options):
    choices = probelm['choices']
    choice_list = []
    for i, c in enumerate(choices):
        choice_list.append("({}) {}".format(options[i], c))
    choice_txt = " ".join(choice_list)
    # print(choice_txt)
    return choice_txt


def get_origin_answer(problem, options):
    return problem['choices'][problem['answer']]


def get_answer(problem, options):
    return options[problem['answer']]


def get_lecture_text(problem):
    # \\n: GPT-3 can generate the lecture with more tokens.
    lecture = problem['lecture'].replace("\n", "\\n")
    return lecture


def get_lecture_text_random(problem, max_choose_num=4, curr_le_data=None):
    # \\n: GPT-3 can generate the lecture with more tokens.
    if curr_le_data != None:
        lecture = problem['lecture'].replace("\n", "\\n")
    else:
        random_num = random.randint(0, max_choose_num - 1)
        if random_num == 0:
            lecture = problem['lecture'].replace("\n", "\\n")
        else:
            adjusted_lecture_name = 'adjusted_lecture_' + str(random_num)
            lecture = problem[adjusted_lecture_name].replace("\n", "\\n")
    return lecture


def get_solution_text(problem):
    # \\n: GPT-3 can generate the solution with more tokens
    solution = problem['solution'].replace("\n", "\\n")
    return solution


def get_solution_text_random(problem, max_choose_num=4, curr_le_data=None):
    # \\n: GPT-3 can generate the solution with more tokens
    if curr_le_data != None:
        solution = problem['solution'].replace("\n", "\\n")
    else:
        random_num = random.randint(0, max_choose_num - 1)
        if random_num == 0:
            solution = problem['solution'].replace("\n", "\\n")
        else:
            adjusted_solution_name = 'adjusted_solution_' + str(random_num)
            solution = problem[adjusted_solution_name].replace("\n", "\\n")
    return solution


def get_solution_text_random_add_neg(problem, max_choose_num=4, curr_le_data=None):
    if curr_le_data != None:
        solution = problem['solution'].replace("\n", "\\n")
    else:
        Flag_pos = True
        random_num = random.randint(0, max_choose_num - 1)
        random_pos_neg = random.random()
        if random_num == 0:
            solution = problem['solution'].replace("\n", "\\n")
        else:
            if random_pos_neg<0.5:
                adjusted_solution_name = 'adjusted_solution_' + str(random_num)
                solution = problem[adjusted_solution_name].replace("\n", "\\n")
            else:
                neg_solution_name = 'neg_solution_' + str(random_num)
                solution = problem[neg_solution_name].replace("\n", "\\n")
                Flag_pos = False
    return solution, Flag_pos


def get_solution_text_random_only_neg(problem, max_choose_num=4, curr_le_data=None):
    if curr_le_data != None:
        solution = problem['solution'].replace("\n", "\\n")
    else:
        Flag_pos = True
        random_num = random.randint(0, max_choose_num - 1)
        random_pos_neg = random.random()
        if random_num == 0:
            solution = problem['solution'].replace("\n", "\\n")
        else:
            if random_pos_neg<0:
                adjusted_solution_name = 'adjusted_solution_' + str(random_num)
                solution = problem[adjusted_solution_name].replace("\n", "\\n")
            else:
                neg_solution_name = 'neg_solution_' + str(random_num)
                solution = problem[neg_solution_name].replace("\n", "\\n")
                Flag_pos = False
    return solution, Flag_pos


def get_solutions_pos_neg_random(problem, test_choose_num=10):
    choose_unique_number_1 = random.sample(range(1, 1001), test_choose_num)
    choose_unique_number_2 = random.sample(range(1, 1001), test_choose_num)
    pos_solutions = []
    neg_solutions = []
    for i in choose_unique_number_1:
        pos_solution_name = 'adjusted_solution_' + str(i)
        pos_solution = problem[pos_solution_name].replace("\n", "\\n")
        pos_solutions.append(pos_solution)
    for j in choose_unique_number_2:
        neg_solution_name = 'neg_solution_' + str(j)
        neg_solution = problem[neg_solution_name].replace("\n", "\\n")
        neg_solutions.append(neg_solution)
    return pos_solutions, neg_solutions



def create_one_example(format, question, context, choice, answer, lecture, solution, test_example=True,
                       WithOutput=False, curr_le_data=None):
    input_format, output_format = format.split("-")

    ## Inputs
    if input_format == "CQM":
        input = f"Context: {context}\nQuestion: {question}\nOptions: {choice}\n"
    elif input_format == "QCM":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\n"
    elif input_format == "QM":
        input = f"Question: {question}\nOptions: {choice}\n"
    elif input_format == "QC":
        input = f"Question: {question}\nContext: {context}\n"
    elif input_format == "QCMG":
        if curr_le_data is not None:
            input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nLecture: {lecture}\nSolution: {curr_le_data}\n"
        else:
            input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nLecture: {lecture}\nSolution: {solution}\n"
    elif input_format == "CQMG":
        if curr_le_data is not None:
            input = f"Context: {context}\nQuestion: {question}\nOptions: {choice}\n{curr_le_data}\n"
        else:
            input = f"Context: {context}\nQuestion: {question}\nOptions: {choice}\nSolution: {lecture} {solution}\n"
    # upper bound experiment
    elif input_format == "QCML":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {lecture}\n"
    elif input_format == "QCME":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {solution}\n"
    elif input_format == "QCMLE":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {lecture} {solution}\n"

    elif input_format == "QCLM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {lecture}\nOptions: {choice}\n"
    elif input_format == "QCEM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {solution}\nOptions: {choice}\n"
    elif input_format == "QCLEM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {lecture} {solution}\nOptions: {choice}\n"
    elif input_format == "QCMA":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nAnswer: The answer is {answer}.\n"
    elif input_format == "QCA":
        input = f"Question: {question}\nContext: {context}\nAnswer: The answer is {answer}. \nBECAUSE:"

    # Outputs
    if test_example:
        if output_format == 'A':
            output = "Answer:"
        elif output_format == 'E':
            output = "Solution:"
        else:
            output = "Solution:"
    elif output_format == 'A':
        output = f"Answer: The answer is {answer}."

    elif output_format == 'AE':
        output = f"Answer: The answer is {answer}. BECAUSE: {solution}"
    elif output_format == 'AL':
        output = f"Answer: The answer is {answer}. BECAUSE: {lecture}"
    elif output_format == 'ALE':
        output = f"Answer: The answer is {answer}. BECAUSE: {lecture} {solution}"
    elif output_format == 'AEL':
        output = f"Answer: The answer is {answer}. BECAUSE: {solution} {lecture}"

    elif output_format == 'LA':
        output = f"Answer: {lecture} The answer is {answer}."
    elif output_format == 'EA':
        output = f"Answer: {solution} The answer is {answer}."
    elif output_format == 'LEA':
        output = f"Answer: {lecture} {solution} The answer is {answer}."
    elif output_format == 'ELA':
        output = f"Answer: {solution} {lecture} The answer is {answer}."

    elif output_format == 'LE':
        output = f"Solution: {lecture} {solution}."

    elif output_format == 'E':
        output = f"Solution: {solution}"

    if WithOutput:
        if output.endswith("BECAUSE:"):
            output = output.replace("BECAUSE:", "").strip()
        if output_format == 'E':
            text = input + f'Solution:'
        elif output_format == 'A':
            text = input + f'Answer:'
        elif output_format == 'AE':
            text = input + f'Answer + Solution:'
        else:
            text = input + f'Solution:'
        text = text.replace("  ", " ").strip()
        output = output.replace("  ", " ").strip()
        return text, output

    text = input + output
    text = text.replace("  ", " ").strip()
    if text.endswith("BECAUSE:"):
        text = text.replace("BECAUSE:", "").strip()
    return text



def create_one_example_output_pos(format, question, context, choice, answer, lecture, solution, solution_phase2_pos_out,test_example=True,
                       WithOutput=False, curr_le_data=None):
    input_format, output_format = format.split("-")

    ## Inputs
    if input_format == "CQM":
        input = f"Context: {context}\nQuestion: {question}\nOptions: {choice}\n"
    elif input_format == "QCM":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\n"
    elif input_format == "QM":
        input = f"Question: {question}\nOptions: {choice}\n"
    elif input_format == "QC":
        input = f"Question: {question}\nContext: {context}\n"
    elif input_format == "QCMG":
        if curr_le_data is not None:
            input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nLecture: {lecture}\nSolution: {curr_le_data}\n"
        else:
            input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nLecture: {lecture}\nSolution: {solution}\n"
    elif input_format == "CQMG":
        if curr_le_data is not None:
            input = f"Context: {context}\nQuestion: {question}\nOptions: {choice}\n{curr_le_data}\n"
        else:
            input = f"Context: {context}\nQuestion: {question}\nOptions: {choice}\nSolution: {lecture} {solution}\n"
    # upper bound experiment
    elif input_format == "QCML":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {lecture}\n"
    elif input_format == "QCME":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {solution}\n"
    elif input_format == "QCMLE":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {lecture} {solution}\n"

    elif input_format == "QCLM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {lecture}\nOptions: {choice}\n"
    elif input_format == "QCEM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {solution}\nOptions: {choice}\n"
    elif input_format == "QCLEM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {lecture} {solution}\nOptions: {choice}\n"
    elif input_format == "QCMA":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nAnswer: The answer is {answer}.\n"
    elif input_format == "QCA":
        input = f"Question: {question}\nContext: {context}\nAnswer: The answer is {answer}. \nBECAUSE:"

    # Outputs
    if test_example:
        if output_format == 'A':
            output = "Answer:"
        elif output_format == 'E':
            output = "Solution:"
        else:
            output = "Solution:"
    elif output_format == 'A':
        output = f"Answer: The answer is {answer}."

    elif output_format == 'AE':
        output = f"Answer: The answer is {answer}. BECAUSE: {solution_phase2_pos_out}"
    elif output_format == 'AL':
        output = f"Answer: The answer is {answer}. BECAUSE: {lecture}"
    elif output_format == 'ALE':
        output = f"Answer: The answer is {answer}. BECAUSE: {lecture} {solution_phase2_pos_out}"
    elif output_format == 'AEL':
        output = f"Answer: The answer is {answer}. BECAUSE: {solution_phase2_pos_out} {lecture}"

    elif output_format == 'LA':
        output = f"Answer: {lecture} The answer is {answer}."
    elif output_format == 'EA':
        output = f"Answer: {solution_phase2_pos_out} The answer is {answer}."
    elif output_format == 'LEA':
        output = f"Answer: {lecture} {solution_phase2_pos_out} The answer is {answer}."
    elif output_format == 'ELA':
        output = f"Answer: {solution_phase2_pos_out} {lecture} The answer is {answer}."

    elif output_format == 'LE':
        output = f"Solution: {lecture} {solution_phase2_pos_out}."

    elif output_format == 'E':
        output = f"Solution: {solution_phase2_pos_out}"

    if WithOutput:
        if output.endswith("BECAUSE:"):
            output = output.replace("BECAUSE:", "").strip()
        # if output.endswith("BECAUSE: """):
        #     output = output.replace("BECAUSE: """, "").strip()
        if output_format == 'E':
            text = input + f'Solution:'
        elif output_format == 'A':
            text = input + f'Answer:'
        elif output_format == 'AE':
            text = input + f'Answer + Solution:'
        else:
            text = input + f'Solution:'
        text = text.replace("  ", " ").strip()
        output = output.replace("  ", " ").strip()
        return text, output

    text = input + output
    text = text.replace("  ", " ").strip()
    if text.endswith("BECAUSE:"):
        text = text.replace("BECAUSE:", "").strip()
    return text


def build_prompt(problems, shot_qids, test_qid, args):
    examples = []

    # n-shot training examples
    for qid in shot_qids:
        question = get_question_text(problems[qid])
        context = get_context_text(problems[qid], args.use_caption)
        choice = get_choice_text(problems[qid], args.options)
        answer = get_answer(problems[qid], args.options)
        lecture = get_lecture_text(problems[qid])
        solution = get_solution_text(problems[qid])

        train_example = create_one_example(args.prompt_format,
                                           question,
                                           context,
                                           choice,
                                           answer,
                                           lecture,
                                           solution,
                                           test_example=False)
        examples.append(train_example)

    # test example
    question = get_question_text(problems[test_qid])
    context = get_context_text(problems[test_qid], args.use_caption)
    choice = get_choice_text(problems[test_qid], args.options)
    answer = get_answer(problems[test_qid], args.options)
    lecture = get_lecture_text(problems[test_qid])
    solution = get_solution_text(problems[test_qid])

    test_example = create_one_example(args.prompt_format,
                                      question,
                                      context,
                                      choice,
                                      answer,
                                      lecture,
                                      solution,
                                      test_example=True)
    examples.append(test_example)

    # create the prompt input
    prompt_input = '\n\n'.join(examples)

    return prompt_input


def build_train_pair(problems, test_qid, args, curr_le_data=None):
    phase2_cot_num = args.phase2_cot_num
    examples = []
    if curr_le_data==None:
        # test example
        question = get_question_text_random(problems[test_qid], max_choose_num=1, curr_le_data=curr_le_data)   ##当max_choose_num=1时就是只用原始的
        context = get_context_text_random(problems[test_qid], args.use_caption, max_choose_num=1, curr_le_data=curr_le_data)   ##当max_choose_num=1时就是只用原始的
        lecture = get_lecture_text_random(problems[test_qid], max_choose_num=1, curr_le_data=curr_le_data)   ##当max_choose_num=1时就是只用原始的
        if args.phase2_use_neg_input:
            solution,Flag_pos = get_solution_text_random_add_neg(problems[test_qid], max_choose_num=phase2_cot_num, curr_le_data=curr_le_data)  ##当max_choose_num=1时就是只用原始的
            #solution_phase2_pos_out = get_solution_text_random(problems[test_qid],max_choose_num=args.phase2_cot_out_choose_num,curr_le_data=curr_le_data)
            if args.phase2_only_pos_have_rationale:
                if Flag_pos:
                    solution_phase2_pos_out = "The input solution is correct! The solution is " + solution
                else:
                    solution_phase2_pos_out = "The input solution is incorrect!"

            elif args.phase2_only_neg_have_rationale:
                if Flag_pos:
                    solution_phase2_pos_out = "The input solution is correct!"
                else:
                    solution_phase2_pos_out = "The input solution is incorrect! The correct one is as follows: \n" + get_solution_text_random(problems[test_qid],
                                                                    max_choose_num=args.phase2_cot_out_choose_num,
                                                                    curr_le_data=curr_le_data)
            else:
                if Flag_pos:
                    solution_phase2_pos_out = "The input solution is correct! The solution is " + solution
                else:
                    solution_phase2_pos_out = "The input solution is incorrect! The correct one is as follows: \n" + get_solution_text_random(problems[test_qid],
                                                                    max_choose_num=args.phase2_cot_out_choose_num,
                                                                    curr_le_data=curr_le_data)

        elif args.phase2_use_neg_input_only:
            solution,Flag_pos = get_solution_text_random_only_neg(problems[test_qid], max_choose_num=phase2_cot_num, curr_le_data=curr_le_data)  ##当max_choose_num=1时就是只用原始的
            #solution_phase2_pos_out = get_solution_text_random(problems[test_qid],max_choose_num=args.phase2_cot_out_choose_num,curr_le_data=curr_le_data)
            if Flag_pos:
                    solution_phase2_pos_out = "The input solution is correct!"
            else:
                solution_phase2_pos_out = "The input solution is incorrect! The correct one is as follows: \n" + get_solution_text_random(problems[test_qid],
                                                                max_choose_num=args.phase2_cot_out_choose_num,
                                                                curr_le_data=curr_le_data)
        
        else:
            solution = get_solution_text_random(problems[test_qid], max_choose_num=phase2_cot_num, curr_le_data=curr_le_data)   ##当max_choose_num=1时就是只用原始的
            solution_phase2_pos_out = "The input solution is correct! The solution is " + solution
            #solution_phase2_pos_out = solution

    else:
        # test example
        question = get_question_text(problems[test_qid])
        context = get_context_text(problems[test_qid], args.use_caption)
        lecture = get_lecture_text(problems[test_qid])
        solution = get_solution_text(problems[test_qid])
        solution_phase2_pos_out = "The input solution is correct! The solution is " + solution

    choice = get_choice_text(problems[test_qid], args.options)
    answer_option = get_answer(problems[test_qid], args.options)
    answer = "(" + answer_option + ")"
    if args.phase2_use_pos_output == False :
        test_example, target = create_one_example(args.prompt_format,
                                                  question,
                                                  context,
                                                  choice,
                                                  answer,
                                                  lecture,
                                                  solution,
                                                  test_example=False, WithOutput=True, curr_le_data=curr_le_data)
    
    # elif args.phase2_use_neg_input==False and args.phase2_use_neg_input_only==False and args.phase2_use_pos_output ==True:
    #     print("when phase2_use_pos_output ==True, phase2_use_neg_input should be True!!!")
    #     sys.exit(0)

    else:
        test_example, target = create_one_example_output_pos(args.prompt_format,
                                                  question,
                                                  context,
                                                  choice,
                                                  answer,
                                                  lecture,
                                                  solution,
                                                  solution_phase2_pos_out,
                                                  test_example=False, WithOutput=True, curr_le_data=curr_le_data)

    examples.append(test_example)

    target = target.replace("Answer:", "").strip()
    # create the prompt input
    prompt_input = '\n\n'.join(examples)

    return prompt_input, target



def build_train_pair_new(problems, test_qid, args, curr_le_data=None):
    examples = []
    per_pos_neg = args.per_pos_neg
    phase1_cot_num = args.phase1_cot_num

    if curr_le_data == None:
        input_format, output_format = args.prompt_format.split("-")
        # test example
        question = get_question_text_random(problems[test_qid], max_choose_num=1,
                                            curr_le_data=curr_le_data)  ##当max_choose_num=1 use origin
        context = get_context_text_random(problems[test_qid], args.use_caption, max_choose_num=1,
                                          curr_le_data=curr_le_data)  ##当max_choose_num=1 use origin
        lecture = get_lecture_text_random(problems[test_qid], max_choose_num=1,
                                          curr_le_data=curr_le_data)  ##当max_choose_num=1 use origin
        solution = get_solution_text_random(problems[test_qid], max_choose_num=phase1_cot_num,
                                            curr_le_data=curr_le_data)  ##当max_choose_num=1 use origin
        choice = get_choice_text(problems[test_qid], args.options)
        answer_option = get_answer(problems[test_qid], args.options)
        answer = "(" + answer_option + ")"

        test_example, target = create_one_example(args.prompt_format,
                                                  question,
                                                  context,
                                                  choice,
                                                  answer,
                                                  lecture,
                                                  solution,
                                                  test_example=False, WithOutput=True, curr_le_data=curr_le_data)
        examples.append(test_example)
        target = target.replace("Answer:", "").strip()
        # create the prompt input
        prompt_input = '\n\n'.join(examples)

        pos_targets = []
        neg_targets = []
        if output_format == 'E' and args.hardsamplemine == True:
            pos_solutions, neg_solutions = get_solutions_pos_neg_random(problems[test_qid], test_choose_num=per_pos_neg)
            for i in range(len(pos_solutions)):
                pos_targets.append(f"Solution: {pos_solutions[i]}")
            for i in range(len(neg_solutions)):
                neg_targets.append(f"Solution: {neg_solutions[i]}")
            return prompt_input, target,pos_targets, neg_targets
        else:
            return prompt_input, target

    else:
        # test example
        question = get_question_text(problems[test_qid])
        context = get_context_text(problems[test_qid], args.use_caption)
        lecture = get_lecture_text(problems[test_qid])
        solution = get_solution_text(problems[test_qid])
        choice = get_choice_text(problems[test_qid], args.options)
        answer_option = get_answer(problems[test_qid], args.options)
        answer = "(" + answer_option + ")"
        test_example, target = create_one_example(args.prompt_format,
                                                  question,
                                                  context,
                                                  choice,
                                                  answer,
                                                  lecture,
                                                  solution,
                                                  test_example=False, WithOutput=True, curr_le_data=curr_le_data)
        examples.append(test_example)

        target = target.replace("Answer:", "").strip()
        # create the prompt input
        prompt_input = '\n\n'.join(examples)

        return prompt_input, target

@dataclass(frozen=True)
class InputFeatures:
    """
    A single set of features of data.
    Property names are the same names as the corresponding inputs to a model.
    """

    input_ids: List[List[int]]
    attention_mask: Optional[List[List[int]]]
    token_type_ids: Optional[List[List[int]]]
    le_input_ids: List[List[int]]
    le_attention_mask: Optional[List[List[int]]]
    le_token_type_ids: Optional[List[List[int]]]
    label: Optional[int]
