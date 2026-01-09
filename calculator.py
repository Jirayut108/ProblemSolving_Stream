#เมื่อรันเสร็จจะมีไฟล์ calculator เกิดขึ้นมา
import streamlit as st

def get_number_input(label):
    return st.number_input(label, value=0.0, step=0.1, format="%.2f")

def get_operator_input(label):
    valid_operators = ['+', '-', '*', '/', '%']
    return st.selectbox(label, valid_operators)

def calculate(num1, num2, op):
    result = None
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 == 0:
            st.error("ข้อผิดพลาด ไม่สามารถหารด้วยศูนย์ได้")
            return None
        else:
            return num1 / num2
    elif op == "%":
        if num2 == 0:
            st.error("ข้อผิดพลาด ไม่สามารถหารด้วยศูนย์ได้")
            return None
        else:
            return num1 % num2
    else:
        return None

st.title('My Calculator')

# Get inputs from the user
num1 = get_number_input("ป้อนตัวเลขแรก:")
num2 = get_number_input("ป้อนตัวเลขที่สอง:")
operator = get_operator_input("เลือกตัวดำเนินการ:")

# Perform calculation when the button is clicked
if st.button('คำนวณ'):
    result = calculate(num1, num2, operator)
    if result is not None:
        st.success(f"ผลลัพธ์: {num1} {operator} {num2} = {result}")
