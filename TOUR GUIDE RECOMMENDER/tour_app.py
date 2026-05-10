import streamlit as st
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Tour Guide 🇮🇳",
    page_icon="🇮🇳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.hero {
    background: linear-gradient(135deg, #FF6B35 0%, #f7a072 55%, #ffd4b8 100%);
    border-radius: 20px; padding: 2.2rem 2rem 1.8rem;
    text-align: center; margin-bottom: 2rem;
    box-shadow: 0 8px 30px rgba(255,107,53,0.18);
}
.hero h1 { font-family:'Playfair Display',serif; font-size:2.5rem; color:#1a1a1a; margin:0; }
.hero p  { color:#444; margin-top:0.5rem; font-size:0.97rem; }
.step-box {
    background:#fff; border:1.5px solid #ffe0d0; border-radius:16px;
    padding:1.4rem 1.6rem 0.4rem; margin-bottom:0.4rem;
    box-shadow:0 2px 12px rgba(255,107,53,0.07);
}
.step-header { display:flex; align-items:center; gap:0.6rem; margin-bottom:0.8rem; }
.step-num {
    background:#FF6B35; color:white; border-radius:50%;
    width:28px; height:28px; display:flex; align-items:center; justify-content:center;
    font-weight:700; font-size:0.85rem; flex-shrink:0;
}
.step-title { font-weight:700; font-size:1.05rem; color:#1a1a1a; }
.top-card {
    background:linear-gradient(135deg,#e84c1e 0%,#c0392b 100%);
    border-radius:16px; padding:1.6rem 1.8rem; color:white;
    margin:1.4rem 0 0.6rem; box-shadow:0 6px 28px rgba(232,76,30,0.25);
}
.top-card .badge {
    background:rgba(255,255,255,0.22); border-radius:20px;
    padding:3px 14px; font-size:0.75rem; font-weight:700;
    letter-spacing:0.07em; display:inline-block; margin-bottom:0.7rem;
}
.top-card h2 { font-family:'Playfair Display',serif; font-size:1.8rem; margin:0 0 0.5rem; }
.top-card .meta { opacity:0.9; font-size:0.9rem; line-height:1.8; }
.alt-card {
    background:#fff; border:1px solid #ffe0d0; border-left:4px solid #FF6B35;
    border-radius:12px; padding:1rem 1.3rem; margin:0.55rem 0;
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
}
.alt-card h4 { margin:0 0 0.25rem; font-size:1rem; color:#1a1a1a; }
.alt-card p  { margin:0; color:#666; font-size:0.86rem; }
.rating-box {
    background:#fff8f5; border:2px solid #FF6B35; border-radius:14px;
    padding:1.1rem 0.8rem; text-align:center;
}
.rating-num { font-family:'Playfair Display',serif; font-size:2.8rem; color:#FF6B35; line-height:1; font-weight:800; }
.rating-stars { font-size:1.2rem; color:#FF6B35; margin:0.2rem 0; }
.rating-sub { font-size:0.72rem; color:#999; text-transform:uppercase; letter-spacing:0.06em; }
hr.fancy { border:none; height:2px; background:linear-gradient(90deg,transparent,#FF6B35,transparent); margin:1.8rem 0; }
.no-result { text-align:center; padding:2rem; color:#bbb; font-size:1.05rem; }
</style>
""", unsafe_allow_html=True)

# ── State → valid interest types mapping ──────────────────────────────────────
STATE_INTERESTS = {
    "Andaman & Nicobar Islands": ["Adventure", "Beach", "Nature"],
    "Andhra Pradesh":            ["Beach", "City", "Historical", "Nature"],
    "Arunachal Pradesh":         ["Adventure", "Nature"],
    "Assam":                     ["City", "Historical", "Nature"],
    "Bihar":                     ["City", "Historical", "Nature"],
    "Chandigarh":                ["City", "Historical"],
    "Chhattisgarh":              ["Adventure", "City", "Historical", "Nature"],
    "Dadra & Nagar Haveli":      ["City", "Nature"],
    "Daman & Diu":               ["Beach", "City", "Historical"],
    "Delhi":                     ["City", "Historical"],
    "Goa":                       ["Adventure", "Beach", "City", "Historical", "Nature"],
    "Gujarat":                   ["Beach", "City", "Historical", "Nature"],
    "Haryana":                   ["City", "Historical", "Nature"],
    "Himachal Pradesh":          ["Adventure", "City", "Historical", "Nature"],
    "Jammu and Kashmir":         ["Adventure", "City", "Historical", "Nature"],
    "Jharkhand":                 ["Adventure", "City", "Nature"],
    "Karnataka":                 ["Adventure", "Beach", "City", "Historical", "Nature"],
    "Kerala":                    ["Adventure", "Beach", "City", "Historical", "Nature"],
    "Ladakh":                    ["Adventure", "Historical", "Nature"],
    "Lakshadweep":               ["Adventure", "Beach", "Nature"],
    "Madhya Pradesh":            ["Adventure", "City", "Historical", "Nature"],
    "Maharashtra":               ["Adventure", "Beach", "City", "Historical", "Nature"],
    "Manipur":                   ["Adventure", "City", "Nature"],
    "Meghalaya":                 ["Adventure", "Nature"],
    "Mizoram":                   ["Adventure", "Nature"],
    "Nagaland":                  ["Adventure", "City", "Nature"],
    "Odisha":                    ["Beach", "City", "Historical", "Nature"],
    "Puducherry":                ["Beach", "City", "Historical"],
    "Punjab":                    ["City", "Historical", "Nature"],
    "Rajasthan":                 ["Adventure", "City", "Historical", "Nature"],
    "Sikkim":                    ["Adventure", "Nature"],
    "Tamil Nadu":                ["Beach", "City", "Historical", "Nature"],
    "Telangana":                 ["City", "Historical", "Nature"],
    "Tripura":                   ["City", "Historical", "Nature"],
    "Uttar Pradesh":             ["City", "Historical", "Nature"],
    "Uttarakhand":               ["Adventure", "City", "Historical", "Nature"],
    "West Bengal":               ["Beach", "City", "Historical", "Nature"],
}

# CSV only has 5 states — map display state → CSV state name
CSV_STATE_MAP = {
    "Goa":               "Goa",
    "Kerala":            "Kerala",
    "Jammu and Kashmir": "Jammu and Kashmir",
    "Rajasthan":         "Rajasthan",
    "Uttar Pradesh":     "Uttar Pradesh",
}

# Knowledge base for non-CSV states
KNOWLEDGE = {
    ("Andaman & Nicobar Islands","Beach"):      ("Radhanagar Beach, Havelock Island", 9.6, "Nov–Apr"),
    ("Andaman & Nicobar Islands","Adventure"):  ("Scuba Diving, Neil Island", 9.4, "Oct–May"),
    ("Andaman & Nicobar Islands","Nature"):     ("Mahatma Gandhi Marine Park", 9.1, "Oct–May"),
    ("Andhra Pradesh","Beach"):      ("Rushikonda Beach, Visakhapatnam", 8.2, "Oct–Mar"),
    ("Andhra Pradesh","City"):       ("Hyderabad Old City Tour", 8.5, "Nov–Feb"),
    ("Andhra Pradesh","Historical"): ("Golconda Fort", 8.7, "Nov–Feb"),
    ("Andhra Pradesh","Nature"):     ("Araku Valley", 8.0, "Oct–Feb"),
    ("Arunachal Pradesh","Adventure"): ("Tawang Monastery Trek", 8.9, "Mar–Oct"),
    ("Arunachal Pradesh","Nature"):    ("Namdapha National Park", 9.0, "Nov–Apr"),
    ("Assam","Nature"):     ("Kaziranga National Park", 9.5, "Nov–Apr"),
    ("Assam","City"):       ("Guwahati City Tour", 7.6, "Oct–Mar"),
    ("Assam","Historical"): ("Kamakhya Temple", 8.8, "Oct–Mar"),
    ("Bihar","Historical"): ("Bodh Gaya Temple Complex", 9.2, "Oct–Mar"),
    ("Bihar","City"):       ("Patna Heritage Walk", 7.8, "Oct–Mar"),
    ("Bihar","Nature"):     ("Valmiki National Park", 7.5, "Nov–Mar"),
    ("Chandigarh","City"):       ("Rock Garden & Rose Garden", 8.5, "Oct–Mar"),
    ("Chandigarh","Historical"): ("Capitol Complex, Le Corbusier", 8.2, "Oct–Mar"),
    ("Chhattisgarh","Nature"):     ("Chitrakote Waterfalls", 8.4, "Jul–Mar"),
    ("Chhattisgarh","Adventure"):  ("Barnawapara Wildlife Trek", 7.8, "Nov–Mar"),
    ("Chhattisgarh","Historical"): ("Sirpur Archaeological Site", 7.6, "Oct–Mar"),
    ("Chhattisgarh","City"):       ("Raipur City Tour", 7.2, "Oct–Feb"),
    ("Dadra & Nagar Haveli","Nature"): ("Vansda National Park", 7.5, "Oct–Feb"),
    ("Dadra & Nagar Haveli","City"):   ("Silvassa Heritage Village", 7.2, "Oct–Feb"),
    ("Daman & Diu","Beach"):      ("Diu Beach & Nagoa Beach", 8.1, "Oct–Mar"),
    ("Daman & Diu","City"):       ("Daman Fort & Church", 7.8, "Oct–Feb"),
    ("Daman & Diu","Historical"): ("Diu Fort Portuguese Heritage", 8.3, "Nov–Feb"),
    ("Delhi","City"):       ("Chandni Chowk & Connaught Place", 8.6, "Oct–Mar"),
    ("Delhi","Historical"): ("Red Fort, Qutub Minar & Humayun Tomb", 9.3, "Oct–Mar"),
    ("Gujarat","Beach"):      ("Mandvi Beach", 7.7, "Oct–Mar"),
    ("Gujarat","City"):       ("Ahmedabad Old City (UNESCO)", 8.8, "Oct–Feb"),
    ("Gujarat","Historical"): ("Modhera Sun Temple & Rani ki Vav", 9.0, "Oct–Mar"),
    ("Gujarat","Nature"):     ("Gir National Park – Asiatic Lions", 9.2, "Dec–Mar"),
    ("Haryana","City"):       ("Kurukshetra Heritage City", 8.0, "Oct–Mar"),
    ("Haryana","Historical"): ("Kurukshetra Battleground & Museum", 8.4, "Oct–Mar"),
    ("Haryana","Nature"):     ("Sultanpur Bird Sanctuary", 7.6, "Oct–Mar"),
    ("Himachal Pradesh","Adventure"):  ("Solang Valley & Rohtang Pass, Manali", 9.0, "Dec–Mar"),
    ("Himachal Pradesh","Nature"):     ("Great Himalayan National Park", 8.8, "May–Oct"),
    ("Himachal Pradesh","City"):       ("Shimla – Queen of Hills", 8.6, "Mar–Jun"),
    ("Himachal Pradesh","Historical"): ("Key Monastery, Spiti Valley", 8.3, "May–Sep"),
    ("Jharkhand","Nature"):     ("Betla National Park", 7.9, "Nov–Mar"),
    ("Jharkhand","Adventure"):  ("Hundru Falls & Dassam Falls Trek", 8.0, "Oct–Mar"),
    ("Jharkhand","City"):       ("Ranchi City – Waterfall Capital", 7.5, "Oct–Mar"),
    ("Karnataka","Beach"):      ("Gokarna Beach", 8.6, "Oct–Mar"),
    ("Karnataka","City"):       ("Bengaluru Palace & Cubbon Park", 8.4, "Oct–Feb"),
    ("Karnataka","Historical"): ("Hampi UNESCO Ruins", 9.3, "Oct–Feb"),
    ("Karnataka","Nature"):     ("Coorg Coffee Estates & Abbey Falls", 8.9, "Oct–Feb"),
    ("Karnataka","Adventure"):  ("Kodachadri & Kudremukh Trek", 8.1, "Sep–Jan"),
    ("Ladakh","Adventure"):  ("Pangong Lake High-Altitude Trek", 9.4, "Jun–Sep"),
    ("Ladakh","Nature"):     ("Nubra Valley & Sand Dunes", 9.2, "Jun–Sep"),
    ("Ladakh","Historical"): ("Thiksey & Hemis Monastery", 8.7, "Jun–Sep"),
    ("Lakshadweep","Beach"):     ("Agatti Island Beach", 9.3, "Oct–May"),
    ("Lakshadweep","Adventure"): ("Coral Reef Snorkeling & Diving", 9.5, "Oct–May"),
    ("Lakshadweep","Nature"):    ("Marine National Park", 9.0, "Oct–May"),
    ("Madhya Pradesh","Adventure"):  ("Pachmarhi Hill Station", 8.3, "Oct–Mar"),
    ("Madhya Pradesh","Historical"): ("Khajuraho Temple Complex", 9.1, "Oct–Mar"),
    ("Madhya Pradesh","Nature"):     ("Kanha Tiger Reserve", 9.0, "Oct–Jun"),
    ("Madhya Pradesh","City"):       ("Bhopal Lakes & Heritage City", 7.9, "Oct–Mar"),
    ("Maharashtra","Beach"):      ("Alibaug & Kashid Beach", 7.8, "Oct–Mar"),
    ("Maharashtra","City"):       ("Mumbai – Gateway of India", 8.7, "Nov–Feb"),
    ("Maharashtra","Historical"): ("Ajanta & Ellora Caves (UNESCO)", 9.4, "Oct–Mar"),
    ("Maharashtra","Nature"):     ("Lonavala, Khandala & Bhimashankar", 8.0, "Jun–Feb"),
    ("Maharashtra","Adventure"):  ("Sahyadri Range Trekking", 8.2, "Sep–Feb"),
    ("Manipur","Nature"):     ("Loktak Lake & Floating Islands", 8.8, "Oct–Mar"),
    ("Manipur","City"):       ("Imphal Cultural Tour", 7.7, "Oct–Mar"),
    ("Manipur","Adventure"):  ("Dzukou Valley Border Trek", 8.5, "Jun–Sep"),
    ("Meghalaya","Adventure"): ("Living Root Bridges Trek, Cherrapunji", 9.0, "Oct–May"),
    ("Meghalaya","Nature"):    ("Mawsmai Caves & Nohkalikai Falls", 9.2, "Oct–May"),
    ("Mizoram","Nature"):    ("Phawngpui Blue Mountain NP", 8.6, "Oct–Apr"),
    ("Mizoram","Adventure"): ("Aizawl & Tam Dil Lake Trek", 7.9, "Oct–Apr"),
    ("Nagaland","Adventure"): ("Dzukou Valley Trek", 9.0, "Jun–Sep"),
    ("Nagaland","City"):      ("Kohima War Cemetery & Museum", 8.2, "Oct–May"),
    ("Nagaland","Nature"):    ("Intanki Wildlife Sanctuary", 7.8, "Nov–Apr"),
    ("Odisha","Beach"):      ("Puri Beach & Chilika Lake", 8.5, "Oct–Feb"),
    ("Odisha","Historical"): ("Konark Sun Temple (UNESCO)", 9.2, "Oct–Mar"),
    ("Odisha","Nature"):     ("Simlipal Biosphere Reserve", 8.7, "Nov–Jun"),
    ("Odisha","City"):       ("Bhubaneswar – Temple City of India", 8.3, "Oct–Mar"),
    ("Puducherry","Beach"):      ("Promenade & Paradise Beach", 8.6, "Oct–Mar"),
    ("Puducherry","City"):       ("French Quarter & Auroville", 8.9, "Oct–Mar"),
    ("Puducherry","Historical"): ("Basilica of Sacred Heart Church", 8.3, "Oct–Mar"),
    ("Punjab","City"):       ("Amritsar Food & Culture Tour", 8.9, "Oct–Mar"),
    ("Punjab","Historical"): ("Golden Temple, Amritsar", 9.8, "Oct–Mar"),
    ("Punjab","Nature"):     ("Harike Wetland Bird Sanctuary", 7.8, "Nov–Mar"),
    ("Sikkim","Adventure"): ("Goecha La & Dzongri Trek", 9.1, "Apr–May"),
    ("Sikkim","Nature"):    ("Kanchenjunga Base Camp & Gurudongmar Lake", 9.3, "Mar–Jun"),
    ("Tamil Nadu","Beach"):      ("Marina Beach & Mahabalipuram Coast", 8.5, "Nov–Feb"),
    ("Tamil Nadu","Historical"): ("Brihadeeswarar Temple, Thanjavur (UNESCO)", 9.1, "Oct–Mar"),
    ("Tamil Nadu","City"):       ("Chennai City Heritage Tour", 7.9, "Nov–Feb"),
    ("Tamil Nadu","Nature"):     ("Nilgiri Biosphere & Ooty", 8.7, "Mar–Jun"),
    ("Telangana","City"):       ("Hyderabad City – Charminar & Bazaar", 8.8, "Oct–Mar"),
    ("Telangana","Historical"): ("Charminar, Mecca Masjid & Golconda", 8.9, "Oct–Mar"),
    ("Telangana","Nature"):     ("Nagarjunasagar Wildlife Sanctuary", 7.9, "Oct–Mar"),
    ("Tripura","Historical"): ("Ujjayanta Palace, Agartala", 8.1, "Oct–Mar"),
    ("Tripura","Nature"):     ("Sepahijala Wildlife Sanctuary", 7.8, "Oct–Apr"),
    ("Tripura","City"):       ("Agartala City Tour", 7.3, "Oct–Mar"),
    ("Uttarakhand","Adventure"):  ("River Rafting & Bungee, Rishikesh", 9.2, "Sep–Jun"),
    ("Uttarakhand","Nature"):     ("Valley of Flowers (UNESCO)", 9.5, "Jul–Sep"),
    ("Uttarakhand","City"):       ("Mussoorie – Queen of Hills", 8.7, "Mar–Jun"),
    ("Uttarakhand","Historical"): ("Kedarnath & Badrinath Temples", 9.6, "May–Oct"),
    ("West Bengal","City"):       ("Kolkata Heritage & Victoria Memorial", 8.8, "Oct–Mar"),
    ("West Bengal","Historical"): ("Victoria Memorial & Howrah Bridge", 9.0, "Oct–Mar"),
    ("West Bengal","Nature"):     ("Sundarbans Tiger Reserve (UNESCO)", 9.1, "Oct–Mar"),
    ("West Bengal","Beach"):      ("Digha & Mandarmani Sea Beach", 7.5, "Oct–Mar"),
}

ALL_STATES = sorted(STATE_INTERESTS.keys())


@st.cache_data
def load_data():
    dest    = pd.read_csv("Expanded_Destinations.csv")
    reviews = pd.read_csv("Final_Updated_Expanded_Reviews.csv")
    avg_r = (
        reviews.groupby("DestinationID")["Rating"]
        .mean().reset_index()
        .rename(columns={"Rating": "AvgRating"})
    )
    dest = dest.merge(avg_r, on="DestinationID", how="left")
    dest["AvgRating"] = dest["AvgRating"].fillna(0).round(2)
    rev_cnt = (
        reviews.groupby("DestinationID")["Rating"]
        .count().reset_index()
        .rename(columns={"Rating": "ReviewCount"})
    )
    dest = dest.merge(rev_cnt, on="DestinationID", how="left")
    dest["ReviewCount"] = dest["ReviewCount"].fillna(0).astype(int)
    return dest, reviews

dest_df, reviews_df = load_data()


def get_recommendations(state, interest, top_n=6):
    results = []
    csv_state = CSV_STATE_MAP.get(state)
    if csv_state:
        filtered = dest_df[
            (dest_df["State"] == csv_state) &
            (dest_df["Type"] == interest)
        ].copy()
        if not filtered.empty:
            pop_max = filtered["Popularity"].max()
            filtered["Score"] = (
                0.6 * (filtered["Popularity"] / pop_max) +
                0.4 * (filtered["AvgRating"] / 5.0)
            ).round(3)
            filtered = filtered.sort_values("Score", ascending=False).head(top_n)
            for _, row in filtered.iterrows():
                results.append({
                    "name":         row["Name"],
                    "state":        state,
                    "type":         row["Type"],
                    "popularity":   round(row["Popularity"], 1),
                    "avg_rating":   round(row["AvgRating"], 2),
                    "review_count": row["ReviewCount"],
                    "score":        row["Score"],
                    "best_time":    row["BestTimeToVisit"],
                })
    if not results:
        key = (state, interest)
        if key in KNOWLEDGE:
            name_k, pop, bt = KNOWLEDGE[key]
            results.append({
                "name":         name_k,
                "state":        state,
                "type":         interest,
                "popularity":   pop,
                "avg_rating":   round(pop * 0.48, 1),
                "review_count": 0,
                "score":        round(pop / 10, 2),
                "best_time":    bt,
            })
    return results


def star_str(rating):
    filled = min(5, max(0, round(rating)))
    return "★" * filled + "☆" * (5 - filled)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🇮🇳 India Tour Guide</h1>
  <p>Personalised destination finder — step by step, powered by real traveller data</p>
</div>
""", unsafe_allow_html=True)

# ── STEP 1: Name ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="step-box">
  <div class="step-header">
    <div class="step-num">1</div>
    <div class="step-title">What's your name?</div>
  </div>
</div>""", unsafe_allow_html=True)
name = st.text_input("", placeholder="Enter your name…", label_visibility="collapsed", key="name_in")

# ── STEP 2: State ─────────────────────────────────────────────────────────────
if name.strip():
    st.markdown("""
    <div class="step-box">
      <div class="step-header">
        <div class="step-num">2</div>
        <div class="step-title">Which state do you want to explore?</div>
      </div>
    </div>""", unsafe_allow_html=True)
    selected_state = st.selectbox("", ["— Select a state —"] + ALL_STATES,
                                  label_visibility="collapsed", key="state_in")
else:
    selected_state = None

# ── STEP 3: Interest (filtered by state) ─────────────────────────────────────
if selected_state and selected_state != "— Select a state —":
    valid_interests = STATE_INTERESTS.get(selected_state, [])
    st.markdown("""
    <div class="step-box">
      <div class="step-header">
        <div class="step-num">3</div>
        <div class="step-title">What kind of experience are you looking for?</div>
      </div>
    </div>""", unsafe_allow_html=True)
    selected_interest = st.selectbox("", ["— Select an interest —"] + valid_interests,
                                     label_visibility="collapsed", key="interest_in")
else:
    selected_interest = None

# ── STEP 4: Group details ─────────────────────────────────────────────────────
if selected_interest and selected_interest != "— Select an interest —":
    st.markdown("""
    <div class="step-box">
      <div class="step-header">
        <div class="step-num">4</div>
        <div class="step-title">Who's travelling?</div>
      </div>
    </div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male"], key="gender_in")
    with c2:
        num_adults = st.number_input("Adults", min_value=1, max_value=20, value=1, key="adults_in")
    with c3:
        num_children = st.number_input("Children", min_value=0, max_value=20, value=0, key="children_in")
    st.markdown("<br>", unsafe_allow_html=True)
    find_btn = st.button("🔍 Find My Destinations", type="primary", use_container_width=True)
else:
    find_btn = False
    num_adults, num_children, gender = 1, 0, "Prefer not to say"

# ── Results ───────────────────────────────────────────────────────────────────
if find_btn:
    results = get_recommendations(selected_state, selected_interest)
    st.markdown("<hr class='fancy'>", unsafe_allow_html=True)
    display_name = name.strip().title()

    if not results:
        st.markdown(f"""
        <div class="no-result">
          😔 No destinations found for <strong>{selected_interest}</strong> in <strong>{selected_state}</strong>.<br>
          Try a different combination!
        </div>""", unsafe_allow_html=True)
        st.stop()

    top = results[0]
    avg_r    = top["avg_rating"]
    score_pc = round(top["score"] * 100)

    st.markdown(f"## Hey, {display_name}! 🎉")
    st.markdown(
        f"Here are your **{selected_interest}** destinations in **{selected_state}** — "
        f"tailored for {int(num_adults)} adult(s) and {int(num_children)} child(ren)."
    )

    rev_info = f" &nbsp;|&nbsp; Reviews: <strong>{top['review_count']}</strong>" if top["review_count"] > 0 else ""
    st.markdown(f"""
    <div class="top-card">
      <div class="badge">⭐ TOP PICK</div>
      <h2>{top['name']}</h2>
      <div class="meta">
        📍 {top['state']} &nbsp;|&nbsp; 🏷️ {top['type']} &nbsp;|&nbsp; 🗓️ Best time: {top['best_time']}<br>
        Popularity: <strong>{top['popularity']} / 10</strong>{rev_info}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Rating")
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.markdown(f"""<div class="rating-box">
          <div class="rating-num">{avg_r}</div>
          <div class="rating-sub">Avg Review / 5</div></div>""", unsafe_allow_html=True)
    with rc2:
        st.markdown(f"""<div class="rating-box">
          <div class="rating-stars">{star_str(avg_r)}</div>
          <div class="rating-sub">Star Rating</div></div>""", unsafe_allow_html=True)
    with rc3:
        st.markdown(f"""<div class="rating-box">
          <div class="rating-num">{score_pc}%</div>
          <div class="rating-sub">Match Score</div></div>""", unsafe_allow_html=True)

    if len(results) > 1:
        st.markdown("### 🗺️ More Options")
        for r in results[1:]:
            r_avg = r["avg_rating"]
            rev_txt = f" &nbsp;|&nbsp; ⭐ {r_avg}/5" if r_avg > 0 else ""
            cnt_txt = f" &nbsp;|&nbsp; {r['review_count']} reviews" if r["review_count"] > 0 else ""
            st.markdown(f"""
            <div class="alt-card">
              <h4>{r['name']} &nbsp;<span style="color:#aaa;font-weight:400">— {r['state']}</span></h4>
              <p>🏷️ {r['type']} &nbsp;|&nbsp; Popularity: {r['popularity']}/10{rev_txt}{cnt_txt} &nbsp;|&nbsp; 🗓️ {r['best_time']}</p>
            </div>""", unsafe_allow_html=True)

    with st.expander("📋 Trip Summary"):
        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f"**Traveller:** {display_name}")
            st.markdown(f"**Gender:** {gender}")
            st.markdown(f"**Group:** {int(num_adults)} adult(s), {int(num_children)} child(ren)")
        with s2:
            st.markdown(f"**State:** {selected_state}")
            st.markdown(f"**Interest:** {selected_interest}")
            st.markdown(f"**Destinations shown:** {len(results)}")

st.markdown("<hr class='fancy'>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;color:#bbb;font-size:0.82rem;'>🌏 Powered by real traveller reviews & destination data</div>", unsafe_allow_html=True)