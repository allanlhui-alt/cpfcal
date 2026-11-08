"""
cpf_interactive.py - Interactive Singapore CPF Explorer & Simulator.
100% pure Python without using HTML, CSS, or JavaScript!
Compatible with Streamlit Cloud, local Streamlit, and standard Terminal execution.
"""

import sys
from typing import Dict, Any


# ==============================================================================
# CORE CPF CALCULATION LOGIC (based on cpf37.py)
# ==============================================================================

def calculate_cpf(monthly_salary: float, age: int) -> Dict[str, float]:
    """
    Calculates CPF contributions with a $7,400 Ordinary Wage ceiling.
    
    Rates:
    - Age <= 55: 20% Employee / 17% Employer (Total: 37%)
    - Age 56-60: 15% Employee / 14% Employer (Total: 29%)
    - Age > 60: 15% Employee / 14% Employer (simplified scope from cpf37)
    """
    if monthly_salary < 0:
        raise ValueError("Salary cannot be negative.")
    if age < 16:
        raise ValueError("Age must be at least 16.")

    ow_ceiling = 7400.0
    subject_to_cpf = min(monthly_salary, ow_ceiling)

    if age <= 55:
        employee_rate = 0.20
        employer_rate = 0.17
    elif 56 <= age <= 60:
        employee_rate = 0.15
        employer_rate = 0.14
    else:
        employee_rate = 0.15
        employer_rate = 0.14

    employee_share = round(subject_to_cpf * employee_rate, 2)
    employer_share = round(subject_to_cpf * employer_rate, 2)
    total_contribution = round(employee_share + employer_share, 2)
    take_home_pay = round(monthly_salary - employee_share, 2)

    return {
        "monthly_salary": monthly_salary,
        "age": age,
        "subject_to_cpf": subject_to_cpf,
        "employee_rate": employee_rate,
        "employer_rate": employer_rate,
        "employee_share": employee_share,
        "employer_share": employer_share,
        "total_contribution": total_contribution,
        "take_home_pay": take_home_pay,
    }


def get_fun_metrics(data: Dict[str, float]) -> Dict[str, Any]:
    """Generate fun badges, personas, and Singapore hawker equivalence."""
    age = int(data["age"])
    salary = data["monthly_salary"]
    employer_share = data["employer_share"]
    total = data["total_contribution"]

    # Persona Title
    if age < 25:
        persona = "🌱 Young Hustler"
        persona_desc = "Building your foundation early! Compounding interest is your superpower."
    elif age <= 35:
        persona = "🚀 Prime Career Builder"
        persona_desc = "Peak contribution rates! Perfect for housing (OA) & healthcare (MA) build-up."
    elif age <= 55:
        persona = "💼 Wealth & Asset Maximizer"
        persona_desc = "Strongest earning phase! Supercharge your retirement & investments."
    elif age <= 60:
        persona = "🌟 Senior Asset Veteran"
        persona_desc = "Transitions to revised rates; steady cash flow preservation."
    else:
        persona = "🧘 Retirement Zen Master"
        persona_desc = "Reaping the rewards of lifelong disciplined savings."

    # Singapore Hawker Index (Kopi O = $1.80, Chicken Rice = $4.50)
    kopi_count = int(employer_share / 1.80) if employer_share > 0 else 0
    chicken_rice_count = int(employer_share / 4.50) if employer_share > 0 else 0

    # Ceiling status
    is_capped = salary > 7400.0
    uncapped_amount = round(salary - 7400.0, 2) if is_capped else 0.0

    return {
        "persona": persona,
        "persona_desc": persona_desc,
        "kopi_count": kopi_count,
        "chicken_rice_count": chicken_rice_count,
        "is_capped": is_capped,
        "uncapped_amount": uncapped_amount,
        "annual_cpf": round(total * 12, 2),
        "annual_employer_bonus": round(employer_share * 12, 2),
    }


# ==============================================================================
# STREAMLIT INTERACTIVE WEB APP (Pure Python - No HTML/CSS/JS)
# ==============================================================================

def run_streamlit_app() -> None:
    import streamlit as st

    st.set_page_config(
        page_title="🦁 Singapore CPF Explorer",
        page_icon="🦁",
        layout="wide",
    )

    st.title("🦁 Singapore CPF Explorer & Simulator")
    st.caption("100% Pure Python Interactive App • 2026 CPF Rules ($7,400 OW Ceiling)")

    # Sidebar: Presets & Controls
    st.sidebar.header("⚙️ Settings & Inputs")

    preset = st.sidebar.selectbox(
        "⚡ Quick Presets",
        [
            "Custom",
            "🎒 Intern ($1,200 | Age 21)",
            "🚀 Fresh Grad ($4,200 | Age 24)",
            "💼 Mid-Career ($6,500 | Age 35)",
            "🏆 Ceiling Cap ($8,500 | Age 42)",
            "🌟 Senior Veteran ($5,500 | Age 58)",
        ]
    )

    default_salary = 5000.0
    default_age = 30

    if preset == "🎒 Intern ($1,200 | Age 21)":
        default_salary, default_age = 1200.0, 21
    elif preset == "🚀 Fresh Grad ($4,200 | Age 24)":
        default_salary, default_age = 4200.0, 24
    elif preset == "💼 Mid-Career ($6,500 | Age 35)":
        default_salary, default_age = 6500.0, 35
    elif preset == "🏆 Ceiling Cap ($8,500 | Age 42)":
        default_salary, default_age = 8500.0, 42
    elif preset == "🌟 Senior Veteran ($5,500 | Age 58)":
        default_salary, default_age = 5500.0, 58

    salary = st.sidebar.slider(
        "Monthly Salary (SGD $)",
        min_value=500.0,
        max_value=15000.0,
        value=default_salary,
        step=100.0,
        format="$%.2f",
    )

    age = st.sidebar.slider(
        "Age (Years)",
        min_value=16,
        max_value=75,
        value=default_age,
        step=1,
    )

    data = calculate_cpf(salary, age)
    fun = get_fun_metrics(data)

    # Persona & Ceiling Banners
    st.info(f"**Financial Persona:** {fun['persona']} — *{fun['persona_desc']}*")

    if fun["is_capped"]:
        st.warning(
            f"🚀 **Ordinary Wage Ceiling Active!** Your salary exceeds the **$7,400** monthly cap. "
            f"The remaining **${fun['uncapped_amount']:,.2f}** has **0% CPF deduction** (100% take-home pay)."
        )
    else:
        st.success(f"✅ Entire monthly salary of **${salary:,.2f}** is subject to CPF contributions.")

    # High-level Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="💵 Net Take-Home Pay",
            value=f"${data['take_home_pay']:,.2f}",
            delta=f"{(data['take_home_pay'] / salary) * 100:.1f}% of gross",
        )
    with col2:
        st.metric(
            label="🔵 Employee CPF (Deducted)",
            value=f"${data['employee_share']:,.2f}",
            delta=f"{int(data['employee_rate'] * 100)}% rate",
            delta_color="inverse",
        )
    with col3:
        st.metric(
            label="🎁 Employer CPF (Free Money)",
            value=f"+${data['employer_share']:,.2f}",
            delta=f"{int(data['employer_rate'] * 100)}% extra match",
        )
    with col4:
        st.metric(
            label="🏦 Total Monthly CPF",
            value=f"${data['total_contribution']:,.2f}",
            delta=f"${fun['annual_cpf']:,.2f} / year",
        )

    st.divider()

    # Visual Breakdown & Hawker Index
    col_chart, col_fun = st.columns([3, 2])

    with col_chart:
        st.subheader("📊 Monthly Cashflow Breakdown")
        chart_data = {
            "Component": ["Take-Home Pay", "Employee CPF", "Employer CPF Match"],
            "Amount ($SGD)": [
                data["take_home_pay"],
                data["employee_share"],
                data["employer_share"],
            ],
        }
        st.bar_chart(data=chart_data, x="Component", y="Amount ($SGD)")

    with col_fun:
        st.subheader("🍜 Singapore Hawker Equivalence")
        st.write(
            f"Your employer's monthly CPF contribution of **${data['employer_share']:,.2f}** "
            f"is equivalent to free extra perks every month:"
        )
        st.write(f"☕ **{fun['kopi_count']:,} cups** of Kopi O Peng *($1.80/cup)*")
        st.write(f"🍛 **{fun['chicken_rice_count']:,} plates** of Hainanese Chicken Rice *($4.50/plate)*")
        st.write(f"🎁 **Annual Employer Bonus:** **${fun['annual_employer_bonus']:,.2f}** added to your retirement!")

        if st.button("🎉 Celebrate My CPF Growth!"):
            st.balloons()


# ==============================================================================
# PURE PYTHON TERMINAL TUI / CLI (FALLBACK IF STREAMLIT IS NOT RUN)
# ==============================================================================

def print_banner() -> None:
    print("\n" + "=" * 65)
    print("🦁  SINGAPORE CPF EXPLORER & WEALTH SIMULATOR  🦁")
    print("   Pure Python Interactive Edition • 2026 CPF Rates")
    print("=" * 65)


def render_cli_bar(take_home: float, employee_share: float, employer_share: float, width: int = 40) -> str:
    total = take_home + employer_share + employee_share
    if total <= 0:
        return "[Empty]"
    n_th = int((take_home / total) * width)
    n_ee = int((employee_share / total) * width)
    n_er = width - (n_th + n_ee)
    return f"[{'█' * n_th}{'▒' * n_ee}{'░' * n_er}]"


def run_cli_calculator() -> None:
    print_banner()
    print("Enter your details to explore your CPF breakdown & fun insights!\n")

    while True:
        try:
            sal_input = input("👉 Enter Monthly Salary in SGD (or 'q' to quit): ").strip()
            if sal_input.lower() == 'q':
                break
            salary = float(sal_input)

            age_input = input("👉 Enter Age in years (16 to 100): ").strip()
            age = int(age_input)

            data = calculate_cpf(salary, age)
            fun = get_fun_metrics(data)

            print("\n" + "-" * 65)
            print(f"🎯 RESULTS FOR: ${salary:,.2f} salary | Age {age}")
            print(f"🎖️  Financial Persona: {fun['persona']}")
            print(f"    {fun['persona_desc']}")
            print("-" * 65)

            if fun["is_capped"]:
                print(f"🚀 CEILING STATUS: CAPPED at $7,400.00!")
                print(f"   The excess ${fun['uncapped_amount']:,.2f} has 0% CPF deduction (100% take-home).")
            else:
                print(f"✅ CEILING STATUS: Fully within the $7,400 cap.")

            print("\n📊 MONTHLY CASHFLOW BREAKDOWN:")
            print(f"  💵 Net Take-Home Pay      : ${data['take_home_pay']:>10,.2f} ({(data['take_home_pay']/salary)*100:5.1f}%)")
            print(f"  🔵 Employee CPF (Deducted): ${data['employee_share']:>10,.2f} ({(data['employee_share']/salary)*100:5.1f}%)")
            print(f"  🎁 Employer CPF (Bonus)   : ${data['employer_share']:>10,.2f} ({(data['employer_share']/salary)*100:5.1f}%)")
            print(f"  🏦 Total Monthly CPF      : ${data['total_contribution']:>10,.2f}")

            bar = render_cli_bar(data["take_home_pay"], data["employee_share"], data["employer_share"])
            print(f"\nVisual Bar: {bar}")
            print("  Legend: █ Take-Home Pay | ▒ Employee CPF | ░ Employer Free Money")

            print("\n🍜 SINGAPORE HAWKER EQUIVALENCE:")
            print(f"  • Your employer's monthly gift of ${data['employer_share']:,.2f} buys:")
            print(f"    ☕ {fun['kopi_count']} cups of Kopi O Peng ($1.80/cup)")
            print(f"    🍛 {fun['chicken_rice_count']} plates of Hainanese Chicken Rice ($4.50/plate)")
            print(f"  • In 1 Year, your CPF accumulates: ${fun['annual_cpf']:,.2f}!")
            print("=" * 65 + "\n")

        except ValueError as e:
            print(f"❌ Input Error: {e}. Please try again.\n")


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

if HAS_STREAMLIT:
    # Executed by Streamlit (e.g. on Streamlit Cloud or `streamlit run`)
    run_streamlit_app()
elif __name__ == "__main__":
    run_cli_calculator()
