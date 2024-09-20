def extract_scores(results, finalResults):
    for result in results:

        question = result["example"].inputs["question"]
        evaluators_results = result["evaluation_results"]["results"]

        for eval_result in evaluators_results:
            evaluator = eval_result.key
            score = eval_result.score

            finalResults.setdefault(evaluator, []).append(
                {
                    question: score
                }
            ) 