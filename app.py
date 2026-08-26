import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="جدول إحضار الطعام", page_icon="🍔", layout="centered")

# 1. قائمة الطلاب الـ 11
STUDENTS = [
    "كرار رعد", "زين العابدين", "حيدر محمد", "مصطفى كمر", "سجاد مهند",
    "مصطفى محمد", "مصطفى عيسى", "علي غزوان", "مقتدى", "حيدر جاسم", "مصطفى حسين"
]

# 2. الاتصال بـ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        data = conn.read(ttl=0)
        data.columns = [str(col).strip() for col in data.columns]
        if "Student" not in data.columns or "Meal" not in data.columns:
            return pd.DataFrame(columns=["Student", "Meal"])
        return data
    except Exception:
        return pd.DataFrame(columns=["Student", "Meal"])

df = load_data()

# 3. حساب الأسبوع
current_week = datetime.datetime.now().isocalendar()[1]

def get_duty_students(week_offset=0):
    target_week = current_week + week_offset
    start_index = (target_week * 5) % len(STUDENTS)
    duty = []
    for i in range(5):
        index = (start_index + i) % len(STUDENTS)
        duty.append(STUDENTS[index])
    return duty

st.title("🍔 جدول تنظيم إحضار الطعام")
st.write("موقع لتنظيم الدور الأسبوعي بين الطلاب")
st.divider()

st.subheader(f"📅 المكلفون برفع الأكل - الأسبوع الحالي (أسبوع {current_week})")

this_week_students = get_duty_students(0)

# عرض خانات الكتابة والحفظ لكل طالب
for student in this_week_students:
    col1, col2, col3 = st.columns([2, 3, 1])
    
    existing_meal = ""
    if not df.empty and "Student" in df.columns:
        match = df[df["Student"].astype(str).str.strip() == student]
        if not match.empty:
            meal_val = match["Meal"].values[0]
            if pd.notna(meal_val):
                existing_meal = str(meal_val)

    with col1:
        st.write(f"👤 {student}")
    with col2:
        new_meal = st.text_input(
            "نوع الوجبة", 
            value=existing_meal, 
            key=f"input_{student}", 
            label_visibility="collapsed", 
            placeholder="اكتب نوع الوجبة..."
        )
    with col3:
        if st.button("حفظ", key=f"btn_{student}"):
            if df.empty or "Student" not in df.columns:
                df = pd.DataFrame([{"Student": student, "Meal": new_meal}])
            else:
                if student in df["Student"].astype(str).str.strip().values:
                    df.loc[df["Student"].astype(str).str.strip() == student, "Meal"] = new_meal
                else:
                    new_row = pd.DataFrame([{"Student": student, "Meal": new_meal}])
                    df = pd.concat([df, new_row], ignore_index=True)
            
            conn.update(data=df)
            st.success("تم الحفظ!")
            st.rerun()

st.divider()
st.subheader("🔮 القائمة المبدئية للأسبوع القادم")
for idx, student in enumerate(get_duty_students(1), 1):
    st.write(f"{idx}. {student}")
