import math
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class CasioGraphingGUI(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("Casio Graphing Virtual (fx-9860GIII)")
    self.geometry("780x520")
    self.resizable(False, False)

    self.expression = ""
    self.last_ans = 0.0

    # Chia cửa sổ làm 2 phần: Trái là máy tính, Phải là màn hình vẽ đồ thị
    self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
    self.left_frame.pack(side="left", fill="both", padx=10, pady=10)

    self.right_frame = ctk.CTkFrame(self, fg_color="#181a1b", corner_radius=10)
    self.right_frame.pack(
        side="right", fill="both", expand=True, padx=10, pady=10
    )

    self.create_calculator_ui()
    self.create_graph_ui()

  def create_calculator_ui(self):
    # Màn hình tính toán nhỏ bên trái
    display_frame = ctk.CTkFrame(
        self.left_frame, fg_color="#181a1b", corner_radius=8
    )
    display_frame.pack(fill="x", padx=5, pady=5)

    self.history_var = ctk.StringVar(value="")
    history_label = ctk.CTkLabel(
        display_frame,
        textvariable=self.history_var,
        font=("Consolas", 11),
        text_color="#888888",
        anchor="e",
    )
    history_label.pack(fill="x", padx=8, pady=(5, 0))

    self.display_var = ctk.StringVar(value="0")
    display_label = ctk.CTkLabel(
        display_frame,
        textvariable=self.display_var,
        font=("Consolas", 20, "bold"),
        text_color="#00FF66",
        anchor="e",
    )
    display_label.pack(fill="x", padx=8, pady=(0, 8))

    # Bàn phím thu gọn
    btn_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
    btn_frame.pack(expand=True, fill="both", padx=5, pady=5)

    buttons = [
        ("AC", 0, 0, "#d9534f"),
        ("(", 0, 1, "#3b3b3b"),
        (")", 0, 2, "#3b3b3b"),
        ("⌫", 0, 3, "#f0ad4e"),
        ("x", 1, 0, "#444444"),
        ("^", 1, 1, "#444444"),
        ("/", 1, 2, "#f0ad4e"),
        ("*", 1, 3, "#f0ad4e"),
        ("7", 2, 0, "#1f1f1f"),
        ("8", 2, 1, "#1f1f1f"),
        ("9", 2, 2, "#1f1f1f"),
        ("-", 2, 3, "#f0ad4e"),
        ("4", 3, 0, "#1f1f1f"),
        ("5", 3, 1, "#1f1f1f"),
        ("6", 3, 2, "#1f1f1f"),
        ("+", 3, 3, "#f0ad4e"),
        ("1", 4, 0, "#1f1f1f"),
        ("2", 4, 1, "#1f1f1f"),
        ("3", 4, 2, "#1f1f1f"),
        ("=", 4, 3, "#5cb85c"),
        ("0", 5, 0, "#1f1f1f"),
        (".", 5, 1, "#1f1f1f"),
        ("Ans", 5, 2, "#3b3b3b"),
        ("PLOT", 5, 3, "#3498DB"),  # Nút vẽ đồ thị
    ]

    for text, row, col, bg_color in buttons:
      btn = ctk.CTkButton(
          btn_frame,
          text=text,
          font=("Consolas", 12, "bold"),
          fg_color=bg_color,
          hover_color="#555555" if bg_color != "#5cb85c" else "#4cae4c",
          corner_radius=5,
          command=lambda t=text: self.on_button_click(t),
      )
      btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    for i in range(6):
      btn_frame.rowconfigure(i, weight=1)
    for j in range(4):
      btn_frame.columnconfigure(j, weight=1)

  def create_graph_ui(self):
    # Khởi tạo vùng vẽ đồ thị Matplotlib nhúng thẳng vào Tkinter
    self.fig, self.ax = plt.subplots(figsize=(4.5, 4.2))
    self.fig.patch.set_facecolor("#181a1b")
    self.ax.set_facecolor("#111213")

    # Trang trí màu sắc cho đồ thị tối màu chuẩn hacker/dev
    self.ax.spines["bottom"].set_color("#888888")
    self.ax.spines["top"].set_color("#888888")
    self.ax.spines["left"].set_color("#888888")
    self.ax.spines["right"].set_color("#888888")
    self.ax.xaxis.label.set_color("white")
    self.ax.yaxis.label.set_color("white")
    self.ax.tick_params(colors="white")
    self.ax.grid(True, color="#333333", linestyle="--", linewidth=0.5)

    self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

  def on_button_click(self, char):
    if char == "AC":
      self.expression = ""
      self.display_var.set("0")
      self.history_var.set("")
    elif char == "⌫":
      self.expression = self.expression[:-1]
      self.display_var.set(self.expression if self.expression else "0")
    elif char == "PLOT":
      self.plot_graph()
    elif char == "=":
      try:
        self.history_var.set(self.expression)
        eval_expr = self.expression.replace("Ans", str(self.last_ans))
        eval_expr = eval_expr.replace("^", "**")
        result = eval(eval_expr)
        self.last_ans = result
        self.display_var.set(str(result))
        self.expression = str(result)
      except Exception:
        self.display_var.set("Math ERROR")
        self.expression = ""
    else:
      if self.display_var.get() in ["0", "Math ERROR"] and char not in "+-*/^":
        self.expression = ""
      self.expression += char
      self.display_var.set(self.expression)

  def plot_graph(self):
    try:
      # Lấy biểu thức hàm số chứa biến x từ ô nhập liệu
      expr = self.expression.strip()
      if not expr:
        return

      # Tạo mảng giá trị x từ -10 đến 10
      x = np.linspace(-10, 10, 400)

      # Chuẩn hóa biểu thức sang cú pháp Python/Numpy
      py_expr = expr.replace("^", "**")
      # Tính giá trị y tương ứng
      y = eval(py_expr, {"x": x, "np": np, "math": math, "sin": np.sin, "cos": np.cos})

      # Vẽ lại đồ thị
      self.ax.clear()
      self.ax.set_facecolor("#111213")
      self.ax.grid(True, color="#333333", linestyle="--", linewidth=0.5)
      self.ax.plot(x, y, color="#00FF66", linewidth=2, label=f"y = {expr}")

      # Trang trí lại trục tọa độ
      self.ax.axhline(0, color="#888888", linewidth=0.8)
      self.ax.axvline(0, color="#888888", linewidth=0.8)
      self.ax.legend(loc="upper right", facecolor="#222222", edgecolor="none", labelcolor="white")

      self.canvas.draw()
    except Exception as e:
      self.display_var.set("Plot ERROR")


if __name__ == "__main__":
  app = CasioGraphingGUI()
  app.mainloop()