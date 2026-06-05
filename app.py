import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

font_path = "NanumGothic.ttf"

def get_disposable_item_car_usage_input():

    return {    
        '플라스틱 컵': st.number_input('플라스틱 컵 사용 횟수', 0, 100, 0),
        '비닐봉투': st.number_input('비닐봉투 사용 횟수', 0, 100, 0),
        '나무젓가락': st.number_input('나무젓가락 사용 횟수', 0, 100, 0),
        '빨대': st.number_input('빨대 사용 횟수', 0, 100, 0),
        '일회용 용기': st.number_input('일회용 용기 사용 횟수', 0, 100, 0),
        '기타 일회용품': st.number_input('기타 일회용품 사용 횟수', 0, 100, 0),
        '자가용': st.number_input('오늘 자가용 이용 횟수', 0, 100, 0)
    }

def get_public_transport_input():
    return st.checkbox(
        "오늘 대중교통을 이용했나요?"
    )

def get_meat_consumption_input():

    ate_meat_today = st.checkbox(
        "오늘 육류를 섭취했나요?"
    )

    meat_counts = {
        '소고기': 0,
        '돼지고기': 0,
        '닭고기': 0,
        '기타': 0
    }

    if ate_meat_today:

        meat_counts['소고기'] = st.number_input(
            "소고기 섭취 횟수 (100g당 1회)",
            0, 20, 0
        )

        meat_counts['돼지고기'] = st.number_input(
            "돼지고기 섭취 횟수 (100g당 1회)",
            0, 20, 0
        )

        meat_counts['닭고기'] = st.number_input(
            "닭고기 섭취 횟수 (100g당 1회)",
            0, 20, 0
        )

        meat_counts['기타'] = st.number_input(
            "기타 육류 섭취 횟수 (100g당 1회)",
            0, 20, 0
        )

    return meat_counts

# Function to collect user input for recycling habits
def get_recycling_input():
    return st.checkbox(
        "오늘 분리수거을 제대로 했나요?"
    )

# Modified function to calculate the carbon footprint score with differentiated meat scores and counts
def calculate_carbon_footprint(disposable_items_counts, car_usage_count, used_public_transport, meat_counts, recycled):
    score = 0
    contributions = {}

    # Scoring logic for disposable items
    disposable_item_score_map = {
        '플라스틱 컵': 15, 
        '비닐봉투': 10,  
        '나무젓가락': 5, 
        '빨대': 5,      
        '일회용 용기': 15, 
        '기타 일회용품': 10, 
        '자가용': 10
    }

    total_disposable_car_contribution = 0
    for item_type, count in disposable_items_car_usage_counts.items():
        if count > 0:
            current_disposable_contribution = disposable_item_score_map.get(item_type, 0) * count
            total_disposable_contribution += current_disposable_contribution


    score += total_disposable_car_contribution

    # 대중교통 이용 시 10점 감소 (긍정적 요소)
    public_transport_contribution = -10 if used_public_transport else 0
    score += public_transport_contribution
    contributions['Public Transport Usage'] = public_transport_contribution

    # 육류 종류에 따라 점수 차등 부여 및 횟수 반영
    meat_score_map = {
        '소고기': 27, # 소고기는 탄소 발자국이 가장 높음
        '돼지고기': 12,
        '닭고기': 7,  # 닭고기는 탄소 발자국이 상대적으로 낮음
        '기타': int((20 + 10 + 5) / 3) # 평균 점수 부여
    }

    total_meat_contribution = 0
    for meat_type, count in meat_counts.items():
        if count > 0: # Only add if consumed
            current_meat_contribution = meat_score_map.get(meat_type, 0) * count
            total_meat_contribution += current_meat_contribution
            # Update contributions with English labels
            if meat_type == '소고기':
                contributions[f'Meat Consumption (Beef)'] = current_meat_contribution
            elif meat_type == '돼지고기':
                contributions[f'Meat Consumption (Pork)'] = current_meat_contribution
            elif meat_type == '닭고기':
                contributions[f'Meat Consumption (Chicken)'] = current_meat_contribution
            elif meat_type == '기타':
                contributions[f'Meat Consumption (Other)'] = current_meat_contribution

    score += total_meat_contribution

    # 재활용 시 5점 감소 (긍정적 요소)
    recycling_contribution = -5 if recycled else 0
    score += recycling_contribution
    contributions['Recycling'] = recycling_contribution

    return score, contributions


# Main function to run the calculator
def run_calculator():
    st.title("🌱 탄소 발자국 계산기")

    disposable_items_car_usage_counts = get_disposable_item_input()
    used_public_transport = get_public_transport_input()
    meat_counts = get_meat_consumption_input()
    recycled = get_recycling_input()

    if st.button("탄소 발자국 계산"):

        carbon_score, contributions = calculate_carbon_footprint(
            disposable_items_car_usage_counts,
            used_public_transport,
            meat_counts,
            recycled
        )

        st.metric(
            "오늘의 탄소 발자국 점수",
            carbon_score
        )

        if carbon_score <= 20:
            feedback_message = "훌륭합니다! 오늘 탄소 발자국이 매우 낮습니다. 환경을 위한 노력을 지속해주세요."
        elif carbon_score <= 50:
            feedback_message = "좋은 노력을 하고 계십니다! 조금 더 탄소 발자국을 줄일 수 있는 방법을 찾아보세요."
        elif carbon_score <= 80:
            feedback_message = "탄소 발자국을 줄이기 위해 몇 가지 변화를 고려해 볼 수 있습니다. 예를 들어 대중교통 이용, 육류 섭취 줄이기 등이 있습니다."
        else:
            feedback_message = "탄소 발자국을 줄이기 위한 적극적인 노력이 필요합니다. 생활 습관을 점검해 보세요."

        

        plot_carbon_footprint(
            carbon_score,
            feedback_message
        )

def plot_carbon_footprint(carbon_score, feedback_message):

    fig, ax = plt.subplots(figsize=(10, 2))

    # 구간 색상
    ax.barh(
        y=0,
        width=20,
        left=0,
        color="green"
    )

    ax.barh(
        y=0,
        width=30,
        left=20,
        color="yellow"
    )

    ax.barh(
        y=0,
        width=30,
        left=50,
        color="orange"
    )

    ax.barh(
        y=0,
        width=40,
        left=80,
        color="red"
    )


    # 점수 화살표 범위 제한
    display_score = max(0, min(carbon_score, 120))
    
    # 현재 점수 화살표 표시    
    ax.annotate(
    f"{carbon_score}점",
    xy=(display_score, 0),
    xytext=(display_score, 0.3),
    ha="center",
    arrowprops=dict(arrowstyle="->")
)


    ax.set_xlim(0, 120)
    ax.set_yticks([])

    ax.set_xlabel("오늘의 탄소 발자국 점수")
    ax.set_title("오늘 나의 탄소 발자국 위치")

    ax.text(10, -0.3, "매우 낮음", ha="center")
    ax.text(35, -0.3, "좋음", ha="center")
    ax.text(65, -0.3, "주의", ha="center")
    ax.text(100, -0.3, "높음", ha="center")

    plt.tight_layout()

    st.pyplot(fig)

    st.info(feedback_message)


if __name__ == "__main__":
    run_calculator()
