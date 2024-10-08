import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # TODO) Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # TODO) Plot midterm/final scores as points
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)  # 첫 번째 서브플롯
    plt.scatter(midterm_kr, final_kr, color='red', label='Korean',marker='.')
    plt.scatter(midterm_en, final_en, color='blue', label='English',marker='+')
    plt.xlabel('Midterm Score')
    plt.ylabel('Final Score')
    plt.grid()
    plt.xticks(range(0, int(max(midterm_kr + midterm_en)) + 20, 20))  # x축 눈금 20 간격
    plt.yticks(range(0, int(max(final_kr + final_en)) + 20, 20))      # y축 눈금 20 간격
    plt.xlim(0, 125)
    plt.ylim(0, 100)
    plt.legend()

    # TODO) Plot total scores as a histogram
    plt.subplot(1, 2, 2)  # 두 번째 서브플롯
    plt.hist(total_kr, bins=range(0,101,5), color='#FF0000', label='Korean')
    plt.hist(total_en, bins=range(0,101,5), color='#0000FF', alpha=0.3, label='English')
    plt.xlabel('Total Scores')
    plt.ylabel('The number of students')
    plt.xlim(0, 100)
    plt.ylim(0, None)
    plt.legend()

    plt.show()