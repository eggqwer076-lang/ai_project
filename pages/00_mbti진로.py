import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 추천",
    page_icon="🌟",
    layout="centered"
)

# MBTI별 진로 데이터
career_data = {
    "INTJ": [
        {
            "job": "🧠 데이터 사이언티스트",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "논리적이고 전략적으로 생각하는 사람!",
            "salary": "평균 연봉 약 6,000만원"
        },
        {
            "job": "🏗️ 건축가",
            "major": "건축학과",
            "personality": "계획 세우기 좋아하고 창의적인 사람!",
            "salary": "평균 연봉 약 5,500만원"
        }
    ],

    "INTP": [
        {
            "job": "💻 프로그래머",
            "major": "컴퓨터공학과",
            "personality": "분석적이고 문제 해결을 좋아하는 사람!",
            "salary": "평균 연봉 약 5,800만원"
        },
        {
            "job": "🔬 연구원",
            "major": "물리학과, 화학과",
            "personality": "호기심 많고 탐구를 즐기는 사람!",
            "salary": "평균 연봉 약 5,200만원"
        }
    ],

    "ENTJ": [
        {
            "job": "📈 경영 컨설턴트",
            "major": "경영학과",
            "personality": "리더십 있고 목표지향적인 사람!",
            "salary": "평균 연봉 약 7,000만원"
        },
        {
            "job": "🚀 스타트업 CEO",
            "major": "경영학과, 경제학과",
            "personality": "도전 정신 강하고 추진력 있는 사람!",
            "salary": "평균 연봉 약 8,000만원 이상"
        }
    ],

    "ENTP": [
        {
            "job": "🎤 마케팅 기획자",
            "major": "광고홍보학과",
            "personality": "아이디어 넘치고 말하는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "📺 콘텐츠 크리에이터",
            "major": "미디어학과",
            "personality": "창의적이고 트렌드에 민감한 사람!",
            "salary": "평균 연봉 다양함"
        }
    ],

    "INFJ": [
        {
            "job": "🧡 상담심리사",
            "major": "심리학과",
            "personality": "공감 능력이 뛰어나고 따뜻한 사람!",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "✍️ 작가",
            "major": "문예창작과",
            "personality": "상상력이 풍부하고 감수성이 깊은 사람!",
            "salary": "평균 연봉 다양함"
        }
    ],

    "INFP": [
        {
            "job": "🎨 일러스트레이터",
            "major": "디자인학과",
            "personality": "감성적이고 창의적인 사람!",
            "salary": "평균 연봉 약 4,000만원"
        },
        {
            "job": "📚 작가",
            "major": "문예창작과",
            "personality": "자기 표현을 좋아하는 사람!",
            "salary": "평균 연봉 다양함"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과",
            "personality": "사람을 이끄는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "🎯 HR 매니저",
            "major": "경영학과",
            "personality": "소통 능력이 뛰어난 사람!",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],

    "ENFP": [
        {
            "job": "🎬 방송작가",
            "major": "미디어학과",
            "personality": "에너지 넘치고 아이디어가 많은 사람!",
            "salary": "평균 연봉 다양함"
        },
        {
            "job": "📢 광고 기획자",
            "major": "광고홍보학과",
            "personality": "창의적이고 활발한 사람!",
            "salary": "평균 연봉 약 5,200만원"
        }
    ],

    "ISTJ": [
        {
            "job": "🏦 회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 책임감 강한 사람!",
            "salary": "평균 연봉 약 7,000만원"
        },
        {
            "job": "⚖️ 공무원",
            "major": "행정학과",
            "personality": "성실하고 체계적인 사람!",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],

    "ISFJ": [
        {
            "job": "💉 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 책임감 있는 사람!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "🏥 물리치료사",
            "major": "물리치료학과",
            "personality": "도움을 주는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],

    "ESTJ": [
        {
            "job": "📊 관리자",
            "major": "경영학과",
            "personality": "체계적이고 리더십 있는 사람!",
            "salary": "평균 연봉 약 6,500만원"
        },
        {
            "job": "👮 경찰관",
            "major": "경찰행정학과",
            "personality": "책임감 강하고 결단력 있는 사람!",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],

    "ESFJ": [
        {
            "job": "🩺 의료 코디네이터",
            "major": "보건행정학과",
            "personality": "친절하고 사람 만나는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "🎓 학교 상담사",
            "major": "상담심리학과",
            "personality": "공감 능력이 뛰어난 사람!",
            "salary": "평균 연봉 약 4,800만원"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 기계 엔지니어",
            "major": "기계공학과",
            "personality": "손으로 만드는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 6,000만원"
        },
        {
            "job": "✈️ 파일럿",
            "major": "항공운항학과",
            "personality": "침착하고 집중력이 뛰어난 사람!",
            "salary": "평균 연봉 약 8,000만원"
        }
    ],

    "ISFP": [
        {
            "job": "📸 사진작가",
            "major": "사진영상학과",
            "personality": "감각적이고 자유로운 사람!",
            "salary": "평균 연봉 다양함"
        },
        {
            "job": "🎵 음악 프로듀서",
            "major": "실용음악과",
            "personality": "예술 감각이 뛰어난 사람!",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],

    "ESTP": [
        {
            "job": "💼 영업 전문가",
            "major": "경영학과",
            "personality": "활동적이고 사람과 어울리기 좋아하는 사람!",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "job": "🎤 이벤트 기획자",
            "major": "관광경영학과",
            "personality": "에너지 넘치고 실행력이 강한 사람!",
            "salary": "평균 연봉 약 4,800만원"
        }
    ],

    "ESFP": [
        {
            "job": "🎭 배우",
            "major": "연극영화과",
            "personality": "표현력이 뛰어나고 밝은 사람!",
            "salary": "평균 연봉 다양함"
        },
        {
            "job": "📱 인플루언서",
            "major": "미디어학과",
            "personality": "사람들의 관심을 끄는 걸 좋아하는 사람!",
            "salary": "평균 연봉 다양함"
        }
    ]
}

st.title("🌟 MBTI 진로 추천 프로그램")
st.write("나의 MBTI에 어울리는 진로를 알아보자 😆")

mbti_list = list(career_data.keys())

selected_mbti = st.selectbox(
    "👇 너의 MBTI를 선택해줘!",
    mbti_list
)

if st.button("🔍 진로 추천 보기"):
    st.subheader(f"✨ {selected_mbti} 추천 진로")

    careers = career_data[selected_mbti]

    for idx, career in enumerate(careers, start=1):
        st.markdown(f"""
### {idx}. {career['job']}

- 🎓 추천 학과 : **{career['major']}**
- 😎 잘 맞는 성격 : **{career['personality']}**
- 💰 평균 연봉 : **{career['salary']}**

---
""")

    st.success("🔥 미래의 멋진 너를 응원할게!")
