import streamlit as st
import datetime
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="جدول إحضار الطعام", page_icon="🍔", layout="centered")

# 1. قائمة الطلاب الـ 11
STUDENTS = [
    "كرار رعد", "زين العابدين", "حيدر محمد", "مصطفى كمر", "سجاد مهند",
    "مصطفى محمد", "مصطفى عيسى", "علي غزوان", "مقتدى", "حيدر جاسم", "مصطفى حسين"
]

# 2. رابط جوجل شيتس بصيغة CSV الشفافة
# استبدل هذا المعرف ID بالمعرف الخاص بجدولك إذا تغير
SHEET_ID = "1ZxsRrPAKX8K4HSbAT1A3Z-w5yQ"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        data = pd.read_csv(CSV_URL)
        # تصحيح المسافات وتنظيف الأعمدة
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

# عرض الوجبات والمدخلات
for student in this_week_students:
    col1, col2 = st.columns([2, 3])
    
    # جلب الأكلة الحالية من جدول جوجل
    existing_meal = "لم تحدد بعد"
    if not df.empty and "Student" in df.columns:
        match = df[df["Student"].astype(str).str.strip() == student]
        if not match.empty:
            meal_val = match["Meal"].values[0]
            if pd.notna(meal_val) and str(meal_val).strip() != "":
                existing_meal = str(meal_val)

    with col1:
        st.write(f"👤 {student}")
    with col2:
        st.info(f"🍲 الوجبة: {existing_meal}")

st.divider()
st.warning("💡 لتغيير نوع الوجبة أو إضافتها: افتح جدول جوجل شيتس مباشرة واكتب الوجبة أمام اسمك، وستظهر هنا أوتوماتيكياً للجميع!")

# رابط مباشر للجدول لسهولة التعديل
st.link_button("📂 فتح جدول جوجل لتحديث الوجبات", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

st.divider()
st.subheader("🔮 القائمة المبدئية للأسبوع القادم")
for idx, student in enumerate(get_duty_students(1), 1):
    st.write(f"{idx}. {student}")
