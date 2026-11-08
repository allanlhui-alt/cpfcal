"""
cpf_interactive.py - A fun, interactive, pure-Python CPF Explorer & Simulator.
Built strictly in pure Python (Tkinter GUI + Interactive Terminal TUI)
without any HTML, CSS, or JavaScript!
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Tuple


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
        persona_desc = "Building your foundation early! Compounding is on your side."
    elif age <= 35:
        persona = "🚀 Prime Career Builder"
        persona_desc = "Peak contribution rates! Perfect for housing & Medisave growth."
    elif age <= 55:
        persona = "💼 Wealth & Asset Maximizer"
        persona_desc = "Strongest earning phase! Your CPF OA & SA are supercharged."
    elif age <= 60:
        persona = "🌟 Senior Asset Veteran"
        persona_desc = "Transitions to revised rates; steady cash flow priority."
    else:
        persona = "🧘 Retirement Zen Master"
        persona_desc = "Reaping the rewards of lifelong disciplined savings."

    # Hawker / Fun Index (Prices: Kopi O = $1.80, Chicken Rice = $4.50)
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
# PURE PYTHON TKINTER GUI APPLICATION
# ==============================================================================

class CPFAppGUI:
    """Modern, colorful pure-Python Tkinter GUI for CPF Explorer."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("🦁 Singapore CPF Explorer & Simulator (Pure Python)")
        self.root.geometry("820x720")
        self.root.minsize(780, 680)
        self.root.configure(bg="#F0F4F8")

        # Variables
        self.salary_var = tk.DoubleVar(value=5000.0)
        self.age_var = tk.IntVar(value=30)

        self._setup_styles()
        self._build_ui()
        self.update_calculations()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        # Color palette
        style.configure("TLabel", background="#F0F4F8", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#1E293B", background="#F0F4F8")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 10), foreground="#64748B", background="#F0F4F8")
        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        style.configure("CardHeader.TLabel", font=("Segoe UI", 12, "bold"), foreground="#0F172A", background="#FFFFFF")
        style.configure("CardText.TLabel", font=("Segoe UI", 10), foreground="#334155", background="#FFFFFF")
        style.configure("BigStat.TLabel", font=("Segoe UI", 16, "bold"), foreground="#2563EB", background="#FFFFFF")

    def _build_ui(self) -> None:
        # Main container with scrolling or padding
        main_frame = tk.Frame(self.root, bg="#F0F4F8", padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Header Banner
        header = ttk.Label(main_frame, text="🦁 Singapore CPF Explorer & Simulator", style="Header.TLabel")
        header.pack(anchor="w")
        sub_header = ttk.Label(
            main_frame,
            text="Interactive pure-Python financial visualizer (2026 CPF Rules • $7,400 OW Ceiling)",
            style="SubHeader.TLabel"
        )
        sub_header.pack(anchor="w", pady=(0, 12))

        # 2. Preset Quick Buttons Frame
        preset_frame = tk.Frame(main_frame, bg="#F0F4F8")
        preset_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(preset_frame, text="⚡ Quick Presets:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))

        presets = [
            ("🎒 Intern ($1.2k, 21y)", 1200, 21),
            ("🚀 Fresh Grad ($4.2k, 24y)", 4200, 24),
            ("💼 Mid-Career ($6.5k, 35y)", 6500, 35),
            ("🏆 Ceiling Cap ($8.5k, 42y)", 8500, 42),
            ("🌟 Senior ($5.5k, 58y)", 5500, 58),
        ]

        for label, sal, age in presets:
            btn = tk.Button(
                preset_frame,
                text=label,
                font=("Segoe UI", 8),
                bg="#E2E8F0",
                fg="#1E293B",
                activebackground="#CBD5E1",
                relief="flat",
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda s=sal, a=age: self.set_preset(s, a)
            )
            btn.pack(side=tk.LEFT, padx=3)

        # 3. Interactive Inputs Card
        input_card = tk.Frame(main_frame, bg="#FFFFFF", bd=1, relief="solid", padx=15, pady=12)
        input_card.pack(fill=tk.X, pady=(0, 12))

        # --- Salary Input Row ---
        sal_header_row = tk.Frame(input_card, bg="#FFFFFF")
        sal_header_row.pack(fill=tk.X)
        tk.Label(sal_header_row, text="Monthly Salary ($SGD):", font=("Segoe UI", 10, "bold"), bg="#FFFFFF").pack(side=tk.LEFT)
        self.sal_display = tk.Label(sal_header_row, text="$5,000.00", font=("Segoe UI", 11, "bold"), fg="#2563EB", bg="#FFFFFF")
        self.sal_display.pack(side=tk.RIGHT)

        self.sal_slider = ttk.Scale(
            input_card,
            from_=500,
            to=15000,
            orient=tk.HORIZONTAL,
            variable=self.salary_var,
            command=self._on_slider_change
        )
        self.sal_slider.pack(fill=tk.X, pady=(4, 10))

        # --- Age Input Row ---
        age_header_row = tk.Frame(input_card, bg="#FFFFFF")
        age_header_row.pack(fill=tk.X)
        tk.Label(age_header_row, text="Age (Years):", font=("Segoe UI", 10, "bold"), bg="#FFFFFF").pack(side=tk.LEFT)
        self.age_display = tk.Label(age_header_row, text="30 years old", font=("Segoe UI", 11, "bold"), fg="#7C3AED", bg="#FFFFFF")
        self.age_display.pack(side=tk.RIGHT)

        self.age_slider = ttk.Scale(
            input_card,
            from_=16,
            to=70,
            orient=tk.HORIZONTAL,
            variable=self.age_var,
            command=self._on_slider_change
        )
        self.age_slider.pack(fill=tk.X, pady=(4, 4))

        # 4. Ceiling & Persona Notification Bar
        self.banner_frame = tk.Frame(main_frame, bg="#EFF6FF", bd=1, relief="solid", padx=12, pady=8)
        self.banner_frame.pack(fill=tk.X, pady=(0, 12))
        self.persona_label = tk.Label(self.banner_frame, text="", font=("Segoe UI", 10, "bold"), bg="#EFF6FF", fg="#1E40AF")
        self.persona_label.pack(anchor="w")
        self.ceiling_label = tk.Label(self.banner_frame, text="", font=("Segoe UI", 9), bg="#EFF6FF", fg="#475569")
        self.ceiling_label.pack(anchor="w")

        # 5. Visual Stacked Breakdown Bar
        visual_card = tk.Frame(main_frame, bg="#FFFFFF", bd=1, relief="solid", padx=15, pady=10)
        visual_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(visual_card, text="Monthly Cashflow & CPF Distribution Bar", font=("Segoe UI", 10, "bold"), bg="#FFFFFF").pack(anchor="w")

        self.canvas_bar = tk.Canvas(visual_card, height=36, bg="#F1F5F9", highlightthickness=0)
        self.canvas_bar.pack(fill=tk.X, pady=(6, 6))

        # Legend
        legend_frame = tk.Frame(visual_card, bg="#FFFFFF")
        legend_frame.pack(fill=tk.X)
        self._add_legend_item(legend_frame, "#10B981", "Take-Home Pay")
        self._add_legend_item(legend_frame, "#3B82F6", "Employee CPF (Deducted)")
        self._add_legend_item(legend_frame, "#F59E0B", "Employer CPF (Extra Bonus!)")

        # 6. Detailed Cards Grid
        grid_frame = tk.Frame(main_frame, bg="#F0F4F8")
        grid_frame.pack(fill=tk.BOTH, expand=True)
        grid_frame.columnconfigure((0, 1, 2), weight=1)

        # Card 1: Take Home
        self.card_takehome = self._create_stat_card(
            grid_frame, 0, "💵 Take-Home Pay", "#10B981",
            "What enters your bank account directly each month."
        )

        # Card 2: Total CPF
        self.card_total_cpf = self._create_stat_card(
            grid_frame, 1, "🏦 Total Monthly CPF", "#2563EB",
            "Total saved into OA, SA, and MA accounts."
        )

        # Card 3: Free Money / Hawker
        self.card_hawker = self._create_stat_card(
            grid_frame, 2, "🎁 'Free Money' Factor", "#F59E0B",
            "Employer's extra contribution & hawker equivalent."
        )

    def _add_legend_item(self, parent: tk.Frame, color: str, text: str) -> None:
        box = tk.Label(parent, text="  ", bg=color, width=2)
        box.pack(side=tk.LEFT, padx=(0, 4))
        lbl = tk.Label(parent, text=text, font=("Segoe UI", 8), bg="#FFFFFF", fg="#475569")
        lbl.pack(side=tk.LEFT, padx=(0, 14))

    def _create_stat_card(self, parent: tk.Frame, col: int, title: str, color: str, note: str) -> Dict[str, Any]:
        frame = tk.Frame(parent, bg="#FFFFFF", bd=1, relief="solid", padx=12, pady=10)
        frame.grid(row=0, column=col, sticky="nsew", padx=4)

        t_lbl = tk.Label(frame, text=title, font=("Segoe UI", 10, "bold"), fg=color, bg="#FFFFFF")
        t_lbl.pack(anchor="w")

        val_lbl = tk.Label(frame, text="$0.00", font=("Segoe UI", 15, "bold"), fg="#0F172A", bg="#FFFFFF")
        val_lbl.pack(anchor="w", pady=(4, 2))

        sub_lbl = tk.Label(frame, text="", font=("Segoe UI", 8), fg="#64748B", bg="#FFFFFF", wraplength=220, justify=tk.LEFT)
        sub_lbl.pack(anchor="w")

        note_lbl = tk.Label(frame, text=note, font=("Segoe UI", 7, "italic"), fg="#94A3B8", bg="#FFFFFF", wraplength=220, justify=tk.LEFT)
        note_lbl.pack(anchor="w", pady=(6, 0))

        return {"frame": frame, "val": val_lbl, "sub": sub_lbl}

    def set_preset(self, salary: float, age: int) -> None:
        self.salary_var.set(salary)
        self.age_var.set(age)
        self.update_calculations()

    def _on_slider_change(self, event=None) -> None:
        self.update_calculations()

    def update_calculations(self) -> None:
        salary = round(self.salary_var.get(), 2)
        age = int(self.age_var.get())

        self.sal_display.config(text=f"${salary:,.2f}")
        self.age_display.config(text=f"{age} years old")

        try:
            data = calculate_cpf(salary, age)
            fun = get_fun_metrics(data)
        except ValueError as err:
            messagebox.showerror("Validation Error", str(err))
            return

        # Update Banner
        self.persona_label.config(text=f"{fun['persona']} — {fun['persona_desc']}")
        if fun["is_capped"]:
            self.ceiling_label.config(
                text=f"⚠️ Monthly salary exceeds the $7,400 cap. The remaining ${fun['uncapped_amount']:,.2f} has 0% CPF deduction!"
            )
            self.banner_frame.config(bg="#FEF3C7")
            self.persona_label.config(bg="#FEF3C7", fg="#92400E")
            self.ceiling_label.config(bg="#FEF3C7", fg="#78350F")
        else:
            self.ceiling_label.config(
                text=f"✅ Entire salary of ${salary:,.2f} is subject to CPF contributions."
            )
            self.banner_frame.config(bg="#EFF6FF")
            self.persona_label.config(bg="#EFF6FF", fg="#1E40AF")
            self.ceiling_label.config(bg="#EFF6FF", fg="#475569")

        # Update Cards
        # 1. Take-Home
        pct_takehome = (data["take_home_pay"] / salary) * 100 if salary > 0 else 0
        self.card_takehome["val"].config(text=f"${data['take_home_pay']:,.2f}")
        self.card_takehome["sub"].config(
            text=f"{pct_takehome:.1f}% of gross salary\n(After ${data['employee_share']:,.2f} employee CPF)"
        )

        # 2. Total CPF
        self.card_total_cpf["val"].config(text=f"${data['total_contribution']:,.2f}/mo")
        self.card_total_cpf["sub"].config(
            text=f"Annual CPF: ${fun['annual_cpf']:,.2f}/yr\nRates: {int(data['employee_rate']*100)}% you + {int(data['employer_rate']*100)}% employer"
        )

        # 3. Hawker / Free Money
        self.card_hawker["val"].config(text=f"+${data['employer_share']:,.2f}/mo")
        self.card_hawker["sub"].config(
            text=f"🎁 Employer bonus: ${fun['annual_employer_bonus']:,.2f}/yr\n☕ {fun['kopi_count']} cups Kopi or 🍛 {fun['chicken_rice_count']} plates Chicken Rice!"
        )

        # Update Canvas Bar
        self.draw_bar(data)

    def draw_bar(self, data: Dict[str, float]) -> None:
        self.canvas_bar.delete("all")
        width = self.canvas_bar.winfo_width()
        if width <= 10:
            width = 750  # Fallback initial width

        height = 36

        # Total package value = salary + employer contribution
        total_package = data["monthly_salary"] + data["employer_share"]
        if total_package <= 0:
            return

        w_takehome = (data["take_home_pay"] / total_package) * width
        w_employee = (data["employee_share"] / total_package) * width
        w_employer = (data["employer_share"] / total_package) * width

        # Segment 1: Take home (Green)
        x0 = 0
        x1 = w_takehome
        self.canvas_bar.create_rectangle(x0, 0, x1, height, fill="#10B981", outline="")
        if w_takehome > 70:
            self.canvas_bar.create_text(
                (x0 + x1) / 2, height / 2,
                text=f"${data['take_home_pay']:,.0f}",
                fill="#FFFFFF", font=("Segoe UI", 9, "bold")
            )

        # Segment 2: Employee CPF (Blue)
        x2 = x1 + w_employee
        self.canvas_bar.create_rectangle(x1, 0, x2, height, fill="#3B82F6", outline="")
        if w_employee > 50:
            self.canvas_bar.create_text(
                (x1 + x2) / 2, height / 2,
                text=f"${data['employee_share']:,.0f}",
                fill="#FFFFFF", font=("Segoe UI", 8, "bold")
            )

        # Segment 3: Employer CPF (Orange)
        x3 = width
        self.canvas_bar.create_rectangle(x2, 0, x3, height, fill="#F59E0B", outline="")
        if w_employer > 50:
            self.canvas_bar.create_text(
                (x2 + x3) / 2, height / 2,
                text=f"+${data['employer_share']:,.0f}",
                fill="#FFFFFF", font=("Segoe UI", 8, "bold")
            )


# ==============================================================================
# PURE PYTHON TERMINAL TUI / INTERACTIVE CLI
# ==============================================================================

def print_banner() -> None:
    print("\n" + "=" * 65)
    print("🦁  SINGAPORE CPF EXPLORER & WEALTH SIMULATOR  🦁")
    print("   Pure Python Interactive Edition • 2026 CPF Rates")
    print("=" * 65)


def render_cli_bar(take_home: float, employee_share: float, employer_share: float, width: int = 40) -> str:
    """Render a text-based ASCII distribution bar."""
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

            # Visual bar
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


def run_quiz_mini_game() -> None:
    """Fun trivia mini-game on CPF facts & mental math."""
    print_banner()
    print("🎮 WELCOME TO THE CPF TRIVIA & MATH CHALLENGE!")
    print("Test your Singapore CPF knowledge in 3 quick questions:\n")

    score = 0

    questions = [
        {
            "q": "1. What is the Singapore Ordinary Wage (OW) CPF monthly ceiling for 2026?",
            "options": ["A) $6,000", "B) $6,800", "C) $7,400", "D) $8,000"],
            "ans": "C",
            "explain": "Correct! As implemented in cpf37.py, the ceiling is $7,400."
        },
        {
            "q": "2. For an employee aged 30 earning $5,000/mo, what is the employee contribution rate?",
            "options": ["A) 15%", "B) 17%", "C) 20%", "D) 37%"],
            "ans": "C",
            "explain": "Correct! Workers aged 55 and below contribute 20% (and employer contributes 17%)."
        },
        {
            "q": "3. If an employee aged 58 earns $10,000, what is the maximum monthly salary subject to CPF?",
            "options": ["A) $5,000", "B) $7,400", "C) $10,000", "D) $0"],
            "ans": "B",
            "explain": "Correct! Any salary above $7,400 is capped regardless of high earnings."
        }
    ]

    for item in questions:
        print(item["q"])
        for opt in item["options"]:
            print("   " + opt)
        user_choice = input("Your answer (A/B/C/D): ").strip().upper()
        if user_choice == item["ans"]:
            print(f"🎉 {item['explain']}\n")
            score += 1
        else:
            print(f"❌ Not quite! {item['explain']}\n")

    print(f"🏁 Final Score: {score}/3")
    if score == 3:
        print("🏆 Achievement Unlocked: 'CPF Master Strategist'!\n")
    else:
        print("👍 Good effort! Review cpf37.py to become a CPF master!\n")


def main_interactive_menu() -> None:
    """Main terminal menu offering GUI launch or CLI modes."""
    while True:
        print_banner()
        print("Choose an option:")
        print("  1) 🖥️  Launch Native Desktop GUI (Visual Sliders & Real-Time Bar)")
        print("  2) 🎯 Run Terminal Interactive Calculator (Hawker Index & Insights)")
        print("  3) 🎮 Play CPF Trivia & Mental Math Mini-Game")
        print("  4) 🚪 Exit")
        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            try:
                root = tk.Tk()
                app = CPFAppGUI(root)
                root.mainloop()
            except Exception as e:
                print(f"Could not open GUI window ({e}). Running Terminal Mode instead...")
                run_cli_calculator()
        elif choice == "2":
            run_cli_calculator()
        elif choice == "3":
            run_quiz_mini_game()
        elif choice == "4":
            print("Terima kasih & goodbye!")
            break
        else:
            print("Invalid choice, please select 1-4.")


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # If launched with --cli argument, run directly in CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli_calculator()
    elif len(sys.argv) > 1 and sys.argv[1] == "--quiz":
        run_quiz_mini_game()
    elif len(sys.argv) > 1 and sys.argv[1] == "--gui":
        root = tk.Tk()
        app = CPFAppGUI(root)
        root.mainloop()
    else:
        # Default: if a GUI environment is available, launch the GUI directly!
        try:
            root = tk.Tk()
            app = CPFAppGUI(root)
            root.mainloop()
        except Exception:
            main_interactive_menu()

