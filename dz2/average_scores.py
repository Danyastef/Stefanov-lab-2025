def compute_average_scores(scores):
    if not all(0 <= grade <= 100 for score in scores for grade in score) or not 0 < len(scores) <= 100 or not 0 < len(scores[0]) <= 100:
        return 'Error'
    x = len(scores)
    n = len(scores[0])
    avg_scores = [0]*n
    for stundent in scores:
        for i in range(n):
            avg_scores[i] += stundent[i]
    for i in range(n):
        avg_scores[i] = round(avg_scores[i] / x, 1)
    return tuple(avg_scores)

if __name__ == "__main__":
    N, X = map(int, input().split())
    if 0 < N <= 100 and 0 < X <= 100:
        scores = []
        for i in range(X):
            scores_list = list(map(float, input().split()))
            if all(0 <= score <= 100 for score in scores_list):
                scores.append(tuple(scores_list))
            else:
                print('Error')
        avg_scores = compute_average_scores(scores)
        for score in avg_scores:
            print(score)
    else:
        print('Error')