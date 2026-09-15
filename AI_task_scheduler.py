import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# AI Task Scheduler - CPU Scheduling Simulator
# Assignment 1: Operating Systems
# Algorithms: FCFS, SJF, Round Robin, Priority
# ============================================================

SAMPLE_PROCESSES = [
    ("P1", 0, 5, 2),
    ("P2", 1, 3, 1),
    ("P3", 2, 8, 3),
    ("P4", 3, 2, 2),
]

# ----------------------------- #
# Scheduling Algorithms
# ----------------------------- #

def fcfs(processes):
    """First Come First Serve - non-preemptive."""
    ordered = sorted(processes, key=lambda p: (p["at"], p["order"]))
    time = 0
    result = {}
    segments = []

    for p in ordered:
        if time < p["at"]:
            segments.append(("IDLE", time, p["at"]))
            time = p["at"]

        start = time
        time += p["bt"]
        segments.append((p["pid"], start, time))

        result[p["pid"]] = {
            "ct": time,
            "tat": time - p["at"],
            "wt": time - p["at"] - p["bt"],
        }

    return result, segments


def sjf(processes):
    """Shortest Job First - non-preemptive."""
    remaining = processes[:]
    time = 0
    result = {}
    segments = []

    while remaining:
        available = [p for p in remaining if p["at"] <= time]

        if not available:
            next_at = min(p["at"] for p in remaining)
            segments.append(("IDLE", time, next_at))
            time = next_at
            continue

        p = min(available, key=lambda x: (x["bt"], x["at"], x["order"]))
        remaining.remove(p)

        start = time
        time += p["bt"]
        segments.append((p["pid"], start, time))

        result[p["pid"]] = {
            "ct": time,
            "tat": time - p["at"],
            "wt": time - p["at"] - p["bt"],
        }

    return result, segments


def priority_scheduling(processes):
    """Priority Scheduling - non-preemptive.
    Smaller priority number means higher priority.
    """
    remaining = processes[:]
    time = 0
    result = {}
    segments = []

    while remaining:
        available = [p for p in remaining if p["at"] <= time]

        if not available:
            next_at = min(p["at"] for p in remaining)
            segments.append(("IDLE", time, next_at))
            time = next_at
            continue

        p = min(
            available,
            key=lambda x: (x["priority"], x["at"], x["order"])
        )
        remaining.remove(p)

        start = time
        time += p["bt"]
        segments.append((p["pid"], start, time))

        result[p["pid"]] = {
            "ct": time,
            "tat": time - p["at"],
            "wt": time - p["at"] - p["bt"],
        }

    return result, segments


def round_robin(processes, quantum):
    """Round Robin scheduling with a user-defined time quantum."""
    ordered = sorted(processes, key=lambda p: (p["at"], p["order"]))
    remaining = {p["pid"]: p["bt"] for p in ordered}
    by_pid = {p["pid"]: p for p in ordered}

    queue = []
    result = {}
    segments = []
    time = 0
    i = 0

    while i < len(ordered) or queue:
        if not queue:
            if time < ordered[i]["at"]:
                segments.append(("IDLE", time, ordered[i]["at"]))
                time = ordered[i]["at"]

            while i < len(ordered) and ordered[i]["at"] <= time:
                queue.append(ordered[i]["pid"])
                i += 1

        pid = queue.pop(0)
        run_for = min(quantum, remaining[pid])

        start = time
        time += run_for
        remaining[pid] -= run_for
        segments.append((pid, start, time))

        while i < len(ordered) and ordered[i]["at"] <= time:
            queue.append(ordered[i]["pid"])
            i += 1

        if remaining[pid] > 0:
            queue.append(pid)
        else:
            p = by_pid[pid]
            result[pid] = {
                "ct": time,
                "tat": time - p["at"],
                "wt": time - p["at"] - p["bt"],
            }

    return result, segments


def averages(result):
    if not result:
        return 0.0, 0.0

    avg_wt = sum(v["wt"] for v in result.values()) / len(result)
    avg_tat = sum(v["tat"] for v in result.values()) / len(result)
    return avg_wt, avg_tat


# ----------------------------- #
# Visual Application
# ----------------------------- #

class SchedulerApp:
    BG = "#0B1120"
    PANEL = "#111827"
    PANEL_2 = "#162033"
    PANEL_3 = "#1C2940"
    BORDER = "#2B3A55"
    TEXT = "#E5E7EB"
    MUTED = "#93A4BD"
    CYAN = "#22D3EE"
    VIOLET = "#8B5CF6"
    GREEN = "#34D399"
    AMBER = "#F59E0B"
    RED = "#FB7185"
    WHITE = "#F8FAFC"

    def __init__(self, root):
        self.root = root
        self.root.title("AI Task Scheduler — CPU Scheduling Lab")
        self.root.geometry("1180x820")
        self.root.minsize(960, 680)
        self.root.configure(bg=self.BG)

        self.last_segments = []
        self.last_result = {}

        self.setup_style()
        self.build_ui()
        self.load_sample_data()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Dark.Treeview",
            background=self.PANEL,
            fieldbackground=self.PANEL,
            foreground=self.TEXT,
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=self.PANEL_3,
            foreground=self.CYAN,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=8,
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", "#273B61")],
            foreground=[("selected", self.WHITE)],
        )
        style.configure(
            "Dark.TEntry",
            fieldbackground=self.PANEL,
            foreground=self.TEXT,
            insertcolor=self.CYAN,
            padding=8,
        )
        style.configure(
            "Dark.TCombobox",
            fieldbackground=self.PANEL,
            background=self.PANEL_3,
            foreground=self.TEXT,
            arrowcolor=self.CYAN,
            padding=6,
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", self.PANEL)],
            foreground=[("readonly", self.TEXT)],
        )

    def make_button(self, parent, text, command, bg, fg=None, width=None):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg or self.BG,
            activebackground=self.WHITE,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )
        if width:
            button.configure(width=width)
        return button

    def section_header(self, parent, number, title, subtitle):
        row = tk.Frame(parent, bg=parent["bg"])
        row.pack(fill="x", pady=(0, 10))

        badge = tk.Label(
            row,
            text=number,
            bg=self.CYAN,
            fg=self.BG,
            font=("Segoe UI", 9, "bold"),
            padx=9,
            pady=4,
        )
        badge.pack(side="left", padx=(0, 9))

        title_label = tk.Label(
            row,
            text=title,
            bg=parent["bg"],
            fg=self.WHITE,
            font=("Segoe UI", 14, "bold"),
        )
        title_label.pack(side="left")

        subtitle_label = tk.Label(
            row,
            text=subtitle,
            bg=parent["bg"],
            fg=self.MUTED,
            font=("Segoe UI", 9),
        )
        subtitle_label.pack(side="left", padx=10)

    def build_ui(self):
        # Scrollable shell
        shell = tk.Frame(self.root, bg=self.BG)
        shell.pack(fill="both", expand=True)

        self.main_canvas = tk.Canvas(
            shell,
            bg=self.BG,
            highlightthickness=0,
            bd=0,
        )
        scrollbar = ttk.Scrollbar(
            shell,
            orient="vertical",
            command=self.main_canvas.yview,
        )
        scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        main = tk.Frame(self.main_canvas, bg=self.BG)
        window_id = self.main_canvas.create_window(
            (0, 0),
            window=main,
            anchor="nw",
        )

        def update_scroll(_event=None):
            self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )

        def resize_width(event):
            self.main_canvas.itemconfigure(window_id, width=event.width)

        main.bind("<Configure>", update_scroll)
        self.main_canvas.bind("<Configure>", resize_width)

        self.main_canvas.bind("<Enter>", self._bind_wheel)
        self.main_canvas.bind("<Leave>", self._unbind_wheel)

        # Page padding
        content = tk.Frame(main, bg=self.BG)
        content.pack(fill="x", padx=26, pady=22)

        self.build_header(content)
        self.build_input_section(content)
        self.build_run_section(content)
        self.build_result_section(content)
        self.build_footer(content)

    def build_header(self, parent):
        header = tk.Frame(parent, bg=self.BG)
        header.pack(fill="x", pady=(0, 22))

        left = tk.Frame(header, bg=self.BG)
        left.pack(side="left")

        tk.Label(
            left,
            text="SCHEDULR",
            bg=self.BG,
            fg=self.CYAN,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        tk.Label(
            left,
            text="AI TASK SCHEDULER",
            bg=self.BG,
            fg=self.WHITE,
            font=("Segoe UI", 26, "bold"),
        ).pack(anchor="w", pady=(1, 0))

        tk.Label(
            left,
            text="OS CPU Scheduling Laboratory  •  Assignment 01",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        status = tk.Frame(
            header,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=14,
            pady=9,
        )
        status.pack(side="right", anchor="n")

        tk.Label(
            status,
            text="●",
            bg=self.PANEL,
            fg=self.GREEN,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left", padx=(0, 7))

        self.header_status = tk.Label(
            status,
            text="SIMULATOR READY",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 9, "bold"),
        )
        self.header_status.pack(side="left")

    def build_input_section(self, parent):
        outer = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        outer.pack(fill="x", pady=(0, 14))

        top = tk.Frame(outer, bg=self.PANEL)
        top.pack(fill="x", padx=16, pady=(15, 9))
        self.section_header(
            top,
            "01",
            "Task Queue",
            "Define the AI / ML jobs waiting for CPU time",
        )

        form = tk.Frame(outer, bg=self.PANEL)
        form.pack(fill="x", padx=16, pady=(0, 14))

        fields = [
            ("PROCESS ID", "P1"),
            ("ARRIVAL TIME", "0"),
            ("BURST TIME", "5"),
            ("PRIORITY", "2"),
        ]
        self.entries = []

        for col, (label, placeholder) in enumerate(fields):
            block = tk.Frame(form, bg=self.PANEL)
            block.grid(row=0, column=col, padx=(0 if col == 0 else 10, 10), sticky="w")

            tk.Label(
                block,
                text=label,
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 8, "bold"),
            ).pack(anchor="w", pady=(0, 5))

            entry = ttk.Entry(
                block,
                style="Dark.TEntry",
                width=18,
            )
            entry.insert(0, "")
            entry.pack(fill="x")
            self.entries.append(entry)

        self.pid_entry, self.at_entry, self.bt_entry, self.pr_entry = self.entries

        actions = tk.Frame(form, bg=self.PANEL)
        actions.grid(row=0, column=4, padx=(10, 0), sticky="s")

        self.make_button(
            actions,
            "+ ADD TASK",
            self.add_task,
            self.CYAN,
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            actions,
            "LOAD DEMO",
            self.load_sample_data,
            self.PANEL_3,
            self.TEXT,
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            actions,
            "CLEAR",
            self.clear_tasks,
            self.PANEL_3,
            self.TEXT,
        ).pack(side="left")

        note = tk.Label(
            outer,
            text="Priority rule used in this simulator: smaller number = higher priority.",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8),
        )
        note.pack(anchor="w", padx=16, pady=(0, 13))

        table_wrap = tk.Frame(outer, bg=self.PANEL)
        table_wrap.pack(fill="x", padx=16, pady=(0, 16))

        self.process_table = ttk.Treeview(
            table_wrap,
            columns=("pid", "at", "bt", "priority"),
            show="headings",
            style="Dark.Treeview",
            height=4,
        )
        headings = [
            ("pid", "PID", 140),
            ("at", "ARRIVAL", 190),
            ("bt", "BURST", 190),
            ("priority", "PRIORITY", 190),
        ]
        for col, title, width in headings:
            self.process_table.heading(col, text=title)
            self.process_table.column(col, width=width, anchor="center")

        self.process_table.pack(fill="x", expand=True)

        self.process_hint = tk.Label(
            outer,
            text="",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8),
        )
        self.process_hint.pack(anchor="w", padx=16, pady=(0, 12))

    def build_run_section(self, parent):
        outer = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        outer.pack(fill="x", pady=(0, 14))

        inner = tk.Frame(outer, bg=self.PANEL)
        inner.pack(fill="x", padx=16, pady=15)

        self.section_header(
            inner,
            "02",
            "Scheduler Control",
            "Choose the CPU policy and execute the workload",
        )

        controls = tk.Frame(inner, bg=self.PANEL)
        controls.pack(fill="x")

        tk.Label(
            controls,
            text="POLICY",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=(0, 7))

        self.algorithm = ttk.Combobox(
            controls,
            values=["FCFS", "SJF", "Round Robin", "Priority"],
            state="readonly",
            width=18,
            style="Dark.TCombobox",
        )
        self.algorithm.current(0)
        self.algorithm.pack(side="left", padx=(0, 18))

        tk.Label(
            controls,
            text="TIME QUANTUM",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=(0, 7))

        self.quantum = ttk.Spinbox(
            controls,
            from_=1,
            to=1000,
            width=8,
            style="Dark.TEntry",
        )
        self.quantum.set(2)
        self.quantum.pack(side="left", padx=(0, 18))

        self.make_button(
            controls,
            "▶  RUN SELECTED",
            self.run_selected,
            self.VIOLET,
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            controls,
            "COMPARE ALL",
            self.compare_all,
            self.GREEN,
        ).pack(side="left")

        self.policy_info = tk.Label(
            inner,
            text=self.policy_description("FCFS"),
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.policy_info.pack(fill="x", pady=(11, 0))
        self.algorithm.bind(
            "<<ComboboxSelected>>",
            self.update_policy_description,
        )

    def build_result_section(self, parent):
        outer = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        outer.pack(fill="x", pady=(0, 14))

        top = tk.Frame(outer, bg=self.PANEL)
        top.pack(fill="x", padx=16, pady=(15, 10))

        self.section_header(
            top,
            "03",
            "Simulation Output",
            "Execution timeline, process metrics and performance",
        )

        self.status_label = tk.Label(
            outer,
            text="Run an algorithm to generate the CPU timeline.",
            bg=self.PANEL,
            fg=self.CYAN,
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=16, pady=(0, 8))

        timeline_panel = tk.Frame(
            outer,
            bg=self.PANEL_2,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        timeline_panel.pack(fill="x", padx=16, pady=(0, 14))

        self.gantt_canvas = tk.Canvas(
            timeline_panel,
            height=155,
            bg=self.PANEL_2,
            highlightthickness=0,
        )
        self.gantt_canvas.pack(fill="x", expand=True, padx=8, pady=8)

        bottom = tk.Frame(outer, bg=self.PANEL)
        bottom.pack(fill="x", padx=16, pady=(0, 16))

        metrics = tk.Frame(
            bottom,
            bg=self.PANEL_2,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        metrics.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(
            metrics,
            text="PROCESS METRICS",
            bg=self.PANEL_2,
            fg=self.WHITE,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=12, pady=(10, 7))

        self.result_table = ttk.Treeview(
            metrics,
            columns=("pid", "ct", "tat", "wt"),
            show="headings",
            style="Dark.Treeview",
            height=4,
        )

        for col, title, width in [
            ("pid", "PID", 90),
            ("ct", "COMPLETION", 125),
            ("tat", "TURNAROUND", 125),
            ("wt", "WAITING", 110),
        ]:
            self.result_table.heading(col, text=title)
            self.result_table.column(col, width=width, anchor="center")

        self.result_table.pack(fill="x", padx=8, pady=(0, 10))

        performance = tk.Frame(
            bottom,
            bg=self.PANEL_2,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            width=330,
        )
        performance.pack(side="right", fill="both", padx=(8, 0))
        performance.pack_propagate(False)

        tk.Label(
            performance,
            text="PERFORMANCE SNAPSHOT",
            bg=self.PANEL_2,
            fg=self.WHITE,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=13, pady=(10, 9))

        self.avg_wt_label = tk.Label(
            performance,
            text="AVG WAITING TIME\n—",
            bg=self.PANEL_2,
            fg=self.AMBER,
            justify="left",
            anchor="w",
            font=("Segoe UI", 10, "bold"),
        )
        self.avg_wt_label.pack(fill="x", padx=13, pady=(0, 8))

        self.avg_tat_label = tk.Label(
            performance,
            text="AVG TURNAROUND TIME\n—",
            bg=self.PANEL_2,
            fg=self.CYAN,
            justify="left",
            anchor="w",
            font=("Segoe UI", 10, "bold"),
        )
        self.avg_tat_label.pack(fill="x", padx=13, pady=(0, 8))

        self.best_label = tk.Label(
            performance,
            text="BEST FOR THIS WORKLOAD\n—",
            bg=self.PANEL_2,
            fg=self.GREEN,
            justify="left",
            anchor="w",
            font=("Segoe UI", 10, "bold"),
        )
        self.best_label.pack(fill="x", padx=13, pady=(0, 8))

        comparison_head = tk.Label(
            performance,
            text="ALGORITHM COMPARISON",
            bg=self.PANEL_2,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold"),
        )
        comparison_head.pack(anchor="w", padx=13, pady=(3, 4))

        self.comparison_text = tk.Text(
            performance,
            height=8,
            bg=self.PANEL_2,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            borderwidth=0,
            font=("Consolas", 9),
            state="disabled",
        )
        self.comparison_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def build_footer(self, parent):
        footer = tk.Frame(parent, bg=self.BG)
        footer.pack(fill="x", pady=(2, 18))

        tk.Label(
            footer,
            text="CPU scheduling concepts: FCFS • SJF • Round Robin • Priority",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 8),
        ).pack(side="left")

        tk.Label(
            footer,
            text="CT = Completion  |  TAT = Turnaround  |  WT = Waiting",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 8),
        ).pack(side="right")

    # ----------------------------- #
    # App Behavior
    # ----------------------------- #

    def policy_description(self, algorithm):
        descriptions = {
            "FCFS": "First process to arrive gets the CPU first. Simple, non-preemptive scheduling.",
            "SJF": "Among ready processes, the shortest CPU burst runs first. Non-preemptive.",
            "Round Robin": "Each process receives a fixed time slice, then returns to the ready queue if unfinished.",
            "Priority": "Among ready processes, the highest-priority task runs first. Smaller priority number = higher priority.",
        }
        return descriptions.get(algorithm, "")

    def update_policy_description(self, _event=None):
        self.policy_info.config(
            text=self.policy_description(self.algorithm.get())
        )

    def _bind_wheel(self, _event=None):
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_wheel(self, _event=None):
        self.main_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-event.delta / 120), "units")

    def add_task(self):
        pid = self.pid_entry.get().strip()
        at_text = self.at_entry.get().strip()
        bt_text = self.bt_entry.get().strip()
        pr_text = self.pr_entry.get().strip()

        if not pid or not at_text or not bt_text or not pr_text:
            messagebox.showwarning(
                "Incomplete Task",
                "Please enter Process ID, Arrival Time, Burst Time and Priority.",
            )
            return

        try:
            at = int(at_text)
            bt = int(bt_text)
            priority = int(pr_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Arrival, burst and priority must be integers.",
            )
            return

        if at < 0:
            messagebox.showerror(
                "Invalid Arrival Time",
                "Arrival time cannot be negative.",
            )
            return

        if bt <= 0:
            messagebox.showerror(
                "Invalid Burst Time",
                "Burst time must be greater than 0.",
            )
            return

        existing = {
            str(self.process_table.item(item)["values"][0])
            for item in self.process_table.get_children()
        }

        if pid in existing:
            messagebox.showerror(
                "Duplicate Process",
                "Process ID must be unique.",
            )
            return

        self.process_table.insert(
            "",
            "end",
            values=(pid, at, bt, priority),
        )

        self.clear_entries()
        self.resize_tables()

        self.header_status.config(text="TASK ADDED")
        self.root.after(
            900,
            lambda: self.header_status.config(text="SIMULATOR READY"),
        )

    def clear_entries(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def clear_tasks(self):
        for item in self.process_table.get_children():
            self.process_table.delete(item)

        self.clear_results()
        self.status_label.config(
            text="Task queue cleared. Add processes to begin."
        )
        self.header_status.config(text="QUEUE EMPTY")
        self.resize_tables()

    def load_sample_data(self):
        for item in self.process_table.get_children():
            self.process_table.delete(item)

        for pid, at, bt, priority in SAMPLE_PROCESSES:
            self.process_table.insert(
                "",
                "end",
                values=(pid, at, bt, priority),
            )

        self.clear_results()
        self.status_label.config(
            text="Demo workload loaded. Choose a scheduling policy and run it."
        )
        self.header_status.config(text="DEMO LOADED")
        self.root.after(
            900,
            lambda: self.header_status.config(text="SIMULATOR READY"),
        )
        self.resize_tables()

    def clear_results(self):
        for item in self.result_table.get_children():
            self.result_table.delete(item)

        self.gantt_canvas.delete("all")
        self.avg_wt_label.config(text="AVG WAITING TIME\n—")
        self.avg_tat_label.config(text="AVG TURNAROUND TIME\n—")
        self.best_label.config(text="BEST FOR THIS WORKLOAD\n—")

        self.comparison_text.config(state="normal")
        self.comparison_text.delete("1.0", tk.END)
        self.comparison_text.config(state="disabled")

        self.last_segments = []
        self.last_result = {}

    def resize_tables(self):
        process_count = len(self.process_table.get_children())
        self.process_table.configure(height=max(4, process_count))

        if hasattr(self, "result_table"):
            result_count = len(self.result_table.get_children())
            self.result_table.configure(height=max(4, result_count))

        self.root.update_idletasks()

    def get_processes(self):
        items = self.process_table.get_children()

        if not items:
            raise ValueError("Please add at least one process.")

        processes = []

        for order, item in enumerate(items):
            values = self.process_table.item(item)["values"]

            try:
                pid = str(values[0])
                at = int(values[1])
                bt = int(values[2])
                priority = int(values[3])
            except (ValueError, TypeError):
                raise ValueError("The process table contains invalid values.")

            if at < 0:
                raise ValueError("Arrival time cannot be negative.")

            if bt <= 0:
                raise ValueError("Burst time must be greater than 0.")

            processes.append({
                "pid": pid,
                "at": at,
                "bt": bt,
                "priority": priority,
                "order": order,
            })

        return processes

    def run_selected(self):
        try:
            processes = self.get_processes()
            algorithm = self.algorithm.get()

            if algorithm == "FCFS":
                result, segments = fcfs(processes)

            elif algorithm == "SJF":
                result, segments = sjf(processes)

            elif algorithm == "Priority":
                result, segments = priority_scheduling(processes)

            else:
                try:
                    quantum = int(self.quantum.get())
                except (TypeError, ValueError):
                    raise ValueError("Time quantum must be an integer.")

                if quantum <= 0:
                    raise ValueError("Time quantum must be greater than 0.")

                result, segments = round_robin(processes, quantum)

            self.show_result(
                algorithm,
                processes,
                result,
                segments,
            )

            comparison = self.calculate_comparison(processes)
            self.show_comparison(comparison)

            self.header_status.config(text="SIMULATION COMPLETE")

        except ValueError as error:
            messagebox.showerror("Cannot Run Simulation", str(error))

    def compare_all(self):
        try:
            processes = self.get_processes()
            comparison = self.calculate_comparison(processes)

            # FCFS is shown in the main timeline when Compare All is clicked.
            result, segments = fcfs(processes)

            self.show_result(
                "FCFS",
                processes,
                result,
                segments,
            )
            self.show_comparison(comparison)
            self.status_label.config(
                text="All four algorithms compared. The timeline below shows FCFS."
            )
            self.header_status.config(text="COMPARISON READY")

        except ValueError as error:
            messagebox.showerror("Cannot Compare", str(error))

    def calculate_comparison(self, processes):
        try:
            quantum = int(self.quantum.get())
        except (TypeError, ValueError):
            raise ValueError("Time quantum must be an integer.")

        if quantum <= 0:
            raise ValueError("Time quantum must be greater than 0.")

        algorithms = {
            "FCFS": fcfs(processes),
            "SJF": sjf(processes),
            "Round Robin": round_robin(processes, quantum),
            "Priority": priority_scheduling(processes),
        }

        comparison = {}

        for name, (result, _segments) in algorithms.items():
            wt, tat = averages(result)
            comparison[name] = (wt, tat)

        return comparison

    def show_result(self, algorithm, processes, result, segments):
        self.last_segments = segments
        self.last_result = result

        if algorithm == "Round Robin":
            q = int(self.quantum.get())
            title = f"Round Robin  •  Quantum = {q}"
        else:
            title = algorithm

        self.status_label.config(text=f"CPU TIMELINE  /  {title.upper()}")
        self.draw_gantt(segments)

        for item in self.result_table.get_children():
            self.result_table.delete(item)

        for p in sorted(processes, key=lambda x: x["order"]):
            r = result[p["pid"]]
            self.result_table.insert(
                "",
                "end",
                values=(
                    p["pid"],
                    r["ct"],
                    r["tat"],
                    r["wt"],
                ),
            )

        self.resize_tables()

        avg_wt, avg_tat = averages(result)
        self.avg_wt_label.config(
            text=f"AVG WAITING TIME\n{avg_wt:.2f}"
        )
        self.avg_tat_label.config(
            text=f"AVG TURNAROUND TIME\n{avg_tat:.2f}"
        )

    def show_comparison(self, comparison):
        best = min(
            comparison,
            key=lambda name: (
                comparison[name][0],
                comparison[name][1],
            ),
        )

        self.best_label.config(
            text=f"BEST FOR THIS WORKLOAD\n{best}"
        )

        self.comparison_text.config(state="normal")
        self.comparison_text.delete("1.0", tk.END)

        self.comparison_text.insert(
            tk.END,
            "ALGORITHM          AVG WT    AVG TAT\n"
        )
        self.comparison_text.insert(
            tk.END,
            "────────────────────────────────────\n"
        )

        for name, (wt, tat) in comparison.items():
            self.comparison_text.insert(
                tk.END,
                f"{name:<18}{wt:>7.2f}    {tat:>7.2f}\n"
            )

        self.comparison_text.insert(
            tk.END,
            "\nLower waiting time is better.\n"
        )
        self.comparison_text.insert(
            tk.END,
            f"\nWinner: {best}"
        )

        self.comparison_text.config(state="disabled")

    def draw_gantt(self, segments):
        self.gantt_canvas.delete("all")

        if not segments:
            return

        self.root.update_idletasks()

        width = max(self.gantt_canvas.winfo_width(), 700)
        height = 155

        left = 34
        right = 20
        top = 35
        bar_h = 44

        start_time = segments[0][1]
        end_time = segments[-1][2]
        total = max(1, end_time - start_time)
        usable = max(100, width - left - right)
        scale = usable / total

        palette = [
            "#22D3EE",
            "#8B5CF6",
            "#34D399",
            "#F59E0B",
            "#FB7185",
            "#60A5FA",
            "#A78BFA",
            "#2DD4BF",
        ]

        color_map = {}
        color_index = 0

        self.gantt_canvas.create_text(
            left,
            14,
            text="CPU EXECUTION TIMELINE",
            anchor="w",
            fill=self.MUTED,
            font=("Segoe UI", 8, "bold"),
        )

        for pid, start, end in segments:
            if pid not in color_map:
                if pid == "IDLE":
                    color_map[pid] = "#475569"
                else:
                    color_map[pid] = palette[color_index % len(palette)]
                    color_index += 1

            x1 = left + (start - start_time) * scale
            x2 = left + (end - start_time) * scale

            self.gantt_canvas.create_rectangle(
                x1,
                top,
                x2,
                top + bar_h,
                fill=color_map[pid],
                outline=self.PANEL_2,
                width=2,
            )

            text_color = self.BG if pid != "IDLE" else self.TEXT

            self.gantt_canvas.create_text(
                (x1 + x2) / 2,
                top + bar_h / 2,
                text=pid,
                fill=text_color,
                font=("Segoe UI", 9, "bold"),
            )

            self.gantt_canvas.create_text(
                x1,
                top + bar_h + 17,
                text=str(start),
                anchor="n",
                fill=self.MUTED,
                font=("Segoe UI", 8),
            )

        final_x = left + (end_time - start_time) * scale

        self.gantt_canvas.create_text(
            final_x,
            top + bar_h + 17,
            text=str(end_time),
            anchor="n",
            fill=self.MUTED,
            font=("Segoe UI", 8),
        )

        # Timeline baseline and endpoint markers.
        self.gantt_canvas.create_line(
            left,
            top + bar_h + 3,
            final_x,
            top + bar_h + 3,
            fill=self.BORDER,
            width=1,
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
