import streamlit as st
import datetime
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="جدول إحضار الطعام", page_icon="🍔", layout="centered")

# 1. قائمة الطلاب الـ 11
STUDENTS = [
    "كرار رعد", "زين العابدين", "حيدر محمد", "مصطفى كمر", "مهند سجاد",
    "مصطفى محمد", "مصطفى عيسى", "علي غزوان", "مقتدى", "حيدر جاسم", "مصطفى حسين"
]

# 2. رابط قراءة جدول جوجل مباشرة كـ CSV
SHEET_ID = "1-VvcuVNQUnb1U6pfoR"  
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# ضع رابط نموذج جوجل الخاص بك هنا إذا أنشأت واحداً، أو اترك رابط الجدول المباشر
FORM_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

@st.cache_data(ttl=2)
def load_data():
    try:
        data = pd.read_csv(CSV_URL)
        data.columns = [str(col).strip() for col in data.columns]
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

# عرض الوجبات فقط بأسلوب أنيق وبدون أخطاء كتابة
for student in this_week_students:
    col1, col2 = st.columns([2, 3])
    
    existing_meal = "لم تحدد بعد"
    if not df.empty and "Student" in df.columns:
        match = df[df["Student"].astype(str).str.strip() == student]
        if not match.empty:
            meal_val = match["Meal"].values[-1] # جلب أحدث وجبة مدخلة
            if pd.notna(meal_val) and str(meal_val).strip() != "":
                existing_meal = str(meal_val)

    with col1:
        st.write(f"👤 {student}")
    with col2:
        if existing_meal == "لم تحدد بعد":
            st.warning(f"🍲 الوجبة: {existing_meal}")
        else:
            st.success(f"🍲 الوجبة: {existing_meal}")

st.divider()

# زر يفتح الجدول لتعديل أو كتابة الوجبة مباشرة
st.link_button("📝 اضغط هنا لكتابة أو تعديل وجبتك", FORM_URL, use_container_width=True)

st.divider()
st.subheader("🔮 القائمة المبدئية للأسبوع القادم")
for idx, student in enumerate(get_duty_students(1), 1):
    st.write(f"{idx}. {student}")
