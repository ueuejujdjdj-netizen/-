import streamlit as st
import datetime

# ضبط إعدادات الصفحة
st.set_page_config(page_title="جدول إحضار الطعام", page_icon="🍔", layout="centered")

# 1. قائمة الطلاب الـ 11
STUDENTS = [
    "مصطفى كمر", "حيدر محمد", "زين العابدين", "كرار رعد", " مهند سجاد",
    "مقتدى", "5مصطفى محمد", "مصطفى عيسى", "علي غزوان", "حيدر جاسم", "مصطفى حسين"
]

# 2. حساب رقم الأسبوع الحالي
current_week = datetime.datetime.now().isocalendar()[1]

def get_duty_students(week_offset=0):
    """دالة تحسب الـ 5 طلاب المكلفين بناءً على رقم الأسبوع"""
    target_week = current_week + week_offset
    start_index = (target_week * 5) % len(STUDENTS)
    
    duty = []
    for i in range(5):
        index = (start_index + i) % len(STUDENTS)
        duty.append(STUDENTS[index])
    return duty

# 3. واجهة الموقع
st.title("🍔 جدول تنظيم إحضار الطعام")
st.write("موقع لتنظيم الدور الأسبوعي بين الطلاب")
st.divider()

# عرض الأسبوع الحالي
st.subheader(f"📅 المكلفون برفع الأكل - الأسبوع الحالي (أسبوع {current_week})")

this_week_students = get_duty_students(0)

# إنشاء نموذج لتأكيد الإحضار ونوع الوجبة
for student in this_week_students:
    col1, col2 = st.columns([2, 3])
    with col1:
        st.write(f"👤 {student}")
    with col2:
        meal = st.text_input(f"نوع الوجبة لـ {student}", key=student, placeholder="مثلاً: دجاج، فطائر...")

st.divider()

# عرض الأسبوع القادم
st.subheader("🔮 القائمة المبدئية للأسبوع القادم")
next_week_students = get_duty_students(1)

for idx, student in enumerate(next_week_students, 1):
    st.write(f"{idx}. {student}")

st.info("💡 يتم تدوير الدور أوتوماتيكياً مع بداية كل أسبوع جديد!")