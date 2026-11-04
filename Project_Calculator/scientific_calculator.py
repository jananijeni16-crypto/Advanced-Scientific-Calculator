import tkinter as tk
from tkinter import ttk, messagebox
import math
import statistics
from datetime import datetime, timedelta

# Matplotlib for Graphing Tab
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("540x680")
        self.root.resizable(False, False)

        # State Variables
        self.angle_mode = tk.StringVar(value="DEG")
        self.history = []  # Stores tuples of (timestamp, expression, result)

        # Apply Light Professional Theme Colors
        self.bg_color = "#F4F6F9"
        self.panel_color = "#FFFFFF"
        self.btn_bg = "#E1E6EB"
        self.btn_fg = "#2C3E50"
        self.btn_active = "#CBD5E1"
        self.accent_color = "#3B82F6"
        self.accent_fg = "#FFFFFF"

        self.root.configure(bg=self.bg_color)
        self.setup_styles()

        # Top Angle Mode Selector Frame
        self.create_top_bar()

        # Notebook (Main Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Create Main Tabs
        self.basic_tab = ttk.Frame(self.notebook)
        self.advanced_tab = ttk.Frame(self.notebook)
        self.unit_tab = ttk.Frame(self.notebook)
        self.graph_tab = ttk.Frame(self.notebook)
        self.hist_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.basic_tab, text="Basic")
        self.notebook.add(self.advanced_tab, text="Advanced")
        self.notebook.add(self.unit_tab, text="Unit Conversions")
        self.notebook.add(self.graph_tab, text="Graph")
        self.notebook.add(self.hist_tab, text="History")

        # Build Tab Contents
        self.build_basic_tab()
        self.build_advanced_tab()
        self.build_unit_tab()
        self.build_graph_tab()
        self.build_history_tab()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.btn_bg, foreground=self.btn_fg, padding=[10, 5], font=("Arial", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.accent_color)], foreground=[("selected", self.accent_fg)])
        style.configure("TFrame", background=self.bg_color)

    def create_top_bar(self):
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill="x", padx=15, pady=8)

        lbl = tk.Label(top_frame, text="Angle Mode:", bg=self.bg_color, fg="#475569", font=("Arial", 9, "bold"))
        lbl.pack(side="left", padx=5)

        self.deg_btn = tk.Button(top_frame, text="DEG", bg=self.accent_color, fg=self.accent_fg, width=6, font=("Arial", 9, "bold"),
                                 command=lambda: self.set_angle_mode("DEG"))
        self.deg_btn.pack(side="left", padx=2)

        self.rad_btn = tk.Button(top_frame, text="RAD", bg=self.btn_bg, fg=self.btn_fg, width=6, font=("Arial", 9, "bold"),
                                 command=lambda: self.set_angle_mode("RAD"))
        self.rad_btn.pack(side="left", padx=2)

    def set_angle_mode(self, mode):
        self.angle_mode.set(mode)
        if mode == "DEG":
            self.deg_btn.config(bg=self.accent_color, fg=self.accent_fg)
            self.rad_btn.config(bg=self.btn_bg, fg=self.btn_fg)
        else:
            self.rad_btn.config(bg=self.accent_color, fg=self.accent_fg)
            self.deg_btn.config(bg=self.btn_bg, fg=self.btn_fg)

    def clean_history(self):
        """Removes history records older than 1 day (24 hours)."""
        now = datetime.now()
        self.history = [item for item in self.history if now - item[0] <= timedelta(days=1)]

    def add_history(self, expr, res):
        self.clean_history()
        self.history.append((datetime.now(), expr, str(res)))
        # Automatically update the history tab view if it's already built
        if hasattr(self, 'hist_listbox'):
            self.refresh_history_view()

    # ==================== TAB 1: BASIC CALCULATOR ====================
    def build_basic_tab(self):
        frame = tk.Frame(self.basic_tab, bg=self.bg_color)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.basic_display = tk.Entry(frame, font=("Arial", 18), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove", justify="right")
        self.basic_display.pack(fill="x", ipady=8, pady=(0, 10))

        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(fill="both", expand=True)

        buttons = [
            ('C', 0, 0), ('(', 0, 1), (')', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('DEL', 4, 2), ('=', 4, 3)
        ]

        for (text, row, col) in buttons:
            cmd = lambda t=text: self.on_basic_click(t)
            b = tk.Button(btn_frame, text=text, font=("Arial", 12, "bold"), bg=self.btn_bg, fg=self.btn_fg,
                          activebackground=self.btn_active, bd=1, relief="raised", command=cmd)
            b.grid(row=row, column=col, sticky="nsew", ipadx=5, ipady=10, padx=3, pady=3)

        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

    def on_basic_click(self, char):
        current = self.basic_display.get()
        if char == 'C':
            self.basic_display.delete(0, tk.END)
        elif char == 'DEL':
            self.basic_display.delete(len(current)-1, tk.END)
        elif char == '=':
            try:
                result = eval(current)
                self.add_history(current, result)
                self.basic_display.delete(0, tk.END)
                self.basic_display.insert(0, str(result))
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
        else:
            self.basic_display.insert(tk.END, char)

    # ==================== TAB 2: ADVANCED CALCULATOR ====================
    def build_advanced_tab(self):
        container = ttk.Notebook(self.advanced_tab)
        container.pack(fill="both", expand=True, padx=5, pady=5)

        sci_frame = tk.Frame(container, bg=self.bg_color)
        stat_frame = tk.Frame(container, bg=self.bg_color)
        bmi_age_frame = tk.Frame(container, bg=self.bg_color)

        container.add(sci_frame, text="Scientific")
        container.add(stat_frame, text="Statistics")
        container.add(bmi_age_frame, text="BMI & Age")

        # --- Scientific Sub-tab ---
        self.sci_display = tk.Entry(sci_frame, font=("Arial", 14), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove", justify="right")
        self.sci_display.pack(fill="x", padx=10, pady=8, ipady=5)

        s_btns = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('sqrt', 0, 3), ('^', 0, 4),
            ('asin', 1, 0), ('acos', 1, 1), ('atan', 1, 2), ('log', 1, 3), ('ln', 1, 4),
            ('(', 2, 0), (')', 2, 1), ('!', 2, 2), ('pi', 2, 3), ('e', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3), ('C', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3), ('%', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3), ('DEL', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2, 3)
        ]

        s_grid = tk.Frame(sci_frame, bg=self.bg_color)
        s_grid.pack(fill="both", expand=True, padx=10, pady=5)
        for item in s_btns:
            text = item[0]
            r, c = item[1], item[2]
            colspan = item[3] if len(item) > 3 else 1
            b = tk.Button(s_grid, text=text, font=("Arial", 10, "bold"), bg=self.btn_bg, fg=self.btn_fg,
                          command=lambda t=text: self.on_sci_click(t))
            b.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=2, pady=2, ipady=4)

        for i in range(7):
            s_grid.rowconfigure(i, weight=1)
        for i in range(5):
            s_grid.columnconfigure(i, weight=1)

        # --- Statistics Sub-tab ---
        tk.Label(stat_frame, text="X Values (comma-separated):", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").pack(anchor="w", padx=15, pady=(8, 2))
        self.stat_entry_x = tk.Entry(stat_frame, font=("Arial", 11), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove")
        self.stat_entry_x.pack(fill="x", padx=15, pady=2)

        tk.Label(stat_frame, text="Y Values (optional, for Correlation):", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").pack(anchor="w", padx=15, pady=(5, 2))
        self.stat_entry_y = tk.Entry(stat_frame, font=("Arial", 11), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove")
        self.stat_entry_y.pack(fill="x", padx=15, pady=2)

        stat_btn_frame = tk.Frame(stat_frame, bg=self.bg_color)
        stat_btn_frame.pack(fill="x", padx=15, pady=8)

        tk.Button(stat_btn_frame, text="Calculate Statistics", bg=self.accent_color, fg=self.accent_fg, font=("Arial", 9, "bold"),
                  command=self.calculate_statistics).pack(side="left", expand=True, fill="x", padx=2, ipady=4)
        tk.Button(stat_btn_frame, text="Clear", bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 9, "bold"), width=10,
                  command=self.clear_statistics).pack(side="left", padx=2, ipady=4)

        self.stat_result_lbl = tk.Label(stat_frame, text="", bg=self.panel_color, fg="#1E293B", font=("Arial", 10), justify="left", anchor="nw", bd=2, relief="solid", padx=8, pady=5)
        self.stat_result_lbl.pack(fill="both", expand=True, padx=15, pady=5)

        # --- BMI & Age Sub-tab ---
        bmi_frame = tk.LabelFrame(bmi_age_frame, text="BMI Calculator", bg=self.bg_color, fg="#334155", font=("Arial", 10, "bold"))
        bmi_frame.pack(fill="x", padx=15, pady=8, ipadx=5, ipady=5)

        tk.Label(bmi_frame, text="Weight (kg):", bg=self.bg_color, font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.bmi_w_entry = tk.Entry(bmi_frame, font=("Arial", 10), width=10)
        self.bmi_w_entry.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(bmi_frame, text="Height (m):", bg=self.bg_color, font=("Arial", 9)).grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.bmi_h_entry = tk.Entry(bmi_frame, font=("Arial", 10), width=10)
        self.bmi_h_entry.grid(row=0, column=3, padx=5, pady=4)

        tk.Button(bmi_frame, text="Calculate BMI", bg=self.accent_color, fg=self.accent_fg, font=("Arial", 9, "bold"),
                  command=self.calculate_bmi).grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=4)
        tk.Button(bmi_frame, text="Clear", bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 9, "bold"),
                  command=self.clear_bmi).grid(row=1, column=2, columnspan=2, sticky="ew", padx=5, pady=4)

        self.bmi_lbl = tk.Label(bmi_frame, text="Result: ", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#1E293B")
        self.bmi_lbl.grid(row=2, column=0, columnspan=4, sticky="w", padx=5, pady=4)

        age_frame = tk.LabelFrame(bmi_age_frame, text="Age Calculator", bg=self.bg_color, fg="#334155", font=("Arial", 10, "bold"))
        age_frame.pack(fill="x", padx=15, pady=8, ipadx=5, ipady=5)

        tk.Label(age_frame, text="Birth Date (YYYY-MM-DD):", bg=self.bg_color, font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.age_entry = tk.Entry(age_frame, font=("Arial", 10), width=15)
        self.age_entry.grid(row=0, column=1, padx=5, pady=4)

        tk.Button(age_frame, text="Calculate Age", bg=self.accent_color, fg=self.accent_fg, font=("Arial", 9, "bold"),
                  command=self.calculate_age).grid(row=1, column=0, sticky="ew", padx=5, pady=4)
        tk.Button(age_frame, text="Clear", bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 9, "bold"),
                  command=self.clear_age).grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        self.age_lbl = tk.Label(age_frame, text="Result: ", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#1E293B")
        self.age_lbl.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=4)

    def on_sci_click(self, char):
        current = self.sci_display.get()
        if char == 'C':
            self.sci_display.delete(0, tk.END)
        elif char == 'DEL':
            self.sci_display.delete(len(current)-1, tk.END)
        elif char == 'pi':
            self.sci_display.insert(tk.END, str(math.pi))
        elif char == 'e':
            self.sci_display.insert(tk.END, str(math.e))
        elif char == '=':
            try:
                expr_eval = current.replace('^', '**')
                while '!' in expr_eval:
                    idx = expr_eval.index('!')
                    sub = ""
                    i = idx - 1
                    while i >= 0 and (expr_eval[i].isdigit() or expr_eval[i] == '.'):
                        sub = expr_eval[i] + sub
                        i -= 1
                    val = int(float(sub))
                    fact_val = math.factorial(val)
                    expr_eval = expr_eval.replace(sub + '!', str(fact_val), 1)

                is_deg = (self.angle_mode.get() == "DEG")
                for trig_name, trig_func, inv_flag in [
                    ('asin', math.asin, True), ('acos', math.acos, True), ('atan', math.atan, True),
                    ('sin', math.sin, False), ('cos', math.cos, False), ('tan', math.tan, False)
                ]:
                    while f'{trig_name}(' in expr_eval:
                        expr_eval = self.eval_trig_func(expr_eval, trig_name, trig_func, is_deg, inv_flag)

                if 'sqrt(' in expr_eval:
                    expr_eval = expr_eval.replace('sqrt(', 'math.sqrt(')
                if 'log(' in expr_eval:
                    expr_eval = expr_eval.replace('log(', 'math.log10(')
                if 'ln(' in expr_eval:
                    expr_eval = expr_eval.replace('ln(', 'math.log(')

                result = eval(expr_eval)
                self.add_history(current, result)
                self.sci_display.delete(0, tk.END)
                self.sci_display.insert(0, str(result))
            except Exception as e:
                messagebox.showerror("Error", f"Calculation Error: {str(e)}")
        else:
            self.sci_display.insert(tk.END, char)

    def eval_trig_func(self, expr, name, func, is_deg, is_inverse):
        while f'{name}(' in expr:
            start = expr.index(f'{name}(')
            paren_count = 1
            end = start + len(name) + 1
            while end < len(expr) and paren_count > 0:
                if expr[end] == '(':
                    paren_count += 1
                elif expr[end] == ')':
                    paren_count -= 1
                end += 1
            sub_expr = expr[start:end]
            inner_val = eval(sub_expr[len(name)+1:-1])
            
            if is_inverse:
                res_rad = func(inner_val)
                res = math.degrees(res_rad) if is_deg else res_rad
            else:
                if is_deg:
                    inner_val = math.radians(inner_val)
                res = func(inner_val)
            expr = expr.replace(sub_expr, str(res), 1)
        return expr

    def calculate_statistics(self):
        try:
            raw_x = self.stat_entry_x.get()
            nums_x = [float(x.strip()) for x in raw_x.split(",") if x.strip()]
            if not nums_x:
                raise ValueError("No numbers provided for X")
            
            count = len(nums_x)
            mean_val = statistics.mean(nums_x)
            median_val = statistics.median(nums_x)
            
            try:
                mode_val = statistics.mode(nums_x)
            except Exception:
                mode_val = "No unique mode"

            stdev_s = statistics.stdev(nums_x) if count > 1 else 0.0
            stdev_p = statistics.pstdev(nums_x) if count > 0 else 0.0
            var_s = statistics.variance(nums_x) if count > 1 else 0.0
            sum_val = sum(nums_x)
            min_val = min(nums_x)
            max_val = max(nums_x)

            res_text = (
                f"Count: {count}  |  Sum: {sum_val:.4f}\n"
                f"Mean: {mean_val:.4f}  |  Median: {median_val:.4f}\n"
                f"Mode: {mode_val}\n"
                f"Sample StdDev (s): {stdev_s:.4f}  |  Pop StdDev (σ): {stdev_p:.4f}\n"
                f"Variance: {var_s:.4f}\n"
                f"Min: {min_val}\n"
                f"Max: {max_val}"
            )

            raw_y = self.stat_entry_y.get().strip()
            if raw_y:
                nums_y = [float(y.strip()) for y in raw_y.split(",") if y.strip()]
                if len(nums_y) != count:
                    raise ValueError("X and Y must have matching entry counts for correlation.")
                mean_y = statistics.mean(nums_y)
                num = sum((nums_x[i] - mean_val) * (nums_y[i] - mean_y) for i in range(count))
                den_x = math.sqrt(sum((nums_x[i] - mean_val)**2 for i in range(count)))
                den_y = math.sqrt(sum((nums_y[i] - mean_y)**2 for i in range(count)))
                corr = num / (den_x * den_y) if (den_x * den_y) != 0 else 0.0
                res_text += f"\nCorrelation (r): {corr:.4f}"

            self.stat_result_lbl.config(text=res_text)
            self.add_history(f"Stats({raw_x})", f"Mean: {mean_val:.4f}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input for statistics: {str(e)}")

    def clear_statistics(self):
        self.stat_entry_x.delete(0, tk.END)
        self.stat_entry_y.delete(0, tk.END)
        self.stat_result_lbl.config(text="")

    def calculate_bmi(self):
        try:
            w = float(self.bmi_w_entry.get())
            h = float(self.bmi_h_entry.get())
            if h <= 0:
                raise ValueError("Height must be greater than zero.")
            bmi = w / (h ** 2)
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            self.bmi_lbl.config(text=f"Result: BMI {bmi:.2f} ({category})")
            self.add_history(f"BMI(w={w}, h={h})", f"{bmi:.2f} ({category})")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid BMI inputs: {str(e)}")

    def clear_bmi(self):
        self.bmi_w_entry.delete(0, tk.END)
        self.bmi_h_entry.delete(0, tk.END)
        self.bmi_lbl.config(text="Result: ")

    def calculate_age(self):
        try:
            birth_date = datetime.strptime(self.age_entry.get().strip(), "%Y-%m-%d")
            today = datetime.now()
            if birth_date > today:
                raise ValueError("Birth date cannot be in the future.")
            years = today.year - birth_date.year
            months = today.month - birth_date.month
            days = today.day - birth_date.day
            if days < 0:
                months -= 1
                days += 30
            if months < 0:
                years -= 1
                months += 12
            self.age_lbl.config(text=f"Result: {years}y, {months}m, {days}d")
            self.add_history(f"Age({self.age_entry.get()})", f"{years}y {months}m {days}d")
        except Exception as e:
            messagebox.showerror("Error", f"Use format YYYY-MM-DD: {str(e)}")

    def clear_age(self):
        self.age_entry.delete(0, tk.END)
        self.age_lbl.config(text="Result: ")

    # ==================== TAB 3: UNIT CONVERSIONS ====================
    def build_unit_tab(self):
        frame = tk.Frame(self.unit_tab, bg=self.bg_color)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(frame, text="Choose a conversion category:", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").pack(anchor="w", pady=(0, 2))
        
        self.conv_category = ttk.Combobox(frame, values=["Length", "Mass", "Temperature"], state="readonly", font=("Arial", 10))
        self.conv_category.pack(fill="x", pady=4)
        self.conv_category.set("Length")
        self.conv_category.bind("<<ComboboxSelected>>", self.update_unit_dropdowns)

        tk.Label(frame, text="Value:", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").pack(anchor="w", pady=(4, 2))
        self.unit_val_entry = tk.Entry(frame, font=("Arial", 11), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove")
        self.unit_val_entry.pack(fill="x", pady=4)

        tk.Label(frame, text="From:", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").pack(anchor="w", pady=(4, 2))
        self.from_unit_combo = ttk.Combobox(frame, state="readonly", font=("Arial", 10))
        self.from_unit_combo.pack(fill="x", pady=4)

        tk.Label(frame, text="To:", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").pack(anchor="w", pady=(4, 2))
        self.to_unit_combo = ttk.Combobox(frame, state="readonly", font=("Arial", 10))
        self.to_unit_combo.pack(fill="x", pady=4)

        btn_row = tk.Frame(frame, bg=self.bg_color)
        btn_row.pack(fill="x", pady=8)

        tk.Button(btn_row, text="Convert", bg=self.accent_color, fg=self.accent_fg, font=("Arial", 9, "bold"), width=12,
                  command=self.perform_unit_conversion).pack(side="left", padx=3)
        tk.Button(btn_row, text="Clear", bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 9, "bold"), width=12,
                  command=self.clear_unit_tab).pack(side="left", padx=3)

        tk.Label(frame, text="Result:", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").pack(anchor="w", pady=(8, 2))
        self.unit_result_lbl = tk.Label(frame, text="", bg=self.panel_color, fg="#1E293B", font=("Arial", 11, "bold"), anchor="w", padx=10, bd=2, relief="solid")
        self.unit_result_lbl.pack(fill="x", ipady=6, pady=4)

        self.update_unit_dropdowns(None)

    def update_unit_dropdowns(self, event):
        cat = self.conv_category.get()
        if cat == "Length":
            units = ["Millimeter", "Centimeter", "Meter", "Kilometer", "Inch", "Foot"]
        elif cat == "Mass":
            units = ["Milligram", "Gram", "Kilogram", "Pound", "Ounce"]
        elif cat == "Temperature":
            units = ["Celsius", "Fahrenheit", "Kelvin"]
        else:
            units = []
        self.from_unit_combo['values'] = units
        self.to_unit_combo['values'] = units
        if units:
            self.from_unit_combo.set(units[0])
            self.to_unit_combo.set(units[1] if len(units) > 1 else units[0])

    def perform_unit_conversion(self):
        try:
            val = float(self.unit_val_entry.get())
            cat = self.conv_category.get()
            f_unit = self.from_unit_combo.get()
            t_unit = self.to_unit_combo.get()
            result = 0.0

            if cat == "Length":
                to_meters = {"Millimeter": 0.001, "Centimeter": 0.01, "Meter": 1.0, "Kilometer": 1000.0, "Inch": 0.0254, "Foot": 0.3048}
                meters = val * to_meters[f_unit]
                result = meters / to_meters[t_unit]
            elif cat == "Mass":
                to_grams = {"Milligram": 0.001, "Gram": 1.0, "Kilogram": 1000.0, "Pound": 453.592, "Ounce": 28.3495}
                grams = val * to_grams[f_unit]
                result = grams / to_grams[t_unit]
            elif cat == "Temperature":
                if f_unit == "Celsius": c = val
                elif f_unit == "Fahrenheit": c = (val - 32) * 5/9
                elif f_unit == "Kelvin": c = val - 273.15

                if t_unit == "Celsius": result = c
                elif t_unit == "Fahrenheit": result = (c * 9/5) + 32
                elif t_unit == "Kelvin": result = c + 273.15

            self.unit_result_lbl.config(text=f"{result:.4f} {t_unit}")
            self.add_history(f"Convert {val} {f_unit} to {t_unit}", f"{result:.4f} {t_unit}")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def clear_unit_tab(self):
        self.unit_val_entry.delete(0, tk.END)
        self.unit_result_lbl.config(text="")

    # ==================== TAB 4: GRAPH ====================
    def build_graph_tab(self):
        frame = tk.Frame(self.graph_tab, bg=self.bg_color)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(frame, text="X values (comma-separated):", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").grid(row=0, column=0, sticky="w", pady=2)
        self.graph_x_entry = tk.Entry(frame, font=("Arial", 10), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove")
        self.graph_x_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        self.graph_x_entry.insert(0, "1, 2, 3, 4, 5")

        tk.Label(frame, text="Y values (comma-separated):", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").grid(row=1, column=0, sticky="w", pady=2)
        self.graph_y_entry = tk.Entry(frame, font=("Arial", 10), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove")
        self.graph_y_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        self.graph_y_entry.insert(0, "2, 4, 6, 8, 10")

        tk.Label(frame, text="Chart type:", bg=self.bg_color, font=("Arial", 9, "bold"), fg="#334155").grid(row=2, column=0, sticky="w", pady=2)
        self.chart_type_combo = ttk.Combobox(frame, values=["Line", "Scatter", "Bar", "Step", "Stem"], state="readonly", font=("Arial", 10))
        self.chart_type_combo.grid(row=2, column=1, sticky="ew", pady=2, padx=5)
        self.chart_type_combo.set("Line")

        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=6, sticky="ew")

        tk.Button(btn_frame, text="Draw Chart", bg=self.accent_color, fg=self.accent_fg, font=("Arial", 9, "bold"),
                  command=self.draw_chart).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="Clear", bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 9, "bold"),
                  command=self.clear_graph).pack(side="left", expand=True, fill="x", padx=2)

        frame.columnconfigure(1, weight=1)

        self.fig = Figure(figsize=(4, 2.2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, sticky="nsew", pady=5)
        frame.rowconfigure(4, weight=1)

    def draw_chart(self):
        try:
            x_vals = [float(v.strip()) for v in self.graph_x_entry.get().split(",") if v.strip()]
            y_vals = [float(v.strip()) for v in self.graph_y_entry.get().split(",") if v.strip()]
            if len(x_vals) != len(y_vals) or not x_vals:
                raise ValueError("X and Y must have matching non-empty lengths.")

            chart_type = self.chart_type_combo.get()
            self.ax.clear()

            if chart_type == "Line":
                self.ax.plot(x_vals, y_vals, marker='o', color="#3B82F6", linewidth=2)
            elif chart_type == "Scatter":
                self.ax.scatter(x_vals, y_vals, color="#3B82F6", s=50)
            elif chart_type == "Bar":
                self.ax.bar(x_vals, y_vals, color="#3B82F6", width=0.5)
            elif chart_type == "Step":
                self.ax.step(x_vals, y_vals, where='mid', color="#3B82F6", linewidth=2)
            elif chart_type == "Stem":
                self.ax.stem(x_vals, y_vals)

            self.ax.set_title("Data Plot", fontsize=10, color="#1E293B")
            self.ax.grid(True, linestyle="--", alpha=0.5)
            self.canvas.draw()
            self.add_history(f"Graph ({chart_type})", f"Points: {len(x_vals)}")
        except Exception as e:
            messagebox.showerror("Graph Error", f"Ensure matching numeric values: {str(e)}")

    def clear_graph(self):
        self.graph_x_entry.delete(0, tk.END)
        self.graph_y_entry.delete(0, tk.END)
        self.ax.clear()
        self.canvas.draw()

    # ==================== TAB 5: HISTORY ====================
    def build_history_tab(self):
        frame = tk.Frame(self.hist_tab, bg=self.bg_color)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        hist_top = tk.Frame(frame, bg=self.bg_color)
        hist_top.pack(fill="x", pady=5)
        
        tk.Button(hist_top, text="Refresh History", bg=self.accent_color, fg=self.accent_fg, font=("Arial", 9, "bold"),
                  command=self.refresh_history_view).pack(side="left", padx=3)
        tk.Button(hist_top, text="Reuse Selected Result", bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 9, "bold"),
                  command=self.reuse_history_item).pack(side="left", padx=3)
        tk.Button(hist_top, text="Clear History", bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 9, "bold"),
                  command=self.clear_history_log).pack(side="left", padx=3)

        self.hist_listbox = tk.Listbox(frame, font=("Courier", 9), bg=self.panel_color, fg="#1E293B", bd=2, relief="groove", selectbackground=self.accent_color)
        self.hist_listbox.pack(fill="both", expand=True, padx=0, pady=5)
        self.refresh_history_view()

    def refresh_history_view(self):
        self.clean_history()
        self.hist_listbox.delete(0, tk.END)
        if not self.history:
            self.hist_listbox.insert(tk.END, "No recent history within the last 24 hours.")
            return
        for time_stamp, expr, res in reversed(self.history):
            t_str = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
            self.hist_listbox.insert(tk.END, f"[{t_str}]  {expr}  =  {res}")

    def reuse_history_item(self):
        try:
            selected_idx = self.hist_listbox.curselection()
            if not selected_idx:
                messagebox.showwarning("Warning", "Please select a history item to reuse.")
                return
            item_text = self.hist_listbox.get(selected_idx[0])
            if "=" in item_text:
                res_val = item_text.split("=")[-1].strip()
                self.basic_display.insert(tk.END, res_val)
                self.sci_display.insert(tk.END, res_val)
                messagebox.showinfo("Success", f"Reused result '{res_val}' into display.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not reuse item: {str(e)}")

    def clear_history_log(self):
        self.history.clear()
        self.refresh_history_view()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()