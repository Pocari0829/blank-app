import streamlit as st
import random

# 사이드바 설정
st.sidebar.title("🃏 타로 점 보기 앱")
st.sidebar.markdown("원하는 옵션을 선택하고 타로 카드를 뽑아보세요!")

# 카드 선택 모드 설정
card_count = st.sidebar.selectbox(
    "카드 뽑기",
    ("한 장 뽑기", "세 장 뽑기")
)

# 세션 상태 초기화 및 모드 변경 시 초기화
if 'cards_drawn' not in st.session_state:
    st.session_state.cards_drawn = []
if 'last_mode' not in st.session_state:
    st.session_state.last_mode = card_count

if st.session_state.cards_drawn and st.session_state.last_mode != card_count:
    st.session_state.cards_drawn = []
    st.session_state.last_mode = card_count
    st.rerun()

# --- 타로 카드 데이터 (78장) ---
tarot_data = {
    "The Fool": {"meaning": "새로운 시작, 자유, 모험, 순수함", "sentence": "당신은 새로운 여정의 출발점에 서 있습니다. 두려워하지 말고 순수한 마음으로 모험을 떠나보세요. 자유와 가능성이 당신을 기다립니다."},
    "The Magician": {"meaning": "능력, 의지, 창조력, 집중력", "sentence": "당신의 잠재된 능력이 빛을 발할 때입니다. 강한 의지와 집중력으로 당신이 원하는 것을 현실로 만들어낼 수 있습니다."},
    "The High Priestess": {"meaning": "직관, 신비, 잠재력, 지혜", "sentence": "내면의 목소리에 귀 기울여 보세요. 당신의 직관이 가장 현명한 길을 알려줄 것입니다. 겉으로 드러나지 않는 숨겨진 진실을 찾아보세요."},
    "The Empress": {"meaning": "풍요, 창조, 모성, 자연", "sentence": "당신에게 풍요와 안정의 시기가 찾아왔습니다. 사랑과 창조적인 에너지를 주변에 나누고, 자연의 아름다움 속에서 평온을 느껴보세요."},
    "The Emperor": {"meaning": "권위, 안정, 구조, 통제", "sentence": "확고한 리더십과 계획이 필요한 때입니다. 질서와 안정을 통해 당신의 목표를 통제하고 강력한 기반을 다지세요."},
    "The Hierophant": {"meaning": "전통, 가치관, 교육, 조언", "sentence": "당신은 누군가의 조언이나 가이드가 필요한 상황에 있습니다. 전통적인 가치나 교육을 통해 올바른 길을 찾을 수 있을 것입니다."},
    "The Lovers": {"meaning": "사랑, 선택, 관계, 조화", "sentence": "중요한 선택의 기로에 섰습니다. 사랑과 관계에서 진실된 마음을 따르는 것이 당신에게 조화와 행복을 가져다줄 것입니다."},
    "The Chariot": {"meaning": "승리, 의지, 추진력, 통제", "sentence": "강한 의지와 추진력으로 목표를 향해 달려가세요. 곧 승리와 성공을 거머쥐게 될 것입니다. 감정을 잘 통제하는 것이 중요합니다."},
    "Strength": {"meaning": "힘, 용기, 인내, 동정심", "sentence": "당신은 내면의 강인함을 발휘할 때입니다. 물리적인 힘이 아닌 용기와 인내심으로 어려움을 극복하고, 부드러운 동정심을 잃지 마세요."},
    "The Hermit": {"meaning": "내면 탐색, 고독, 성찰, 지혜", "sentence": "혼자만의 시간을 가지며 내면을 깊이 성찰해야 합니다. 잠시 멈춰 서서 스스로에게 집중하면 진정한 지혜를 얻을 수 있을 것입니다."},
    "Wheel of Fortune": {"meaning": "운명, 변화, 행운, 기회", "sentence": "운명의 수레바퀴가 당신에게 유리하게 돌아가고 있습니다. 갑작스러운 변화나 새로운 기회가 찾아올 수 있으니 행운을 놓치지 마세요."},
    "Justice": {"meaning": "정의, 균형, 진실, 공정함", "sentence": "정의롭고 공정한 판단이 필요한 상황입니다. 진실을 직시하고 올바른 결정을 내리면 모든 것이 균형을 되찾을 것입니다."},
    "The Hanged Man": {"meaning": "희생, 새로운 시각, 정지, 인내", "sentence": "현재의 상황을 다른 관점에서 바라봐야 합니다. 잠시 모든 것을 멈추고 새로운 시각을 얻기 위해 인내하는 시간을 가지세요. 때로는 희생이 필요할 수도 있습니다."},
    "Death": {"meaning": "종말, 변화, 재탄생, 새로운 시작", "sentence": "오래된 것을 끝내고 새로운 시작을 맞이할 때입니다. 두려워하지 마세요. 이 변화는 당신을 더 나은 방향으로 이끌 재탄생의 과정입니다."},
    "Temperance": {"meaning": "균형, 절제, 조화, 인내", "sentence": "삶의 여러 부분에서 균형과 조화를 찾아야 합니다. 절제와 인내심을 발휘하면 당신의 내면은 평화로워질 것입니다."},
    "The Devil": {"meaning": "집착, 유혹, 물질주의, 속박", "sentence": "당신을 얽매고 있는 유혹이나 집착에서 벗어나야 합니다. 물질적인 것에 대한 탐욕을 경계하고, 진정한 자유를 찾아보세요."},
    "The Tower": {"meaning": "파괴, 갑작스러운 변화, 혼란, 전환점", "sentence": "지금까지 쌓아왔던 것이 무너지는 혼란스러운 시기입니다. 하지만 이는 피할 수 없는 변화이며, 당신의 삶에 중요한 전환점이 될 것입니다."},
    "The Star": {"meaning": "희망, 영감, 평온, 치유", "sentence": "어두운 밤하늘 속에서도 희망의 별은 빛나고 있습니다. 평온함을 되찾고, 당신의 영감을 따라가면 치유와 행복을 얻을 수 있습니다."},
    "The Moon": {"meaning": "환상, 잠재의식, 불안, 미스터리", "sentence": "감정과 잠재의식이 혼란을 일으키고 있습니다. 눈에 보이는 것이 전부가 아닐 수 있습니다. 당신을 불안하게 만드는 미스터리를 직시하세요."},
    "The Sun": {"meaning": "성공, 기쁨, 활력, 행복", "sentence": "당신에게 성공과 행복이 가득한 시기입니다. 긍정적인 에너지가 넘치고 모든 것이 순조롭게 풀릴 것입니다. 이 기쁨을 만끽하세요."},
    "Judgement": {"meaning": "심판, 부활, 결단, 용서", "sentence": "과거를 돌아보고 새로운 삶을 시작해야 할 때입니다. 스스로를 용서하고, 용기 있는 결단으로 진정한 부활을 맞이하세요."},
    "The World": {"meaning": "완성, 성취, 통일, 성공", "sentence": "오랜 여정의 끝에 완전한 성공과 성취가 기다리고 있습니다. 모든 노력이 결실을 맺고, 당신의 세계는 통합과 조화를 이룰 것입니다."},
    "Ace of Wands": {"meaning": "새로운 영감, 시작, 창조력", "sentence": "새로운 시작을 알리는 강력한 영감이 떠올랐습니다. 당신의 창조적인 에너지를 믿고 행동으로 옮기세요. 기회가 곧 다가옵니다."},
    "Two of Wands": {"meaning": "계획, 미래 결정, 잠재력", "sentence": "미래를 계획하고 중요한 결정을 내려야 합니다. 당신의 잠재력은 무한하니, 넓은 시야로 다음 단계를 구상하세요."},
    "Three of Wands": {"meaning": "확장, 전망, 협력, 성공", "sentence": "노력이 결실을 맺고 있습니다. 이제 당신의 사업이나 관계를 확장할 좋은 시기입니다. 다른 사람들과 협력하면 더 큰 성공을 거둘 수 있습니다."},
    "Four of Wands": {"meaning": "기념, 안정, 조화, 집", "sentence": "기념하고 축하할 일이 생길 것입니다. 지금 당신의 삶은 안정적이고 평화롭습니다. 사랑하는 사람들과 함께 이 행복한 순간을 나누세요."},
    "Five of Wands": {"meaning": "갈등, 경쟁, 긴장", "sentence": "주변에 갈등과 경쟁이 있을 수 있습니다. 하지만 이는 성장을 위한 건전한 긴장일 수 있습니다. 정면으로 마주하고 이겨내세요."},
    "Six of Wands": {"meaning": "승리, 성공, 대중적 인정", "sentence": "당신의 노력이 마침내 인정받는 시기입니다. 주변 사람들에게 칭찬과 찬사를 받게 될 것입니다. 당신의 승리를 마음껏 즐기세요."},
    "Seven of Wands": {"meaning": "방어, 도전, 용기", "sentence": "당신의 위치를 지키기 위해 도전해야 합니다. 경쟁이나 비판에 맞서 용기를 내어 스스로를 방어하세요. 당신은 충분히 강합니다."},
    "Eight of Wands": {"meaning": "빠른 행동, 여행, 소식", "sentence": "모든 일이 빠르게 진행될 것입니다. 새로운 소식이 들려오거나 갑작스러운 여행을 떠날 수도 있습니다. 흐름을 놓치지 마세요."},
    "Nine of Wands": {"meaning": "인내, 방어, 회복력", "sentence": "마지막 고비를 앞두고 있습니다. 지쳤더라도 포기하지 마세요. 당신의 회복력과 인내심을 발휘하면 곧 승리할 수 있을 것입니다."},
    "Ten of Wands": {"meaning": "부담, 책임, 짐", "sentence": "어깨가 무겁고 책임감이 버겁게 느껴집니다. 혼자 모든 짐을 지려 하지 마세요. 필요한 경우 도움을 요청하고 부담을 나누어야 합니다."},
    "Page of Wands": {"meaning": "새로운 아이디어, 열정, 메시지", "sentence": "새로운 아이디어와 열정적인 메시지가 당신을 찾아올 것입니다. 호기심을 갖고 이 새로운 기회를 탐색해 보세요."},
    "Knight of Wands": {"meaning": "에너지, 모험, 돌진", "sentence": "당신은 모험을 향해 거침없이 나아가고 있습니다. 넘치는 에너지와 자신감으로 당신의 목표를 향해 돌진하세요."},
    "Queen of Wands": {"meaning": "열정, 독립, 자신감", "sentence": "당신은 주체적인 삶을 살며 강한 열정과 자신감을 가지고 있습니다. 당신의 독립적인 매력으로 주변 사람들을 이끌어 보세요."},
    "King of Wands": {"meaning": "비전, 리더십, 통제", "sentence": "당신은 비전을 제시하고 사람들을 이끌어가는 타고난 리더입니다. 당신의 지혜와 통제력으로 모두가 올바른 방향으로 나아가게 하세요."},
    "Ace of Cups": {"meaning": "새로운 감정, 사랑, 직관", "sentence": "새로운 감정이나 사랑이 시작될 것입니다. 당신의 직관을 믿고 마음이 이끄는 대로 따라가세요. 새로운 관계가 당신을 기다립니다."},
    "Two of Cups": {"meaning": "파트너십, 조화, 관계", "sentence": "당신과 누군가의 관계가 깊어지고 조화를 이룹니다. 사랑, 우정, 사업 등 모든 파트너십이 긍정적으로 발전할 것입니다."},
    "Three of Cups": {"meaning": "축하, 우정, 공동체", "sentence": "축하할 일이 생기고 즐거운 시간을 보내게 될 것입니다. 친구들과의 우정을 확인하고 공동체 속에서 행복을 찾으세요."},
    "Four of Cups": {"meaning": "불만족, 지루함, 새로운 기회", "sentence": "현재에 만족하지 못하고 지루함을 느끼고 있습니다. 당신의 주변에 새로운 기회가 찾아와도 보지 못하고 있을 수 있습니다."},
    "Five of Cups": {"meaning": "상실, 슬픔, 후회", "sentence": "과거의 상실과 실패에 묶여 슬퍼하고 있습니다. 엎질러진 우유를 보고 울지 마세요. 아직 남아있는 기회에 집중해야 합니다."},
    "Six of Cups": {"meaning": "과거, 순수, 추억", "sentence": "과거의 추억이 당신을 찾아올 것입니다. 잊고 지냈던 사람을 다시 만나거나 어린 시절의 순수한 마음을 되찾을 수 있습니다."},
    "Seven of Cups": {"meaning": "선택, 환상, 꿈", "sentence": "많은 선택지 속에서 길을 잃고 있습니다. 현실을 직시하고 환상에서 벗어나야 합니다. 가장 중요한 목표가 무엇인지 다시 생각하세요."},
    "Eight of Cups": {"meaning": "떠남, 새로운 길, 포기", "sentence": "현재의 만족스러운 상황을 뒤로하고 새로운 길을 떠나야 할 때입니다. 더 큰 목표를 위해 미련 없이 포기하는 용기가 필요합니다."},
    "Nine of Cups": {"meaning": "만족, 소원성취, 기쁨", "sentence": "당신의 소원이 이루어질 것입니다. 행복과 만족이 당신을 감싸고 있습니다. 노력의 결실을 기쁘게 받아들이세요."},
    "Ten of Cups": {"meaning": "완전한 행복, 가족, 조화", "sentence": "진정한 행복을 찾고 가족과의 관계가 조화를 이룹니다. 당신의 삶은 완벽하게 채워지고, 평온함과 안정감을 느낄 것입니다."},
    "Page of Cups": {"meaning": "감정적 소식, 직관, 예술성", "sentence": "감정적인 소식이나 새로운 관계가 시작될 것입니다. 당신의 예술적인 감각을 발휘하고 직관을 따르세요."},
    "Knight of Cups": {"meaning": "낭만, 감성, 제안", "sentence": "당신은 로맨틱하고 감성적인 제안을 받거나, 직접 그런 역할을 하게 될 것입니다. 당신의 감정을 솔직하게 표현해 보세요."},
    "Queen of Cups": {"meaning": "공감, 감성적 지혜, 치유", "sentence": "당신은 다른 사람의 감정을 이해하고 공감하는 능력이 뛰어납니다. 당신의 따뜻한 지혜로 주변 사람들을 치유하고 보살펴주세요."},
    "King of Cups": {"meaning": "감정적 통제, 관용, 지혜", "sentence": "당신은 감정을 잘 통제하며 지혜롭고 관용적인 사람입니다. 혼란스러운 상황 속에서도 평정심을 유지하고 현명한 결정을 내릴 것입니다."},
    "Ace of Swords": {"meaning": "새로운 생각, 진실, 명확성", "sentence": "새로운 아이디어가 당신의 마음을 밝힙니다. 진실을 직시하고 명확한 목표를 세워보세요. 지금은 논리적인 판단이 필요한 시기입니다."},
    "Two of Swords": {"meaning": "교착상태, 선택의 어려움, 회피", "sentence": "중요한 결정을 내리지 못하고 교착상태에 빠져 있습니다. 마음의 눈을 가린 수건을 벗고 현실을 직시하세요."},
    "Three of Swords": {"meaning": "상심, 슬픔, 고통", "sentence": "예상치 못한 고통이나 상실로 인해 마음의 상처를 입게 될 수 있습니다. 슬픔을 인정하고 치유의 시간을 가지세요."},
    "Four of Swords": {"meaning": "휴식, 회복, 명상", "sentence": "잠시 모든 것을 멈추고 쉬어야 할 때입니다. 에너지를 재충전하고, 명상을 통해 마음의 평화를 찾으세요. 휴식 후 다시 나아가세요."},
    "Five of Swords": {"meaning": "갈등, 패배, 비겁함", "sentence": "치열한 경쟁으로 인해 패배하거나, 비겁한 행동을 하게 될 수 있습니다. 무리하게 이기려 하지 마세요. 진정한 승리는 평화를 찾는 것입니다."},
    "Six of Swords": {"meaning": "이동, 전환, 어려움 극복", "sentence": "어려운 상황을 뒤로하고 새로운 곳으로 이동하게 될 것입니다. 당신은 곧 평온하고 나은 환경에 도달할 수 있습니다. 변화를 두려워하지 마세요."},
    "Seven of Swords": {"meaning": "속임수, 전략, 비밀", "sentence": "누군가 당신을 속이거나, 당신이 비밀스러운 전략을 쓸 수 있습니다. 정직한 태도가 중요합니다. 상황을 신중하게 살펴보세요."},
    "Eight of Swords": {"meaning": "구속, 한계, 자기 제약", "sentence": "스스로를 가두고 한계를 짓고 있습니다. 현실은 당신이 생각하는 것만큼 갇혀있지 않습니다. 당신의 두려움은 환상일 뿐입니다."},
    "Nine of Swords": {"meaning": "고통, 불안, 악몽", "sentence": "극심한 고통과 불안에 시달리고 있습니다. 그러나 이 고통은 당신의 생각에서 비롯된 것일 수 있습니다. 도움을 요청하고 악몽에서 벗어나야 합니다."},
    "Ten of Swords": {"meaning": "종말, 최악, 재탄생", "sentence": "모든 것이 끝났다고 느껴질 만큼 최악의 상황에 놓여 있습니다. 하지만 이 종말은 새로운 삶을 위한 필수적인 재탄생의 과정입니다."},
    "Page of Swords": {"meaning": "새로운 생각, 호기심, 진실", "sentence": "새로운 정보나 생각이 당신을 찾아올 것입니다. 호기심을 갖고 진실을 파헤쳐 보세요. 지금은 배우고 탐구해야 할 시기입니다."},
    "Knight of Swords": {"meaning": "돌진, 명확성, 빠른 행동", "sentence": "당신은 목표를 향해 거침없이 나아가고 있습니다. 명확한 판단과 빠른 행동력이 당신의 성공을 이끌 것입니다. 하지만 너무 서두르지 않도록 조심하세요."},
    "Queen of Swords": {"meaning": "날카로운 지성, 독립, 진실", "sentence": "당신은 날카로운 지성과 독립적인 정신을 가진 사람입니다. 감정에 휩쓸리지 않고 냉철하게 진실을 파악하는 능력이 뛰어납니다."},
    "King of Swords": {"meaning": "논리, 공정, 지성", "sentence": "당신은 논리적이고 공정한 판단력을 가지고 있습니다. 이성적인 태도로 상황을 분석하면 모든 문제를 해결할 수 있습니다. 리더로서의 자질을 발휘하세요."},
    "Ace of Pentacles": {"meaning": "새로운 기회, 풍요, 시작", "sentence": "재정적인 새로운 기회가 당신을 찾아왔습니다. 풍요로운 시작을 알리는 신호입니다. 실용적인 계획을 세우고 행동으로 옮기세요."},
    "Two of Pentacles": {"meaning": "균형, 유연성, 우선순위", "sentence": "여러 가지 일 사이에서 균형을 잡아야 합니다. 유연한 태도로 우선순위를 정하면 혼란을 극복할 수 있을 것입니다."},
    "Three of Pentacles": {"meaning": "협력, 팀워크, 숙련", "sentence": "당신의 재능이 인정받고, 다른 사람들과 협력할 기회가 찾아옵니다. 팀워크를 통해 더 큰 성과를 얻을 수 있습니다. 당신의 숙련된 기술을 보여주세요."},
    "Four of Pentacles": {"meaning": "보유, 안정, 통제, 인색함", "sentence": "당신은 현재의 것을 잃을까 두려워하고 있습니다. 안정은 좋지만, 모든 것을 통제하고 인색한 태도를 보이면 오히려 기회를 놓칠 수 있습니다."},
    "Five of Pentacles": {"meaning": "결핍, 빈곤, 소외", "sentence": "재정적 어려움이나 소외감을 느낄 수 있습니다. 힘들지만 혼자가 아니라는 것을 기억하세요. 도움을 요청하면 길이 열릴 것입니다."},
    "Six of Pentacles": {"meaning": "관용, 자선, 공유", "sentence": "당신은 관용을 베풀거나, 반대로 누군가로부터 도움을 받게 될 것입니다. 당신이 가진 것을 나누고 공유하면 풍요로움이 순환될 것입니다."},
    "Seven of Pentacles": {"meaning": "인내, 노력, 결과 대기", "sentence": "지금은 당신이 뿌린 씨앗이 결실을 맺을 때까지 기다려야 합니다. 조급해하지 말고 꾸준히 노력하면 좋은 결과를 얻을 수 있을 것입니다."},
    "Eight of Pentacles": {"meaning": "기술, 노력, 헌신", "sentence": "당신은 자신의 기술을 연마하고 있는 시기입니다. 꾸준한 노력과 헌신으로 전문가가 될 수 있습니다. 일에 집중하세요."},
    "Nine of Pentacles": {"meaning": "독립, 풍요, 자기 만족", "sentence": "노력으로 얻은 풍요와 독립적인 삶을 즐기고 있습니다. 당신의 삶은 안정적이고 만족스럽습니다. 자신을 위해 보상을 주세요."},
    "Ten of Pentacles": {"meaning": "부, 유산, 가족의 안정", "sentence": "당신에게 재정적인 안정과 행복한 가정이 보장됩니다. 물질적, 정신적으로 풍요로운 삶을 누릴 수 있습니다. 가족과 함께 이 행복을 나누세요."},
    "Page of Pentacles": {"meaning": "새로운 기회, 학습, 성실", "sentence": "새로운 직업이나 금전적인 기회가 찾아올 것입니다. 성실한 태도로 배우고 탐구하면 성공적인 시작을 할 수 있습니다."},
    "Knight of Pentacles": {"meaning": "성실, 책임감, 끈기", "sentence": "당신은 성실하고 책임감이 강한 사람입니다. 느리지만 끈기 있게 한 걸음씩 나아가면 당신의 목표를 확실하게 달성할 수 있습니다."},
    "Queen of Pentacles": {"meaning": "풍요, 안정, 실용적", "sentence": "당신은 주변 사람들에게 안정과 편안함을 주는 존재입니다. 현실적인 감각으로 풍요를 만들고 실용적으로 삶을 관리하는 능력이 뛰어납니다."},
    "King of Pentacles": {"meaning": "성공, 안정성, 신뢰성", "sentence": "당신은 재정적 성공과 안정성을 이룬 사람입니다. 당신의 신뢰성과 지혜는 주변 사람들에게 큰 도움을 줄 것입니다. 당신의 풍요를 나누세요."}
}

# 카드 이름 리스트
tarot_cards = list(tarot_data.keys())

# --- UI 레이아웃 및 기능 ---
st.title("🔮 당신의 운세를 알려드립니다")
st.markdown("버튼을 눌러 당신의 타로 카드를 뽑아보세요.")

# 카드 뽑기 버튼
if st.button("카드를 뽑겠습니다"):
    st.session_state.cards_drawn = []
    num_to_draw = 1 if card_count == "한 장 뽑기" else 3
    drawn_cards = random.sample(tarot_cards, num_to_draw)
    st.session_state.cards_drawn = drawn_cards
    st.balloons()

# 뽑힌 카드가 있을 경우 결과 표시
if st.session_state.cards_drawn:
    st.markdown("---")
    st.subheader("결과")
    
    if len(st.session_state.cards_drawn) == 3:
        # 과거-현재-미래 스프레드
        positions = ["과거", "현재", "미래"]
        cols = st.columns(3)
        for i, card_name in enumerate(st.session_state.cards_drawn):
            card_info = tarot_data.get(card_name, {})
            meaning = card_info.get("meaning", "정보 없음")
            sentence = card_info.get("sentence", "해석을 찾을 수 없습니다.")

            with cols[i]:
                st.markdown(f"### **{positions[i]}**")
                st.markdown(f"**{card_name}**")
                
                # 위치에 맞는 해석 문장 추가
                if positions[i] == "과거":
                    st.write(f"**키워드:** *{meaning}*")
                    st.write(f"**해석:** 당신의 과거는 **{sentence}**")
                elif positions[i] == "현재":
                    st.write(f"**키워드:** *{meaning}*")
                    st.write(f"**해석:** 현재 당신은 **{sentence}**")
                else: # 미래
                    st.write(f"**키워드:** *{meaning}*")
                    st.write(f"**해석:** 당신의 미래는 **{sentence}**")
    
    elif len(st.session_state.cards_drawn) == 1:
        # 한 장 뽑기
        card_name = st.session_state.cards_drawn[0]
        card_info = tarot_data.get(card_name, {})
        meaning = card_info.get("meaning", "정보 없음")
        sentence = card_info.get("sentence", "해석을 찾을 수 없습니다.")

        st.markdown(f"### **{card_name}**")
        st.write(f"**의미:** *{meaning}*")
        st.write(f"**해석:** {sentence}")

    st.markdown("---")
    st.success("새로운 시작을 위해 다시 카드를 뽑아보세요!")